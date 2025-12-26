---
name: gitlab-mr-resolvable-notes
description: Create a GitLab merge request resolvable discussion comment with a规范化问题格式, using glab api projects/<id>/merge_requests/<iid>/discussions.
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

3) **Compose the message body** using the required format.

4) **Post as resolvable discussion**

```
/bin/zsh -lc "cd <repo> && glab api projects/<project_id>/merge_requests/<mr_iid>/discussions -X POST -f body=\"<message>\""
```

## Notes

- Use the API `discussions` endpoint to ensure the comment is resolvable and blocks merge if required by project settings.
- Avoid non-resolvable `mr note` for this workflow.
- If you need to update the content, post a new discussion and resolve the old one manually in GitLab UI.
