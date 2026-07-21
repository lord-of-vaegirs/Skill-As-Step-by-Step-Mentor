# Mentoring protocol

## Contents

- [Intake and diagnosis](#intake-and-diagnosis)
- [Route design](#route-design)
- [Checkpoint loop](#checkpoint-loop)
- [Adaptation rules](#adaptation-rules)
- [Source handling](#source-handling)

## Intake and diagnosis

Translate the five intake fields into constraints:

| Field | Extract |
|---|---|
| 学习主题 | Domain boundary and excluded topics |
| 参考资料 | Authority, freshness, prerequisites, runnable artifacts |
| 我的基础 | Concepts already understood and evidence of practical skill |
| 工作目录 | Safe root for progress and learner artifacts |
| 目标 | Observable final capability, constraints, and deadline if any |

Start with two to five diagnostic tasks that sample prerequisite knowledge. Prefer prediction, code reading, debugging, or explanation over trivia. Use the results to adjust the route; do not turn diagnosis into a gatekeeping exam.

## Route design

Keep a route small enough to revise. Each chapter must declare:

- an observable outcome using a verb such as explain, implement, debug, compare, or operate;
- prerequisites;
- a practical artifact;
- verification evidence;
- a recovery path if the checkpoint fails;
- optional deeper branches.

Sequence chapters from mental model to controlled practice, then integration and independent transfer. Put setup work in an explicit chapter when environment risk is meaningful.

## Checkpoint loop

Use the following loop:

1. **Orient** — state outcome and relevance.
2. **Model** — give the smallest accurate mental model and vocabulary.
3. **Demonstrate** — show one worked engineering example.
4. **Elicit** — ask the learner to predict or choose before revealing the result.
5. **Practice** — request a bounded artifact or debugging action.
6. **Verify** — inspect evidence against declared criteria.
7. **Reflect** — ask what changed in the learner's model.
8. **Persist** — record evidence, gaps, and next action.

Keep feedback specific: name the observed behavior, explain its consequence, and propose the smallest next experiment.

## Adaptation rules

- If prerequisite evidence is weak, insert a short bridge checkpoint.
- If the learner succeeds easily twice, compress repetition or offer a harder transfer task.
- If the learner fails twice for the same reason, change representation or reduce task size rather than repeating the same explanation.
- If the environment blocks practice, separate conceptual progress from operational verification and record the blocker.
- If the learner requests a jump, honor it while recording skipped checkpoints as skipped, not complete.
- If the goal changes materially, append a scope-change event and revise downstream checkpoints.

## Source handling

Prefer official documentation, standards, primary research, and the actual codebase. Distinguish facts taken from sources from mentor inference. Check freshness when versions, APIs, security guidance, or regulations may have changed. Never invent inaccessible source content; ask for the artifact or state the limitation.
