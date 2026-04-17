# Migration Plan

## Goal

Define how to move from an earlier, broader memory approach into the simpler Agent Memory system used by this project.

## Strategic change

### Before
- broad knowledge extraction ambitions
- concept / workflow / reference style note planning
- heavier documentation and pipeline surface area

### After
- keep only durable agent memory
- retrieve through QMD
- fetch external knowledge live when needed

## Migration phases

### Phase 1. Define the new system
- create project folder
- write architecture and workflow docs
- define vault structure
- define multi-agent policy

### Phase 2. Build the new vault layout
- create the simplified vault directories
- decide whether to reuse the current AgentMemoryVault vault or create a dedicated vault root

### Phase 3. Repoint capture and retrieval
- ensure session capture lands in the new Journal structure
- ensure QMD indexes the new Agent Memory paths

### Phase 4. Remove broader knowledge-specific flows from the live path
- keep only what is still needed for journal capture, Agent Memory extraction, and QMD refresh
- ensure the live path stays inside this project

### Phase 5. Validate
- save one session
- create one memory note
- refresh QMD
- verify retrieval works in conversation

## Approval-sensitive items

The following should be explicitly confirmed before execution:
- modifying the live vault in place
- changing active hooks
- changing active cron jobs
- changing live OpenClaw config
- archiving or deleting old project content
