# QMD Retrieval Rules

## Retrieval priority

### Priority 1
`20_Agent-Memory/`

### Priority 2
`10_Journal/`

### Priority 3
`30_Index/`

## Default retrieval pattern

1. run `qmd query`
2. inspect top 3-5 results
3. open the best 1-2 full notes
4. inspect journal source if needed

## Why progressive disclosure still matters

Vector search finds likely matches, not guaranteed full context.
Reading only snippets can lead to overconfidence and wrong recall.

## Minimal indexing guidance

Keep lightweight metadata only:
- type
- status
- tags
- source_session
- created
- updated
- visibility

Do not build a heavy hand-maintained knowledge graph.

## Conversation rule

When a user asks a recall-style question such as "妳記得……嗎？"
- recall builtin memory
- also search Obsidian/QMD when relevant
- prefer Agent Memory notes first
- use Journal notes only as supporting source context
