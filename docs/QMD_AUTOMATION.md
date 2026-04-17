# QMD Automation

## Goal

Refresh the Agent Memory retrieval index after new canonical memory has been written.

## Scope

This automation handles:
- `qmd update`
- `qmd embed`

It should run after Journal-to-Memory extraction is already working.

## Script

```text
projects/agent-memory/scripts/qmd_refresh.py
```

## Behavior

The script:
1. runs `qmd update`
2. runs `qmd embed`
3. prints a short plain-text status line

## Intended cron shape

A separate OpenClaw cron job should call:

```bash
python3 /path/to/projects/agent-memory-public/scripts/qmd_refresh.py
```

Recommended delivery behavior during stabilization:
- announce status to an operator-facing channel

Possible later behavior:
- quieter or silent delivery once the system is stable

## Dependency order

The correct order is:

```text
10_Journal
  -> 20_Agent-Memory extraction
  -> QMD refresh
```

Do not treat QMD refresh as the primary automation stage.
It is the second stage after successful memory extraction.
