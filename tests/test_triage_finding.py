#!/usr/bin/env python3
"""
Unit tests for skills/triage-finding/scripts/triage_evaluator.py.
Validates static reachability analysis, verdicts (confirmed, not_actionable, needs_review),
and markdown reporting.
"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "skills" / "triage-finding" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from triage_evaluator import (
    evaluate_single_finding,
    format_markdown_triage,
    search_codebase_for_symbol,
)


class TestTriageFinding(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name)

        # Create sample codebase files
        src_dir = self.repo_root / "src"
        src_dir.mkdir(parents=True, exist_ok=True)

        # File importing 'pyyaml' and using 'load'
        (src_dir / "yaml_parser.py").write_text(
            "import pyyaml\n\ndef parse_data(raw):\n    return pyyaml.load(raw)\n",
            encoding="utf-8",
        )

        # File importing 'requests' but NOT calling 'post' or vulnerable methods
        (src_dir / "api_client.py").write_text(
            "import requests\n\ndef get_status():\n    return requests.get('/health')\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_missing_package_in_finding(self):
        finding = {
            "id": "ALERT-EMPTY",
        }
        res = evaluate_single_finding(finding, self.repo_root)
        self.assertEqual(res.verdict, "needs_review")
        self.assertEqual(res.confidence, "LOW")
        self.assertIn("does not specify package", res.evidence)

    def test_package_not_imported_is_not_actionable(self):
        finding = {
            "id": "GHSA-UNUSED",
            "package": "lodash",
            "vulnerable_symbol": "template",
        }
        res = evaluate_single_finding(finding, self.repo_root)
        self.assertEqual(res.verdict, "not_actionable")
        self.assertEqual(res.confidence, "HIGH")
        self.assertIn("not imported", res.evidence)

    def test_package_imported_but_symbol_unused_is_not_actionable(self):
        finding = {
            "id": "GHSA-REQUESTS-UNUSED-SYM",
            "package": "requests",
            "vulnerable_symbol": "post",
        }
        res = evaluate_single_finding(finding, self.repo_root)
        self.assertEqual(res.verdict, "not_actionable")
        self.assertEqual(res.confidence, "MEDIUM")
        self.assertIn("is never invoked", res.evidence)

    def test_package_and_symbol_used_is_confirmed(self):
        finding = {
            "id": "GHSA-PYYAML-LOAD",
            "package": "pyyaml",
            "vulnerable_symbol": "load",
        }
        res = evaluate_single_finding(finding, self.repo_root)
        self.assertEqual(res.verdict, "confirmed")
        self.assertEqual(res.confidence, "HIGH")
        self.assertIn("imported and called", res.evidence)

    def test_package_imported_without_symbol_needs_review(self):
        finding = {
            "id": "CVE-GENERIC-REQUESTS",
            "package": "requests",
        }
        res = evaluate_single_finding(finding, self.repo_root)
        self.assertEqual(res.verdict, "needs_review")
        self.assertEqual(res.confidence, "MEDIUM")
        self.assertIn("does not name a specific vulnerable function", res.evidence)

    def test_format_markdown_triage(self):
        findings = [
            {"id": "ALERT-1", "package": "pyyaml", "vulnerable_symbol": "load"},
            {"id": "ALERT-2", "package": "lodash", "vulnerable_symbol": "template"},
            {"id": "ALERT-3", "package": "requests"},
        ]
        results = [evaluate_single_finding(f, self.repo_root) for f in findings]
        md = format_markdown_triage(results)

        self.assertIn("# 📋 Relatório de Triagem Estática de Alertas", md)
        self.assertIn("🔴 1 Confirmados", md)
        self.assertIn("🟢 1 Descartáveis", md)
        self.assertIn("🟡 1 Em Revisão", md)
        self.assertIn("ALERT-1", md)
        self.assertIn("ALERT-2", md)
        self.assertIn("ALERT-3", md)


if __name__ == "__main__":
    unittest.main()
