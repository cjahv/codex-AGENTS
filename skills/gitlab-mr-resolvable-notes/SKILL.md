---
name: gitlab-mr-resolvable-notes
description: Create GitLab MR resolvable discussions anchored到具体代码行，使用 glab api projects/<id>/merge_requests/<iid>/discussions 并按规范化问题格式输出。
metadata:
  short-description: Post formatted resolvable MR issues
---

# GitLab MR Resolvable Notes

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

4) **Post one discussion per finding, anchored to the changed line**

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
- If you need to update the content, post a new discussion and resolve the old one manually in GitLab UI.
