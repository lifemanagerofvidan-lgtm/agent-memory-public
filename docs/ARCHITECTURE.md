# Architecture

## Design goal

Build a lightweight, migration-friendly Agent Memory system that stores only durable collaboration memory and retrieves it through QMD.

## Principles

1. Minimal memory, not maximal knowledge capture
2. QMD is the main semantic retrieval layer
3. Main agent is the single canonical memory writer
4. Supporting agents are execution helpers, not independent long-term memory owners
5. Retrieval should use progressive disclosure

## High-level flow

```text
conversation
  -> session capture
  -> journal file
  -> minimal memory extraction
  -> classified memory note
  -> QMD update/embed
  -> later retrieval via qmd query/vsearch
```

## System components

### 1. Journal layer
Stores raw session history for traceability.

### 2. Agent Memory layer
Stores only durable memory types:
- Preferences
- Decisions
- Pitfalls
- People
- Projects
- Identity

### 3. Index layer
Minimal human-readable navigation only.
Not the main retrieval backbone.

### 4. Retrieval layer
QMD query and vector search over Agent Memory first, Journal second.

## Retrieval model

### First pass
Search `20_Agent-Memory/` using QMD.

### Second pass
Open the top matching memory notes.

### Third pass
If needed, inspect `10_Journal/` for source context.

This is the intended lightweight progressive disclosure model.

## Why knowledge extraction is removed

External knowledge changes quickly and is usually better fetched live.
This system should focus on memory that is specific to the user, the assistant, ongoing projects, and collaboration behavior.

## Canonical write policy

Canonical memory should be written by `main` only, unless the policy is intentionally changed later.
