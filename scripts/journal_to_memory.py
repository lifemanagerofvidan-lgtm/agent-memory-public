#!/usr/bin/env python3
"""
journal_to_memory.py — extract durable Agent Memory candidates from one Journal note.

Behavior:
- reads one Journal markdown source
- sends prompt + Journal text to OpenClaw `/v1/responses`
- validates the returned JSON structure
- writes zero or more canonical notes into `20_Agent-Memory/`
- records extraction status in `state/extraction-state.json`

Stdout contract:
- `SKIP <path>` when the source was already processed with the same hash
- `NO_SIGNAL <path>` when no durable memory should be written
- `EXTRACTED` followed by one output path per written note
- `ERROR <message>` on failure
"""

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

from extraction_state import load_state, save_state, should_skip, record_result

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
PROMPT_FILE = PROJECT_ROOT / "prompts" / "journal_to_memory_v1.md"
DEFAULT_VAULT_ROOT = Path.home() / "Library" / "Mobile Documents" / "iCloud~md~obsidian" / "Documents" / "AgentMemoryVault"
VAULT_ROOT = Path(os.environ.get("AGENT_MEMORY_VAULT", DEFAULT_VAULT_ROOT)).expanduser()
JOURNAL_ROOT = VAULT_ROOT / "10_Journal"
MEMORY_ROOT = VAULT_ROOT / "20_Agent-Memory"
OPENCLAW_CONFIG = Path(os.environ.get("OPENCLAW_CONFIG", str(Path.home() / ".openclaw" / "openclaw.json"))).expanduser()
DEFAULT_MODEL = "minimax/MiniMax-M2.7"
DEFAULT_AGENT_ID = "main"

TYPE_DIRS = {
    "preference": MEMORY_ROOT / "Preferences",
    "decision": MEMORY_ROOT / "Decisions",
    "pitfall": MEMORY_ROOT / "Pitfalls",
    "person": MEMORY_ROOT / "People",
    "project-state": MEMORY_ROOT / "Projects",
    "identity-rule": MEMORY_ROOT / "Identity",
}

ALLOWED_TYPES = set(TYPE_DIRS.keys())


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def extract_session_id(text: str):
    m = re.search(r"^SessionId:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def find_latest_journal():
    files = sorted(JOURNAL_ROOT.rglob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-") or "memory-note"


def load_openclaw_auth():
    data = json.loads(OPENCLAW_CONFIG.read_text(encoding="utf-8"))
    token = data["gateway"]["auth"]["token"]
    base = data.get("gateway", {}).get("http", {}).get("baseURL")
    if not base:
        base = "http://127.0.0.1:18789"
    return base.rstrip("/"), token


def load_prompt_text():
    return PROMPT_FILE.read_text(encoding="utf-8")


def call_llm(prompt_text: str, journal_text: str, model: str, agent_id: str):
    base, token = load_openclaw_auth()
    url = f"{base}/v1/responses"
    payload = {
        "model": model,
        "input": f"{prompt_text}\n\n## Journal source\n\n{journal_text}",
    }
    req = urllib.request.Request(url, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("x-openclaw-agent-id", agent_id)
    data = json.dumps(payload).encode("utf-8")
    with urllib.request.urlopen(req, data=data, timeout=120) as resp:
        body = resp.read().decode("utf-8")

    debug_dir = PROJECT_ROOT / "state" / "debug"
    debug_dir.mkdir(parents=True, exist_ok=True)
    (debug_dir / "last_responses_body.json").write_text(body, encoding="utf-8")

    parsed = json.loads(body)

    output_text = None
    for item in parsed.get("output", []):
        if item.get("type") == "message":
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    output_text = content.get("text")
                    break
        if output_text:
            break

    if not output_text and isinstance(parsed.get("output_text"), str):
        output_text = parsed["output_text"]

    (debug_dir / "last_output_text.txt").write_text(output_text or "", encoding="utf-8")

    if not output_text:
        raise RuntimeError("No output text returned from /v1/responses")

    cleaned = output_text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        (debug_dir / "last_output_text_cleaned.txt").write_text(cleaned, encoding="utf-8")
        raise RuntimeError(f"Model did not return valid JSON: {cleaned[:1000]}") from exc


def normalize_visibility(value: str) -> str:
    return value if value in {"shared", "main-only"} else "shared"


def write_memory_note(candidate: dict, source_session: str):
    memory_type = candidate["type"]
    target_dir = TYPE_DIRS[memory_type]
    target_dir.mkdir(parents=True, exist_ok=True)
    title = candidate["title"].strip()
    slug = slugify(title)
    path = target_dir / f"{memory_type}-{slug}-001.md"
    tags = candidate.get("retrieval_hints", [])
    tags_str = ", ".join([t.strip() for t in tags if str(t).strip()])
    visibility = normalize_visibility(candidate.get("visibility", "shared"))
    content = f"""---
type: {memory_type}
status: active
visibility: {visibility}
tags: [{tags_str}]
source_session: {source_session or 'unknown'}
created: {datetime.now().date().isoformat()}
updated: {datetime.now().date().isoformat()}
confidence: high
owner: main
---

# {title}

## Summary
{candidate['summary'].strip()}

## Why it matters
{candidate['why_it_matters'].strip()}

## Retrieval hints
{tags_str}
"""
    if path.exists():
        counter = 2
        while True:
            candidate_path = target_dir / f"{memory_type}-{slug}-{counter:03d}.md"
            if not candidate_path.exists():
                path = candidate_path
                break
            counter += 1

    path.write_text(content, encoding="utf-8")
    return path


def validate_candidates(result: dict):
    if result.get("result") != "candidates":
        return result
    cleaned = []
    for candidate in result.get("candidates", []):
        ctype = candidate.get("type")
        if ctype not in ALLOWED_TYPES:
            continue
        required = ["title", "summary", "why_it_matters"]
        if not all(candidate.get(k) for k in required):
            continue
        candidate["retrieval_hints"] = candidate.get("retrieval_hints", [])
        cleaned.append(candidate)
    if not cleaned:
        return {"result": "no_signal", "reason": "no valid candidates"}
    return {"result": "candidates", "candidates": cleaned}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--agent-id", default=DEFAULT_AGENT_ID)
    args = parser.parse_args()

    source = Path(args.source).expanduser() if args.source else find_latest_journal()
    if not source or not source.exists():
        print("No journal source found")
        sys.exit(1)

    text = source.read_text(encoding="utf-8")
    source_sha = sha256_file(source)
    session_id = extract_session_id(text)
    state = load_state()
    source_key = str(source)

    if should_skip(state, source_key, source_sha):
        print(f"SKIP {source}")
        return

    prompt_text = load_prompt_text()

    try:
        result = validate_candidates(call_llm(prompt_text, text, args.model, args.agent_id))
    except Exception as e:
        record_result(state, source_key, source_sha, session_id, "error", outputs=[], last_error=str(e))
        save_state(state)
        print(f"ERROR {e}")
        sys.exit(1)

    if result.get("result") == "no_signal":
        record_result(state, source_key, source_sha, session_id, "no_signal", outputs=[], last_error=None)
        save_state(state)
        print(f"NO_SIGNAL {source}")
        return

    outputs = []
    for candidate in result.get("candidates", []):
        if args.dry_run:
            outputs.append(f"DRY_RUN:{candidate['type']}:{candidate['title']}")
            continue
        output = write_memory_note(candidate, session_id or source.stem)
        outputs.append(str(output))

    if not args.dry_run:
        record_result(state, source_key, source_sha, session_id, "extracted", outputs=outputs, last_error=None)
        save_state(state)
    print("EXTRACTED")
    for item in outputs:
        print(item)


if __name__ == "__main__":
    main()
