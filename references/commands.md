# Portable command contract

## Contents

- [General rules](#general-rules)
- [`[help]`](#help)
- [`[command]`](#command)
- [Session commands](#session-commands)
- [Resolution and safety](#resolution-and-safety)

## General rules

- Recognize commands case-insensitively after trimming surrounding whitespace.
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
我的基础：
工作目录：
目标：
```

Then explain:

- 学习主题：希望系统学习的技术方向。
- 参考资料：官方文档、书籍、课程、论文、代码仓库等。
- 我的基础：当前知识水平和实践经验。
- 工作目录：用于保存学习进度 Markdown 文件。
- 目标：希望最终能够解释、实现、调试或交付的结果。

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

[restart ...]
从指定学习章节重新开始。

[restart all]
从学习路线最开始重新学习，但保留历史记录。

[goto ...]
跳转到指定学习位置。

[goto whole head]
前往整个学习路线开始。

[goto whole tail]
前往最终总结阶段。

[goto part head]
重新学习当前章节。

[goto part tail]
总结当前章节。

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
| `[start]` | Validate intake, create the route and a new progress file, then begin the first checkpoint. |
| `[restart <chapter>]` | Append a history event, reset that chapter's checkpoint state, and retain earlier evidence. |
| `[restart all]` | Append a history event and return to the first route checkpoint without erasing history. |
| `[goto <target>]` | Resolve a unique chapter/checkpoint by number or title; ask for clarification if multiple targets match. |
| `[goto whole head]` | Move to the first checkpoint in the route. |
| `[goto whole tail]` | Move to final integration and summary. Do not mark skipped checkpoints complete. |
| `[goto part head]` | Move to the first checkpoint of the current chapter. |
| `[goto part tail]` | Move to the current chapter's summary and assessment. |
| `[save]` | Persist the current state atomically to the active file. |
| `[save <path>]` | Save a copy under the explicit path after validating it. The literal `[save path]` asks the user for a path. |
| `[save exit]` / `[exit]` | Save, report the exact next action and file path, then stop mentoring for this turn. |
| `[del]` | Show the active progress file and ask for explicit deletion confirmation. |
| `[del exit]` | Confirm, delete only the active progress file, then stop. |
| `[list]` | List progress Markdown files in the active work directory. |
| `[list <path>]` | List progress Markdown files under the specified directory. The literal `[list path]` asks for a path. |
| `[load <filename>]` | Load one validated progress file and summarize its next action. |
| `[load all]` | Discover all progress files but do not merge incompatible routes silently. Summarize each and ask which to activate. |

## Resolution and safety

- Resolve relative paths against the active work directory, not the process home directory.
- Prevent path traversal outside the explicit root unless the user clearly supplies and authorizes another root.
- Write via a temporary sibling file and atomic replacement.
- Preserve prior evidence and history across restart and goto operations.
- Ask for confirmation immediately before delete; a previous broad request is not confirmation.
- If save fails, keep the in-memory state and report the error. Never claim success without verifying the file.
