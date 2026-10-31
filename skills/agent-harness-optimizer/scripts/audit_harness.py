#!/usr/bin/env python3
"""
Agent Harness Auditor CLI (Google Research Harness² Methodology)
Audits agent scaffolding across the 8 harness components, token budgets,
skill trigger lines, and physical script existence.
"""

import argparse
import json
import re
import sys
from pathlib import Path

ALWAYS_ON_CANDIDATES = [
    "AGENTS.md",
    "CLAUDE.md",
    "systemprompt.md",
    "guardrails.md",
    "LongTermMEMORY.md",
    ".cursorrules",
    "CONTEXT.md",
]

LINE_LIMIT_ALWAYS_ON = 250
ESTIMATED_TOKENS_LIMIT = 2000


def audit_harness(root_path: Path) -> dict:
    if not root_path.is_dir():
        return {
            "status": "ERROR",
            "root": str(root_path),
            "errors": [f"Directory not found: {root_path}"],
            "findings": [],
            "score": 0,
            "passed": False,
        }

    findings = []

    # 1. Inspect Always-On Components
    always_on_files = []
    combined_always_on_text = ""

    for candidate in ALWAYS_ON_CANDIDATES:
        p = root_path / candidate
        if p.is_file():
            content = p.read_text(encoding="utf-8", errors="ignore")
            lines = content.splitlines()
            char_count = len(content)
            approx_tokens = char_count // 4
            always_on_files.append({
                "path": candidate,
                "lines": len(lines),
                "approx_tokens": approx_tokens,
            })
            combined_always_on_text += "\n" + content

            if len(lines) > LINE_LIMIT_ALWAYS_ON:
                findings.append({
                    "component": candidate,
                    "category": "Token Economics",
                    "severity": "HIGH",
                    "message": f"Always-on file '{candidate}' has {len(lines)} lines (exceeds recommended {LINE_LIMIT_ALWAYS_ON} limit). Every token competes with agent output budget.",
                })

    # Also include README.md in trigger search if present
    readme_path = root_path / "README.md"
    readme_text = readme_path.read_text(encoding="utf-8", errors="ignore") if readme_path.is_file() else ""
    searchable_context = combined_always_on_text + "\n" + readme_text

    # 2. Inspect Skills & Trigger Lines
    skills_found = []
    skill_dirs = []

    for base in [root_path / "skills", root_path / ".agents" / "skills"]:
        if base.is_dir():
            for d in base.iterdir():
                if d.is_dir() and (d / "SKILL.md").is_file():
                    skill_dirs.append(d)

    for sdir in skill_dirs:
        skill_name = sdir.name
        skill_md = sdir / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8", errors="ignore")

        has_frontmatter = content.startswith("---") and "description:" in content
        if not has_frontmatter:
            findings.append({
                "component": f"skills/{skill_name}",
                "category": "Skill Contract",
                "severity": "CRITICAL",
                "message": f"Skill '{skill_name}/SKILL.md' is missing valid YAML frontmatter with a description.",
            })

        # Harness² Trigger Line Rule: Skill directory name must appear in always-on text or root README
        # Pattern checks if the skill name appears as text or trigger
        is_triggered = skill_name in searchable_context
        if not is_triggered:
            findings.append({
                "component": f"skills/{skill_name}",
                "category": "Trigger Line Invariant",
                "severity": "HIGH",
                "message": f"Skill '{skill_name}' is never referenced in always-on context (AGENTS.md, CLAUDE.md, or README.md). Unnamed skills are dead weight at runtime.",
            })

        # 3. Check for Scripts referenced in the skill
        # Look for references like scripts/xyz.py or python3 ...
        script_refs = re.findall(r"(?:python3?\s+)?(?:[\w\-]+/)*scripts/([a-zA-Z0-9_\-]+\.py)", content)
        for sref in set(script_refs):
            expected_local = sdir / "scripts" / sref
            expected_root = root_path / "scripts" / sref
            if not (expected_local.is_file() or expected_root.is_file()):
                findings.append({
                    "component": f"skills/{skill_name}",
                    "category": "Script Verification",
                    "severity": "CRITICAL",
                    "message": f"Skill '{skill_name}' references script '{sref}', but it does not exist in skill scripts/ or root scripts/.",
                })

        skills_found.append({
            "name": skill_name,
            "has_frontmatter": has_frontmatter,
            "has_trigger": is_triggered,
        })

    # 4. Inspect Subagents
    subagents_found = []
    subagents_dir = root_path / "sub_agents"
    if subagents_dir.is_dir():
        for d in subagents_dir.iterdir():
            if d.is_dir() and (d / "AGENT.md").is_file():
                subagents_found.append(d.name)

    # 5. Inspect Hooks
    hooks_file = root_path / ".codex" / "hooks.json"
    has_hooks = hooks_file.is_file()

    # Calculate Score
    crit_count = sum(1 for f in findings if f["severity"] == "CRITICAL")
    high_count = sum(1 for f in findings if f["severity"] == "HIGH")
    med_count = sum(1 for f in findings if f["severity"] == "MEDIUM")
    low_count = sum(1 for f in findings if f["severity"] == "LOW")

    deductions = (crit_count * 30) + (high_count * 15) + (med_count * 5) + (low_count * 2)
    score = max(0, 100 - deductions)
    passed = crit_count == 0 and high_count == 0 and score >= 70

    return {
        "status": "PASS" if passed else "FAIL",
        "root": str(root_path),
        "score": score,
        "passed": passed,
        "components_summary": {
            "always_on_files": always_on_files,
            "skills_count": len(skills_found),
            "subagents_count": len(subagents_found),
            "has_hooks": has_hooks,
        },
        "summary": {
            "critical": crit_count,
            "high": high_count,
            "medium": med_count,
            "low": low_count,
            "total_findings": len(findings),
        },
        "findings": findings,
    }


def main():
    parser = argparse.ArgumentParser(description="Agent Harness Auditor CLI (Google Research Harness² Methodology)")
    parser.add_argument("path", nargs="?", default=".", help="Root directory of the project harness (default: .)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    target_path = Path(args.path).resolve()
    result = audit_harness(target_path)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("\n" + "=" * 75)
        print("  🧩 HARNESS² AGENT SCAFFOLDING AUDITOR REPORT")
        print("=" * 75)
        print(f"Target Root: {result['root']}")
        print(f"Status:      {'🟢 PASSED' if result['passed'] else '🔴 FAILED'}")
        print(f"Score:       {result['score']}/100")
        print(f"Components:  {len(result['components_summary']['always_on_files'])} always-on files | {result['components_summary']['skills_count']} skills | {result['components_summary']['subagents_count']} subagents")
        print(f"Findings:    {result['summary']['critical']} Critical | {result['summary']['high']} High | {result['summary']['medium']} Medium | {result['summary']['low']} Low")
        print("-" * 75)

        if not result["findings"]:
            print("✨ Perfect compliance with Harness² component hierarchy and invariants.")
        else:
            for idx, finding in enumerate(result["findings"], start=1):
                icon = "🔴" if finding["severity"] == "CRITICAL" else ("🟠" if finding["severity"] == "HIGH" else "🟡")
                print(f"{idx}. {icon} [{finding['severity']}] {finding['category']} ({finding['component']})")
                print(f"   {finding['message']}")

        print("=" * 75 + "\n")

    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
