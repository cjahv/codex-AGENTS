# GLab Cheatsheet

## 1) 环境与仓库检查
```bash
glab --version
glab auth status
git remote -v
git branch --show-current
```

## 2) 分支对应 MR 查询
```bash
branch=$(git branch --show-current)
glab mr list -s "$branch" -F json
```

## 3) 创建 MR（推荐非交互）
```bash
branch=$(git branch --show-current)
git push -u origin "$branch"

glab mr create \
  --source-branch "$branch" \
  --target-branch main \
  --title "fix(scope): 简述变更" \
  --description "## 变更内容\n- ..." \
  --yes
```

## 4) 更新 MR 描述（安全写法）
```bash
desc=$(cat <<'EOF'
## 变更内容
- ...

## 测试
- ...
EOF
)

glab mr update 123 --description "$desc" --yes
```

## 5) 查看 MR 详情与 CI 状态
```bash
glab mr view 123 -F json
```

可结合文本过滤快速看关键字段：
```bash
glab mr view 123 -F json | rg '"title"|"target_branch"|"source_branch"|"web_url"|"status"'
```

## 6) 常见坑与规避
1. 不要假设 flags 跨版本一致。
- 先执行 `glab mr list --help` 再用参数。
- 某些版本不支持 `--state`，改用 `--all` / `--closed` / `--merged` 等可用参数。

2. 不要在 `--description` 里直接放含反引号与通配符的复杂文本。
- 使用单引号 heredoc 构造变量后再传参，避免 shell 展开。

3. 变量全部加引号。
- 使用 `"$branch"`、`"$desc"`，避免空格或特殊字符导致命令失败。

4. 优先显式参数。
- 创建/更新 MR 时显式指定 source/target/title/description，减少交互提示与歧义。
