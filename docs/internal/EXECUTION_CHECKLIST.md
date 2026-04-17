# Execution Checklist

> Maintainer note: this is an internal project tracking file, not part of the beginner setup path.

Use this file to track implementation progress across sessions.

## A. Project skeleton
- [x] Create `projects/agent-memory/`
- [x] Write `README.md`
- [x] Write architecture doc
- [x] Write vault structure doc
- [x] Write workflow doc
- [x] Write multi-agent policy doc
- [x] Write QMD retrieval rules doc
- [x] Write migration plan doc
- [x] Write status tracking files

## B. Vault design
- [x] Decide whether to reuse an existing vault or create a new vault root
- [x] Create simplified vault folder structure
- [x] Define note template for canonical Agent Memory notes
- [x] Define visibility policy for `shared` vs `main-only`

## C. Capture path
- [x] Confirm whether existing `/save10` flow will be reused
- [x] Confirm final Journal output path
- [x] Confirm whether old journal hooks remain active or are replaced

## D. Memory write path
- [x] Define the minimal extraction rule set
- [x] Define canonical note naming rules
- [x] Decide whether memory creation is manual, assisted, or automated
- [x] Decide where candidate memory notes should live, if any

## E. QMD integration
- [x] Update QMD collections to point at simplified Agent Memory paths
- [x] Set weight priority for `20_Agent-Memory/`
- [x] Set lower weight for `10_Journal/`
- [x] Verify `qmd query` works on the new structure
- [x] Verify vector retrieval quality with 2-3 real examples

## F. Multi-agent policy rollout
- [ ] Confirm `main` as canonical writer
- [ ] Confirm read scope for `coder`
- [ ] Confirm read scope for `researcher`
- [ ] Confirm read scope for `deputy`
- [ ] Confirm whether any `main-only` memory exists now

## G. Live environment transition
- [x] Disable old knowledge-extraction cron jobs
- [x] Change live hooks/config where needed for the new Agent Memory path
- [x] Move live save flow into the Agent Memory project
- [x] Repoint QMD active config to the simplified Agent Memory scope

## H. Validation
- [x] Save one real session into Journal
- [x] Create one real Agent Memory note
- [x] Refresh QMD successfully
- [x] Retrieve that memory successfully in chat
- [x] Validate retrieval for `project-state`
- [x] Validate retrieval for `preference`
- [x] Validate retrieval for `pitfall`
- [x] Validate retrieval for `decision`
- [x] Validate retrieval for `identity-rule`
- [ ] Test the phrase "妳記得……嗎？" against the new workflow

## I. Release readiness
- [x] Clean the project docs
- [x] Reduce stale files and document remaining runtime state files
- [x] Write setup instructions for another machine
- [x] Write publication-oriented README pass
- [x] Add cron strategy documentation
