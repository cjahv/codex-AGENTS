---
name: glab-efficient-workflow
description: GLAB 面向 GitLab 仓库的高效操作技能。用于查询、创建、更新 Merge Request，推送分支，查看 CI 状态，或处理 MR 评论与讨论的场景；当用户要求创建 MR、更新 MR、检查分支是否已有 MR、查看流水线或用 glab 处理审查意见时触发。
---

# Glab Efficient Workflow

## 目标
使用 `glab` 以非交互方式稳定完成 MR 全流程，优先可脚本化与可复现操作。

## 快速决策
1. 先判断仓库类型：仅在 GitLab 仓库使用 `glab`；GitHub 仓库改用 `gh`。
2. 先确认命令兼容性：对关键子命令先运行 `glab <subcommand> --help`，再执行正式命令。
3. 默认使用非交互参数：优先 `--yes`、显式 `--source-branch`、`--target-branch`、`--title`、`--description`。

## 标准流程
1. 进行环境检查。
- 运行 `glab --version`。
- 运行 `glab auth status`；若未登录，明确提示用户先完成登录。
- 读取当前分支：`branch=$(git branch --show-current)`。

2. 处理 MR。
- 先检查当前分支是否已有 MR：`glab mr list -s "$branch" -F json`。
- 若已有 MR，使用 `glab mr update <iid> ...` 更新标题、描述、目标分支等信息。
- 若无 MR，先执行 `git push -u origin "$branch"`，再执行 `glab mr create ... --yes` 创建 MR。

3. 回报结果。
- 输出 MR 链接、标题、目标分支。
- 如可获取流水线信息，补充 CI 状态（`running`/`success`/`failed`）。

## 高可靠规则
1. 描述文本使用单引号 heredoc，禁止直接在命令中内联复杂 Markdown。
```bash
desc=$(cat <<'EOF'
## 变更内容
- ...
EOF
)
glab mr update 123 --description "$desc" --yes
```

2. 优先使用 JSON 输出进行判断与提取。
- `glab mr list ... -F json`
- `glab mr view <iid> -F json`

3. 遇到 flag 不兼容时，先查帮助并切换到当前版本支持的参数，不假设跨版本一致。

## 参考文件
- 常用命令与模板：`references/glab-cheatsheet.md`
