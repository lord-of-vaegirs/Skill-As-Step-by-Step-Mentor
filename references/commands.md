# Portable command contract

## Contents

- [General rules](#general-rules)
- [`[help]`](#help)
- [`[command]`](#command)
- [Session commands](#session-commands)
- [Resolution and safety](#resolution-and-safety)

## General rules

- Recognize commands case-insensitively after trimming surrounding whitespace.
- Match the longest complete command first so `[summarize all]` is never handled as `[summarize]`.
- Require the whole user message to be a command, unless the user explicitly says that an inline token is an instruction.
- Treat general usage questions as `[help]`.
- Treat questions about command names or syntax as `[command]`.
- For an invalid or ambiguous argument, show the closest valid syntax and do not mutate state.
- Report the resulting file path after every state-changing command.

## `[help]`

Return this first-level guide, preserving the field names:

```text
Skill As Step by Step Mentor 使用方法

请提供：

学习主题：
参考资料：
工作目录：
目标：
我的基础（可选）：
```

Then explain:

- 学习主题：希望系统学习的技术方向。
- 参考资料：官方文档、书籍、课程、论文、代码仓库等。
- 工作目录：用于保存学习进度 Markdown 文件。
- 目标：希望最终能够解释、实现、调试或交付的结果；如果未提供，Codex 会提出包含成功证据和范围假设的暂定目标，交由你检查、确认或修改。
- 我的基础（可选）：当前知识水平和实践经验；未提供时从保守起点开始，并根据后续问答和练习调整。

End with:

```text
如果需要查看特殊指令的详细使用方式，请输入：

[command]
```

## `[command]`

Return the complete command list:

```text
[start]
开始新的学习任务。

[finish]
标识当前学习部分的讲解已经理解，并解锁当前部分的练习。

[summarize]
总结已经无错误的当前学习部分，然后进入下一部分。

[summarize all]
在所有学习部分均已总结后，生成最终总总结。

[restart]
保留当前部分的问答记录，清除其学习与练习状态，并从讲解重新开始。

[restart ...]
保留回退范围内的问答记录，清除该范围的学习与练习状态，并从指定部分重新开始。

[restart all]
保留全部问答记录，清除全部学习与练习状态，并从第一部分讲解重新开始。

[goto ...]
前往已经解锁的位置，不允许越过当前阶段或进入未解锁部分。

[goto whole head]
前往整个学习路线开始。

[goto whole tail]
仅在所有部分均已总结后前往最终总结阶段。

[goto part head]
回到当前部分已经解锁的最早位置；需要重新学习时按 `[restart]` 规则处理。

[goto part tail]
前往当前部分已经解锁的最晚阶段，不会绕过 `[finish]`、练习审查或 `[summarize]`。

[save]
保存当前学习进展。

[save path]
保存学习进展到指定路径。

[save exit]
保存进度并退出。

[exit]
保存进度并退出。

[del]
删除当前学习进展。

[del exit]
删除当前学习进展并退出。

[list]
列出已有学习进展文件。

[list path]
查询指定位置的学习进展文件。

[load filename]
加载指定学习进展。

[load all]
加载所有可用学习进展。
```

## Session commands

| Command | Required behavior |
|---|---|
| `[start]` | Validate the required intake, inspect references, create the part route and progress file, show only the route overview, then give Part 1's explanation without practice. |
| `[finish]` | Valid only in `part_explanation`; record that the explanation phase ended and return the active part's practice. Never interpret it as practice completion. |
| `[summarize]` | Valid only in `part_summary_ready`; summarize and complete the active part, then start only the next part's explanation. After the last part, enter `final_summary_ready`. |
| `[summarize all]` | Valid only in `final_summary_ready`; synthesize all summarized parts and mark the route completed. |
| `[restart]` | Apply restart semantics to the current part and return to its explanation. |
| `[restart <part>]` | Resolve a unique current or previously unlocked part, preserve Q&A for the affected range, clear its learning and exercise state, reset the target and later unlocked parts, and return to the target explanation. Reject locked future parts. |
| `[restart all]` | Preserve Q&A, clear learning and exercise state for every part, retain the route and restart Part 1's explanation. |
| `[goto <target>]` | Resolve a unique already unlocked part or phase. Refuse locked future content and any transition that would bypass the current gate. |
| `[goto whole head]` | Revisit the beginning only by applying `[restart all]` semantics; do not silently retain completion evidence. |
| `[goto whole tail]` | Enter final summary only when every part has been summarized; otherwise refuse and report the current gate. |
| `[goto part head]` | Revisit the active part's beginning by applying `[restart]` semantics when that would cross completed phase state. |
| `[goto part tail]` | Move only to the latest phase already unlocked in the active part; never create a phase transition or summary. |
| `[save]` | Persist the current state atomically to the active file. |
| `[save <path>]` | Save a copy under the explicit path after validating it. The literal `[save path]` asks the user for a path. |
| `[save exit]` / `[exit]` | Save, report the exact next action and file path, then stop mentoring for this turn. |
| `[del]` | Show the active progress file and ask for explicit deletion confirmation. |
| `[del exit]` | Confirm, delete only the active progress file, then stop. |
| `[list]` | List progress Markdown files in the active work directory. |
| `[list <path>]` | List progress Markdown files under the specified directory. The literal `[list path]` asks for a path. |
| `[load <filename>]` | Load one validated progress file, restore its authoritative active part and phase, and report the exact next valid action without leaking locked content. |
| `[load all]` | Discover all progress files but do not merge incompatible routes silently. Summarize each and ask which to activate. |

## Resolution and safety

- Resolve relative paths against the active work directory, not the process home directory.
- Prevent path traversal outside the explicit root unless the user clearly supplies and authorizes another root.
- Write via a temporary sibling file and atomic replacement.
- Preserve evidence and history when using goto. Apply the narrower Q&A-only preservation rule when restarting.
- For restart, preserve Q&A archives but clear theory, terminology, exercises, review evidence, completion markers, and summaries in the reset range. Do not delete learner artifacts.
- Never use save, load, restart, or goto to unlock a phase or future part.
- Ask for confirmation immediately before delete; a previous broad request is not confirmation.
- If save fails, keep the in-memory state and report the error. Never claim success without verifying the file.
