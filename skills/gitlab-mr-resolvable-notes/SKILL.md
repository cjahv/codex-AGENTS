---
name: gitlab-mr-resolvable-notes
description: Create GitLab MR resolvable discussions anchored到具体代码行，使用 glab api projects/<id>/merge_requests/<iid>/discussions 并按规范化问题格式输出。
metadata:
  short-description: Post formatted resolvable MR issues
---

# GitLab MR Resolvable Notes

## Review focus

- 优先关注自动化工具难以发现的边界情况、设计缺陷与逻辑问题。
- 不要花精力报告编译/语法错误；这类问题应由 CI 自动拦截。
- 若 MR/PR 关联了 Issue，需要参考 Issue 的描述与验收标准，评价当前 MR/PR 的完成度（覆盖度、偏差、未满足点）。
- 审查阶段优先查看 MR/PR 的流水线测试结果与日志，不在本地重复运行测试。

## When to use

Use this skill when you need to turn review findings into a single, formatted, resolvable discussion on a GitLab merge request, and post it via `glab api projects/<id>/merge_requests/<iid>/discussions`.

## Inputs to collect

- **Project ID**: prefer `glab api projects/:id` in the repo root to resolve the numeric ID.
- **Merge Request IID**: find the target MR for the current branch, e.g. `glab mr list --source-branch <branch>`.
- **Findings**: each issue needs a type, message, and a precise `file:line` in repo-relative form.
- **Diff refs**: `base_sha`, `head_sha`, `start_sha` for anchoring to the diff.

## Required message format

Each issue block must follow this exact structure, separated by a blank line:

```
<问题类型>: <消息>
- <文件相对路径>:<行>

<问题类型>: <消息>
- <文件相对路径>:<行>
```

Guidelines:
- Keep `<问题类型>` short (e.g., 安全风险, 可靠性, 逻辑错误).
- `<消息>` should be specific and actionable; include the impact and a concise fix suggestion.
- Use repo-relative paths and single line numbers (`path/to/File.java:31`).

## Quality evaluation (always)

Always post a quality evaluation comment regardless of outcome, and keep it as a single updatable comment:
- If a prior quality evaluation comment exists, update it; otherwise create it.
- This evaluation is a normal MR/PR comment (non-resolvable), not a discussion note.
- Use a stable hidden marker `<!-- quality-eval -->` at the top so it can be found and updated.
- **规范性**、**代码质量**、**表达清晰度** 三项评分，每项满分 10 分。
- Use Markdown with 5 symbols per item: ⭐️=2 points, ✨=1 point, 全角空格=0 points.

Example format:

```
<!-- quality-eval -->
本次 MR/PR 完成度高，改动聚焦且一致。
- 规范性: ⭐️⭐️⭐️⭐️　 (8/10)
- 代码质量: ⭐️⭐️⭐️⭐️✨ (9/10)
- 表达清晰度: ⭐️⭐️⭐️　　 (6/10)
```

## Procedure

1) **Resolve Project ID**

```
/bin/zsh -lc "cd <repo> && glab api projects/:id"
```

2) **Find MR IID**

```
/bin/zsh -lc "cd <repo> && glab mr list --source-branch <branch>"
```

3) **Get diff refs for line anchors**

```
/bin/zsh -lc "cd <repo> && glab api projects/<project_id>/merge_requests/<mr_iid> | jq '.diff_refs'"
```

Record `base_sha`, `head_sha`, `start_sha`.

4) **Fetch existing discussions for de-dup and reopen**

```
/bin/zsh -lc "cd <repo> && glab api projects/<project_id>/merge_requests/<mr_iid>/discussions"
```

Match rule (use this to locate a prior note):
- `note.body` equals `"<问题类型>: <消息>"` (exact match), and
- `note.position.new_path` equals `<path>` and `note.position.new_line` equals `<line>`.

Decision:
- If a matching discussion is **resolvable** and **unresolved** (`discussion.resolved == false`), **do not post** a new note.
- If a matching discussion is **resolved**, **reopen and edit the existing note** to explain why it is reopened (see step 5).
- If no match exists, create a new discussion (step 6).

5) **Reopen + edit resolved note (when the same issue reappears)**

```
/bin/zsh -lc 'cd <repo> && glab api projects/<project_id>/merge_requests/<mr_iid>/discussions/<discussion_id>/notes/<note_id> -X PUT \
  -H "Content-Type: application/json" \
  -d "{\\"body\\":\\"<问题类型>: <消息>\\n\\n重新打开原因: <说明>\\",\\"resolved\\":false}"'
```

Notes:
- Use the first matching note in the discussion for the update.
- Keep the original message, then append a short, concrete reason for reopening.

6) **Post one discussion per finding, anchored to the changed line**

```
/bin/zsh -lc 'cd <repo> && glab api projects/<project_id>/merge_requests/<mr_iid>/discussions -X POST \
  -H "Content-Type: application/json" \
  -d "{\\"body\\":\\"<问题类型>: <消息>\\",\\"position\\":{\\"base_sha\\":\\"<base_sha>\\",\\"start_sha\\":\\"<start_sha>\\",\\"head_sha\\":\\"<head_sha>\\",\\"position_type\\":\\"text\\",\\"new_path\\":\\"<path>\\",\\"new_line\\":<line>}}"'
```

## Notes

- 对删除行，改用 `old_path`/`old_line`；对未变更文件无法挂载行内讨论。
- 每个问题单独建一个 discussion，方便提交时自动解决。
- Use the API `discussions` endpoint to ensure the comment is resolvable and blocks merge if required by project settings.
- Avoid non-resolvable `mr note` for this workflow.
- 若同一问题已存在且未解决，不重复提交；若已解决但复现，必须按步骤 5 重新打开并说明原因。
