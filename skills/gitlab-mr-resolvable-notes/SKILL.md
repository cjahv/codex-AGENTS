---
name: gitlab-mr-resolvable-notes
description: Create GitLab MR resolvable discussions anchored到具体代码行，使用 glab api projects/<id>/merge_requests/<iid>/discussions 并按规范化问题格式输出。
metadata:
  short-description: Post formatted resolvable MR issues
---

# GitLab MR Resolvable Notes

## Review focus

- 项目运行在内网环境；讨论风险与方案时优先站在本地部署/内网运维的现实约束上。
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
- **Author intent / constraints**: MR description and submitter comments that explain edge cases or rationale.

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
- `<消息>` must be in **大白话**，面向不懂技术的产品经理：
  - 先说明“会发生什么影响/用户会遇到什么问题/业务会损失什么”。
  - 再给出“怎么改会更好”的一句话建议（避免术语与缩写）。
  - 避免“代码/函数/类/接口”等实现词，改用“功能/页面/流程/数据”表述。
- Use repo-relative paths and single line numbers (`path/to/File.java:31`).

## Quality evaluation (always)

Always post a quality evaluation comment regardless of outcome, and keep it as a single updatable comment:
- If a prior quality evaluation comment exists, update it; otherwise create it.
- This evaluation is a normal MR/PR comment (non-resolvable), not a discussion note.
- Use a stable hidden marker `<!-- quality-eval -->` at the top so it can be found and updated.
- The quality evaluation must be the first output and the first published comment in the review flow:
  - When generating the final response, output the quality evaluation before any findings.
  - When calling the API, update/create the quality evaluation comment before creating any resolvable discussions.
- Even when there are **zero findings**, you must still post/update the quality evaluation comment.
- If there are **zero findings**, do **not** create any discussions; only publish the quality evaluation comment, and resolve any previously open discussions that are now fixed.
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

0) **Post or update quality evaluation first**

Ensure the quality evaluation comment (with `<!-- quality-eval -->`) is created/updated before any discussion notes are posted.
If there are no findings, continue to step 5 to resolve any existing open discussions, then stop.

1) **Resolve Project ID**

```
/bin/zsh -lc "cd <repo> && glab api projects/:id"
```

2) **Find MR IID**

```
/bin/zsh -lc "cd <repo> && glab mr list --source-branch <branch>"
```

3) **Read submitter comments and MR context**

```
/bin/zsh -lc "cd <repo> && for page in {1..20}; do glab api projects/<project_id>/merge_requests/<mr_iid>/notes?page=$page&per_page=100; done"
```

Focus on author notes that explain intent, edge cases, or constraints; carry this context into review findings.

4) **Get diff refs for line anchors**

```
/bin/zsh -lc "cd <repo> && glab api projects/<project_id>/merge_requests/<mr_iid> | jq '.diff_refs'"
```

Record `base_sha`, `head_sha`, `start_sha`.

5) **Fetch existing discussions for de-dup and reopen (with pagination)**

```
/bin/zsh -lc "cd <repo> && for page in {1..20}; do glab api projects/<project_id>/merge_requests/<mr_iid>/discussions?page=$page&per_page=100; done"
```

Match rule (use this to locate a prior note):
- `note.body` equals `"<问题类型>: <消息>"` (exact match), and
- `note.position.new_path` equals `<path>` and `note.position.new_line` equals `<line>`.

Decision:
- If a matching discussion is **resolvable** and **unresolved** (`discussion.resolved == false`), **do not post** a new note.
- If a matching discussion is **resolved** and the issue **still exists**, **reopen and add a follow-up note** to explain why it is reopened (see step 5).
- If a matching discussion is **resolved** and the issue **no longer exists**, **ensure it is marked resolved** (see step 6).
- If a matching discussion is **resolved == false** but the issue **is already fixed**, **mark it resolved** (see step 6).
- If no match exists, create a new discussion (step 7).

6) **Reopen + follow-up note (when the same issue reappears)**

```
/bin/zsh -lc 'cd <repo> && glab api projects/<project_id>/merge_requests/<mr_iid>/discussions/<discussion_id>/notes/<note_id> -X PUT \
  -H "Content-Type: application/json" \
  -d "{\\"resolved\\":false}"'
'
```

Notes:
- Use the first matching note in the discussion for the update.
- Then add a new follow-up note to explain why it is reopened and include concrete evidence.

Follow-up note example:

```
/bin/zsh -lc 'cd <repo> && glab api projects/<project_id>/merge_requests/<mr_iid>/discussions/<discussion_id>/notes -X POST \
  -H "Content-Type: application/json" \
  -d "{\\"body\\":\\"重新打开原因: <说明>\\n证据: <更具体的证据>\\",\\"resolved\\":false}"'
```

7) **Mark a discussion as resolved when the issue is fixed**

```
/bin/zsh -lc 'cd <repo> && glab api projects/<project_id>/merge_requests/<mr_iid>/discussions/<discussion_id>/notes/<note_id> -X PUT \
  -H "Content-Type: application/json" \
  -d "{\\"resolved\\":true}"'
```

Notes:
- Use the first matching note in the discussion for the update.
- This is required when the issue is already fixed but the discussion is still unresolved.

8) **Post one discussion per finding, anchored to the changed line**

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
 - 讨论措辞尽量“非技术化”：用场景和结果表达，不用工程细节。
