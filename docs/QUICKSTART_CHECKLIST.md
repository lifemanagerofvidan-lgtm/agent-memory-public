# Quickstart Checklist

Use this checklist if you want a beginner-friendly, step-by-step setup path.

## 1. Install the required apps

- [ ] I installed Obsidian.
- [ ] I installed QMD.
- [ ] I can open a terminal on my machine.

## 2. Create or choose an Obsidian vault

- [ ] I created or opened an Obsidian vault.
- [ ] I know the vault's filesystem path.
- [ ] I can open that folder in Finder or my file manager.

Expected default path on macOS if using iCloud Obsidian sync:

```text
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/AgentMemoryVault
```

## 3. Create the required folders inside the vault

- [ ] `00_Inbox/`
- [ ] `10_Journal/`
- [ ] `20_Agent-Memory/`
- [ ] `20_Agent-Memory/Preferences/`
- [ ] `20_Agent-Memory/Decisions/`
- [ ] `20_Agent-Memory/Pitfalls/`
- [ ] `20_Agent-Memory/People/`
- [ ] `20_Agent-Memory/Projects/`
- [ ] `20_Agent-Memory/Identity/`
- [ ] `30_Index/`
- [ ] `90_Archive/`

## 4. Confirm QMD is installed

Run:

```bash
qmd status
```

- [ ] The command runs successfully.
- [ ] I do not get "command not found".

## 5. Configure QMD to index this vault

Edit:

```text
~/.config/qmd/index.yml
```

- [ ] I found the config file.
- [ ] I pointed the `agent-memory` collection to my vault's `20_Agent-Memory` folder.
- [ ] I pointed the `journal` collection to my vault's `10_Journal` folder.
- [ ] I saved the config file.

## 6. Build the initial QMD index

Run:

```bash
qmd update
qmd embed
```

- [ ] `qmd update` succeeded.
- [ ] `qmd embed` succeeded.

## 7. Create one test memory note

Create a markdown file under:

```text
20_Agent-Memory/Preferences/
```

Example filename:

```text
preference-test-001.md
```

- [ ] I created one test note.
- [ ] The note is inside the correct folder.

## 8. Test retrieval

Run:

```bash
qmd query "test query here"
```

- [ ] QMD returns my note.
- [ ] My intended note appears near the top.

## 9. Optional OpenClaw save flow

If you use this project with OpenClaw:

- [ ] I know where this repo lives on disk.
- [ ] I know how my `/save10` flow calls `scripts/save_to_raw.py`.
- [ ] I understand that `save_to_raw.py` writes into `10_Journal/`.

## 10. Optional extraction flow

If you want Journal-to-Memory automation:

Run:

```bash
python3 scripts/journal_to_memory.py --source "/path/to/journal-note.md"
```

- [ ] Python 3 is installed.
- [ ] The script runs.
- [ ] It writes notes or returns a clear `NO_SIGNAL` / `SKIP` status.

## Done criteria

You are done when all of these are true:

- [ ] Obsidian vault exists
- [ ] QMD is configured
- [ ] QMD update works
- [ ] QMD embed works
- [ ] One memory note is retrievable
- [ ] Optional save and extraction scripts behave as expected

If something fails, go to:
- `docs/TROUBLESHOOTING.md`
- `docs/SETUP_AND_VALIDATION.md`
