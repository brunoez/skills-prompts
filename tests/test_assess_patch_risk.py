#!/usr/bin/env python3
"""
Unit tests for skills/assess-patch-risk/scripts/patch_risk_checker.py.
Validates auto-merge candidate criteria, human review triggers, and rubric evaluation.
"""

import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "skills" / "assess-patch-risk" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from patch_risk_checker import evaluate_patch_risk


class TestAssessPatchRisk(unittest.TestCase):
    def test_auto_merge_candidate_with_tests(self):
        diff = """diff --git a/src/utils/math.ts b/src/utils/math.ts
--- a/src/utils/math.ts
+++ b/src/utils/math.ts
@@ -1,2 +1,3 @@
+export function helper() {}
diff --git a/tests/test_math.ts b/tests/test_math.ts
--- a/tests/test_math.ts
+++ b/tests/test_math.ts
@@ -1,2 +1,3 @@
+test("helper", () => {});
"""
        assessment = evaluate_patch_risk(diff)
        self.assertEqual(assessment.recommendation, "merge")
        self.assertEqual(assessment.workflow_label, "auto_merge_candidate")
        self.assertTrue(assessment.has_test_coverage)

    def test_schema_triggers_human_review(self):
        diff = """diff --git a/prisma/schema.prisma b/prisma/schema.prisma
--- a/prisma/schema.prisma
+++ b/prisma/schema.prisma
@@ -1,2 +1,3 @@
+field String
"""
        assessment = evaluate_patch_risk(diff)
        self.assertEqual(assessment.recommendation, "merge")
        self.assertEqual(assessment.workflow_label, "human_review_required")
        self.assertTrue(assessment.affects_database_schema)

    def test_sensitive_auth_triggers_human_review(self):
        diff = """diff --git a/src/services/auth_token.ts b/src/services/auth_token.ts
--- a/src/services/auth_token.ts
+++ b/src/services/auth_token.ts
@@ -1,2 +1,3 @@
+export function sign() {}
"""
        assessment = evaluate_patch_risk(diff)
        self.assertEqual(assessment.workflow_label, "human_review_required")
        self.assertTrue(assessment.affects_auth_or_billing)

    def test_missing_tests_triggers_revise(self):
        diff = """diff --git a/src/utils/format.ts b/src/utils/format.ts
--- a/src/utils/format.ts
+++ b/src/utils/format.ts
@@ -1,2 +1,3 @@
+export function format() {}
"""
        assessment = evaluate_patch_risk(diff)
        self.assertEqual(assessment.recommendation, "revise")
        self.assertEqual(assessment.workflow_label, "revise")
        self.assertFalse(assessment.has_test_coverage)

    def test_removing_guards_triggers_block(self):
        diff = """diff --git a/src/controllers/user.ts b/src/controllers/user.ts
--- a/src/controllers/user.ts
+++ b/src/controllers/user.ts
@@ -1,3 +1,2 @@
-@UseGuards(AuthGuard)
 export class UserController {}
"""
        assessment = evaluate_patch_risk(diff)
        self.assertEqual(assessment.recommendation, "block")
        self.assertEqual(assessment.workflow_label, "block")


if __name__ == "__main__":
    unittest.main()
