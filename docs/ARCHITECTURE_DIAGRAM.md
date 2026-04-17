# Architecture Diagram

## High-level flow

```text
OpenClaw conversation
        |
        v
/save10 or scripts/save_to_raw.py
        |
        v
10_Journal/
(raw conversation history)
        |
        | optional extraction
        v
scripts/journal_to_memory.py
        |
        v
20_Agent-Memory/
(canonical durable memory notes)
        |
        v
scripts/qmd_refresh.py
        |
        v
qmd update + qmd embed
        |
        v
qmd query
        |
        v
future recall during later conversations
```

## Storage and retrieval layers

```text
                +----------------------+
                |   Obsidian Vault     |
                |----------------------|
                | 00_Inbox/            |
                | 10_Journal/          |
                | 20_Agent-Memory/     |
                | 30_Index/            |
                | 90_Archive/          |
                +----------+-----------+
                           |
                           | indexed by
                           v
                +----------------------+
                |         QMD          |
                |----------------------|
                | update               |
                | embed                |
                | query                |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |  Retrieval Results   |
                |----------------------|
                | canonical notes      |
                | then Journal context |
                +----------------------+
```

## Retrieval priority

```text
Priority 1: 20_Agent-Memory/
Priority 2: 10_Journal/
Priority 3: 30_Index/
```

## Mental model

Think of the system like this:
- Journal is the raw log
- Agent Memory is the distilled memory
- QMD is the retrieval engine

If you are a beginner, this is the simplest successful path:
1. create vault folders
2. write one canonical note
3. run `qmd update`
4. run `qmd embed`
5. test `qmd query`
