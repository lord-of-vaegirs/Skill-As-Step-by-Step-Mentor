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
current_part: "part-1"
current_phase: "part_explanation"
created_at: "<ISO 8601>"
updated_at: "<ISO 8601>"
---

# Learning Progress: <topic>

## Sources

- <source or none provided>

## Route overview

- [ ] Part 1 — <title>: <explanation outcome>; <practice outcome>
- [ ] Part 2 — <title>: <explanation outcome>; <practice outcome>

## Part status

| Part | Explanation | Practice | Review | Summary |
|---|---|---|---|---|
| Part 1 | active | locked | locked | locked |
| Part 2 | locked | locked | locked | locked |

## Current part

**ID:** part-1

**Phase:** part_explanation

**Next action:** Read and question the explanation, then send `[finish]` when it is understood.

## Terminology ledger

| Term | Expansion | Plain-language meaning | First part |
|---|---|---|---|
| <term or none yet> | <full form or —> | <short definition> | <part ID> |

## Evidence

- No evidence recorded yet.

## Q&A archive

- No questions or answers recorded yet.

## Part summaries

- No part summarized yet.

## Open questions

- None.

## History

- <timestamp> — Session created.
```

The bundled helper writes a minimal valid form. The mentor may extend sections but must preserve the frontmatter keys and standard headings. Replace route placeholders after inspecting the learner's references. Record each concept-bearing term when it is first explained so vocabulary state survives save and load operations. For an older valid file missing `current_part`, `current_phase`, `## Part status`, `## Q&A archive`, or `## Terminology ledger`, add the missing state on the next mutation without rewriting unrelated history.

## Status vocabulary

- `active`: learning can continue;
- `paused`: state is saved and has a next action;
- `blocked`: an external or prerequisite blocker is recorded;
- `completed`: the final artifact has been assessed against the original goal;
- route markers: pending `[ ]` and summarized `[x]`;
- phases: `intake`, `part_explanation`, `part_practice`, `part_review`, `part_summary_ready`, `final_summary_ready`, and `completed`.

Do not mark a part complete until its error-free practice has been reviewed and `[summarize]` has produced the part summary. Do not use `completed` before `[summarize all]` produces the final synthesis.

## History rules

Append events and do not rewrite unrelated history. Record start, save, restart, goto, phase transition, scope change, blocker, resume, and completion. Include enough context to explain why the current state differs from the original route, without storing secrets or unnecessary personal data.

Restart is the exception for affected learning history: preserve Q&A entries for the reset range, but remove that range's theory-learning records, terminology entries first established there, exercises, submitted results, review evidence, completion markers, part summaries, and history events that assert those states. Append only a minimal restart event naming the target and reset range. Actual learner files are outside restart cleanup and must not be deleted.
