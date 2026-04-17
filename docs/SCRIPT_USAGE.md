# Script Usage

This file explains what each script does, when to run it, and what it expects.

## Requirements

Before using these scripts, make sure you have:
- Python 3
- an Obsidian vault on disk
- QMD installed if you plan to refresh or query retrieval
- OpenClaw config access if you plan to run Journal-to-Memory extraction

## `scripts/save_to_raw.py`

### Purpose
Save one OpenClaw session into a clean Journal note.

### What it reads
- OpenClaw session files from the sessions directory

### What it writes
- a Markdown file under `10_Journal/YYYY/YYYY-MM-DD/`
- staged attachments under `10_Journal/_assets/`
- save bookkeeping under `state/sessions-written.json`

### Command

```bash
python3 scripts/save_to_raw.py "<session_key>"
```

### If no session key is provided
The script tries to use the latest available session file.

### Environment variables
- `AGENT_MEMORY_VAULT`
- `OPENCLAW_SESSIONS_DIR`

## `scripts/journal_to_memory.py`

### Purpose
Read one Journal note and extract durable Agent Memory candidates.

### What it reads
- one Journal markdown file
- `prompts/journal_to_memory_v1.md`
- OpenClaw gateway auth from `openclaw.json`

### What it writes
- zero or more canonical notes under `20_Agent-Memory/`
- extraction bookkeeping in `state/extraction-state.json`
- debug artifacts under `state/debug/` when needed

### Command

```bash
python3 scripts/journal_to_memory.py --source "/path/to/journal-note.md"
```

### Optional flags

```bash
--dry-run
--model minimax/MiniMax-M2.7
--agent-id main
```

### Output meanings
- `EXTRACTED` = wrote one or more notes
- `NO_SIGNAL` = no durable memory should be written
- `SKIP` = already processed same file content before
- `ERROR` = failed, inspect debug files and config

### Environment variables
- `AGENT_MEMORY_VAULT`
- `OPENCLAW_CONFIG`

## `scripts/qmd_refresh.py`

### Purpose
Refresh the QMD index after memory changes.

### What it does
1. runs `qmd update`
2. runs `qmd embed`
3. prints a short success or failure status

### Command

```bash
python3 scripts/qmd_refresh.py
```

## `scripts/journal_to_memory_cron.py`

### Purpose
Provide a cron-friendly entry point for Journal-to-Memory extraction.

### When to use it
Use it when you want scheduled extraction instead of one-off manual runs.

## `scripts/extraction_state.py`

### Purpose
Provide helpers for extraction state tracking.

### Note
This is a support module used by `journal_to_memory.py`, not a normal operator entry point.

## Beginner recommendation

If you are new, learn the scripts in this order:
1. `save_to_raw.py`
2. `qmd_refresh.py`
3. `journal_to_memory.py`

That order matches the mental model:
- save Journal
- refresh retrieval
- add automation later
