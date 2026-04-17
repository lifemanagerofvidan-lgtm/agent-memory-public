# Publishing Rules

> Maintainer note: this file is about repo hygiene and publication boundaries, not first-time operator setup.

## Project intent

`projects/agent-memory-public/` should be a self-contained, publishable project.

## Hard rules

1. Do not rely on runtime code that lives only in old project folders.
2. If a script is still needed, copy or rewrite it inside `projects/agent-memory-public/`.
3. Old projects may be used only as temporary reference during migration.
4. After migration, old project code should be archived and should not remain a live dependency.
5. The publishable project should explain its own architecture, workflow, scripts, and paths without requiring hidden context.

## Practical meaning

### Allowed
- reading old project files during migration
- selectively copying code that still fits the new design
- rewriting old scripts into simpler Agent Memory versions

### Not allowed for final state
- active hooks pointing to old project scripts
- active skills that execute old project scripts
- project docs that say "see the old project"
- hidden operational dependence on `obsidian-qmd-knowledge-brain`

## End-state goal

By the end of this project:
- `projects/agent-memory-public/` should contain the live docs it needs
- `projects/agent-memory-public/` should contain the live scripts it needs
- old knowledge-brain systems should be archival, not operational
