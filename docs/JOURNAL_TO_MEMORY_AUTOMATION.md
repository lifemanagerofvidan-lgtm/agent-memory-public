# Journal to Memory Automation

## Goal

Define the v1 automation path from `10_Journal/` to `20_Agent-Memory/`.

## Core requirement

A Journal note that was already processed should not be processed again unless its content actually changed.

## v1 design

### Input
- one Journal note under `10_Journal/`

### Output
- zero or more canonical memory notes under `20_Agent-Memory/`
- one state record in `state/extraction-state.json`

## Allowed memory types
- preference
- decision
- pitfall
- person
- project-state
- identity-rule

## Language rule

Canonical notes written into `20_Agent-Memory/` should use English for the main note body.
`retrieval_hints` may use English, Chinese, or mixed phrasing when needed for better recall.

## Processing states
- `extracted`
- `no_signal`
- `error`

## Source identity rule

A Journal note is considered already processed only when:
- `source_path` matches
- `source_sha256` matches
- previous status is terminal (`extracted` or `no_signal`)

If the file path is the same but content changed, it must be treated as needing reprocessing.

## Required state fields

```json
{
  "source_path": ".../10_Journal/.../file.md",
  "source_sha256": "...",
  "source_session_id": "...",
  "status": "extracted",
  "processed_at": "2026-04-17T12:49:00+08:00",
  "outputs": [
    ".../20_Agent-Memory/.../note.md"
  ],
  "last_error": null
}
```

## Skip rule

Skip when:
- same `source_path`
- same `source_sha256`
- status is `extracted` or `no_signal`

## Retry rule

Retry when:
- no prior state exists
- prior state is `error`
- same path but different sha256

## Why path-only is not enough

A Journal file may be overwritten in place while keeping the same filename.
Path-only tracking would miss meaningful content changes.

## Why hash-only is not enough

Hash-only tracking makes it harder to understand which source file was processed and what outputs came from it.

## v1 implementation shape

- `scripts/extraction_state.py`
- `scripts/journal_to_memory.py`
- `state/extraction-state.json`

## v1 scope

This first implementation focuses on:
- state tracking
- duplicate prevention
- content-change detection
- clear skip/retry behavior

The current implementation keeps automation deliberately simple, with extraction handled by a dedicated live cron job.
