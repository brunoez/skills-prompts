#!/usr/bin/env python3
"""
Unit tests for skills/agents-md-generator/scripts/validate_agents_md.py.
Validates structure checks, single-test detection, unwarned build command detection, and conciseness.
"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "skills" / "agents-md-generator" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from validate_agents_md import audit_agents_md


class TestAgentsMdGenerator(unittest.TestCase):
    def test_compliant_agents_md_passes(self):
        doc = """# AGENTS Guidelines

## Dev environment tips
- Run `pnpm dev` to start the local dev server.
- Do NOT run `pnpm build` during interactive agent sessions.

## Testing instructions
- Full suite: `pnpm test`.
- Single test: `pnpm vitest run -t "<name>"`.

## Coding conventions
- Use TypeScript with strict: true.
- Validate inputs with Zod.

## PR and Git instructions
- Follow Conventional Commits (`feat:`, `fix:`).
"""
        with tempfile.NamedTemporaryFile("w+", suffix=".md", encoding="utf-8") as f:
            f.write(doc)
            f.flush()
            res = audit_agents_md(Path(f.name))
            self.assertTrue(res["passed"])
            self.assertEqual(res["status"], "PASS")
            self.assertEqual(res["score"], 100)

    def test_missing_sections_flagged(self):
        doc = """# Incomplete AGENTS.md
Only has text without standard headings.
"""
        with tempfile.NamedTemporaryFile("w+", suffix=".md", encoding="utf-8") as f:
            f.write(doc)
            f.flush()
            res = audit_agents_md(Path(f.name))
            self.assertFalse(res["passed"])
            self.assertEqual(res["status"], "FAIL")
            self.assertGreater(res["summary"]["high"], 0)

    def test_unwarned_production_build_flagged(self):
        doc = """# AGENTS.md

## Dev environment
- Run `npm run build` to compile the app.

## Testing instructions
- `npm test -k single`

## Coding conventions
- TypeScript only.

## PR instructions
- Open PR to main.
"""
        with tempfile.NamedTemporaryFile("w+", suffix=".md", encoding="utf-8") as f:
            f.write(doc)
            f.flush()
            res = audit_agents_md(Path(f.name))
            hmr_findings = [f for f in res["findings"] if f["category"] == "HMR Protection"]
            self.assertGreater(len(hmr_findings), 0)


if __name__ == "__main__":
    unittest.main()
