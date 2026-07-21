# Skill As Step by Step Mentor

<p align="right">
  <a href="./README.md">English</a> | <strong>简体中文</strong>
</p>

这是一个面向 Codex 的 Skill Agent 项目，用于开展有资料依据、强调动手实践的工程技术学习。它能够把宽泛的学习目标转化为可调整的学习路线，逐个检查点验证实践证据，并使用可恢复的 Markdown 文件保存学习进度。

## 为什么我要创建这样一个skill
当今时代学习各种领域的知识，尤其是计算机科学相关的知识，会面临资源很多，但是学不进去的问题。我想了很久，发现问题的根源就在于无法沉浸式学习。手头空有资源，但是不知道从何处入手，也不知道该如何组织自己的学习计划，学完之后很快就会忘记学过的内容。为了解决这些长久以来的问题，我决定借助AI的力量，让AI帮助我们完成规划和安排练习的部分，充当我们24h随叫随到言听计从的私人导师，解决我们每个人自己的问题，应对我们每个人自己的想法，并给出对应的练习和例题让我们可以从新应手的掌握对应的知识。为了方便使用，我还添加了一些便携的特殊指令，你只需在对话框敲入`[command]`，你就可以了解他们的用法的。希望这个skill能帮助你更牢固和有参与感的完成你的学习之旅！

## 项目内容

- `SKILL.md` —— 精简的 Agent 工作流程和请求路由说明
- `agents/openai.yaml` —— Codex 界面元数据和默认提示词
- `references/` —— 可移植命令契约、指导协议、状态格式和质量评估标准
- `scripts/mentor_state.py` —— 无第三方依赖、具有安全路径限制的进度文件命令行工具
- `tests/` —— 行为与契约回归测试
- `.github/` —— Pull Request 模板、Issue 表单和 CI 配置

## 安装

将本仓库克隆到 Codex Skills 目录：

```bash
git clone <repository-url> "${CODEX_HOME:-$HOME/.codex}/skills/skill-as-step-by-step-mentor"
```

重新启动或重新加载 Codex，然后调用：

```text
$skill-as-step-by-step-mentor
```

进行本地开发时，也可以把仓库保存在任意位置，再通过符号链接将其连接到 Skills 目录。

## 验证

运行仓库测试：

```bash
python3 -m unittest discover -s tests -v
```

如果已经安装 Codex 的 `skill-creator` 工具，还应运行：

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py .
```

## 参与贡献

请先创建一个 Issue，说明具体的学习场景，然后在修改行为时增加或更新相应的回归测试。保持 `SKILL.md` 精简，并将详细协议放在 `references/` 中。详情请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

本项目采用 MIT License，详情请参阅 [LICENSE](LICENSE)。
