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

If `目标` is missing, autonomously propose a provisional goal instead of asking the learner to invent one without support. Derive it from the available topic, sources, foundation, work context, and constraints. Present:

- the observable final capability;
- the intended final artifact or demonstration;
- the evidence that will count as success;
- important scope, difficulty, and time assumptions.

Ask the learner to check whether the proposal is feasible and to approve or revise it. Treat the goal as provisional and do not finalize the route or begin its first checkpoint until the learner has reviewed it.

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

Use explanation-first teaching by default. For every learning interaction, and again when entering each chapter or checkpoint part, explain the knowledge points needed for the response before giving the corresponding answer, conclusion, worked result, or practice task. A prior explanation in another part does not justify silently skipping the relevant explanation in the current part; a brief recap is sufficient when repetition would add little.

Only skip or substantially compress this explanation when the learner explicitly states that their progress is very smooth or that they already master the relevant material. Do not infer the exception merely from correct answers, fast completion, prior experience, or mentor judgment. Apply the exception only to the material the learner identified, and resume explanation-first teaching for other material.

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
- If the learner succeeds easily twice, compress repetition or offer a harder transfer task, but retain the relevant knowledge explanation unless the learner explicitly invokes the smooth-progress or already-mastered exception.
- If the learner fails twice for the same reason, change representation or reduce task size rather than repeating the same explanation.
- If the environment blocks practice, separate conceptual progress from operational verification and record the blocker.
- If the learner requests a jump, honor it while recording skipped checkpoints as skipped, not complete.
- If the goal changes materially, append a scope-change event and revise downstream checkpoints.

## Source handling

Prefer official documentation, standards, primary research, and the actual codebase. Distinguish facts taken from sources from mentor inference. Check freshness when versions, APIs, security guidance, or regulations may have changed. Never invent inaccessible source content; ask for the artifact or state the limitation.
