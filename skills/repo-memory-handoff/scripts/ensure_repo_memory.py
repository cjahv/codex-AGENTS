#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import re
import sys


MEMORY_SECTION = """## Memory Workflow
- Before substantial cross-module work, read `.agent-handoff/README.md` and the latest handoff file it points to.
- Use code/tests as source of truth; if memory conflicts with current code, follow code and then update memory.
- After finishing a substantial repo-level change, add or update one handoff file under `.agent-handoff/` including: decision, current behavior, validation commands, and pending follow-ups.
- Keep AGENTS and handoff memory focused on current, active workflows only; deprecated or historical narratives belong in changelog/ADR documents.
"""

README_TEMPLATE = """# Agent Handoff

Read this directory before substantial cross-module work.

Latest: {latest}
"""

HANDOFF_TEMPLATE = """# Handoff

## Decision
{decision}

## Current Behavior
{behavior}

## Validation Commands
{validation}

## Pending Follow-Ups
{follow_ups}
"""


@dataclass
class PlannedChanges:
    agents_changed: bool = False
    readme_changed: bool = False
    handoff_changed: bool = False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ensure repository memory workflow and handoff files exist."
    )
    parser.add_argument("--repo", default=".", help="Repository path or a nested path within it.")
    parser.add_argument("--check", action="store_true", help="Validate without writing files.")
    parser.add_argument("--handoff-slug", default="memory-update", help="Slug for the handoff file name.")
    parser.add_argument("--handoff-date", help="Date prefix for the handoff file name, default: today in YYYY-MM-DD.")
    parser.add_argument("--decision", action="append", default=[], help="Decision line for the handoff file.")
    parser.add_argument("--behavior", action="append", default=[], help="Current behavior line for the handoff file.")
    parser.add_argument("--validate", action="append", default=[], help="Validation command for the handoff file.")
    parser.add_argument("--follow-up", action="append", default=[], help="Pending follow-up line for the handoff file.")
    return parser.parse_args()


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise SystemExit(f"Could not find repository root from: {start}")


def render_list(items: list[str], empty_fallback: str) -> str:
    values = [item.strip() for item in items if item.strip()]
    if not values:
        values = [empty_fallback]
    return "\n".join(f"- {value}" for value in values)


def update_agents(agents_path: Path, check: bool) -> bool:
    if agents_path.exists():
        original = agents_path.read_text()
    else:
        original = ""

    pattern = re.compile(r"(?ms)^## Memory Workflow\n(?:- .*\n?)+")
    if pattern.search(original):
        updated = pattern.sub(MEMORY_SECTION.rstrip(), original).rstrip() + "\n"
    else:
        if original.strip():
            updated = original.rstrip() + "\n\n" + MEMORY_SECTION
        else:
            updated = MEMORY_SECTION

    changed = updated != original
    if changed and not check:
        agents_path.write_text(updated)
    return changed


def read_latest_from_readme(readme_path: Path) -> str | None:
    if not readme_path.exists():
        return None
    match = re.search(r"^Latest:\s+(.+)$", readme_path.read_text(), re.MULTILINE)
    return match.group(1).strip() if match else None


def update_readme(readme_path: Path, latest_relative: str, check: bool) -> bool:
    updated = README_TEMPLATE.format(latest=latest_relative)
    original = readme_path.read_text() if readme_path.exists() else ""
    changed = updated != original
    if changed and not check:
        readme_path.write_text(updated)
    return changed


def update_handoff(handoff_path: Path, args: argparse.Namespace, check: bool) -> bool:
    content = HANDOFF_TEMPLATE.format(
        decision=render_list(args.decision, "Document the latest repository-level decision."),
        behavior=render_list(args.behavior, "Describe the current repository behavior."),
        validation=render_list(args.validate, "List the commands used to validate the change."),
        follow_ups=render_list(args.follow_up, "Record the next active follow-up or state that none are pending."),
    )
    original = handoff_path.read_text() if handoff_path.exists() else ""
    changed = content != original
    if changed and not check:
        handoff_path.write_text(content)
    return changed


def main() -> int:
    args = parse_args()
    repo_root = find_repo_root(Path(args.repo))
    agents_path = repo_root / "AGENTS.md"
    handoff_dir = repo_root / ".agent-handoff"

    date_prefix = args.handoff_date or datetime.now().strftime("%Y-%m-%d")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_prefix) is None:
        raise SystemExit("--handoff-date must use YYYY-MM-DD")

    handoff_filename = f"{date_prefix}-{args.handoff_slug}.md"
    handoff_path = handoff_dir / handoff_filename
    readme_path = handoff_dir / "README.md"

    if not args.check:
        handoff_dir.mkdir(parents=True, exist_ok=True)

    changes = PlannedChanges()
    changes.agents_changed = update_agents(agents_path, args.check)
    changes.handoff_changed = update_handoff(handoff_path, args, args.check)
    changes.readme_changed = update_readme(readme_path, handoff_filename, args.check)

    if args.check:
        problems = []
        if not agents_path.exists():
            problems.append("Missing AGENTS.md")
        else:
            content = agents_path.read_text()
            if MEMORY_SECTION.strip() not in content:
                problems.append("AGENTS.md is missing the required Memory Workflow section")

        latest = read_latest_from_readme(readme_path)
        if not readme_path.exists():
            problems.append("Missing .agent-handoff/README.md")
        elif latest != handoff_filename:
            problems.append(
                f".agent-handoff/README.md does not point to {handoff_filename}"
            )

        if not handoff_path.exists():
            problems.append(f"Missing .agent-handoff/{handoff_filename}")

        if problems:
            for problem in problems:
                print(problem)
            return 1

        print("Repository memory files are present and current.")
        return 0

    print(f"Repository root: {repo_root}")
    print(f"AGENTS.md: {'updated' if changes.agents_changed else 'unchanged'}")
    print(f".agent-handoff/README.md: {'updated' if changes.readme_changed else 'unchanged'}")
    print(f"{handoff_filename}: {'updated' if changes.handoff_changed else 'unchanged'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
