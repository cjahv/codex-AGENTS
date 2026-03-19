---
name: reword-unpushed-commits-pr
description: PR 检查当前分支未推送提交、结合每个提交 diff 重写提交信息，并在确认后批量更新历史再创建或更新 PR/MR。用于用户要走完整提交流程时触发。
metadata:
  short-description: PR 重写未推送提交并创建 PR/MR
---

# 重写未推送提交并创建 PR/MR

## 适用场景

当用户希望针对**当前分支**执行以下完整流程时使用本技能：

- 检查当前分支尚未推送的提交
- 结合每个提交的 diff 重新整理提交文案
- 在用户确认全部新文案后批量重写 commit message
- 然后基于当前分支创建或更新 PR/MR

## 工作流程

0. 若仓库远端为 GitLab，或流程中需要使用 `glab` 处理 MR，则先加载并遵循 [`../glab-efficient-workflow/SKILL.md`](../glab-efficient-workflow/SKILL.md) 的规则。

1. 先检查工作区是否干净：

```bash
git status --porcelain
```

- 只要存在未提交或未暂存改动，立即拒绝执行后续任何操作。
- 明确告知用户“当前分支不干净，先清理工作区后再继续”。

2. 识别当前分支未推送提交：

- 若当前分支已设置 upstream，使用：

```bash
git rev-list --reverse @{upstream}..HEAD
```

- 若未设置 upstream，则先确定 PR/MR 目标基线（优先远端默认分支），再用 `merge-base` 计算当前分支相对基线的提交范围。
- 若无法可靠确定比较基线，停止并要求用户先明确基线或设置 upstream。
- 若没有未推送提交，直接说明“当前分支没有未推送提交”，停止。

3. 对每个未推送提交逐个读取差异并整理新文案：

```bash
git show --stat --patch --format=fuller <commit>
```

- 基于每个提交自身 diff 单独整理提交文案，不要把多个提交混成一次总结。
- 新文案必须遵循仓库提交规范；默认使用中文。
- 需要保留每个提交的粒度、顺序和语义边界。

4. 在改写历史之前，先向用户展示完整确认稿：

- 按提交顺序列出：
  - commit SHA（短 SHA 即可）
  - 原 message
  - 新 message 草稿
- 在用户明确确认前，不执行任何历史重写、push、PR/MR 创建操作。

5. 用户确认后，使用**非交互**方式批量重写 commit message：

- 仅针对当前分支的未推送提交执行。
- 必须保持提交数量、顺序和 diff 内容不变，只改 message。
- 优先使用可脚本化的非交互 `git rebase` 方案；不要依赖手工交互式编辑器。

6. 重写完成后，运行项目推荐的测试或检查命令。

7. 然后基于**当前分支**创建或更新 PR/MR：

- 不新建分支，不切换到别的分支。
- 先检查当前分支是否已有 PR/MR；有则更新，无则创建。
- 工具选择与 `check-commit-pr-push` 保持一致：
  - GitHub 远端使用 `gh`
  - 其他远端默认使用 `glab`

8. 由于历史已被改写，推送时使用：

```bash
git push --force-with-lease
```

9. 最终输出：

- 本次重写后的提交文案清单
- PR/MR 链接
- PR/MR 标题
- 目标分支

## 约束

- 当前分支不干净时，拒绝执行任何操作。
- 用户未确认全部新文案前，禁止改写历史。
- 不要引入回滚式或双保险式流程。
- 不要把提交合并成一个提交；本技能只重写 message，不改变提交边界。
- 不要把 PR/MR 建在新分支上；始终围绕当前分支操作。
