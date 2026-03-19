---
name: check-commit-pr-push
description: PR 检查代码、提交、创建 PR 并 push 的工作流。用于用户希望一轮完成完整流程时触发。
metadata:
  short-description: PR 检查代码、提交并创建 PR
---

# 检查-提交-PR-push

当触发本技能时，不进行中途确认，直接按以下顺序一次性完成全部流程：

0. 若仓库远端为 GitLab，或流程中需要使用 `glab` 处理 MR，则先加载并遵循 [`../glab-efficient-workflow/SKILL.md`](../glab-efficient-workflow/SKILL.md) 的规则（命令兼容性检查、非交互参数、MR 描述安全写法、JSON 输出优先）。
1. 先运行测试（使用项目推荐的检查或测试命令；除非用户明确要求只检查某个范围）。
2. 提交所有变更（遵循仓库的提交规范；默认检查全部变更并尽量一次性提交，只有在变更确实难以合并为一次提交时才拆分）。
3. 创建或更新 PR（先检查当前分支是否已有 PR；有则更新该 PR，无则基于变更内容生成一个简洁的分支名并创建新分支，再用该新分支创建 PR）。
4. push（若尚未推送）。
5. 输出 PR 链接、标题与目标分支（链接必须使用 Markdown `[]()` 语法）。
