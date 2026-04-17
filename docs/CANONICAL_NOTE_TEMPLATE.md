# Canonical Note Template

This document defines the standard note shape for canonical Agent Memory notes.

## Goals

- keep notes short and durable
- maximize retrieval quality for QMD
- keep enough metadata for filtering and visibility control
- avoid turning memory notes into long essays

## Required frontmatter

```yaml
type: preference
status: active
visibility: shared
tags: [collaboration, retrieval]
source_session: 20260417-100900-main
created: 2026-04-17
updated: 2026-04-17
confidence: high
owner: main
```

## Language rule

Canonical Agent Memory notes should use English for the main body fields:
- title
- summary
- why it matters
- optional trigger/action sections

`retrieval_hints` may use English, Chinese, or mixed phrasing when that improves real-world recall quality.

## Field definitions

- `type`: one of `preference`, `decision`, `pitfall`, `person`, `project-state`, `identity-rule`
- `status`: usually `active`, later may include `archived` or `superseded`
- `visibility`: `shared` or `main-only`
- `tags`: short retrieval-oriented keywords
- `source_session`: the originating Journal session id or filename stem
- `created`: canonical note creation date
- `updated`: latest meaningful update date
- `confidence`: `high`, `medium`, or `low`
- `owner`: default `main`

## Required body sections

```md
# Title

## Summary
One concise statement of the memory.

## Why it matters
Why this should affect future work, collaboration, or execution.

## Retrieval hints
Likely search phrases, aliases, tool names, or context clues.
```

## Optional body sections

Use only when they materially help.

```md
## Trigger
When this memory should be recalled.

## Action
What the assistant or another agent should do.

## Source note
Short reference to the originating Journal note.
```

## Type-specific guidance

### preference
Capture stable user preferences, collaboration style, formatting rules, and workflow habits.

### decision
Capture confirmed decisions that should shape later work.

### pitfall
Capture failure pattern, cause, fix, and prevention in concise form.

Suggested body:

```md
## Summary
A short statement of the pitfall.

## Why it matters
What it breaks or why it repeats.

## Retrieval hints
Error text, tool name, symptom keywords.

## Trigger
When this issue is likely to appear.

## Action
What to check or do first.
```

### person
Capture stable, non-sensitive information relevant to future work.

### project-state
Capture durable project direction, active constraints, or implementation status that will matter later.

### identity-rule
Capture assistant operating rules that should persist across sessions.

## Example

```md
---
type: preference
status: active
visibility: shared
tags: [traditional-chinese, concise, qmd]
source_session: 20260417-100900-main
created: 2026-04-17
updated: 2026-04-17
confidence: high
owner: main
---

# Boss prefers concise Traditional Chinese responses

## Summary
Default replies should be concise Traditional Chinese, with English technical terms preserved when useful.

## Why it matters
This affects nearly every reply, planning document, and technical explanation.

## Retrieval hints
language preference, concise replies, Traditional Chinese, technical English terms
```
