#!/usr/bin/env python3
"""
Goldfish Reviewer CLI - EGM Spec Stress-Testing Validator
Audits design documents and implementation plans against the Zero-Decision Rule,
Heilmeier criteria, Semantic Split, and Anti-Glazing standards.
"""

import argparse
import json
import re
import sys
from pathlib import Path

BANNED_ADJECTIVES = [
    r"\bseamless\b",
    r"\bseamlessly\b",
    r"\bblazingly\s+fast\b",
    r"\beffortless\b",
    r"\beffortlessly\b",
    r"\brobusto\s+e\s+elegante\b",
    r"\brevolucion[aá]rio\b",
    r"\bperfeito\b",
]

UNDECIDED_MARKERS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"\bFIXME\b",
    r"\ba\s+definir\b",
    r"\ba\s+escolher\b",
    r"\bdecidir\s+depois\b",
    r"\bdecidir\s+posteriormente\b",
    r"\bescolher\s+biblioteca\b",
    r"\bdefinir\s+depois\b",
]

HEILMEIER_KEYWORDS = {
    "objectives": [r"objetivo", r"objective", r"meta", r"goal"],
    "current_state": [r"hoje", r"today", r"estado\s+da\s+arte", r"state\s+of\s+the\s+art", r"limita[çc]"],
    "risks": [r"risco", r"risk", r"trade-off", r"tradeoff", r"falha"],
    "metrics_or_tests": [r"m[eé]trica", r"metric", r"teste", r"test", r"crit[eé]rio", r"exam"],
}


def audit_document(file_path: Path) -> dict:
    if not file_path.is_file():
        return {
            "status": "ERROR",
            "file": str(file_path),
            "errors": [f"File not found: {file_path}"],
            "findings": [],
            "score": 0,
            "passed": False,
        }

    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    findings = []
    errors = []

    # 1. Anti-Glazing / Banned Adjectives Check
    glazing_hits = []
    for line_idx, line in enumerate(lines, start=1):
        for pattern in BANNED_ADJECTIVES:
            if re.search(pattern, line, re.IGNORECASE):
                glazing_hits.append({"line": line_idx, "snippet": line.strip()})
                findings.append({
                    "category": "Anti-Glazing",
                    "severity": "LOW",
                    "line": line_idx,
                    "message": f"Promotional or unsubstantiated phrasing detected: '{line.strip()}'",
                })

    # 2. Semantic Split Check (High-Level vs Implementation Plan)
    has_high_level = bool(re.search(r"##\s+(Arquitetura|Vis[aã]o|Overview|Design|Objetivo|Contexto)", content, re.IGNORECASE))
    has_plan = bool(re.search(r"##\s+(Implementa[çc][aã]o|Plano|Tasks|Passo\s+a\s+Passo|Execu[çc][aã]o|Fases)", content, re.IGNORECASE))

    if not (has_high_level and has_plan):
        findings.append({
            "category": "Semantic Split",
            "severity": "HIGH",
            "line": 1,
            "message": "Missing explicit Semantic Split: document must contain both High-Level Architecture and Detailed Implementation Plan sections.",
        })

    # 3. Zero-Decision Rule Check
    # Look for undecided markers in the implementation plan
    open_decisions = []
    for line_idx, line in enumerate(lines, start=1):
        for pattern in UNDECIDED_MARKERS:
            if re.search(pattern, line, re.IGNORECASE):
                open_decisions.append({"line": line_idx, "snippet": line.strip()})
                findings.append({
                    "category": "Zero-Decision Rule",
                    "severity": "CRITICAL",
                    "line": line_idx,
                    "message": f"Open design decision left to implementer: '{line.strip()}'",
                })

    # Check for target files / paths mentioned
    has_file_references = bool(re.search(r"`[a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+`", content))
    if not has_file_references and has_plan:
        findings.append({
            "category": "Zero-Decision Rule",
            "severity": "HIGH",
            "line": 1,
            "message": "Implementation plan does not specify concrete target file paths to create/modify.",
        })

    # 4. Heilmeier Catechism Checks
    missing_heilmeier = []
    for aspect, patterns in HEILMEIER_KEYWORDS.items():
        matched = any(re.search(p, content, re.IGNORECASE) for p in patterns)
        if not matched:
            missing_heilmeier.append(aspect)
            findings.append({
                "category": "Heilmeier Catechism",
                "severity": "MEDIUM",
                "line": 1,
                "message": f"Document does not clearly address Heilmeier criterion: '{aspect}'.",
            })

    # Calculate overall score and readiness
    critical_count = sum(1 for f in findings if f["severity"] == "CRITICAL")
    high_count = sum(1 for f in findings if f["severity"] == "HIGH")
    medium_count = sum(1 for f in findings if f["severity"] == "MEDIUM")
    low_count = sum(1 for f in findings if f["severity"] == "LOW")

    deductions = (critical_count * 30) + (high_count * 15) + (medium_count * 5) + (low_count * 2)
    score = max(0, 100 - deductions)
    passed = critical_count == 0 and high_count == 0 and score >= 70

    return {
        "status": "PASS" if passed else "FAIL",
        "file": str(file_path),
        "score": score,
        "passed": passed,
        "summary": {
            "critical": critical_count,
            "high": high_count,
            "medium": medium_count,
            "low": low_count,
            "total_findings": len(findings),
        },
        "findings": findings,
    }


def main():
    parser = argparse.ArgumentParser(description="Goldfish Reviewer CLI - EGM Spec Stress-Testing Validator")
    parser.add_argument("file", help="Path to specification Markdown file")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    target_path = Path(args.file)
    result = audit_document(target_path)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("\n" + "=" * 70)
        print("  🐡 GOLDFISH REVIEWER - EGM SPEC STRESS-TEST REPORT")
        print("=" * 70)
        print(f"Target File: {result['file']}")
        print(f"Status:      {'🟢 PASSED' if result['passed'] else '🔴 FAILED'}")
        print(f"Score:       {result['score']}/100")
        print(f"Findings:    {result['summary']['critical']} Critical | {result['summary']['high']} High | {result['summary']['medium']} Medium | {result['summary']['low']} Low")
        print("-" * 70)

        if not result["findings"]:
            print("✨ No violations detected. Document complies with Goldfish & Zero-Decision standards.")
        else:
            for idx, finding in enumerate(result["findings"], start=1):
                sev_icon = "🔴" if finding["severity"] == "CRITICAL" else ("🟠" if finding["severity"] == "HIGH" else "🟡")
                print(f"{idx}. {sev_icon} [{finding['severity']}] {finding['category']} (L{finding['line']})")
                print(f"   {finding['message']}")

        print("=" * 70 + "\n")

    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
