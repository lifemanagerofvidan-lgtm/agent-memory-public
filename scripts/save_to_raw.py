#!/usr/bin/env python3
"""
save_to_raw.py — save the current session into the Agent Memory Journal.

Keep only:
- user / assistant messages
- cleaned message text
- staged attachments

Remove:
- system messages
- tool call/result content
- transport metadata
- startup / control chatter
"""

import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
STATE_FILE = PROJECT_ROOT / "state" / "sessions-written.json"
DEFAULT_VAULT_ROOT = Path.home() / "Library" / "Mobile Documents" / "iCloud~md~obsidian" / "Documents" / "AgentMemoryVault"
VAULT_ROOT = Path(os.environ.get("AGENT_MEMORY_VAULT", DEFAULT_VAULT_ROOT)).expanduser()
DEFAULT_AGENT_ROLE = "main"
ATTACHMENTS_DIR = VAULT_ROOT / "10_Journal" / "_assets"
SESSIONS_DIR = Path(os.environ.get("OPENCLAW_SESSIONS_DIR", str(Path.home() / ".openclaw" / "agents" / "main" / "sessions"))).expanduser()

SYSTEM_MARKERS = [
    "A new session was started via",
    "Model switched to",
    "Session Startup sequence",
    "Run your Session Startup",
    "Current time:",
    "System:",
]

REPLY_TAG_RE = re.compile(r"\[\[\s*reply_to\s*(?::\s*[^\]]+)?\]\]\s*", re.IGNORECASE)
MEDIA_PREFIX_RE = re.compile(r"^\[media attached:\s*(.*?)\]$", re.IGNORECASE | re.DOTALL)
CONVO_BLOCK_RE = re.compile(r"Conversation info \(untrusted metadata\):\s*```json.*?```\s*", re.DOTALL)
SENDER_BLOCK_RE = re.compile(r"Sender \(untrusted metadata\):\s*```json.*?```\s*", re.DOTALL)
IMAGE_TOOL_NOTE_RE = re.compile(
    r"To send an image back, prefer the message tool.*?Keep caption in the text body\.\s*",
    re.DOTALL,
)
LEADING_BRACKET_BLOCK_RE = re.compile(r"^\[\[[^\]]*\]\]\s*")


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"sessions": {}}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def strip_wrappers(text: str) -> str:
    text = text or ""
    text = REPLY_TAG_RE.sub("", text)
    text = LEADING_BRACKET_BLOCK_RE.sub("", text)
    text = CONVO_BLOCK_RE.sub("", text)
    text = SENDER_BLOCK_RE.sub("", text)
    text = IMAGE_TOOL_NOTE_RE.sub("", text)
    return text.strip()


def is_system_text(text: str) -> bool:
    text = strip_wrappers((text or "").strip())
    if not text:
        return True
    return any(marker in text for marker in SYSTEM_MARKERS)


def flatten_markdown(text: str) -> str:
    lines = []
    in_code_block = False

    for raw_line in (text or "").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            lines.append(line)
            continue

        if in_code_block:
            lines.append(line)
            continue

        if re.match(r"^#{1,6}\s+", stripped):
            line = re.sub(r"^#{1,6}\s+", "", stripped)
        else:
            line = line

        lines.append(line)

    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_text(text: str) -> str:
    text = strip_wrappers(text)
    if not text or is_system_text(text):
        return ""
    return flatten_markdown(text)


def find_session_id(session_key):
    if session_key:
        direct_path = SESSIONS_DIR / f"{session_key}.jsonl"
        if direct_path.exists():
            return session_key

    env_session_id = os.environ.get("OPENCLAW_SESSION_ID")
    if env_session_id and (SESSIONS_DIR / f"{env_session_id}.jsonl").exists():
        return env_session_id

    session_files = sorted(SESSIONS_DIR.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    if session_files:
        return session_files[0].stem

    raise FileNotFoundError("Cannot find any usable session file")


def load_session_messages(session_id: str):
    session_file = SESSIONS_DIR / f"{session_id}.jsonl"
    if not session_file.exists():
        raise FileNotFoundError(f"Session file not found: {session_file}")

    messages = []
    for line in session_file.open("r", encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue

        if obj.get("type") != "message":
            continue

        msg = obj.get("message", {})
        role = msg.get("role", "")
        if role not in ("user", "assistant"):
            continue
        messages.append(msg)

    return messages


def stage_attachment(source_path: str):
    if not source_path:
        return None
    src = Path(source_path)
    if not src.exists() or not src.is_file():
        return None

    ATTACHMENTS_DIR.mkdir(parents=True, exist_ok=True)
    dest = ATTACHMENTS_DIR / src.name
    if not dest.exists():
        shutil.copy2(src, dest)
    return dest.name


def extract_wrapped_media(text: str):
    attachments = []
    remaining_lines = []

    for raw_line in (text or "").splitlines():
        line = raw_line.strip()
        m = MEDIA_PREFIX_RE.match(line)
        if m:
            raw_items = m.group(1)
            for part in raw_items.split("|"):
                part = part.strip()
                if not part:
                    continue

                media_type = None
                type_match = re.search(r"\(([^()]+/[^()]+)\)\s*$", part)
                if type_match:
                    media_type = type_match.group(1)
                    part = re.sub(r"\s*\([^()]+/[^()]+\)\s*$", "", part).strip()

                staged_name = stage_attachment(part)
                if staged_name:
                    suffix = (Path(part).suffix or "").lower()
                    if (media_type and media_type.startswith("image/")) or suffix in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
                        attachments.append(f"![[{staged_name}]]")
                    else:
                        attachments.append(f"[[{staged_name}]]")
                else:
                    name = Path(part).name if "/" in part else part
                    attachments.append(f"[[{name}]]")
            continue

        remaining_lines.append(raw_line)

    return "\n".join(remaining_lines).strip(), attachments


def extract_text_and_attachments(content):
    texts = []
    attachments = []

    if isinstance(content, str):
        stripped, found = extract_wrapped_media(content)
        attachments.extend(found)
        cleaned = clean_text(stripped)
        if cleaned:
            texts.append(cleaned)
        return texts, attachments

    if not isinstance(content, list):
        return texts, attachments

    for item in content:
        if not isinstance(item, dict):
            continue

        item_type = item.get("type", "")

        if item_type == "text":
            stripped, found = extract_wrapped_media(item.get("text", ""))
            attachments.extend(found)
            cleaned = clean_text(stripped)
            if cleaned:
                texts.append(cleaned)
            continue

        if item_type in (
            "thinking",
            "reasoning",
            "tool_use",
            "tool_result",
            "server_tool_use",
            "server_tool_result",
            "toolCall",
        ):
            continue

        if item_type in ("image", "file", "input_image", "input_file", "attachment"):
            raw_path = item.get("path") or item.get("file_path") or item.get("url") or item.get("uri")
            staged_name = stage_attachment(raw_path) if raw_path else None
            if staged_name:
                media_type = item.get("mimeType") or item.get("contentType") or item_type
                if media_type.startswith("image/"):
                    attachments.append(f"![[{staged_name}]]")
                else:
                    attachments.append(f"[[{staged_name}]]")
            continue

    deduped = []
    seen = set()
    for item in attachments:
        if item not in seen:
            seen.add(item)
            deduped.append(item)

    return texts, deduped


def role_label(role: str) -> str:
    return "老闆" if role == "user" else DEFAULT_AGENT_ROLE


def format_messages(messages: list, session_id: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Session Capture",
        "",
        f"SavedAt: {now}",
        f"SessionId: {session_id}",
        "",
    ]

    kept = 0
    for msg in messages:
        role = msg.get("role", "")
        texts, attachments = extract_text_and_attachments(msg.get("content", []))
        if not texts and not attachments:
            continue

        kept += 1
        lines.append(f"=== {role_label(role)} ===")
        if texts:
            lines.append("\n\n".join(texts))
        if attachments:
            if texts:
                lines.append("")
            lines.extend(attachments)
        lines.append("")

    if kept == 0:
        lines.append("（沒有可保存的對話內容）")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def get_target_path(session_id: str):
    state = load_state()
    existing = state.get("sessions", {}).get(session_id, {})
    existing_path = existing.get("path")
    if existing_path:
        path = Path(existing_path)
        if path.exists():
            return path, state, False

    now = datetime.now()
    date_dir = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%Y%m%d-%H%M%S")
    filename = f"{time_str}-{DEFAULT_AGENT_ROLE}.md"
    target_dir = VAULT_ROOT / "10_Journal" / str(now.year) / date_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / filename, state, True


def write_session(session_key: str, session_id: str, formatted_content: str):
    target_path, state, is_new = get_target_path(session_id)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(formatted_content)

    state.setdefault("sessions", {})[session_id] = {
        "path": str(target_path),
        "session_key": session_key,
        "written_at": datetime.now().isoformat(),
    }
    save_state(state)
    print(f"[{'NEW' if is_new else 'OVERWRITE'}] {target_path}")
    return target_path


def main():
    session_key = sys.argv[1] if len(sys.argv) >= 2 else None
    try:
        session_id = find_session_id(session_key)
        messages = load_session_messages(session_id)
        formatted = format_messages(messages, session_id)
        target_path = write_session(session_key, session_id, formatted)
        print(f"完成！寫入：{target_path}")
    except Exception as e:
        print(f"錯誤：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
