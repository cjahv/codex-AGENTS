---
name: gitignore-change-review
description: Review .gitignore changes before creating, editing, staging, or explaining ignore rules. Use when Codex writes or modifies .gitignore, decides whether a generated file should be ignored or committed, sees a negated ignore rule such as !/path, or needs to justify whether build outputs, tool templates, cache files, generated assets, or local configuration belong in version control.
---

# Gitignore Change Review

Use this skill to treat `.gitignore` edits as version-control boundary decisions, not as cleanup after a file already exists.

## Decision Flow

Before adding, removing, or defending a `.gitignore` rule:

1. Classify the path: source/configuration, project-owned generated artifact, tool default template, build output, cache, dependency install, secret, local workspace file, or editor/OS noise.
2. Check whether the file contains project-specific intent. Do not count the fact that a tool can use the file, or that an existing ignore rule allows it, as sufficient intent.
3. Ask what breaks if the file is not committed. Prefer committing only when absence harms reproducibility, runtime behavior, build correctness, schema/API contracts, or team-shared configuration.
4. Ask what maintenance burden appears if the file is committed. Watch for vendored default templates, generated files that drift after tool upgrades, per-machine paths, timestamps, caches, or duplicated configuration.
5. Decide the ignore rule from that boundary decision. Do not use a `.gitignore` exception to prove the file belongs in the repository; the exception is itself part of the change under review.

## Commit Criteria

Commit a file normally ignored by broad rules only when at least one is true:

- It is authored project source or hand-maintained configuration.
- It captures a team-shared runtime, build, packaging, or development contract that is not reliably regenerated.
- It is a generated artifact intentionally used as repository input, and the project documents or enforces how to refresh it.
- It is a placeholder needed to preserve an otherwise-empty tracked directory, such as `.gitkeep`.

Ignore the file when any of these are true unless there is explicit project-specific justification:

- It is a build product, cache, dependency install, log, temporary file, coverage output, or local environment file.
- It is a tool-generated default template with no project customization.
- It exists only because a command was run locally.
- It duplicates information already owned by a source file or upstream tool template.
- It would require future sync work after tool upgrades without providing project value.

## Negated Rules

Treat `!` rules as high-scrutiny exceptions. For every negated rule:

1. Identify the broad rule it overrides.
2. State the positive reason the exception is shared project state.
3. Verify the exception does not accidentally unignore generated siblings.
4. Prefer a narrower placeholder or source-owned path when that satisfies the need.

## Response Pattern

When the user asks why a `.gitignore`-related file should or should not be committed, answer from consensus criteria:

- What the file represents.
- Whether it has project-specific content.
- What breaks if it is absent.
- What maintenance cost appears if it is present.
- The final decision and the exact `.gitignore` rule change, if needed.

If prior work added a weak exception, correct it directly when safe: remove the exception, restage `.gitignore` if it was already staged, and verify with `git check-ignore -v <path>`.
