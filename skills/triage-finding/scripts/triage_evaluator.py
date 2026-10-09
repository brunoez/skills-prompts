#!/usr/bin/env python3
"""
Triage Evaluator CLI
Evaluates security alerts, CVEs, and scanner findings against static repository evidence.
Inspired by OpenAI Codex Security (triage-finding) & OWASP ASVS v4.0.3.
"""

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class TriageResult:
    finding_id: str
    package_or_module: str
    vulnerable_symbol: Optional[str]
    verdict: str  # confirmed, not_actionable, needs_review
    confidence: str  # HIGH, MEDIUM, LOW
    evidence: str
    action_item: str


def search_codebase_for_symbol(repo_root: Path, package_name: str, symbol: Optional[str]) -> Dict[str, Any]:
    """
    Scans repository files for imports and usages of a given package/symbol.
    """
    found_import = False
    found_symbol = False
    matching_files = []

    # File extensions to search
    valid_exts = {".py", ".ts", ".js", ".tsx", ".jsx", ".go", ".rs", ".java"}

    for root, dirs, files in os.walk(repo_root):
        # Skip node_modules, .git, venv, test caches
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}]

        for f in files:
            p = Path(root) / f
            if p.suffix in valid_exts:
                try:
                    content = p.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue

                pkg_pattern = rf"(\b(?:import|require|from)\b.*['\"]{re.escape(package_name)}['\"]|\b(?:import|from)\s+{re.escape(package_name)}\b)"
                pkg_imported = bool(re.search(pkg_pattern, content))
                if pkg_imported:
                    found_import = True
                    matching_files.append(str(p.relative_to(repo_root)))

                if symbol and pkg_imported and re.search(rf"\b{re.escape(symbol)}\b", content):
                    found_symbol = True

    return {
        "found_import": found_import,
        "found_symbol": found_symbol,
        "files": matching_files,
    }


def evaluate_single_finding(finding: Dict[str, Any], repo_root: Path) -> TriageResult:
    """
    Triages a single finding against static codebase evidence.
    """
    finding_id = finding.get("id", "UNKNOWN-ALERT")
    pkg = finding.get("package", finding.get("component", ""))
    sym = finding.get("vulnerable_symbol", finding.get("symbol", None))

    if not pkg:
        return TriageResult(
            finding_id=finding_id,
            package_or_module="N/A",
            vulnerable_symbol=sym,
            verdict="needs_review",
            confidence="LOW",
            evidence="Finding does not specify package or component name.",
            action_item="Review manually with full scanner context.",
        )

    res = search_codebase_for_symbol(repo_root, pkg, sym)

    if not res["found_import"]:
        return TriageResult(
            finding_id=finding_id,
            package_or_module=pkg,
            vulnerable_symbol=sym,
            verdict="not_actionable",
            confidence="HIGH",
            evidence=f"Package `{pkg}` is not imported in any production code file.",
            action_item="Dismiss in security dashboard as dead code / unused dependency.",
        )

    if sym and not res["found_symbol"]:
        return TriageResult(
            finding_id=finding_id,
            package_or_module=pkg,
            vulnerable_symbol=sym,
            verdict="not_actionable",
            confidence="MEDIUM",
            evidence=f"Package `{pkg}` is imported in `{len(res['files'])}` files, but the vulnerable symbol `{sym}` is never invoked.",
            action_item="Dismiss in dashboard as uncalled vulnerable function.",
        )

    if sym and res["found_symbol"]:
        return TriageResult(
            finding_id=finding_id,
            package_or_module=pkg,
            vulnerable_symbol=sym,
            verdict="confirmed",
            confidence="HIGH",
            evidence=f"Package `{pkg}` and vulnerable symbol `{sym}` are imported and called in active code files: {res['files'][:3]}.",
            action_item="Prioritize immediate engineering fix or library patch.",
        )

    # Imported, but no specific symbol was defined in alert
    return TriageResult(
        finding_id=finding_id,
        package_or_module=pkg,
        vulnerable_symbol=sym,
        verdict="needs_review",
        confidence="MEDIUM",
        evidence=f"Package `{pkg}` is actively imported in {res['files'][:3]}. Advisory does not name a specific vulnerable function.",
        action_item="Inspect imports to determine if affected sub-modules are utilized.",
    )


def format_markdown_triage(results: List[TriageResult]) -> str:
    """
    Formats triage results into an executive Markdown table.
    """
    confirmed = sum(1 for r in results if r.verdict == "confirmed")
    not_act = sum(1 for r in results if r.verdict == "not_actionable")
    needs_rev = sum(1 for r in results if r.verdict == "needs_review")

    lines = [
        "# 📋 Relatório de Triagem Estática de Alertas (Triage Finding)",
        "",
        f"**Total de Alertas Analisados:** {len(results)}  ",
        f"**Vereditos:** 🔴 {confirmed} Confirmados | 🟢 {not_act} Descartáveis (Not Actionable) | 🟡 {needs_rev} Em Revisão  ",
        "",
        "---",
        "",
        "## 📊 Matriz Consolidada de Triagem",
        "",
        "| ID do Alerta | Pacote / Módulo | Símbolo | Veredito | Confiança | Evidência Estática |",
        "| :--- | :--- | :--- | :---: | :---: | :--- |",
    ]

    for r in results:
        v_icon = "🔴" if r.verdict == "confirmed" else "🟢" if r.verdict == "not_actionable" else "🟡"
        sym_str = f"`{r.vulnerable_symbol}`" if r.vulnerable_symbol else "*-*"
        lines.append(f"| **{r.finding_id}** | `{r.package_or_module}` | {sym_str} | {v_icon} `{r.verdict}` | {r.confidence} | {r.evidence} |")

    lines.extend([
        "",
        "---",
        "",
        "## 🎯 Ações Recomendadas",
        "",
    ])

    for idx, r in enumerate(results, 1):
        lines.append(f"{idx}. **[{r.finding_id}]** (`{r.verdict}`): {r.action_item}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Static Triage Evaluator for Security Alerts & CVEs")
    parser.add_argument("--findings", required=True, help="Path to JSON file containing findings list")
    parser.add_argument("--repo-root", default=".", help="Root directory of the repository to audit")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text", help="Output format")
    parser.add_argument("--output", help="Save output to file")

    args = parser.parse_args()

    findings_path = Path(args.findings)
    if not findings_path.is_file():
        print(f"Error: Findings file not found: {findings_path}", file=sys.stderr)
        sys.exit(1)

    with open(findings_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        data = [data]

    repo_root = Path(args.repo_root).resolve()
    results = [evaluate_single_finding(item, repo_root) for item in data]

    if args.format == "json":
        output_str = json.dumps([asdict(r) for r in results], indent=2)
    elif args.format == "markdown":
        output_str = format_markdown_triage(results)
    else:
        output_lines = [
            f"=== Static Triage Results ({len(results)} alerts) ===",
            "",
        ]
        for r in results:
            output_lines.append(f"[{r.verdict.upper()}] {r.finding_id} ({r.package_or_module})")
            output_lines.append(f"  Evidence: {r.evidence}")
            output_lines.append(f"  Action:   {r.action_item}")
            output_lines.append("")
        output_str = "\n".join(output_lines)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_str)
        print(f"✅ Triagem salva em: {args.output}", file=sys.stderr)
    else:
        print(output_str)

    # Return 1 if confirmed findings exist
    if any(r.verdict == "confirmed" for r in results):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
