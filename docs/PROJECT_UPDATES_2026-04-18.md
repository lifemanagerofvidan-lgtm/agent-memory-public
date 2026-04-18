# Project Updates, 2026-04-18

## Updated

- The Journal-to-Memory extraction path was refined to use the validated OpenClaw Gateway request contract.
- The extraction call pattern now uses:
  - `POST /v1/responses`
  - `model: "openclaw"`
  - header `x-openclaw-agent-id: main`
  - header `x-openclaw-model: minimax/MiniMax-M2.7`
  - one plain-string `input`
- More complex item-array request shapes were removed from the live extraction path because they triggered agent-style side effects instead of reliable JSON extraction.
- The extraction prompt now requires whole-session judgment before writing memory.
- The prompt now rejects provisional mid-conversation conclusions and keeps only final settled conclusions.
- The prompt no longer uses a hard maximum candidate count.
- The prompt now requires candidate notes to be distinct and non-overlapping within the same session.
- Cron guidance was updated to recommend verbatim stdout output for low-ambiguity automation scripts.

## Validated

- The corrected extraction request shape returned parseable JSON again.
- Journal Extraction completed successfully on a fresh saved Journal entry and wrote canonical memory notes.
- Journal Extraction and QMD Refresh both delivered successfully to the operator-facing Discord channel after delivery-target correction in the live environment.
- Verbatim stdout delivery removed misleading model-added interpretation from cron output.

## Current direction

- Keep extraction conservative and memory-oriented rather than summary-oriented.
- Prefer durable session conclusions over mid-discussion proposals.
- Keep cron delivery literal and low-interpretation.
- Continue stabilizing the live system before any broader publication cleanup.
