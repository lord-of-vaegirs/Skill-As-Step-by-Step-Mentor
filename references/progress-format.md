# Progress file format

## Contents

- [File rules](#file-rules)
- [Required document shape](#required-document-shape)
- [Status vocabulary](#status-vocabulary)
- [History rules](#history-rules)

## File rules

- Use UTF-8 Markdown.
- Name files `YYYYMMDD-HHMMSS-<topic-slug>.md` by default.
- Store machine-readable identity in YAML frontmatter and human-readable learning state in sections.
- Keep `session_id` stable for the lifetime of a route.
- Update `updated_at` in ISO 8601 format after each mutation.
- Write atomically and verify the final file exists.

## Required document shape

```markdown
---
schema_version: 1
session_id: "<uuid>"
topic: "<topic>"
goal: "<observable goal>"
foundation: "<learner foundation>"
status: "active"
current_checkpoint: "diagnostic"
created_at: "<ISO 8601>"
updated_at: "<ISO 8601>"
---

# Learning Progress: <topic>

## Sources

- <source or none provided>

## Route

- [ ] Diagnostic — establish prerequisites
- [ ] Chapter 1 — <observable outcome>
- [ ] Integration — <final artifact>

## Current checkpoint

**ID:** diagnostic

**Next action:** <one concrete action>

## Evidence

- No evidence recorded yet.

## Open questions

- None.

## History

- <timestamp> — Session created.
```

The bundled helper writes a minimal valid form. The mentor may extend sections but must preserve the frontmatter keys and standard headings.

## Status vocabulary

- `active`: learning can continue;
- `paused`: state is saved and has a next action;
- `blocked`: an external or prerequisite blocker is recorded;
- `completed`: the final artifact has been assessed against the original goal;
- checkpoint markers: pending `[ ]`, complete `[x]`, and skipped `[-]`.

Do not mark a checkpoint complete without evidence. Do not use `completed` merely because the planned time ended.

## History rules

Append events; do not rewrite history. Record start, save, restart, goto, scope change, blocker, resume, and completion. Include enough context to explain why the current state differs from the original route, without storing secrets or unnecessary personal data.
