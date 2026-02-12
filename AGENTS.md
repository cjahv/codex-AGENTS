# ~/.codex/AGENTS.md

## Working agreements

- Default to Chinese when communicating with the user unless they explicitly request another language.
- Before executing any user-requested operation (including code changes), analyze the user's intent based on context. Restate it as a concrete plan and ask for confirmation only when the request is complex or ambiguous; for simple one-sentence requests, proceed directly without mandatory restatement.
- When proposing next steps or decisions, offer concrete, ready-to-execute suggestions (with a clear default) and ask the user to confirm or adjust, instead of posing open-ended questions.
- When a user's wording is unclear (e.g., "delete auto handling"), first interrogate the phrase yourself—ask what action it likely targets, how it connects to the recent context, and whether similarly named concepts (such as automated actions vs. automatic prompts) differ; only if intent remains uncertain after that self-check should you ask the user for clarification.
- In review mode, first determine the review scope and whether the user is asking to review a directory or a branch; do not treat branch names as directory paths.
- When a problem already has a strong solution documented here, follow it; if no solid approach exists (e.g., brittle hardcoding, unbounded enumeration, or unclear efficacy), pause and clearly tell the user about the issue, propose ideas, and collaborate instead of forcing a poor fix.
- Treat tasks as real production work (not a rehearsal or demo); consider the complete system architecture before coding, and avoid building throwaway demos.
- Prefer Context7 for library/framework/API questions; call `resolve-library-id` then `query-docs` (unless the user provides a library ID) before relying on memory, and keep usage within the per-task call limits.
- Prefer running language-specific checks after editing source files, but only when the project exposes the relevant tooling (skip when scripts/configs are missing):
  - JavaScript: `npm test -- <filepath>` if the package defines `test`
  - Python: `pytest <filepath>` when pytest is configured
  - Go: `go fmt <filepath>` and `go test <package>` when modules/packages are set
  - Java: `./gradlew test` for Gradle projects or `mvn test` for Maven projects that include test tasks
- Prefer `pnpm` when installing dependencies.
- Ask for confirmation before adding new production dependencies.
- Absolutely do not add rollback-style logic. Replace it with stricter constraints/checks that surface issues early; rollbacks are forbidden unless explicitly required.
- Do not layer "double insurance" solutions. Decide on the best approach first; if the project already has a mechanism meant to solve the problem but it is ineffective, focus on fixing that existing solution instead of adding parallel safeguards—adding redundant layers is treated as "dumping" and must be avoided.
- Whenever introducing a new path or an optimized implementation, explicitly mark the old path/implementation as `Deprecated`; never assume it will be cleaned up later without a deprecation marker. When describing removed features, also mark related rollback tests and rollback-oriented code as `Deprecated` to prevent accidental regression usage.
- Product form: this repo ships customer self-hosted builds (offline/private environments), so do not assume an internet SaaS model by default; when discussing security/protocols, first consider the on-prem trust boundary and optional hardening knobs, then offer opt-in enhancements.

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
