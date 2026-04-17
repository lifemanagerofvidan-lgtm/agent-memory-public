#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
STATE_FILE = PROJECT_ROOT / "state" / "extraction-state.json"


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"sources": {}}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def get_record(state, source_path):
    return state.get("sources", {}).get(source_path)


def is_terminal_status(status):
    return status in {"extracted", "no_signal"}


def should_skip(state, source_path, source_sha256):
    record = get_record(state, source_path)
    if not record:
        return False
    return record.get("source_sha256") == source_sha256 and is_terminal_status(record.get("status"))


def record_result(state, source_path, source_sha256, source_session_id, status, outputs=None, last_error=None):
    state.setdefault("sources", {})[source_path] = {
        "source_path": source_path,
        "source_sha256": source_sha256,
        "source_session_id": source_session_id,
        "status": status,
        "processed_at": datetime.now().astimezone().isoformat(),
        "outputs": outputs or [],
        "last_error": last_error,
    }
    return state
