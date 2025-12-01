# ~/.codex/AGENTS.md

## Working agreements

- Prefer running language-specific checks after editing source files, but only when the project exposes the relevant tooling (skip when scripts/configs are missing):
  - JavaScript: `npm test -- <filepath>` if the package defines `test`
  - Python: `pytest <filepath>` when pytest is configured
  - Go: `go fmt <filepath>` and `go test <package>` when modules/packages are set
  - Java: `./gradlew test` for Gradle projects or `mvn test` for Maven projects that include test tasks
- Prefer `pnpm` when installing dependencies.
- Ask for confirmation before adding new production dependencies.

## Commit & Pull Request Conventions

### Commit Message Format

All commits **must** follow the conventional form:

```
<type>(<scope>): <subject>
<body>
<footer>
```

Requirements:

- The entire message **must be written in Chinese**.
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

### Code Execution Rules for Codex

When executing commands inside Codex automation or agent flows:

- All commands **must** be wrapped with:

```
/bin/sh -c '<command>'
```

- Do not execute commands directly; always ensure shell wrapping for consistency, portability, and safety.
- Multi-step commands must be combined into a single `/bin/sh -c` invocation using `&&` or `;` as appropriate.

Example:

```
/bin/sh -c 'pnpm install && pnpm build'
```
