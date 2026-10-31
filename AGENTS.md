# AGENTS.md — Guidelines for AI Coding Agents in this Repository

Welcome to the **Skills & Prompts Suite** (`brunoez/skills-prompts`).
This repository contains production-ready prompts, Open Agent Skills ([agentskills.io](https://agentskills.io/specification)), CI/CD integrations, and deterministic evaluation scripts for Software Engineering, AppSec (Yellow Team), and Driven Development.

Follow these strict guidelines when working interactively in this repository (Claude Code, Google Antigravity, OpenAI Codex, Cursor, etc.).

---

## 1. Development & Testing Commands

| Command | Purpose | Required Output |
| :--- | :--- | :--- |
| `pytest tests/` | Runs all test suites (integrity, skills, sync) | `== XX passed ==` (Zero failures) |
| `pytest -k "<pattern>"` | Runs filtered tests matching a pattern | `== XX passed ==` |
| `python3 tests/test_integrity.py` | Validates prompt catalogs, installer sync & structure | `✅ Todos os checks passaram com sucesso.` |
| `python3 -m unittest tests/test_<name>.py` | Runs unit tests for a specific skill script | `OK` |
| `bash install.sh /tmp/test-install all` | Validates installer execution locally | Exit code 0 |
| `shellcheck install.sh` | Shell script linter | Zero warnings/errors |
| `bash -n install.sh` | Bash syntax validation | Exit code 0 |

> [!IMPORTANT]
> Always run `pytest tests/` before reporting any task as complete or creating a commit. Never modify tests to artificially pass without fixing underlying issues.

---

## 2. Architecture & File Structure

```plaintext
prompts/                  # Structured markdown prompts
  ├── driven-development/ # SDD, TDD, BDD, CDD, DDD, TypeDD, DataDD
  ├── security/           # OWASP ASTF, ASVS L2, AppSec Auditor, Threat Modeling
  ├── devops/             # CI/CD, IaC, Resilience
  └── jev/                # System One, Guardrails, MCP Security
skills/                   # Executable Open Agent Skills (agentskills.io)
  └── <skill-name>/
      ├── SKILL.md        # YAML frontmatter (name, description) + instructions
      ├── references/     # Modular rubrics and guidelines
      └── scripts/        # Deterministic Python CLI automation
tests/                    # Pytest and unittest suites
install.sh                # Universal multi-assistant installer
README.md                 # Human documentation, quickstart & catalog
CHANGELOG.md              # Keep a Changelog (SemVer)
```

---

## 3. Strict Invariants for Prompts & Skills

1. **Mandatory Prompt Sections:**
   Every prompt in `prompts/` MUST contain these exact headers to satisfy `tests/test_integrity.py`:
   - `## OBJETIVO`
   - `## ESCOPO` (or `## ESCOPO E OBRIGATORIEDADE DE LEITURA`)
   - `## CHECKLIST DE VALIDAÇÃO PRÁTICA` (or numbered subsections `### 1.`)
   - `## SAÍDA` (or `## SAÍDA NO CHAT / TERMINAL`)
   - `## ENTREGÁVEIS` (or `## ENTREGÁVEIS FINAIS`)

2. **Mandatory Skill Contract:**
   - Every directory under `skills/` MUST contain a `SKILL.md` starting with YAML frontmatter `---` with `name:` and `description:`.
   - Every CLI script in `skills/<name>/scripts/` MUST be accompanied by unit tests in `tests/test_<name>.py`.

3. **Catalog Synchronization:**
   Whenever a prompt or skill is added, renamed, or deleted, you MUST update:
   - `tests/test_integrity.py` (`EXPECTED_PROMPTS` and/or `EXPECTED_SKILLS`)
   - `install.sh` (`PROMPT_FILES` and/or `SKILL_NAMES` + slash command mapping)
   - `README.md` (tree, skills table, router, catalog)
   - `CHANGELOG.md` (release notes)

---

## 4. Code & Commit Conventions

- **Commit Format:** Conventional Commits (`feat(...)`, `fix(...)`, `docs(...)`, `chore(...)`, `test(...)`).
- **No Secrets:** Never commit real API keys, tokens, or private credentials. Use `gitleaks` patterns.
- **Artifact-First:** Avoid dumping massive markdown text into the chat; write outputs directly to files and summarize with links.
- **Anti-Glazing & Technical Rigor:** Maintain direct, objective, and evidence-grounded communications without sycophantic praise (*No Glazing*) and prioritize risk analysis (*Critique First*).
