# Skill As Step by Step Mentor

<p align="right">
  <a href="./README.md">English</a> | <strong>简体中文</strong>
</p>

这是一个 Codex Skill，同时也是 DeepSeek Harness 插件，用于开展有资料依据、强调动手实践的工程技术学习。它能够把宽泛的学习目标转化为可调整的学习路线，逐个检查点验证实践证据，并使用可恢复的 Markdown 文件保存学习进度。

学习者确认学习主题、参考资料、工作目录和最终目标后，Agent 会推导有序学习路线，并严格一次只推进一个部分。每部分固定遵循“仅讲解 → `[finish]` → 练习与审查 → `[summarize]`”；前一部分尚未总结时，不会出现后一部分的学习内容。最后一部分总结后，只有 `[summarize all]` 才会生成最终总总结。首次出现的专业名词会先得到解释，讲解会依据资料从背景和前置知识逐步展开，进度文件会记录当前阶段。`[restart]` 保留问答记录，但清除回退范围内的理论学习、练习、证据和完成状态，以便重新学习。

## 为什么我要创建这样一个skill
当今时代学习各种领域的知识，尤其是计算机科学相关的知识，会面临资源很多，但是学不进去的问题。我想了很久，发现问题的根源就在于无法沉浸式学习。手头空有资源，但是不知道从何处入手，也不知道该如何组织自己的学习计划，学完之后很快就会忘记学过的内容。为了解决这些长久以来的问题，我决定借助AI的力量，让AI帮助我们完成规划和安排练习的部分，充当我们24h随叫随到言听计从的私人导师，解决我们每个人自己的问题，应对我们每个人自己的想法，并给出对应的练习和例题让我们可以从新应手的掌握对应的知识。为了方便使用，我还添加了一些便携的特殊指令，你只需在对话框敲入`[command]`，你就可以了解他们的用法的。希望这个skill能帮助你更牢固和有参与感的完成你的学习之旅！

## 项目内容

- `SKILL.md` —— 精简的 Agent 工作流程和请求路由说明
- `agents/openai.yaml` —— Codex 界面元数据和默认提示词
- `references/` —— 可移植命令契约、指导协议、状态格式、质量评估标准和宿主集成说明
- `scripts/mentor_state.py` —— 无第三方依赖、具有安全路径限制的进度文件命令行工具
- `package.json`、`cordis.patch.yml`、`lib/index.js` —— DeepSeek Harness bundle，把同一套 Skill 作为受管插件提供
- `locale/`、`icon.svg` —— bundle 的展示元数据
- `tests/` —— 行为、契约、宿主兼容性与 provider 回归测试
- `.github/` —— Pull Request 模板、Issue 表单和 CI 配置

## 安装

### Codex

将本仓库克隆到 Codex Skills 目录：

```bash
git clone <repository-url> "${CODEX_HOME:-$HOME/.codex}/skills/skill-as-step-by-step-mentor"
```

重新启动或重新加载 Codex，然后调用：

```text
$skill-as-step-by-step-mentor
```

### DeepSeek Harness：本地 Skill 根目录

DeepSeek Harness 会从其文件系统 Skill 根目录发现本地 Skill，因此无需构建插件。把仓库链接到用户级根目录即可：

```bash
mkdir -p "${DSH_HOME:-$HOME/.dsh}/skills"
ln -s "$PWD" "${DSH_HOME:-$HOME/.dsh}/skills/skill-as-step-by-step-mentor"
```

在输入框中输入 `/skill-as-step-by-step-mentor` 调用，或者让 Agent 在请求匹配描述时自行加载。发现过程带有监听，Skill 无需重启 Harness 即可进入下一次目录。若只想在某个仓库内使用，可把 bundle 放到 `<repository>/.dsh/skills/` 下。修改 Skill 时优先使用这种方式，因为改动会立即生效。

### DeepSeek Harness：受管插件

仓库根目录同时是一个名为 `dsh-skill-step-by-step-mentor` 的 DeepSeek Harness bundle 包。如果希望按 profile 启用、停用、更新或删除该 Skill，而不是让它直接放在磁盘上，请通过 Harness 插件管理器安装：

| 项目 | 值 |
|---|---|
| Bundle 包名 | `dsh-skill-step-by-step-mentor` |
| 插件行 id | `skill-step-mentor` |
| 安装目标 | `https://github.com/lord-of-vaegirs/Skill-As-Step-by-Step-Mentor` 或本地仓库的绝对路径 |
| 调用方式 | `/skill-as-step-by-step-mentor` |

插件管理器会执行 pnpm、把包记录到 profile、选中该 bundle，并应用 `cordis.patch.yml` 插入的 Skill provider 行。provider 在每次请求目录时重新读取已安装包中的 `SKILL.md`，因此重新安装即可替换指令内容。

请只选择一种方式：本地 Skill 根目录与已安装 bundle 会声明同一个 Skill 名称，其中本地根目录按优先级胜出。

进行本地开发时，也可以把仓库保存在任意位置，再通过符号链接将其连接到任一 Skills 目录。

扫描根目录、frontmatter 约束、bundle 结构与安装检查清单见 [references/harness-integration.md](references/harness-integration.md)。

## 验证

运行仓库测试：

```bash
python3 -m unittest discover -s tests -v
node --test tests/provider.test.mjs
```

`npm pack --dry-run` 会列出安装后 bundle 实际包含的文件，预期只有 Skill bundle、`lib/index.js`、`cordis.patch.yml` 与展示元数据。

如果已经安装 Codex 的 `skill-creator` 工具，还应运行：

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py .
```

## 参与贡献

请先创建一个 Issue，说明具体的学习场景，然后在修改行为时增加或更新相应的回归测试。保持 `SKILL.md` 精简，并将详细协议放在 `references/` 中。详情请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

本项目采用 MIT License，详情请参阅 [LICENSE](LICENSE)。
