# Setup and Validation

## Goal

Help another operator install the environment, connect the vault and QMD correctly, and verify the system end to end.

If you want the fastest beginner path, also keep these two files open while following this guide:
- `docs/QUICKSTART_CHECKLIST.md`
- `docs/TROUBLESHOOTING.md`

## Before you begin

You need three things:
- an Obsidian vault on disk
- a working QMD installation
- this repo available locally

If any of those are missing, stop and fix that first.

## Step 1. Install Obsidian and create a vault

Obsidian is the Markdown app that stores the Journal and canonical memory notes.

Official site:
- <https://obsidian.md>

After installing Obsidian:
1. create a new vault or open an existing one
2. locate the vault folder on disk
3. confirm you can open that folder in Finder or your file manager

Default vault path used by the scripts in this repo:

```text
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/AgentMemoryVault
```

If your vault lives elsewhere, you can override it later with:

```bash
export AGENT_MEMORY_VAULT="/path/to/your/vault"
```

## Step 2. Install and verify QMD

QMD is the retrieval layer. It indexes the Markdown files and makes semantic search possible.

After installing QMD, verify the CLI works:

```bash
qmd status
```

You should not see `command not found`.

It is also helpful to confirm that these commands exist in your environment:

```bash
qmd update
qmd embed
qmd query "test"
```

If QMD is not installed or not working, this project cannot provide semantic retrieval.

## Step 3. Create the vault folder structure

Inside your vault, create this structure:

```text
00_Inbox/
10_Journal/
20_Agent-Memory/
20_Agent-Memory/Preferences/
20_Agent-Memory/Decisions/
20_Agent-Memory/Pitfalls/
20_Agent-Memory/People/
20_Agent-Memory/Projects/
20_Agent-Memory/Identity/
30_Index/
90_Archive/
```

## Step 4. Configure QMD collections

Edit:

```text
~/.config/qmd/index.yml
```

Use collections equivalent to:

```yaml
collections:
  agent-memory:
    path: /path/to/vault/20_Agent-Memory
    pattern: '**/*.md'
    weight: 2.4
  journal:
    path: /path/to/vault/10_Journal
    pattern: '**/*.md'
    weight: 0.8
  index:
    path: /path/to/vault/30_Index
    pattern: '**/*.md'
    weight: 0.4
  inbox:
    path: /path/to/vault/00_Inbox
    pattern: '**/*.md'
    weight: 0.2
  archive:
    path: /path/to/vault/90_Archive
    pattern: '**/*.md'
    weight: 0.1
search:
  hybrid: true
  rerank: true
  limit: 10
```

### Important checks

Before moving on, confirm:
- each `path:` points to a real folder on disk
- `agent-memory` points to `20_Agent-Memory`
- `journal` points to `10_Journal`
- `agent-memory` has a higher weight than `journal`

## Step 5. Build the first index

Run:

```bash
qmd update
qmd embed
```

Expected result:
- both commands succeed
- no path errors
- no YAML config errors

If they fail, use:
- `docs/TROUBLESHOOTING.md`

## Step 6. Create one test memory note

Create one Markdown note under:

```text
20_Agent-Memory/Preferences/
```

Example content:

```md
---
type: preference
status: active
visibility: shared
tags: [test, setup]
source_session: manual-test
created: 2026-04-17
updated: 2026-04-17
confidence: high
owner: main
---

# Prefer concise responses

## Summary
The user prefers concise responses that lead with the main point.

## Why it matters
This should shape future collaboration style.

## Retrieval hints
concise responses, short answers, lead with the main point
```

Then run again:

```bash
qmd update
qmd embed
```

## Step 7. Test retrieval

Run a query that should match your new note:

```bash
qmd query "concise responses"
```

Success looks like this:
- your intended note appears in the results
- ideally it appears near the top

## Step 8. Optional OpenClaw save flow

If you want OpenClaw to save sessions into Journal, configure your `/save10`-style flow to call:

```bash
python3 /path/to/projects/agent-memory-public/scripts/save_to_raw.py "<session_key>"
```

Optional environment overrides:

```bash
export AGENT_MEMORY_VAULT="/path/to/Obsidian/Vault"
export OPENCLAW_SESSIONS_DIR="/path/to/.openclaw/agents/main/sessions"
export OPENCLAW_CONFIG="/path/to/.openclaw/openclaw.json"
```

What this script does:
- reads one OpenClaw session
- removes system and tool noise
- writes a cleaned transcript into `10_Journal/YYYY/YYYY-MM-DD/`

## Step 9. Optional Journal-to-Memory extraction

If you want automation that turns Journal notes into canonical memory notes, run:

```bash
python3 scripts/journal_to_memory.py --source "/path/to/journal-note.md"
```

What to expect:
- `EXTRACTED` means notes were written
- `NO_SIGNAL` means the note had no durable memory worth saving
- `SKIP` means the exact same file was already processed
- `ERROR` means something failed and should be inspected

This script requires:
- Python 3
- access to `~/.openclaw/openclaw.json` or `OPENCLAW_CONFIG`
- a reachable OpenClaw gateway config

## End-to-end validation

A minimal validation pass should confirm all of these:
- one note exists under `20_Agent-Memory/`
- `qmd update` succeeds
- `qmd embed` succeeds
- `qmd query` returns the intended note
- optional: `/save10` writes a Journal note
- optional: `journal_to_memory.py` writes one or more canonical notes

## Known-good first validation pattern

A reliable first test is:
- one `preference` note
- one `project-state` note
- one `pitfall` note
- one query per type

## Common failure patterns

### QMD returns unrelated workspace docs
Your active QMD config probably still includes extra collections outside the vault.

### Journal writes but retrieval fails
Run `qmd update` and `qmd embed` again, then test the exact query wording from the note's retrieval hints.

### Retrieval finds only Journal but not canonical memory
Your `agent-memory` collection path or weight is probably wrong.
