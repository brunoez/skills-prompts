#!/usr/bin/env python3
"""
Unit tests for skills/agent-harness-optimizer/scripts/audit_harness.py.
Validates the 8 components check, trigger lines, script presence, and token economics.
"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "skills" / "agent-harness-optimizer" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from audit_harness import audit_harness


class TestAgentHarnessOptimizer(unittest.TestCase):
    def test_compliant_harness_passes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            # Create always-on file with trigger
            agents_md = tmppath / "AGENTS.md"
            agents_md.write_text("# AGENTS.md\n\nWhen optimizing, use `test-skill`.", encoding="utf-8")

            # Create skill
            sdir = tmppath / "skills" / "test-skill"
            sdir.mkdir(parents=True)
            (sdir / "SKILL.md").write_text("---\nname: test-skill\ndescription: Test\n---\nBody", encoding="utf-8")

            res = audit_harness(tmppath)
            self.assertTrue(res["passed"])
            self.assertEqual(res["status"], "PASS")
            self.assertEqual(res["summary"]["critical"], 0)
            self.assertEqual(res["summary"]["high"], 0)

    def test_untriggered_skill_flagged(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            # Create always-on file without trigger
            agents_md = tmppath / "AGENTS.md"
            agents_md.write_text("# AGENTS.md\nNo skills mentioned.", encoding="utf-8")

            # Create skill
            sdir = tmppath / "skills" / "orphan-skill"
            sdir.mkdir(parents=True)
            (sdir / "SKILL.md").write_text("---\nname: orphan-skill\ndescription: Orphan\n---\nBody", encoding="utf-8")

            res = audit_harness(tmppath)
            self.assertFalse(res["passed"])
            high_findings = [f for f in res["findings"] if f["severity"] == "HIGH"]
            self.assertTrue(any("never referenced" in f["message"] for f in high_findings))

    def test_missing_script_flagged_as_critical(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            agents_md = tmppath / "AGENTS.md"
            agents_md.write_text("# AGENTS.md\nUse `broken-skill`.", encoding="utf-8")

            sdir = tmppath / "skills" / "broken-skill"
            sdir.mkdir(parents=True)
            (sdir / "SKILL.md").write_text("---\nname: broken-skill\ndescription: Broken\n---\nRun `scripts/missing.py`", encoding="utf-8")

            res = audit_harness(tmppath)
            self.assertFalse(res["passed"])
            crit_findings = [f for f in res["findings"] if f["severity"] == "CRITICAL"]
            self.assertTrue(any("references script 'missing.py'" in f["message"] for f in crit_findings))


if __name__ == "__main__":
    unittest.main()
