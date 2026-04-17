# FAQ

## What is this project for?

It gives an OpenClaw assistant a small, durable, human-readable memory system.

Instead of storing everything, it stores only collaboration memory that is likely to matter later.

## What will I have after setup?

After setup, you should have:
- an Obsidian vault containing Journal notes and canonical memory notes
- QMD indexing that vault for retrieval
- a workflow for saving conversations and finding durable memory later

## Do I need OpenClaw to use this repo?

Not for the basic memory model.

You can use the vault structure and QMD retrieval manually without OpenClaw automation.

You only need OpenClaw-specific integration if you want flows like:
- `/save10`
- Journal-to-Memory extraction through the local OpenClaw gateway

## Do I need Obsidian?

You need a Markdown vault on disk.

Obsidian is the intended tool and the docs assume it, but the deeper requirement is really:
- a local vault folder
- readable and writable Markdown files

## Do I need QMD?

Yes, if you want semantic retrieval.

Without QMD, this repo is just a structured Markdown memory vault.

## Is this a knowledge base?

No.

This project is intentionally narrower than a general wiki or PKM system.
It focuses on durable assistant memory such as:
- preferences
- decisions
- pitfalls
- people
- project-state
- identity rules

## How long should setup take?

For a first-time operator:
- about 10 to 20 minutes for basic manual setup
- longer if QMD is new to you or your local environment needs debugging

## What is the easiest way to validate my setup?

Use this sequence:
1. create the vault folders
2. configure QMD
3. create one test note under `20_Agent-Memory/Preferences/`
4. run `qmd update`
5. run `qmd embed`
6. run `qmd query "..."`

If your note shows up, the core retrieval path works.

## What is the easiest way to start if I do not want automation yet?

Use manual mode first.

That means:
- skip `/save10`
- skip cron
- skip Journal-to-Memory extraction
- create a few canonical memory notes by hand
- confirm QMD retrieval works

This is the best beginner path.

## Why are Journal and canonical memory separate?

Because they serve different purposes.

- `10_Journal/` stores raw captured conversations
- `20_Agent-Memory/` stores distilled durable memory

If those are mixed together, retrieval quality and maintainability both get worse.

## Why does the project prefer canonical notes over Journal notes in retrieval?

Because canonical notes are smaller, cleaner, and more durable.

Journal notes are useful supporting evidence, but they are not the best primary memory surface.

## What does `NO_SIGNAL` mean in Journal-to-Memory extraction?

It means the Journal note did not contain durable memory worth saving.

That is a valid outcome, not necessarily an error.

## What does `SKIP` mean?

It means the same Journal file content was already processed before.

The project uses both file path and file hash to decide this.

## Where should I start reading if I am new?

Use this order:
1. `../README.md`
2. `SETUP_AND_VALIDATION.md`
3. `QUICKSTART_CHECKLIST.md`
4. `TROUBLESHOOTING.md`
5. `SCRIPT_USAGE.md`
