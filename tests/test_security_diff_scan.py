#!/usr/bin/env python3
"""
Unit tests for skills/security-diff-scan/scripts/diff_scanner.py.
Validates diff parsing, security rule detection, SARIF export, and markdown formatting.
"""

import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "skills" / "security-diff-scan" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from diff_scanner import (
    DiffFinding,
    build_sarif_report,
    format_markdown_report,
    parse_diff_content,
    scan_diff_files,
)


class TestSecurityDiffScanner(unittest.TestCase):
    def setUp(self):
        self.vulnerable_diff = """diff --git a/src/api/users.ts b/src/api/users.ts
index 1234567..89abcdef 100644
--- a/src/api/users.ts
+++ b/src/api/users.ts
@@ -10,6 +10,12 @@ export class UserController {
+  async getReport(req: Request, res: Response) {
+    const token = "TESTING_DUMMY_SECRET_KEY_123456789";
+    const userId = req.query.id;
+    const data = await db.$queryRawUnsafe(`SELECT * FROM users WHERE id = '${userId}'`);
+    return res.json(data);
+  }
 }
"""
        self.clean_diff = """diff --git a/src/api/users.ts b/src/api/users.ts
index 1234567..89abcdef 100644
--- a/src/api/users.ts
+++ b/src/api/users.ts
@@ -10,6 +10,12 @@ export class UserController {
+  async getReport(req: Request, res: Response) {
+    const token = process.env.API_KEY;
+    const userId = req.user.id;
+    const data = await db.user.findFirst({ where: { id: userId, tenantId: req.user.tenantId } });
+    return res.json(data);
+  }
 }
"""

    def test_parse_diff_content(self):
        parsed = parse_diff_content(self.vulnerable_diff)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["new_path"], "src/api/users.ts")
        self.assertEqual(len(parsed[0]["added_lines"]), 6)

    def test_scan_diff_detects_vulnerabilities(self):
        parsed = parse_diff_content(self.vulnerable_diff)
        findings = scan_diff_files(parsed)

        self.assertGreaterEqual(len(findings), 2)
        rule_ids = [f.rule_id for f in findings]
        self.assertIn("SEC-DIFF-001", rule_ids)  # Hardcoded secret
        self.assertIn("SEC-DIFF-003", rule_ids)  # Raw SQL

    def test_scan_diff_on_clean_diff(self):
        parsed = parse_diff_content(self.clean_diff)
        findings = scan_diff_files(parsed)
        self.assertEqual(len(findings), 0)

    def test_sarif_export(self):
        parsed = parse_diff_content(self.vulnerable_diff)
        findings = scan_diff_files(parsed)
        sarif = build_sarif_report(findings)

        self.assertEqual(sarif["version"], "2.1.0")
        self.assertIn("runs", sarif)
        self.assertEqual(len(sarif["runs"]), 1)
        self.assertGreaterEqual(len(sarif["runs"][0]["results"]), 2)

    def test_markdown_report_formatting(self):
        parsed = parse_diff_content(self.vulnerable_diff)
        findings = scan_diff_files(parsed)
        md = format_markdown_report(findings, len(parsed))

        self.assertIn("Security Diff Scan", md)
        self.assertIn("BLOQUEADO", md)
        self.assertIn("SEC-DIFF-001", md)


if __name__ == "__main__":
    unittest.main()
