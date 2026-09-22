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


if __name__ == "__main__":
    unittest.main()
