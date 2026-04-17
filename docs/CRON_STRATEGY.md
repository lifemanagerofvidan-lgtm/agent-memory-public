# Cron Strategy

## Goal

Document a recommended cron strategy for the Agent Memory project.

## Recommended cron jobs

### 1. Agent Memory Journal Extraction
- schedule: `0 3 * * *`
- timezone: `Asia/Taipei`
- session: `isolated`
- model: `minimax/MiniMax-M2.7`
- delivery: announce to an operator-facing channel

Purpose:
- process Journal notes into canonical Agent Memory notes
- report whether extraction succeeded or failed
- report how many Journal items were processed
- report how many Agent Memory notes were written

### 2. Agent Memory QMD Refresh
- schedule: `30 3 * * *`
- timezone: `Asia/Taipei`
- session: `isolated`
- model: `minimax/MiniMax-M2.7`
- delivery: announce to an operator-facing channel

Purpose:
- refresh QMD after the extraction stage
- run `qmd update`
- run `qmd embed`
- report success or failure

## Execution order

```text
03:00  Journal -> Agent Memory extraction
03:30  QMD refresh
```

This ordering assumes the extraction stage should finish before the retrieval index refresh runs.

## Why this strategy

- keeps the system easy to reason about
- keeps the model cost controlled with MiniMax M2.7
- gives the operator observable health signals during early stabilization
- keeps the two automations separate for easier debugging

## Monitoring mode

Early rollout mode may be intentionally non-silent.

Cron jobs may announce their status until the system has proven stable over time.
Later, delivery can be reduced or disabled.

## Future adjustments

Possible later changes:
- reduce notification verbosity
- make refresh conditional on extraction output
- merge reporting into a cleaner health summary
- move from daily cadence to a different cadence if needed
