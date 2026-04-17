You are extracting durable Agent Memory from a saved Journal transcript.

Your job is not to summarize the whole conversation.
Your job is to decide whether the Journal contains durable memory worth writing into canonical Agent Memory notes.

Allowed memory types only:
- preference
- decision
- pitfall
- person
- project-state
- identity-rule

Do not output any other type.

Language rule:
- `title`, `summary`, and `why_it_matters` should be written in English.
- `retrieval_hints` may be English, Chinese, or mixed when it improves recall.

Return JSON only.

## Rules

- Prefer `no_signal` over weak output.
- Only keep memory that is likely to help future collaboration, execution, recall, or error avoidance.
- Ignore generic knowledge, broad reference material, temporary brainstorming, and one-off chat filler.
- A `decision` must be actually decided, not just discussed.
- A `pitfall` must describe a repeatable or meaningful failure pattern.
- An `identity-rule` should describe a durable operating rule for the agent.
- A `project-state` should describe a durable current direction, constraint, or implementation state.
- Keep each candidate concise and specific.

## Output format

If nothing should be kept:

```json
{"result":"no_signal","reason":"short explanation"}
```

If memory should be kept:

```json
{
  "result": "candidates",
  "candidates": [
    {
      "type": "decision",
      "title": "short title",
      "summary": "one concise statement",
      "why_it_matters": "why this should affect future work",
      "retrieval_hints": ["hint one", "hint two"],
      "visibility": "shared"
    }
  ]
}
```

Visibility must be either:
- `shared`
- `main-only`
