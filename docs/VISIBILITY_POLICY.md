# Visibility Policy

This document defines which Agent Memory notes should be shared with supporting agents and which should stay main-only.

## Purpose

Support multi-agent coordination without letting shared memory become noisy, overly personal, or unsafe.

## Visibility levels

### shared
Readable by supporting agents such as `coder`, `researcher`, and `deputy`.

Use for memory that helps task execution, coordination, and consistency.

### main-only
Readable only by `main`-facing workflows by default.

Use for memory that is sensitive, highly relational, or not necessary for supporting agents.

## Default rule by type

### Usually shared
- preference
- decision
- pitfall
- project-state
- selected identity-rule

### Usually main-only
- sensitive person notes
- nuanced relational notes
- private collaboration context that does not help execution
- identity notes that are more interpersonal than operational

## Folder-neutral policy

Visibility is controlled at the note level through frontmatter:

```yaml
visibility: shared
```

or

```yaml
visibility: main-only
```

This keeps the vault layout simple and avoids splitting every category into duplicated folder trees.

## Practical guidance

### Mark as shared when
- another agent needs this to do better work
- it reduces repeated mistakes
- it clarifies project direction
- it captures stable execution constraints

### Mark as main-only when
- it contains sensitive interpersonal nuance
- it is not needed for delegated task execution
- sharing would create unnecessary intimacy leakage
- it is a user-facing note rather than an execution-facing note

## Agent read guidance

### coder
May read shared technical and project-relevant memory.

### researcher
May read shared project, preference, and decision memory relevant to research tasks.

### deputy
May read most shared operational memory.

## Write guidance

Supporting agents should not directly create canonical memory by default.
They may propose candidates for `main` to review.
