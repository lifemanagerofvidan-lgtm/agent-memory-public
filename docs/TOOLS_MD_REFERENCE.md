# TOOLS.md Reference

This file documents a recommended workspace-level `TOOLS.md` convention for Agent Memory recall behavior.

It is included here as project reference so another operator or maintainer knows which workspace rule should exist outside the project folder.

## Recommended recall rule

```md
- Recall convention: when a user asks about prior interactions, earlier discussions, previous decisions, older plans, time-based past context, or anything phrased like「妳記得……嗎？」「我們之前說過……」「上次提過……」「上禮拜……」, treat it as a recall trigger. Search Agent Memory in Obsidian via QMD first, then use Journal notes for supporting context when needed. OpenClaw builtin memory (`memory_search`) can be used as a secondary recall source.
```

## Why this matters

The project itself can define architecture and workflow, but actual assistant behavior inside OpenClaw may also depend on workspace-level instructions.

This recall convention helps ensure that past-interaction questions trigger the intended retrieval path:

1. Agent Memory via QMD first
2. Journal for supporting context when needed
3. builtin memory as a secondary source

## Scope

This file is a documentation reference only.
It does not replace the real workspace `TOOLS.md`.
