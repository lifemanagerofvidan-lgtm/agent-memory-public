#!/usr/bin/env python3
"""
journal_to_memory_cron.py — cron-facing wrapper for Journal-to-Memory extraction.

Runs the extractor once, then prints a compact one-line status summary suitable
for OpenClaw cron announcements.
"""

import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
EXTRACTOR = PROJECT_ROOT / "scripts" / "journal_to_memory.py"
STATE_FILE = PROJECT_ROOT / "state" / "extraction-state.json"


def load_state_count():
    if not STATE_FILE.exists():
        return 0
    data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return len(data.get("sources", {}))


def main():
    before = load_state_count()
    proc = subprocess.run(
        [sys.executable, str(EXTRACTOR)],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
    )
    after = load_state_count()
    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()

    extracted_journals = 0
    extracted_memories = 0
    status = "success" if proc.returncode == 0 else "failed"

    if stdout.startswith("EXTRACTED"):
        extracted_journals = 1
        extracted_memories = max(0, len([line for line in stdout.splitlines()[1:] if line.strip()]))
    elif stdout.startswith("NO_SIGNAL"):
        extracted_journals = 1
        extracted_memories = 0
    elif stdout.startswith("SKIP"):
        extracted_journals = 0
        extracted_memories = 0
    elif stdout.startswith("ERROR"):
        extracted_journals = 1
        extracted_memories = 0

    lines = [
        f"status: {status}",
        f"journal_processed: {extracted_journals}",
        f"memory_written: {extracted_memories}",
        f"state_records_before: {before}",
        f"state_records_after: {after}",
    ]

    if stdout:
        lines.append(f"stdout: {stdout.splitlines()[0]}")
    if proc.returncode != 0 and stderr:
        lines.append(f"stderr: {stderr.splitlines()[0]}")

    print(" | ".join(lines))
    sys.exit(proc.returncode)


if __name__ == "__main__":
    main()
