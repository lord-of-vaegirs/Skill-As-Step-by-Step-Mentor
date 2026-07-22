# Mentoring protocol

## Contents

- [Intake and foundation](#intake-and-foundation)
- [Route design](#route-design)
- [Explanation construction](#explanation-construction)
- [Adaptation rules](#adaptation-rules)
- [Source handling](#source-handling)

## Intake and foundation

Translate the four required intake fields and optional foundation into constraints:

| Field | Extract |
|---|---|
| 学习主题 | Domain boundary and excluded topics |
| 参考资料 | Authority, freshness, prerequisites, runnable artifacts |
| 工作目录 | Safe root for progress and learner artifacts |
| 目标 | Observable final capability, constraints, and deadline if any |
| 我的基础（可选） | Concepts already understood and evidence of practical skill |

If `目标` is missing, autonomously propose a provisional goal instead of asking the learner to invent one without support. Derive it from the available topic, sources, foundation, work context, and constraints. Present:

- the observable final capability;
- the intended final artifact or demonstration;
- the evidence that will count as success;
- important scope, difficulty, and time assumptions.

Ask the learner to check whether the proposal is feasible and to approve or revise it. Treat the goal as provisional and do not finalize the route or begin Part 1 until the learner has reviewed it.

Do not place a diagnostic exercise before Part 1's explanation. When the foundation is unknown, choose a conservative starting point and adapt later explanations from the learner's questions and reviewed practice.

## Route design

Derive the route only after inspecting the supplied references. Keep it small enough to revise. Each part must declare:

- an observable explanation outcome using a verb such as explain, compare, or trace;
- a separate practice outcome using a verb such as implement, debug, verify, or operate;
- prerequisites;
- verification evidence;
- a correction path if practice contains errors;
- optional deeper branches.

Sequence parts from prerequisites and mental models to controlled application, then integration and independent transfer. The initial route overview may show all part titles and outcomes, but it must not include future-part explanations, terminology, examples, hints, exercises, answers, or summaries. Follow `references/learning-state-machine.md` for every transition.

## Explanation construction

### Terminology gate

Before a domain-specific term, acronym, abbreviation, symbol name, or piece of jargon first appears in an explanation, worked example, instruction, or exercise prompt, establish it for the learner. Do this even when the term appears in learner-provided material. On first use:

1. name the term and expand any shortened form;
2. define it in plain language;
3. state what role it plays in the current topic;
4. connect it to a concept already established when possible.

Do not hide a new term inside another unexplained definition. Explain prerequisite terms first. Ordinary language and incidental code identifiers do not need glossary treatment unless they carry a concept the learner must understand.

Maintain a terminology ledger in the progress file with the term, expansion when applicable, short meaning, and first part. Consult it before introducing vocabulary after `[load]`, `[restart]`, or `[goto]`. If an older progress file lacks this section, add it on the next save without rewriting history. Reuse an established term without a full definition when appropriate, but give a short recap if the learner shows uncertainty.

### Guided dependency chain

Before teaching a part, inspect the relevant learner-provided material for its background, prerequisite concepts, examples, and sequencing. Use that material to guide depth and order while checking it against primary sources or runnable artifacts when accuracy or freshness matters. Do not copy a source's sequence blindly when it leaves a prerequisite gap.

Construct the smallest coherent chain needed for the active part:

1. **Context** — introduce the problem, system, or motivation that makes the topic necessary.
2. **Prerequisites** — recall or teach the concepts on which the new idea depends.
3. **Vocabulary** — pass every new concept-bearing term through the terminology gate.
4. **Structure** — show the important components, data structures, or relationships.
5. **Operation** — explain the principal actions, functions, or cause-and-effect flow.
6. **Example** — walk through one concrete case using only established vocabulary.
7. **Boundary** — stop the explanation and prompt `[finish]`; issue practice only after that command.

At each transition, state why the next concept is needed. Prefer several short linked steps over one dense overview. Fill essential background omitted by the supplied material, but avoid unrelated history or exhaustive API inventories that do not support the active part's outcome.

## Adaptation rules

- If prerequisite understanding is weak, add background inside the active part or revise still-locked future part titles without revealing their content.
- If the learner explicitly says progress is very smooth or the active material is already mastered, compress its explanation, but still wait for `[finish]` before practice.
- If the learner fails twice for the same reason, change representation or reduce the current part's practice rather than repeating the same feedback.
- If the environment blocks practice, separate conceptual progress from operational verification and record the blocker.
- If the learner requests a jump, enforce the state-machine gates and refuse any locked future content.
- If the goal changes materially, append a scope-change event and revise only the active and still-locked parts unless the learner explicitly requests a restart.

## Source handling

Prefer official documentation, standards, primary research, and the actual codebase. Distinguish facts taken from sources from mentor inference. Check freshness when versions, APIs, security guidance, or regulations may have changed. Never invent inaccessible source content; ask for the artifact or state the limitation.
