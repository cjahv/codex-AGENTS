---
name: repo-memory-handoff
description: Ensure repository-scoped memory is present and current. Use when Codex needs to check or add a project's AGENTS.md memory workflow, bootstrap or refresh `.agent-handoff/README.md`, record a latest handoff file after substantial repo-level work, or reconcile repo memory with the current code and tests.
---

# Repo Memory Handoff

Use this skill to keep repository memory explicit, current, and minimal.

## Workflow

1. Resolve the repository root.
   Prefer the current working tree root. If the user gives a nested path, walk upward until `.git` is found.

2. Check the repository memory surface.
   Inspect `AGENTS.md`, `.agent-handoff/README.md`, and the latest handoff file referenced by the README.

3. Trust code over memory.
   If handoff notes or AGENTS instructions conflict with the current code or tests, follow the code, then update memory artifacts to match reality.

4. Ensure the standard memory workflow exists.
   If the repository-level `AGENTS.md` is missing the `## Memory Workflow` section, add it. If `AGENTS.md` does not exist, create a concise one that contains only the current memory workflow.

5. Record the latest substantial change.
   After a substantial repo-level change, create or update one handoff file under `.agent-handoff/` and update `.agent-handoff/README.md` so it points to that file.

## Required Memory Workflow

Keep this section exactly in the repository `AGENTS.md` unless the user explicitly asks for a different active workflow:

```markdown
## Memory Workflow
- Before substantial cross-module work, read `.agent-handoff/README.md` and the latest handoff file it points to.
- Use code/tests as source of truth; if memory conflicts with current code, follow code and then update memory.
- After finishing a substantial repo-level change, add or update one handoff file under `.agent-handoff/` including: decision, current behavior, validation commands, and pending follow-ups.
- Keep AGENTS and handoff memory focused on current, active workflows only; deprecated or historical narratives belong in changelog/ADR documents.
```

## Files To Maintain

- `AGENTS.md`
  Ensure the memory workflow section exists once and is current.

- `.agent-handoff/README.md`
  Keep a single clear pointer to the latest handoff file. Use a relative path from `.agent-handoff/`.

- `.agent-handoff/<date>-<slug>.md`
  Write concise sections for:
  - `## Decision`
  - `## Current Behavior`
  - `## Validation Commands`
  - `## Pending Follow-Ups`

## Script

Use [`scripts/ensure_repo_memory.py`](./scripts/ensure_repo_memory.py) to make deterministic updates instead of rewriting these files by hand.

Typical usage:

```bash
python3 /path/to/repo-memory-handoff/scripts/ensure_repo_memory.py \
  --repo /path/to/repo \
  --handoff-slug memory-bootstrap \
  --decision "Added repository memory workflow and initialized handoff tracking." \
  --behavior "Repository AGENTS.md now includes the standard memory workflow." \
  --behavior "The repo now has .agent-handoff/README.md pointing to the latest handoff file." \
  --validate "python3 /path/to/repo-memory-handoff/scripts/ensure_repo_memory.py --repo /path/to/repo --check" \
  --follow-up "Update the latest handoff file after the next substantial repo-level change."
```

Use `--check` for validation-only runs.

## Writing Rules

- Keep AGENTS and handoff content concise and current.
- Do not add deprecated history, migration stories, or design prose.
- If `AGENTS.md` already has unrelated active instructions, preserve them and only add or replace the `## Memory Workflow` section.
- If no latest handoff file exists yet, create one when the task meaningfully changes repository-level behavior.
