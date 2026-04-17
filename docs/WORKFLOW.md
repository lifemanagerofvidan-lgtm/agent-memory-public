# Workflow

## Intended workflow

### Step 1. Capture the session
Save the conversation into `10_Journal/`.

### Step 2. Decide whether durable memory exists
Only create memory if the session contains durable collaboration signal.

### Step 3. Classify the memory
Allowed types:
- preference
- decision
- pitfall
- person
- project-state
- identity-rule

### Step 4. Write canonical memory note
Write the note into the correct folder under `20_Agent-Memory/`.

### Step 5. Refresh QMD index
Run QMD update/embed only when the vault changed.

### Step 6. Retrieve later
During future conversations:
1. search memory notes first
2. open top matches
3. inspect journal only if needed

## Do not store
- generic knowledge summaries
- web article notes
- broad technical reference notes
- temporary brainstorming residue
- one-off emotional remarks

## Write threshold
Create memory only when it will likely help future collaboration, future task execution, or future error avoidance.
