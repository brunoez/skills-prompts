#!/usr/bin/env python3
"""
Unit tests for skills/driven-development scripts:
- test_runner.py
"""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "skills" / "driven-development" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from test_runner import (
    detect_test_framework,
    parse_test_summary,
    run_tests,
)


class TestDrivenDevelopmentRunner(unittest.TestCase):
    @patch("shutil.which")
    def test_detect_test_framework_pytest(self, mock_which):
        mock_which.side_effect = lambda binary: "/usr/bin/pytest" if binary == "pytest" else None
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / "pytest.ini").touch()
            framework, cmd = detect_test_framework(tmp_path)
            self.assertIn("pytest", framework)
            self.assertIn("pytest", cmd)

    @patch("shutil.which")
    def test_detect_test_framework_python_unittest_fallback(self, mock_which):
        mock_which.return_value = None
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / "tests").mkdir()
            framework, cmd = detect_test_framework(tmp_path)
            self.assertIn("unittest", framework)
            self.assertIn("unittest", cmd)

    @patch("shutil.which")
    def test_detect_test_framework_node(self, mock_which):
        mock_which.side_effect = lambda binary: "/usr/bin/npm" if binary == "npm" else None
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            pkg_json = tmp_path / "package.json"
            pkg_json.write_text('{"scripts": {"test": "vitest"}}', encoding="utf-8")
            framework, cmd = detect_test_framework(tmp_path)
            self.assertIn("node", framework)
            self.assertEqual(cmd, ["npm", "test"])

    def test_parse_pytest_summary(self):
        mock_stdout = "================== 12 passed, 2 failed in 0.45s =================="
        summary = parse_test_summary(mock_stdout, "", "python (pytest)")
        self.assertEqual(summary["passed"], 12)
        self.assertEqual(summary["failed"], 2)
        self.assertEqual(summary["total"], 14)
        self.assertEqual(summary["status"], "FAILED")

    def test_parse_unittest_summary_success(self):
        mock_stdout = "Ran 8 tests in 0.002s\n\nOK"
        summary = parse_test_summary(mock_stdout, "", "python (unittest)")
        self.assertEqual(summary["passed"], 8)
        self.assertEqual(summary["failed"], 0)
        self.assertEqual(summary["total"], 8)
        self.assertEqual(summary["status"], "PASSED")

    def test_parse_vitest_summary(self):
        mock_stdout = "Tests:       1 failed, 9 passed, 10 total"
        summary = parse_test_summary(mock_stdout, "", "node (npm)")
        self.assertEqual(summary["passed"], 9)
        self.assertEqual(summary["failed"], 1)
        self.assertEqual(summary["total"], 10)
        self.assertEqual(summary["status"], "FAILED")

    def test_typedd_example_invariants(self):
        typedd_example = ROOT_DIR / "skills" / "driven-development" / "examples" / "typedd-state-machine.ts"
        self.assertTrue(typedd_example.is_file(), "typedd-state-machine.ts deve existir")
        content = typedd_example.read_text(encoding="utf-8")
        self.assertIn("Brand<string, 'OrderId'>", content)
        self.assertIn("type OrderState =", content)
        self.assertIn("function assertNever", content)
        self.assertIn("parsePositiveCents", content)

    def test_datadd_example_esr_rules(self):
        datadd_example = ROOT_DIR / "skills" / "driven-development" / "examples" / "datadd-access-patterns.sql"
        self.assertTrue(datadd_example.is_file(), "datadd-access-patterns.sql deve existir")
        content = datadd_example.read_text(encoding="utf-8")
        self.assertIn("ACCESS PATTERNS MATRIX", content)
        self.assertIn("Rule ESR", content)
        self.assertIn("INCLUDE", content)
        self.assertIn("version INT NOT NULL DEFAULT 1", content)

    def test_driven_references_complete(self):
        ref_dir = ROOT_DIR / "skills" / "driven-development" / "references"
        expected_refs = [
            "ddd-domain-driven.md",
            "typedd-type-driven.md",
            "datadd-data-driven.md",
            "driven-pipeline-matrix.md",
            "sdd-spec-driven.md",
            "cdd-contract-testing.md",
            "bdd-gherkin-scenarios.md",
            "secdd-abuse-cases.md",
            "tdd-red-green-refactor.md",
            "test-pyramid-strategy.md",
        ]
        for ref in expected_refs:
            ref_path = ref_dir / ref
            self.assertTrue(ref_path.is_file(), f"Referência {ref} deve existir em {ref_dir}")
            text = ref_path.read_text(encoding="utf-8")
            self.assertGreater(len(text), 100, f"Referência {ref} não deve estar vazia")


if __name__ == "__main__":
    unittest.main()
