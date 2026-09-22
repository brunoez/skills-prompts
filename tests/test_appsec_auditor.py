#!/usr/bin/env python3
"""
Unit tests for skills/appsec-auditor scripts:
- sarif_builder.py
- report_generator.py
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "skills" / "appsec-auditor" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from sarif_builder import (
    Finding,
    build_sarif,
    load_findings_from_dict,
)
from report_generator import (
    generate_markdown_report,
    generate_issue_template,
    sort_findings,
)


class TestSarifBuilder(unittest.TestCase):
    def setUp(self):
        self.sample_findings_data = [
            {
                "id": "SEC-001",
                "title": "BOLA in Invoice Retrieval Endpoint",
                "description": "Endpoint /api/invoices/:id queries DB by primary key without checking organizationId.",
                "severity": "CRITICAL",
                "file_path": "src/controllers/invoice.controller.ts",
                "start_line": 42,
                "end_line": 48,
                "owasp": "API1:2023",
                "asvs": "V13.1.1",
                "cwe": "CWE-639",
                "likelihood": "Alta",
                "impact": "Alto",
                "remediation": "Scope query to req.user.organizationId",
            },
            {
                "id": "SEC-002",
                "title": "Missing Rate Limiting on Login",
                "description": "Brute force attack possible on /api/auth/login.",
                "severity": "MEDIUM",
                "file_path": "src/routes/auth.ts",
                "start_line": 15,
                "owasp": "API4:2023",
                "asvs": "V13.1.5",
                "cwe": "CWE-770",
                "likelihood": "Alta",
                "impact": "Baixo",
                "remediation": "Add express-rate-limit middleware",
            },
        ]

    def test_load_findings_from_dict(self):
        findings = load_findings_from_dict(self.sample_findings_data)
        self.assertEqual(len(findings), 2)
        self.assertEqual(findings[0].id, "SEC-001")
        self.assertEqual(findings[0].severity, "CRITICAL")
        self.assertEqual(findings[0].start_line, 42)
        self.assertEqual(findings[0].end_line, 48)

    def test_build_sarif_structure(self):
        findings = load_findings_from_dict(self.sample_findings_data)
        sarif = build_sarif(findings, tool_name="Test Tool", tool_version="2.0.0")

        self.assertEqual(sarif["version"], "2.1.0")
        self.assertIn("$schema", sarif)
        self.assertEqual(len(sarif["runs"]), 1)

        run = sarif["runs"][0]
        self.assertEqual(run["tool"]["driver"]["name"], "Test Tool")
        self.assertEqual(run["tool"]["driver"]["version"], "2.0.0")

        # Check rules
        rules = run["tool"]["driver"]["rules"]
        self.assertEqual(len(rules), 2)
        rule_ids = [r["id"] for r in rules]
        self.assertIn("API1:2023", rule_ids)
        self.assertIn("API4:2023", rule_ids)

        # Check results
        results = run["results"]
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["level"], "error")  # CRITICAL -> error
        self.assertEqual(results[1]["level"], "warning")  # MEDIUM -> warning

        # Check location
        loc = results[0]["locations"][0]["physicalLocation"]
        self.assertEqual(loc["artifactLocation"]["uri"], "src/controllers/invoice.controller.ts")
        self.assertEqual(loc["region"]["startLine"], 42)
        self.assertEqual(loc["region"]["endLine"], 48)

    def test_build_sarif_empty(self):
        sarif = build_sarif([])
        self.assertEqual(len(sarif["runs"][0]["results"]), 0)
        self.assertEqual(len(sarif["runs"][0]["tool"]["driver"]["rules"]), 0)


class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        self.findings = [
            {
                "id": "SEC-002",
                "title": "Medium Issue",
                "severity": "MEDIUM",
                "file_path": "src/b.ts",
                "start_line": 10,
                "effort": "Médio",
            },
            {
                "id": "SEC-001",
                "title": "Critical Issue",
                "severity": "CRITICAL",
                "file_path": "src/a.ts",
                "start_line": 5,
                "effort": "Baixo",
                "quick_win": True,
            },
        ]

    def test_sort_findings(self):
        sorted_f = sort_findings(self.findings)
        self.assertEqual(sorted_f[0]["id"], "SEC-001")  # CRITICAL first
        self.assertEqual(sorted_f[1]["id"], "SEC-002")  # MEDIUM second

    def test_generate_markdown_report(self):
        md = generate_markdown_report(self.findings, title="Auditoria de Teste")
        self.assertIn("# 🛡️ Auditoria de Teste", md)
        self.assertIn("🔴 **CRÍTICA**", md)
        self.assertIn("🟡 **MÉDIA**", md)
        self.assertIn("SEC-001", md)
        self.assertIn("SEC-002", md)
        self.assertIn("✅", md)  # Quick win chip

    def test_generate_issue_template(self):
        tpl = generate_issue_template(self.findings[0])
        self.assertIn("Title: [SEC] Medium Issue (MEDIUM)", tpl)
        self.assertIn("src/b.ts:10", tpl)
        self.assertIn("Acceptance Criteria", tpl)


if __name__ == "__main__":
    unittest.main()
