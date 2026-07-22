# Learning state machine

This file is the authoritative transition contract. When another instruction conflicts with it, follow this file.

## Invariants

1. Keep exactly one active part and one active phase.
2. Treat the progress file as the authoritative learning state after save, load, goto, or restart.
3. Allow future-part titles and outcomes only in the route overview. Hide all other future-part content until every preceding part is summarized.
4. Do not combine a part's first explanation with its practice.
5. After route initialization, do not infer a transition. Require the exact command or submitted evidence listed for the current state.
6. Do not let `[goto]`, `[restart]`, ordinary language, or evidence bypass a locked phase.

## States and valid transitions

| State | Allowed response | Valid transition |
|---|---|---|
| `intake` | Collect the missing topic, references, work directory, and confirmed final goal. | All required intake confirmed → initialize the route; `[start]` explicitly requests the same validation and initialization. |
| `part_explanation` | Give only the active part's explanation; answer questions and clarify only that part; remind the learner to send `[finish]` when ready. | `[finish]` → `part_practice`. |
| `part_practice` | Give only the active part's exercise and wait for a result. | A submitted result → `part_review`. |
| `part_review` | Review the result, explain errors, and request corrections. Do not reveal later-part content. | Error-free result → `part_summary_ready`. |
| `part_summary_ready` | State that no errors remain; keep optional optimization suggestions brief; answer current-part requests; prompt `[summarize]`. | `[summarize]` → summarize the part, then next `part_explanation` or `final_summary_ready`. |
| `final_summary_ready` | Handle ordinary learning requests, including questions, term explanations, and task help, without producing the all-parts summary; prompt `[summarize all]` when appropriate. | `[summarize all]` → `completed`. |
| `completed` | Give the final synthesis and optional maintenance path. | A new explicitly requested route → `intake`. |

Reject a phase command used in the wrong state. State the current part, current phase, and exact next valid action without leaking locked content.

## Part response rules

### Explanation

- Ground the explanation in the supplied references and the confirmed goal.
- Apply the terminology gate and guided dependency chain from `references/mentoring-protocol.md`.
- End with a clear message that the learner may ask questions now and should send `[finish]` only after understanding the current explanation.
- Do not include exercises, practice previews, hidden-answer prompts, readiness quizzes, or content from later parts.

### Practice and review

- After `[finish]`, issue a bounded exercise for the active part only.
- Review actual submitted evidence. If an error exists, identify it, explain its effect, and request the smallest correction.
- When no error exists but optional improvement is possible, mention it briefly and let the learner choose whether to expand it.
- Prompt `[summarize]` only after no correctness error remains.

### Summary and advancement

- On `[summarize]`, summarize the active part's theory, learner questions, practice result, corrections, and durable takeaway.
- Mark the part complete only after emitting its summary.
- If another part remains, activate it and give only its explanation in the same response; never preview its practice.
- After the last part summary, enter `final_summary_ready` and prompt `[summarize all]` without giving the all-parts synthesis.

## Restart semantics

`[restart]` targets the current part. `[restart <part>]` targets the named current or previously unlocked part. `[restart all]` targets Part 1.

For the target part through the latest unlocked part:

1. preserve a Q&A archive containing the learner's questions and Codex's answers;
2. remove memories of theory learned, terminology established, exercise prompts, submitted results, review evidence, optimization decisions, completion markers, part summaries, and affected history events that assert learning or exercise completion;
3. reset each affected part to pending and reset the target to `part_explanation`;
4. append one minimal restart history event identifying the target and affected range;
5. begin the target part again with explanation only.

Do not delete the learner's source files, code, or other work-directory artifacts. Do not treat preserved chat messages or the Q&A archive as evidence that reset theory or practice is complete. Re-explain reset terminology on first use. Because a Skill cannot erase messages already present in the conversation, ignore their former completion status and use the reset progress file as authority.

## Jump constraints

- Allow `[goto]` only to revisit an already unlocked part or phase.
- Never unlock a future part or skip `[finish]`, practice review, `[summarize]`, or `[summarize all]`.
- If revisiting an earlier location should restart learning, apply the restart semantics instead of marking skipped work complete.
- Refuse `[goto whole tail]` until every part has been summarized; before then, report the current gate.
