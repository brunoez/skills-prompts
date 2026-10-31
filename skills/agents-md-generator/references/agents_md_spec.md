# AGENTS.md Specification & Reference (Linux Foundation / agents.md)

This reference outlines the open specification for `AGENTS.md` files as governed under LF Projects, LLC ([agents.md](https://agents.md/)).

---

## 1. File Placement & Precedence

1. **Root Placement:** The primary file MUST be placed at the repository root (`./AGENTS.md`).
2. **Nested Precedence (Monorepos):** In multi-package repositories or monorepos, an `AGENTS.md` file MAY be placed inside any package subdirectory (e.g. `packages/ui/AGENTS.md`, `services/billing/AGENTS.md`).
3. **Resolution Rule:** Coding agents automatically read the nearest `AGENTS.md` file in the directory hierarchy. The closest file takes precedence over parent instructions.

---

## 2. Standard Schema & Recommended Headings

A well-formed `AGENTS.md` contains the following level-2 headings:

### `## Dev environment tips`
- How to start the local development server with Hot Module Replacement (HMR).
- Specific commands to avoid during interactive agent sessions (e.g. `npm run build`).
- Package jump commands for monorepos (e.g. `pnpm dlx turbo run where <name>`).

### `## Testing instructions`
- Exact test command for the entire package or repository.
- Parameterized command to run a single test by name or regex pattern.
- Requirement for green suites before commits.
- Prohibition against deleting or weakening tests.

### `## Coding conventions`
- Target language runtime and strict compiler flags.
- Preferred validation libraries (e.g. Zod, Pydantic).
- Co-location rules for assets and test files.

### `## PR & Commit instructions`
- Branch naming and pull request title format.
- Conventional Commits requirement.
- Mandatory pre-commit verification steps.

---

## 3. Minimal Reference Template

```markdown
# AGENTS.md — Development Guidelines

## Dev environment tips
- Use `pnpm dev` to start the local development server with HMR.
- Do NOT run `pnpm build` during interactive agent sessions; it disrupts hot-reload state.
- In monorepo: run `pnpm --filter <pkg_name> dev` to work on a specific package.

## Testing instructions
- Full suite: `pnpm test`.
- Single test: `pnpm vitest run -t "<test_name>"`.
- All checks must pass with zero failures before committing.
- Add or update tests for any code you change.

## Coding conventions
- Use TypeScript with strict mode enabled.
- Parse and validate all external inputs with Zod.
- Co-locate unit tests alongside implementation (`foo.test.ts` next to `foo.ts`).

## PR & Commit instructions
- Use Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`).
- Run `pnpm lint` and `pnpm test` before committing.
```
