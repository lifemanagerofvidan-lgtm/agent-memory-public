# Project Updates

> Maintainer note: this file records project evolution and validation history. New users do not need it for setup.

## 2026-04-17

### Added
- project skeleton for Agent Memory
- simplified live vault structure
- canonical note template
- visibility policy
- memory write workflow v1
- publishing rules
- local `save_to_raw.py` under `projects/agent-memory-public/scripts/`

### Updated
- `/save10` now points to the Agent Memory script path
- Journal output format was refined for cleaner transcript capture
- speaker boundaries now use `=== 老闆 ===` and `=== main ===`
- markdown heading noise in saved transcript content was reduced
- QMD config now prioritizes `20_Agent-Memory/` over `10_Journal/`
- the default extraction model was set to `minimax/MiniMax-M2.7`
- canonical note language policy now requires English main body fields with multilingual retrieval hints allowed
- a new OpenClaw cron wrapper script was added for Journal-to-Memory extraction reporting
- a QMD refresh automation script and cron path were added
- a cron strategy document was added to describe the live schedule and delivery mode
- progress tracking files were updated to reflect the live vault reset and workflow decisions

### Validated
- live vault was reset into the simplified Agent Memory structure
- old QMD-related cron jobs were disabled
- the active journal save path now runs from `projects/agent-memory/`
- `/save10` successfully writes into the live Journal path
- saved Journal output now uses the new speaker boundary format
- QMD retrieval was validated for `project-state`, `preference`, `pitfall`, `decision`, and `identity-rule`
- QMD active collections were reduced to the simplified Agent Memory scope only

### Current direction
- keep the project self-contained
- keep the project publishable
- keep live operational logic inside `projects/agent-memory/`
- keep documentation focused on the current system only
