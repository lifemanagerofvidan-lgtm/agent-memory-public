# Memory Write Workflow

## Goal

Define the first practical write path for canonical Agent Memory notes.

## Recommended v1 workflow

Human-approved, main-written, low-automation.

This keeps the system simple while the new structure is stabilizing.

## v1 write path

### Step 1. Source exists
A conversation is saved or otherwise available as a source session in `10_Journal/`.

### Step 2. Main identifies durable memory
`main` decides whether the session contains one of the allowed memory types:
- preference
- decision
- pitfall
- person
- project-state
- identity-rule

### Step 3. Main writes one canonical note
Write a short canonical memory note into the correct folder under `20_Agent-Memory/`.

### Step 4. Refresh QMD if the vault changed
Run QMD update/embed only after real note creation or meaningful note edits.

### Step 5. Validate retrieval
Test with one realistic future-style query.

## Why this workflow

- low risk
- low complexity
- easy to audit
- no accidental memory spam
- no premature automation lock-in

## Deferred for later versions

Not included in v1:
- auto-writing from every session
- background extraction cron
- automatic candidate queue
- supporting-agent direct writes

## Supporting agent behavior

Supporting agents may suggest memory candidates in normal task replies, but `main` remains the canonical writer.

## Canonical note naming

Recommended filename pattern:

```text
{type}-{slug}-001.md
```

Examples:
- `preference-concise-traditional-chinese-default-001.md`
- `pitfall-qmd-results-need-full-note-check-001.md`
- `project-state-agent-memory-uses-single-brain-model-001.md`

These are filename examples only, not files that must already exist in the repo.

## Write threshold

Create a note only if it is likely to help:
- future collaboration
- future execution
- future retrieval
- future error avoidance

If not, do not write it.
