---
name: commit-message-from-staged
description: 根据 git diff --cached 整理提交文案草稿（不执行提交）
metadata:
  short-description: 从暂存区生成提交文案
---

# 根据暂存区整理提交文案

## 适用场景

当用户希望根据已暂存的改动（`git diff --cached`）生成提交文案草稿，但明确要求**不要提交**。

## 工作流程

1) 读取暂存区差异（只读）：

```
git diff --cached
```

2) 若无暂存改动，直接说明“暂存区为空，无法生成提交文案”，停止。

3) 基于差异整理提交文案草稿：

- 给出简洁的 subject（优先用动词开头，避免过长）
- 可选的 body：说明动机、关键设计、影响面
- 可选的 footer：关联任务或破坏性变更（若无则省略）

4) 明确说明未执行 `git commit`。

## 输出格式（建议）

- 提交文案草稿（按 subject/body/footer 展示）
- 变更要点的简短列表（可选）

## 约束

- 不要执行 `git commit` 或其他会改变仓库状态的命令。
- 如需进一步操作（例如实际提交），要求用户确认。