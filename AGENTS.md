# ~/.codex/AGENTS.md

## Working agreements

- Default to Chinese when communicating with the user unless they explicitly request another language.
- Before making any code changes, confirm or restate the user's intent only when the request is ambiguous or does not map to a concrete action.
- When proposing next steps or decisions, offer concrete, ready-to-execute suggestions (with a clear default) and ask the user to confirm or adjust, instead of posing open-ended questions.
- When a user's wording is unclear (e.g., "delete auto handling"), first interrogate the phrase yourself—ask what action it likely targets, how it connects to the recent context, and whether similarly named concepts (such as automated actions vs. automatic prompts) differ; only if intent remains uncertain after that self-check should you ask the user for clarification.
- In review mode, first determine the review scope and whether the user is asking to review a directory or a branch; do not treat branch names as directory paths.
- When a problem already has a strong solution documented here, follow it; if no solid approach exists (e.g., brittle hardcoding, unbounded enumeration, or unclear efficacy), pause and clearly tell the user about the issue, propose ideas, and collaborate instead of forcing a poor fix.
- When performing check operations in local development, if the target is local or directly accessible locally, run the check without asking for user approval. Treat checks as read-only; tests that perform writes are not checks.
- Prefer running language-specific checks after editing source files, but only when the project exposes the relevant tooling (skip when scripts/configs are missing):
  - JavaScript: `npm test -- <filepath>` if the package defines `test`
  - Python: `pytest <filepath>` when pytest is configured
  - Go: `go fmt <filepath>` and `go test <package>` when modules/packages are set
  - Java: `./gradlew test` for Gradle projects or `mvn test` for Maven projects that include test tasks
- Prefer `pnpm` when installing dependencies.
- Ask for confirmation before adding new production dependencies.
- Do not add rollback-style logic for compatibility; use lean, effective checks/constraints to surface and fix issues early, and only introduce rollbacks when explicitly required.
- Do not layer "double insurance" solutions. Decide on the best approach first; if the project already has a mechanism meant to solve the problem but it is ineffective, focus on fixing that existing solution instead of adding parallel safeguards—adding redundant layers is treated as "dumping" and must be avoided.

## Commit & Pull Request Conventions

### Commit Message Format

All commits **must** follow the conventional form:

```
<type>(<scope>): <subject>
<body>
<footer>
```

Requirements:

- The entire message **should be written in Chinese by default unless explicitly requested otherwise**.
- `<subject>` should be concise and written in one line.
- `<body>` may describe motivation, design decisions, or side-effects.
- `<footer>` can include references, breaking changes, or related tasks.

### Pull Request Rules

When creating a Pull Request:

- If the current repository **remote URL is GitHub**, PRs must be created using the `gh` CLI.
- Otherwise (e.g., GitLab), PRs must be created using the `glab` CLI.
- PR titles and descriptions **must be written in Chinese**.
- PR descriptions should follow common best practices:
  - State *what* changed.
  - Explain *why* the change is necessary.
  - List any *breaking changes*.
  - Attach relevant tests, screenshots, or logs when applicable.
- When using `glab`, messages do not support `\n`; for Markdown PR bodies, use `printf` to convert strings or insert real newlines directly instead of `\n`.

### Code Execution Rules for Codex

When executing commands inside Codex automation or agent flows:

- Use `/bin/zsh -lc` only when directly executing a command. In all other contexts (documentation, code examples, suggested commands), do not add the wrapper.
- Exceptions (no wrapper needed): commands that are included by default on macOS/Linux, and the explicit exception list below.
- Exception list (no wrapper needed): `ls`, `git`, `rg`, `sed`, `curl`, `wget`.
- Use exactly one shell layer with zsh: if an outer shell already exists, do not add another; if no shell wrapper is already present, wrap the command with `/bin/zsh -lc` as the single outermost layer:

```
/bin/zsh -lc '<command>'
```

- When executing commands, do not run them directly unless they are base system commands; otherwise ensure the `/bin/zsh -lc` wrapper when they are not already wrapped.
- If another wrapper would surround the command, restructure the invocation so that `/bin/zsh -lc` remains the outermost layer to avoid nested shells changing behavior.

Example:

```
/bin/zsh -lc 'pnpm install && pnpm build'
```
