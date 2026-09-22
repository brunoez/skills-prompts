#!/usr/bin/env python3
"""
AppSec Audit Report Generator.
Generates terminal executive tables, markdown reports, and GitHub Issue templates.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4, "NIT": 5}
SEVERITY_EMOJIS = {
    "CRITICAL": "🔴",
    "HIGH": "🟠",
    "MEDIUM": "🟡",
    "LOW": "🔵",
    "INFO": "⚪",
    "NIT": "◽",
}


def sort_findings(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(
        findings,
        key=lambda x: (
            SEVERITY_ORDER.get(x.get("severity", "MEDIUM").upper(), 99),
            x.get("file_path", ""),
            x.get("start_line", 0),
        ),
    )


def generate_markdown_report(findings: List[Dict[str, Any]], title: str = "Relatório de Auditoria AppSec") -> str:
    sorted_f = sort_findings(findings)
    counts: Dict[str, int] = {}
    for f in sorted_f:
        sev = f.get("severity", "MEDIUM").upper()
        counts[sev] = counts.get(sev, 0) + 1

    lines = [
        f"# 🛡️ {title}",
        "",
        "## 📊 Sumário Executivo de Riscos",
        "",
        "| Severidade | Quantidade | Nível de Ação |",
        "| :--- | :---: | :--- |",
        f"| 🔴 **CRÍTICA** | {counts.get('CRITICAL', 0)} | Correção imediata (Bloqueante de Deploy) |",
        f"| 🟠 **ALTA** | {counts.get('HIGH', 0)} | Correção em sprint corrente / Hotfix |",
        f"| 🟡 **MÉDIA** | {counts.get('MEDIUM', 0)} | Planejar na próxima sprint |",
        f"| 🔵 **BAIXA / INFO** | {counts.get('LOW', 0) + counts.get('INFO', 0)} | Melhoria técnica / Hardening contínuo |",
        "",
        "---",
        "",
        "## 📋 Matriz de Priorização (OWASP Risk Rating)",
        "",
        "| ID | Arquivo:Linha | Título / Vulnerabilidade | OWASP / ASVS | Severidade | Esforço | Quick Win? |",
        "|---|---|---|---|---|---|:---:|",
    ]

    for f in sorted_f:
        fid = f.get("id", "SEC-001")
        loc = f"`{f.get('file_path', 'unknown')}:{f.get('start_line', 1)}`"
        ftitle = f.get("title", "Finding")
        standard = f"{f.get('owasp', '')} / {f.get('asvs', '')}".strip(" /")
        sev = f.get("severity", "MEDIUM").upper()
        emoji = SEVERITY_EMOJIS.get(sev, "⚪")
        effort = f.get("effort", "Médio")
        qw = "✅" if f.get("quick_win") or effort.lower() in ("baixo", "low") else "—"

        lines.append(f"| {fid} | {loc} | {ftitle} | {standard} | {emoji} {sev} | {effort} | {qw} |")

    lines.extend([
        "",
        "---",
        "",
        "## 🔍 Detalhamento dos Achados & Recomendações",
        "",
    ])

    for f in sorted_f:
        fid = f.get("id", "SEC-001")
        sev = f.get("severity", "MEDIUM").upper()
        emoji = SEVERITY_EMOJIS.get(sev, "⚪")
        lines.extend([
            f"### [{fid}] {emoji} {f.get('title', 'Finding')}",
            f"- **Arquivo:** `{f.get('file_path')}:{f.get('start_line')}`",
            f"- **Severidade:** `{sev}` (Probabilidade: `{f.get('likelihood', 'N/A')}` | Impacto: `{f.get('impact', 'N/A')}`)",
            f"- **Classificação:** OWASP: `{f.get('owasp', 'N/A')}` | ASVS: `{f.get('asvs', 'N/A')}` | CWE: `{f.get('cwe', 'N/A')}`",
            "",
            "**Descrição Técnica & Impacto:**",
            f"{f.get('description', 'Sem descrição.')}",
            "",
        ])

        if f.get("vulnerable_code"):
            lines.extend([
                "**Código Vulnerável Identificado:**",
                "```",
                f"{f.get('vulnerable_code').strip()}",
                "```",
                "",
            ])

        if f.get("remediation"):
            lines.extend([
                "**Recomendação de Correção (Defesa em Profundidade):**",
                f"{f.get('remediation').strip()}",
                "",
            ])

        if f.get("verification"):
            lines.extend([
                "**Comando / Teste de Verificação Pós-Correção:**",
                "```bash",
                f"{f.get('verification').strip()}",
                "```",
                "",
            ])

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def generate_issue_template(finding: Dict[str, Any]) -> str:
    sev = finding.get("severity", "MEDIUM").upper()
    emoji = SEVERITY_EMOJIS.get(sev, "⚪")
    return f"""### Title: [SEC] {finding.get('title')} ({sev})

**Severity:** {emoji} {sev}  
**Location:** `{finding.get('file_path')}:{finding.get('start_line')}`  
**Standard:** OWASP {finding.get('owasp', 'N/A')} | ASVS {finding.get('asvs', 'N/A')} | CWE-{finding.get('cwe', 'N/A')}

#### Description
{finding.get('description')}

#### Remediation
{finding.get('remediation', 'Implement secure validation and authorization check.')}

#### Acceptance Criteria
- [ ] Vulnerability fixed at `{finding.get('file_path')}`.
- [ ] Automated regression / abuse test added and passing.
- [ ] No regression introduced in existing test suite.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate AppSec Markdown reports and issue templates from findings JSON.")
    parser.add_argument("-i", "--input", help="Path to findings JSON file (reads stdin if omitted)")
    parser.add_argument("-o", "--output", default="docs/appsec-audit-report.md", help="Output path for Markdown report")
    parser.add_argument("--issues-dir", help="Optional directory to dump GitHub issue templates (.md)")

    args = parser.parse_args()

    if args.input:
        raw_text = Path(args.input).read_text(encoding="utf-8")
    else:
        raw_text = sys.stdin.read()

    if not raw_text.strip():
        print("Error: Empty input provided.", file=sys.stderr)
        return 1

    try:
        data = json.loads(raw_text)
        if isinstance(data, dict) and "findings" in data:
            data = data["findings"]
    except Exception as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        return 1

    report_md = generate_markdown_report(data)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report_md, encoding="utf-8")
    print(f"✅ Generated Markdown report at {out_path}")

    if args.issues_dir:
        issue_path = Path(args.issues_dir)
        issue_path.mkdir(parents=True, exist_ok=True)
        for i, f in enumerate(data, start=1):
            fid = f.get("id", f"SEC-{i:03d}")
            tpl = generate_issue_template(f)
            (issue_path / f"issue-{fid}.md").write_text(tpl, encoding="utf-8")
        print(f"✅ Generated {len(data)} issue templates in {issue_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
