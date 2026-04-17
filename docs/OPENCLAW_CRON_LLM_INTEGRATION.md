# OpenClaw Cron LLM Integration

## Goal

Document how the Agent Memory project should call an LLM during cron-driven Journal to Memory extraction.

## Design choice

Use OpenClaw's own `/v1/responses` HTTP endpoint from inside the Agent Memory extractor.

This keeps the project self-contained while still using the OpenClaw runtime's model routing and auth.

## Why this approach

- no dependency on old project scripts
- stays compatible with OpenClaw runtime auth
- keeps model invocation inside the same system boundary
- works in both manual runs and the current live cron path

## Default model policy

Default extraction model for this project:

```text
minimax/MiniMax-M2.7
```

This keeps the memory automation path cheaper and preserves stronger models for interactive project discussion.

## Required pieces

- OpenClaw gateway running
- `gateway.http.endpoints.responses.enabled` enabled in `<openclaw-config-path>`
- valid gateway auth token in `<openclaw-config-path>`
- extractor script that POSTs to `/v1/responses`

## v1 extractor behavior

`journal_to_memory.py`:
- loads the prompt from `prompts/journal_to_memory_v1.md`
- reads one Journal file
- sends prompt + Journal text to `/v1/responses`
- validates the returned JSON
- writes canonical notes into `20_Agent-Memory/`
- records extraction state

## Example cron shape

A practical cron path is:

```text
03:00 cron
  -> python3 projects/agent-memory/scripts/journal_to_memory_cron.py
  -> runs Journal-to-Memory extraction
  -> writes 20_Agent-Memory notes when signal exists
  -> announces a status summary to an operator-facing channel

03:30 cron
  -> python3 projects/agent-memory/scripts/qmd_refresh.py
  -> runs qmd update
  -> runs qmd embed
  -> announces a status summary to an operator-facing channel
```

## Important note

Cron wiring should remain simple. During early rollout, delivery may stay non-silent so an operator can observe system health.
