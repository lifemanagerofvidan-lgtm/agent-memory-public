# Agent Memory

A minimal, human-readable long-term memory system for OpenClaw assistants.

Agent Memory stores durable collaboration memory in an Obsidian vault and uses QMD for retrieval.
It is designed to stay small, inspectable, and easy to migrate.

This project is intentionally **not** a general knowledge base and does **not** perform broad knowledge extraction from the web.

**Why people may like it:**
- simple Markdown storage
- explicit retrieval layer
- easy manual mode before automation
- low conceptual overhead
- migration-friendly structure

## Why this project exists

Many assistant memory systems become hard to trust because they are too broad, too hidden, or too noisy.

Agent Memory takes the opposite approach:
- keep the memory model narrow
- keep the storage readable
- keep the retrieval layer explicit
- keep setup simple enough that another operator can reproduce it

## Why not just use a normal notes vault or a giant knowledge base?

Because assistant memory has different needs.

A normal notes vault often becomes too loose.
A giant knowledge base often becomes too broad.
Agent Memory focuses on a smaller target:
- durable collaboration preferences
- project state that matters later
- pitfalls worth avoiding next time
- decisions that should keep influencing behavior

That narrower scope makes retrieval cleaner and maintenance easier.

## Who this is for

Use this project if you want:
- a human-readable memory system in Markdown
- semantic retrieval over durable assistant memory
- a small, inspectable setup instead of a large hidden pipeline

This project is a good fit for operators who use:
- OpenClaw
- Obsidian
- QMD

If you are new to any of those tools, start with:
- `docs/SETUP_AND_VALIDATION.md`
- `docs/TROUBLESHOOTING.md`

## What this project does

- saves conversation transcripts into an Obsidian Journal
- turns selected durable facts into canonical Agent Memory notes
- retrieves those notes later through QMD semantic search
- keeps the system small, understandable, and publishable

## Core ideas

- **Journal is raw history**: save conversations without pretending all of them are memory
- **Agent Memory is distilled**: store only durable notes that should matter later
- **QMD is retrieval**: use a dedicated search layer instead of inventing hidden magic
- **Manual mode comes first**: validate the memory model before adding automation

## What this project does not do

- build a broad concept / reference / workflow wiki
- continuously distill outside knowledge into a vault
- rely on hidden project dependencies outside this folder for its live save path
- use heavy automation before the memory model is stable

## 5-minute mental model

```text
conversation
  -> save transcript into 10_Journal/
  -> write durable notes into 20_Agent-Memory/
  -> run qmd update + qmd embed
  -> retrieve later with qmd query
```

## What you get after setup

After setup, you should have:
- a clean Obsidian vault for assistant memory
- a `10_Journal/` area for raw saved conversations
- a `20_Agent-Memory/` area for durable canonical notes
- QMD indexing and retrieval over those notes
- a path to add OpenClaw save and extraction automation later

## Quick start

Typical first-time setup time:
- about 10 to 20 minutes for the basic manual path

If you want the shortest path to a working setup, do this in order:

1. Install Obsidian and create a vault.
2. Install QMD and confirm `qmd status` works.
3. Create the required vault folders.
4. Point QMD at those folders.
5. Run `qmd update` and `qmd embed`.
6. Create one test memory note.
7. Run `qmd query "..."` and confirm the note is found.

If you only want manual mode, you can stop there.
That path is enough to understand the project before touching automation.

Start here for exact steps:
- `docs/SETUP_AND_VALIDATION.md`
- `docs/QUICKSTART_CHECKLIST.md`
- `docs/TROUBLESHOOTING.md`

Useful examples:
- `examples/qmd/index.yml`
- `examples/notes/sample-canonical-note.md`
- `examples/notes/sample-journal-note.md`

## In one sentence

Agent Memory gives an OpenClaw assistant a small, inspectable memory system that is easy to understand before it is easy to automate.

## System overview

### Storage layer
Obsidian as the human-readable memory store.

### Retrieval layer
QMD as the semantic and hybrid search layer.

### Memory model
Only durable Agent Memory types:
- preference
- decision
- pitfall
- person
- project-state
- identity-rule

### Multi-agent model
Single-brain, multi-agent:
- `main` is the canonical memory writer
- supporting agents may read shared memory and suggest memory candidates
- supporting agents should not become independent long-term memory owners by default

## Environment requirements

This project assumes two core environments.

### 1. Obsidian environment
You need:
- Obsidian installed
- a vault path available on disk
- read/write access to that vault path

Default vault path used by the scripts:

```text
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/AgentMemoryVault
```

You can override this with:
- `AGENT_MEMORY_VAULT`

### 2. QMD environment
You need:
- QMD installed and working
- a valid QMD config file
- the ability to run:
  - `qmd status`
  - `qmd update`
  - `qmd embed`
  - `qmd query "..."`

Default QMD config path:

```text
~/.config/qmd/index.yml
```

## Path map

These are the paths most operators need to understand first.

| Item | Default path | Purpose |
| --- | --- | --- |
| Obsidian vault root | `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/AgentMemoryVault` | stores Journal and canonical memory notes |
| Journal notes | `<vault>/10_Journal/` | raw saved conversations |
| Canonical memory notes | `<vault>/20_Agent-Memory/` | durable memory used for retrieval |
| QMD config | `~/.config/qmd/index.yml` | tells QMD what to index |
| Save script | `scripts/save_to_raw.py` | writes session transcripts into Journal |
| Extraction script | `scripts/journal_to_memory.py` | turns Journal into canonical memory notes |
| QMD refresh script | `scripts/qmd_refresh.py` | runs `qmd update` and `qmd embed` |
| Local state | `state/` | keeps extraction and save bookkeeping |

## Configuration overrides

Public scripts support these environment variables:

```text
AGENT_MEMORY_VAULT
OPENCLAW_SESSIONS_DIR
OPENCLAW_CONFIG
```

## Script entry points

### Save a session into Journal

```bash
python3 scripts/save_to_raw.py "<session_key>"
```

### Extract durable memory from a Journal note

```bash
python3 scripts/journal_to_memory.py --source "/path/to/journal-note.md"
```

### Refresh QMD after memory changes

```bash
python3 scripts/qmd_refresh.py
```

## What good looks like

A basic working system should let you do all of these successfully:
- save one conversation into `10_Journal/`
- create or extract one canonical note into `20_Agent-Memory/`
- run `qmd update`
- run `qmd embed`
- retrieve the intended note with `qmd query`

## Recommended reading order

If you are new, read in this order:

1. `README.md`
2. `docs/SETUP_AND_VALIDATION.md`
3. `docs/QUICKSTART_CHECKLIST.md`
4. `docs/TROUBLESHOOTING.md`
5. `docs/FAQ.md`
6. `docs/ARCHITECTURE_DIAGRAM.md`
7. `docs/ARCHITECTURE.md`
8. `docs/VAULT_STRUCTURE.md`
9. `docs/WORKFLOW.md`

If you want deeper implementation details after setup, continue with:
- `docs/SCRIPT_USAGE.md`
- `docs/CANONICAL_NOTE_TEMPLATE.md`
- `docs/JOURNAL_TO_MEMORY_AUTOMATION.md`
- `docs/QMD_AUTOMATION.md`
- `docs/CRON_STRATEGY.md`
- `docs/QMD_RETRIEVAL_RULES.md`
- `docs/MULTI_AGENT_POLICY.md`
- `docs/VISIBILITY_POLICY.md`

## Maintainer docs

Some files are mainly useful for maintainers, migration history, or project evolution.
They are not required for a first-time setup.

These include:
- `docs/internal/PROJECT_UPDATES.md`
- `docs/internal/EXECUTION_CHECKLIST.md`
- `docs/internal/MIGRATION_PLAN.md`
- `docs/internal/PUBLISHING_RULES.md`
- `docs/OPENCLAW_CRON_LLM_INTEGRATION.md`
- `docs/TOOLS_MD_REFERENCE.md`

## File map

```text
agent-memory-public/
├── README.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── ARCHITECTURE_DIAGRAM.md
│   ├── FAQ.md
│   ├── QUICKSTART_CHECKLIST.md
│   ├── SCRIPT_USAGE.md
│   ├── SETUP_AND_VALIDATION.md
│   ├── TROUBLESHOOTING.md
│   ├── VAULT_STRUCTURE.md
│   ├── WORKFLOW.md
│   ├── CANONICAL_NOTE_TEMPLATE.md
│   ├── JOURNAL_TO_MEMORY_AUTOMATION.md
│   ├── QMD_AUTOMATION.md
│   ├── CRON_STRATEGY.md
│   ├── QMD_RETRIEVAL_RULES.md
│   ├── MULTI_AGENT_POLICY.md
│   ├── VISIBILITY_POLICY.md
│   ├── OPENCLAW_CRON_LLM_INTEGRATION.md
│   ├── TOOLS_MD_REFERENCE.md
│   └── internal/
├── examples/
│   ├── qmd/
│   │   └── index.yml
│   └── notes/
│       ├── sample-canonical-note.md
│       └── sample-journal-note.md
├── prompts/
│   └── journal_to_memory_v1.md
├── scripts/
│   ├── save_to_raw.py
│   ├── journal_to_memory.py
│   ├── journal_to_memory_cron.py
│   ├── qmd_refresh.py
│   └── extraction_state.py
└── state/
    └── README.md
```

## Status

This publication copy reflects a working system that has already validated:
- Journal writing via a `/save10`-style flow
- canonical memory note creation
- QMD indexing and embedding
- successful retrieval across multiple Agent Memory note types

See also:
- `docs/SETUP_AND_VALIDATION.md`
- `docs/FAQ.md`
- `docs/ARCHITECTURE_DIAGRAM.md`
