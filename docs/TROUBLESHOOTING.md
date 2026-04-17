# Troubleshooting

This guide covers the most common setup and validation failures for Agent Memory.

## 1. `qmd: command not found`

### What it means
QMD is not installed correctly, or your shell cannot find it.

### What to check
- confirm QMD is installed
- confirm the binary is on your shell `PATH`
- open a new terminal and run:

```bash
qmd status
```

### Fix
Install QMD using its upstream install instructions, then verify the command again.

## 2. `qmd update` fails

### Common causes
- syntax error in `~/.config/qmd/index.yml`
- one of the configured paths does not exist
- QMD cannot read one of the indexed folders

### What to check
- open `~/.config/qmd/index.yml`
- verify indentation is valid YAML
- verify every configured `path:` exists on disk
- temporarily reduce the config to only the Agent Memory collections used by this project

## 3. `qmd embed` fails

### Common causes
- QMD is configured, but embeddings are not set up correctly in the local environment
- the previous `qmd update` step did not complete successfully

### What to check
- run `qmd update` first and confirm it succeeds
- run `qmd status`
- check your QMD environment and provider configuration

## 4. `qmd query` returns unrelated notes

### What it usually means
Your QMD config is still indexing extra folders outside this vault.

### Fix
Reduce your active collections to only:
- `20_Agent-Memory/`
- `10_Journal/`
- `30_Index/`
- `00_Inbox/`
- `90_Archive/`

Then run:

```bash
qmd update
qmd embed
```

## 5. `qmd query` only finds Journal notes, not canonical memory notes

### What it usually means
The `agent-memory` collection path or weight is wrong.

### What to check
- confirm `agent-memory.path` points to `<vault>/20_Agent-Memory`
- confirm the folder actually contains `.md` files
- confirm `agent-memory` has a higher weight than `journal`

## 6. Obsidian vault not found

### What it means
The scripts are pointing at a vault path that does not exist.

### What to check
Default vault path used by the scripts:

```text
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/AgentMemoryVault
```

If your vault is elsewhere, set:

```bash
export AGENT_MEMORY_VAULT="/your/real/vault/path"
```

## 7. `save_to_raw.py` runs, but no Journal note appears

### Common causes
- the OpenClaw session path is wrong
- the vault path is wrong
- the session key does not match an existing session file

### What to check
- confirm `AGENT_MEMORY_VAULT` points to the correct vault
- confirm `OPENCLAW_SESSIONS_DIR` points to real OpenClaw session files
- confirm the session file exists as `*.jsonl`

### Helpful note
If no session key is provided, `save_to_raw.py` tries to use the latest available session file.

## 8. `journal_to_memory.py` fails immediately

### Common causes
- Python 3 is missing
- `OPENCLAW_CONFIG` points to the wrong location
- the OpenClaw gateway token cannot be loaded
- the source file path is wrong

### What to check
- run `python3 --version`
- confirm this file exists:

```text
~/.openclaw/openclaw.json
```

- if your OpenClaw config lives elsewhere, set:

```bash
export OPENCLAW_CONFIG="/your/real/openclaw.json"
```

## 9. `journal_to_memory.py` returns `NO_SIGNAL`

### What it means
The script ran successfully, but the Journal note did not contain durable memory worth writing.

### This is not necessarily an error
Expected examples:
- casual chat without durable collaboration signal
- short status updates
- one-off remarks that should not become long-term memory

## 10. `journal_to_memory.py` returns `SKIP`

### What it means
The exact same Journal file was already processed successfully before.

### Why this happens
The project tracks:
- source path
- source file hash
- last terminal status

If you changed the Journal file content, run the script again after saving the updated file.

## 11. `journal_to_memory.py` returns `ERROR`

### What to check first
- confirm the source Journal file exists
- confirm OpenClaw gateway auth can be loaded from `openclaw.json`
- inspect the latest debug artifacts under:

```text
state/debug/
```

Useful files include:
- `last_responses_body.json`
- `last_output_text.txt`
- `last_output_text_cleaned.txt`

## 12. The model returns JSON inside code fences

### Background
This project already defends against fenced JSON in the current implementation.

### If parsing still fails
Open the debug files in `state/debug/` and inspect the exact output text.

## 13. I do not know which file to read first

Use this order:
1. `../README.md`
2. `SETUP_AND_VALIDATION.md`
3. `QUICKSTART_CHECKLIST.md`
4. `TROUBLESHOOTING.md`

## 14. I do not know whether my setup is actually complete

A setup is complete only if all of these work:
- `qmd status`
- `qmd update`
- `qmd embed`
- `qmd query "..."`
- one real note under `20_Agent-Memory/` is retrievable

If you want a stricter checklist, use:
- `QUICKSTART_CHECKLIST.md`
