# Multi-Agent Policy

## Recommended model

Single-brain, multi-agent.

- `main` is the primary long-term collaboration agent
- `coder`, `researcher`, and `deputy` are supporting agents invoked by `main`

## Why

This preserves memory quality and avoids fragmented personalities, duplicate memory, and conflicting writes.

## Read policy

### Shared-readable memory
Supporting agents may read:
- Preferences
- Decisions
- Pitfalls
- Projects
- selected Identity rules

### Restricted memory
Some notes may be `main-only`, especially:
- sensitive people notes
- nuanced user-facing interaction notes
- private relational context

## Write policy

### Default
Only `main` writes canonical memory.

### Supporting agents
Supporting agents may produce:
- memory candidates
- pitfall candidates
- project-state update candidates

These should be reviewed by `main` before canonical write.

## Benefits
- better coordination
- cleaner memory quality
- lower duplication risk
- simpler mental model for the user
