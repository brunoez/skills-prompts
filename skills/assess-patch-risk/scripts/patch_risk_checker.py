#!/usr/bin/env python3
"""
Patch Risk Checker CLI
Evaluates immutable patch artifacts for regression risk, breaking changes, and auto-merge eligibility.
Inspired by OpenAI Codex Security (assess-patch-risk) & Google SRE principles.
"""

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional


@dataclass
class PatchRiskAssessment:
    recommendation: str  # merge, revise, block, hold
    workflow_label: str  # auto_merge_candidate, human_review_required, revise, block, hold_for_evidence
    contract_risk: str  # LOW, MEDIUM, HIGH
    regression_risk: str  # LOW, MEDIUM, HIGH
    has_test_coverage: bool
    affects_database_schema: bool
    affects_auth_or_billing: bool
    files_analyzed: List[str]
    reasons: List[str]
    remediation_advice: Optional[str] = None


SCHEMA_INDICATORS = [
    r"schema\.prisma$",
    r"migrations?/",
    r"\.sql$",
    r"alembic/",
    r"models?\.py$",
    r"entities?/",
]

SENSITIVE_DOMAIN_INDICATORS = [
    r"auth",
    r"login",
    r"jwt",
    r"session",
    r"billing",
    r"payment",
    r"checkout",
    r"crypto",
    r"secret",
]

TEST_INDICATORS = [
    r"tests?/",
    r"__tests__/",
    r"\.test\.[a-z]+$",
    r"\.spec\.[a-z]+$",
    r"test_[a-z0-9_]+\.py$",
]


def extract_files_from_diff(diff_content: str) -> List[Dict[str, Any]]:
    """
    Extracts affected file paths and change stats from unified diff.
    """
    file_records = []
    current_file = None
    file_header_re = re.compile(r"^diff --git a/(.*) b/(.*)")

    for line in diff_content.splitlines():
        match = file_header_re.match(line)
        if match:
            if current_file:
                file_records.append(current_file)
            current_file = {
                "old_path": match.group(1),
                "new_path": match.group(2),
                "added_lines": 0,
                "deleted_lines": 0,
            }
            continue

        if current_file:
            if line.startswith("+") and not line.startswith("+++"):
                current_file["added_lines"] += 1
            elif line.startswith("-") and not line.startswith("---"):
                current_file["deleted_lines"] += 1

    if current_file:
        file_records.append(current_file)

    return file_records


def evaluate_patch_risk(diff_content: str) -> PatchRiskAssessment:
    """
    Evaluates patch content against the strict auto-merge rubric.
    """
    files = extract_files_from_diff(diff_content)
    file_paths = [f["new_path"] for f in files]

    reasons: List[str] = []
    affects_schema = False
    affects_sensitive = False
    has_tests = False

    # 1. Inspect file paths
    for path in file_paths:
        for pat in SCHEMA_INDICATORS:
            if re.search(pat, path, re.IGNORECASE):
                affects_schema = True
                reasons.append(f"Modifies database schema/persistence: `{path}`")
                break

        for pat in SENSITIVE_DOMAIN_INDICATORS:
            if re.search(pat, path, re.IGNORECASE):
                affects_sensitive = True
                reasons.append(f"Touches sensitive security/business boundary: `{path}`")
                break

        for pat in TEST_INDICATORS:
            if re.search(pat, path, re.IGNORECASE):
                has_tests = True
                break

    # 2. Check for breaking deletions or dangerous anti-patterns in diff text
    has_severe_deletions = bool(re.search(r"^-\s*(app\.use\(cors|@UseGuards|authMiddleware|tenant_id)", diff_content, re.MULTILINE))
    has_syntax_or_merge_conflicts = bool(re.search(r"^(<{7}|={7}|>{7})", diff_content, re.MULTILINE))

    if has_syntax_or_merge_conflicts:
        return PatchRiskAssessment(
            recommendation="block",
            workflow_label="block",
            contract_risk="HIGH",
            regression_risk="HIGH",
            has_test_coverage=has_tests,
            affects_database_schema=affects_schema,
            affects_auth_or_billing=affects_sensitive,
            files_analyzed=file_paths,
            reasons=["Patch contains raw unresolved Git merge conflicts"],
            remediation_advice="Resolve merge conflicts before evaluating the patch.",
        )

    if has_severe_deletions:
        return PatchRiskAssessment(
            recommendation="block",
            workflow_label="block",
            contract_risk="HIGH",
            regression_risk="HIGH",
            has_test_coverage=has_tests,
            affects_database_schema=affects_schema,
            affects_auth_or_billing=affects_sensitive,
            files_analyzed=file_paths,
            reasons=["Patch removes critical authentication or tenancy guardrails"],
            remediation_advice="Restore required security guards before attempting to merge.",
        )

    # 3. Decision Matrix
    if affects_schema:
        return PatchRiskAssessment(
            recommendation="merge",
            workflow_label="human_review_required",
            contract_risk="HIGH",
            regression_risk="MEDIUM",
            has_test_coverage=has_tests,
            affects_database_schema=True,
            affects_auth_or_billing=affects_sensitive,
            files_analyzed=file_paths,
            reasons=reasons or ["Database migrations require coordinated rollout and human verification."],
            remediation_advice="Human review required for database migrations and schema changes.",
        )

    if affects_sensitive:
        return PatchRiskAssessment(
            recommendation="merge",
            workflow_label="human_review_required",
            contract_risk="MEDIUM",
            regression_risk="MEDIUM",
            has_test_coverage=has_tests,
            affects_database_schema=False,
            affects_auth_or_billing=True,
            files_analyzed=file_paths,
            reasons=reasons,
            remediation_advice="Authentication, payment, or cryptography changes require explicit peer signoff.",
        )

    if not has_tests:
        return PatchRiskAssessment(
            recommendation="revise",
            workflow_label="revise",
            contract_risk="LOW",
            regression_risk="MEDIUM",
            has_test_coverage=False,
            affects_database_schema=False,
            affects_auth_or_billing=False,
            files_analyzed=file_paths,
            reasons=["Patch does not bundle automated tests verifying the fix or change."],
            remediation_advice="Add unit or integration tests to prove correctness and protect against regressions.",
        )

    # Strict auto-merge candidate criteria passed
    return PatchRiskAssessment(
        recommendation="merge",
        workflow_label="auto_merge_candidate",
        contract_risk="LOW",
        regression_risk="LOW",
        has_test_coverage=True,
        affects_database_schema=False,
        affects_auth_or_billing=False,
        files_analyzed=file_paths,
        reasons=["All strict gates passed: Zero schema changes, non-sensitive scope, bundled regression tests."],
        remediation_advice="Eligible for automated merge upon passing CI build.",
    )


def format_markdown_report(assessment: PatchRiskAssessment) -> str:
    """
    Formats the evaluation into a clean Markdown gatekeeper report.
    """
    status_icon = "🟢" if assessment.workflow_label == "auto_merge_candidate" else "🟡" if assessment.workflow_label == "human_review_required" else "🔴"
    
    lines = [
        f"# ⚖️ Parecer de Risco de Patch: {status_icon} `{assessment.workflow_label.upper()}`",
        "",
        f"**Decisão Formal:** `{assessment.recommendation.upper()}`  ",
        f"**Workflow Label:** `{assessment.workflow_label}`  ",
        f"**Risco em Contratos:** `{assessment.contract_risk}` | **Risco de Regressão:** `{assessment.regression_risk}`  ",
        f"**Cobertura de Testes no Patch:** `{'SIM' if assessment.has_test_coverage else 'NÃO'}`  ",
        "",
        "---",
        "",
        "## 🔍 Justificativa da Avaliação",
        "",
    ]

    for r in assessment.reasons:
        lines.append(f"- {r}")

    lines.extend([
        "",
        "## 📂 Arquivos Afetados no Patch",
        "",
    ])

    for f in assessment.files_analyzed:
        lines.append(f"- `{f}`")

    if assessment.remediation_advice:
        lines.extend([
            "",
            "---",
            "",
            f"> 💡 **Orientação do Gatekeeper:** {assessment.remediation_advice}",
        ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Patch Risk Checker CLI for Auto-Merge Verification")
    parser.add_argument("--patch", required=True, help="Path to unified .patch or .diff file")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text", help="Output format")
    parser.add_argument("--output", help="Save report to file")

    args = parser.parse_args()

    if not os.path.isfile(args.patch):
        print(f"Error: Patch file not found: {args.patch}", file=sys.stderr)
        sys.exit(1)

    with open(args.patch, "r", encoding="utf-8") as f:
        diff_text = f.read()

    assessment = evaluate_patch_risk(diff_text)

    if args.format == "json":
        output_str = json.dumps(asdict(assessment), indent=2)
    elif args.format == "markdown":
        output_str = format_markdown_report(assessment)
    else:
        output_str = f"Recommendation: {assessment.recommendation.upper()}\nWorkflow Label: {assessment.workflow_label}\nContract Risk: {assessment.contract_risk}\nRegression Risk: {assessment.regression_risk}\nHas Tests: {assessment.has_test_coverage}\nReasons:\n" + "\n".join(f"  - {r}" for r in assessment.reasons)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_str)
        print(f"✅ Parecer salvo em: {args.output}", file=sys.stderr)
    else:
        print(output_str)

    if assessment.workflow_label in ["block", "revise"]:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
