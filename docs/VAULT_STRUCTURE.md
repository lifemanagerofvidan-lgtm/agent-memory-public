# Vault Structure

## Recommended Obsidian vault layout

```text
Agent-Memory/
├── 00_Inbox/
├── 10_Journal/
│   └── YYYY/
│       └── YYYY-MM-DD/
├── 20_Agent-Memory/
│   ├── Preferences/
│   ├── Decisions/
│   ├── Pitfalls/
│   ├── People/
│   ├── Projects/
│   └── Identity/
├── 30_Index/
└── 90_Archive/
```

## Folder roles

### 00_Inbox
Optional holding area for uncategorized future inputs.

### 10_Journal
Raw captured sessions. These are source records, not canonical memory.

### 20_Agent-Memory
Canonical memory notes used for retrieval.

### 30_Index
Minimal category overview and active project navigation for humans.

### 90_Archive
Inactive, superseded, or stale notes.

## Canonical memory note schema

Suggested frontmatter:

```yaml
type: pitfall
status: active
tags: [openclaw, qmd, retrieval]
source_session: 20260417-094500-main
created: 2026-04-17
updated: 2026-04-17
confidence: high
visibility: shared
```

## Visibility guidance

- `shared`: readable by supporting agents
- `main-only`: readable only by main-facing workflows

## Minimal note body pattern

```md
# Title

## Summary
One concise statement of the memory.

## Why it matters
Why this should affect future work.

## Retrieval hints
Keywords, aliases, and likely future search phrases.
```
