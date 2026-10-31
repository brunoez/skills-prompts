#!/usr/bin/env python3
"""
AGENTS.md Validator CLI
Validates AGENTS.md files against the Linux Foundation agents.md specification.
Checks for required sections, anti-patterns, filtered test commands, and conciseness.
"""

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    ("dev_environment", r"##\s+.*(dev|ambiente|environment|setup|comandos|commands)", "Dev environment tips or commands section"),
    ("testing", r"##\s+.*(test|teste|verifi)", "Testing instructions section"),
    ("conventions", r"##\s+.*(convention|conven[çc][aã]o|style|padr[aã]o|guideline|regra)", "Coding conventions or style guidelines section"),
    ("git_or_pr", r"##\s+.*(pr|pull\s+request|git|commit|workflow)", "PR or commit instructions section"),
]

SINGLE_TEST_PATTERNS = [
    r"-t\s+",
    r"-k\s+",
    r"--testNamePattern",
    r"--filter",
    r"vitest\s+run\s+",
    r"pytest\s+[a-zA-Z0-9_\-/\\]+\.py",
    r"go\s+test\s+-run\s+",
    r"cargo\s+test\s+[a-zA-Z0-9_]+",
]

BUILD_WITHOUT_WARNING = [
    r"(npm|pnpm|yarn|bun)\s+(run\s+)?build\b(?!.*(do\s+not|não\s+execute|avoid|evite|outside))",
]


def audit_agents_md(file_path: Path) -> dict:
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

    # 1. Check Required Sections
    for section_id, pattern, desc in REQUIRED_SECTIONS:
        if not re.search(pattern, content, re.IGNORECASE):
            findings.append({
                "category": "Structure",
                "severity": "HIGH",
                "line": 1,
                "message": f"Missing recommended section: {desc}.",
            })

    # 2. Check for Single Test Instructions
    has_single_test = any(re.search(p, content) for p in SINGLE_TEST_PATTERNS)
    if not has_single_test:
        findings.append({
            "category": "Testing Efficiency",
            "severity": "MEDIUM",
            "line": 1,
            "message": "Missing command for running a single isolated test (e.g., vitest -t, pytest -k, or file path).",
        })

    # 3. Check for Anti-Pattern: Unwarned Production Build Command
    for idx, line in enumerate(lines, start=1):
        if re.search(r"\b(npm|pnpm|yarn|bun)\s+(run\s+)?build\b", line, re.IGNORECASE):
            # Check if this line or the immediate context mentions not running it or warning
            context = " ".join(lines[max(0, idx - 2):min(len(lines), idx + 2)]).lower()
            if not any(w in context for w in ["do not", "don't", "não execute", "avoid", "evite", "outside", "interactiv"]):
                findings.append({
                    "category": "HMR Protection",
                    "severity": "MEDIUM",
                    "line": idx,
                    "message": f"Line {idx} mentions a production build command without explicitly warning the agent against running it during interactive sessions.",
                })

    # 4. Conciseness check
    if len(lines) > 300:
        findings.append({
            "category": "Conciseness",
            "severity": "LOW",
            "line": 1,
            "message": f"AGENTS.md is lengthy ({len(lines)} lines). Consider breaking details into nested AGENTS.md or reference documents.",
        })

    # Scoring
    high_count = sum(1 for f in findings if f["severity"] == "HIGH")
    med_count = sum(1 for f in findings if f["severity"] == "MEDIUM")
    low_count = sum(1 for f in findings if f["severity"] == "LOW")

    deductions = (high_count * 25) + (med_count * 10) + (low_count * 5)
    score = max(0, 100 - deductions)
    passed = high_count == 0 and score >= 70

    return {
        "status": "PASS" if passed else "FAIL",
        "file": str(file_path),
        "score": score,
        "passed": passed,
        "summary": {
            "high": high_count,
            "medium": med_count,
            "low": low_count,
            "total_findings": len(findings),
        },
        "findings": findings,
    }


def main():
    parser = argparse.ArgumentParser(description="AGENTS.md Validator CLI (Linux Foundation agents.md spec)")
    parser.add_argument("file", nargs="?", default="AGENTS.md", help="Path to AGENTS.md file (default: AGENTS.md)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    target_path = Path(args.file)
    result = audit_agents_md(target_path)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("\n" + "=" * 70)
        print("  🤖 AGENTS.md SPECIFICATION VALIDATOR REPORT")
        print("=" * 70)
        print(f"Target File: {result['file']}")
        print(f"Status:      {'🟢 PASSED' if result['passed'] else '🔴 FAILED'}")
        print(f"Score:       {result['score']}/100")
        print(f"Findings:    {result['summary']['high']} High | {result['summary']['medium']} Medium | {result['summary']['low']} Low")
        print("-" * 70)

        if not result["findings"]:
            print("✨ Perfect compliance with the AGENTS.md open specification.")
        else:
            for idx, finding in enumerate(result["findings"], start=1):
                icon = "🟠" if finding["severity"] == "HIGH" else ("🟡" if finding["severity"] == "MEDIUM" else "ℹ️")
                print(f"{idx}. {icon} [{finding['severity']}] {finding['category']} (L{finding['line']})")
                print(f"   {finding['message']}")

        print("=" * 70 + "\n")

    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
