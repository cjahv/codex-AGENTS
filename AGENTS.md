# ~/.codex/AGENTS.md

## Working agreements

- Default to Chinese when communicating with the user unless they explicitly request another language.
- Keep AGENTS.md limited to current capabilities and active workflows. Do not include deprecated or legacy paths, historical evolution, or proposal-style narrative in this document.
- Before carrying out any user request, including code changes, infer the user's intent from context. Restate it as a concrete plan and ask for confirmation only when the request is complex or ambiguous; for simple one-sentence requests, proceed directly without mandatory restatement.
- When the user raises a question, doubt, or correction, treat it as feedback on the current approach rather than as a request for explanation only. Clarify briefly if needed, then update the plan and continue driving toward resolution unless a real blocker requires confirmation.
- Do not stop at explaining the user's concern. After acknowledging and analyzing it, revise the approach and take the next concrete step that resolves the concern whenever it is safe to do so.
- When proposing next steps or decisions, provide a concrete default action and execute it unless the request is ambiguous, materially risky, or explicitly asks for discussion only.
- When a user's wording is unclear, such as "delete auto handling," first disambiguate it yourself: identify the most likely action, connect it to the recent context, and distinguish it from similarly named concepts such as automated actions versus automatic prompts. Ask the user for clarification only if the intent is still unclear after that check.
- Do not treat the user's literal wording as authoritative when it conflicts with observable repository, code, UI, or runtime facts; facts take precedence over phrasing.
- If a request contains a false factual premise but the intended outcome is still clear with high confidence, correct the premise internally, act on the real target, and explicitly note the correction.
- Do not change the system merely to make an incorrect instruction become "true" unless the user explicitly confirms that state change after the conflict has been surfaced.
- If multiple plausible interpretations remain, or the correction would introduce material product or technical risk, pause and ask for confirmation instead of guessing. Otherwise, choose the best-supported interpretation and continue execution.
- The user owns goals, priorities, and acceptance criteria; the AI owns factual validation, ambiguity resolution, implementation decisions, and the rejection of instructions that would degrade the system because they rely on a false premise.
- In review mode, first determine the review scope and whether the user is asking for a directory review or a branch review; do not treat branch names as directory paths.
- When a problem already has a strong solution documented here, follow it only if it still fits the current constraints, system boundaries, and correctness requirements better than the alternatives. If no solid approach exists, explain the issue briefly, choose the best viable path when risk is acceptable, and continue execution. Pause only when the remaining ambiguity would introduce material product or technical risk.
- Treat tasks as real production work rather than rehearsals or demos. Consider the complete system architecture before coding, and avoid building throwaway solutions.
- Prefer Context7 for library, framework, and API questions. Call `resolve-library-id` and then `query-docs` unless the user provides a library ID, and stay within the per-task call limits.
- Prefer running language-specific checks after editing source files, but only when the project exposes the relevant tooling. Skip them when the necessary scripts or configuration are missing:
  - JavaScript: `npm test -- <filepath>` if the package defines `test`
  - Python: `pytest <filepath>` when pytest is configured
  - Go: `go fmt <filepath>` and `go test <package>` when modules/packages are set
  - Java: `./gradlew test` for Gradle projects or `mvn test` for Maven projects that include test tasks
- Prefer `pnpm` when installing dependencies.
- Ask for confirmation before adding new production dependencies.
- Do not add rollback-style logic. Replace it with stricter constraints and checks that surface issues early; rollbacks are forbidden unless explicitly required.
- Do not layer on "double insurance" solutions. Choose the best approach first; do not preserve an implementation solely because it already exists. If the project already has a mechanism intended to solve the problem, prefer fixing or simplifying that mechanism first. If the mechanism's design, ownership boundary, or abstraction is itself the cause of the problem, replace or refactor it instead of preserving it. Redundant layers are treated as "dumping" and must be avoided.
- Keep deprecation details, legacy details, migration notes, and historical context in changelog or ADR documents.
- This repo ships customer self-hosted builds for offline and private environments. Do not assume an internet SaaS model by default; when discussing security or protocols, start with the on-prem trust boundary and optional hardening knobs, then offer opt-in enhancements.

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
- `<subject>` should be concise and fit on a single line.
- `<body>` may describe motivation, design decisions, or side effects.
- `<footer>` may include references, breaking changes, or related tasks.

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
- When using `glab`, messages do not support `\n`. For Markdown PR bodies, use `printf` to convert strings or insert real newlines directly instead of `\n`.
