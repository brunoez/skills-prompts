#!/usr/bin/env python3
"""
Security Diff Scanner CLI
Surgical security analysis of Git diffs, PRs, and patches.
Inspired by OpenAI Codex Security (security-diff-scan) & OWASP ASVS v4.0.3.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class DiffFinding:
    rule_id: str
    title: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    file_path: str
    line_number: int
    matched_line: str
    description: str
    cwe: str
    owasp_category: str
    remediation: str


# Core Security Rules for Diff Inspection
SECURITY_RULES = [
    {
        "id": "SEC-DIFF-001",
        "title": "Hardcoded Secret / API Key in Diff",
        "severity": "CRITICAL",
        "cwe": "CWE-798",
        "owasp": "A07:2021-Identification and Authentication Failures",
        "pattern": r"(?i)(api[_-]?key|secret|token|password|passwd|auth[_-]?token)\s*[:=]\s*['\"][A-Za-z0-9_\-\.]{16,}['\"]",
        "description": "Hardcoded credential or secret detected in changed lines.",
        "remediation": "Move secrets to environment variables or a secure secret manager (e.g., Vault, AWS Secrets Manager).",
    },
    {
        "id": "SEC-DIFF-002",
        "title": "Dangerous Command Execution Sink",
        "severity": "CRITICAL",
        "cwe": "CWE-78",
        "owasp": "A03:2021-Injection",
        "pattern": r"\b(child_process\.exec|child_process\.execSync|os\.system|subprocess\.Popen\(.*shell\s*=\s*True|eval\s*\(|new\s+Function\s*\()",
        "description": "Command execution or dynamic code evaluation sink detected.",
        "remediation": "Avoid shell execution with user input. Use parameterized APIs like subprocess.run([...], shell=False).",
    },
    {
        "id": "SEC-DIFF-003",
        "title": "Raw SQL / Unsafe Query Interpolation",
        "severity": "HIGH",
        "cwe": "CWE-89",
        "owasp": "A03:2021-Injection",
        "pattern": r"(?i)(\$queryRawUnsafe|rawQuery|executeRaw|cursor\.execute\s*\(\s*f['\"]|db\.query\s*\(\s*`[^`]*\$\{)",
        "description": "Raw SQL execution or string interpolation in query builder detected.",
        "remediation": "Use prepared statements, ORM methods, or parameterized query tags (e.g., Prisma.sql).",
    },
    {
        "id": "SEC-DIFF-004",
        "title": "Disabled TLS / Insecure SSL Verification",
        "severity": "HIGH",
        "cwe": "CWE-295",
        "owasp": "A02:2021-Cryptographic Failures",
        "pattern": r"(?i)(rejectUnauthorized\s*:\s*false|verify\s*=\s*False|NODE_TLS_REJECT_UNAUTHORIZED\s*=\s*['\"]?0['\"]?)",
        "description": "TLS certificate verification explicitly disabled, exposing requests to MitM.",
        "remediation": "Enable TLS verification in all environments. Use trusted CA certificates.",
    },
    {
        "id": "SEC-DIFF-005",
        "title": "Permissive Wildcard CORS Configuration",
        "severity": "MEDIUM",
        "cwe": "CWE-942",
        "owasp": "A05:2021-Security Misconfiguration",
        "pattern": r"(?i)(origin\s*:\s*['\"]\*['\"]|Access-Control-Allow-Origin['\"]\s*,\s*['\"]\*['\"])",
        "description": "Wildcard CORS origin configured in modified code.",
        "remediation": "Restrict CORS origins to a verified allow-list of trusted domains.",
    },
    {
        "id": "SEC-DIFF-006",
        "title": "Potentially Unscoped Query (IDOR/BOLA Risk)",
        "severity": "HIGH",
        "cwe": "CWE-639",
        "owasp": "API1:2023-Broken Object Level Authorization",
        "pattern": r"(?i)(\.findUnique\s*\(\s*\{\s*where\s*:\s*\{\s*id\s*\}|\.findById\s*\(\s*req\.(params|query|body)\.id\s*\))",
        "description": "Object fetched by single ID without tenant or ownership verification in query.",
        "remediation": "Enforce tenancy filtering in the query (e.g., where: { id, tenantId: req.user.tenantId }).",
    },
]


def parse_diff_content(diff_text: str) -> List[Dict[str, Any]]:
    """
    Parses a unified diff and extracts modified chunks per file.
    """
    files: List[Dict[str, Any]] = []
    current_file: Optional[Dict[str, Any]] = None
    current_line = 0

    file_header_re = re.compile(r"^diff --git a/(.*) b/(.*)")
    chunk_header_re = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")

    for line in diff_text.splitlines():
        match_file = file_header_re.match(line)
        if match_file:
            if current_file:
                files.append(current_file)
            current_file = {
                "old_path": match_file.group(1),
                "new_path": match_file.group(2),
                "added_lines": [],  # List of (line_num, line_str)
                "deleted_lines": [],  # List of line_str
            }
            continue

        if not current_file:
            continue

        match_chunk = chunk_header_re.match(line)
        if match_chunk:
            current_line = int(match_chunk.group(1))
            continue

        if line.startswith("+") and not line.startswith("+++"):
            current_file["added_lines"].append((current_line, line[1:]))
            current_line += 1
        elif line.startswith("-") and not line.startswith("---"):
            current_file["deleted_lines"].append(line[1:])
        elif not line.startswith("\\"):
            current_line += 1

    if current_file:
        files.append(current_file)

    return files


def scan_diff_files(parsed_files: List[Dict[str, Any]]) -> List[DiffFinding]:
    """
    Audits added/modified lines in parsed diff files for security patterns.
    """
    findings: List[DiffFinding] = []

    for file_info in parsed_files:
        file_path = file_info["new_path"]
        
        # Skip scanning on test files for specific rules if appropriate
        is_test_file = bool(re.search(r"(test|spec|mock|fixture)", file_path, re.IGNORECASE))

        # 1. Scan added lines
        for line_num, line_content in file_info["added_lines"]:
            stripped = line_content.strip()
            if not stripped or stripped.startswith("//") or stripped.startswith("#"):
                continue

            for rule in SECURITY_RULES:
                # Skip secret alerts on test fixtures if clearly mock
                if is_test_file and rule["id"] == "SEC-DIFF-001" and "mock" in stripped.lower():
                    continue

                if re.search(rule["pattern"], line_content):
                    findings.append(
                        DiffFinding(
                            rule_id=rule["id"],
                            title=rule["title"],
                            severity=rule["severity"],
                            file_path=file_path,
                            line_number=line_num,
                            matched_line=stripped[:120],
                            description=rule["description"],
                            cwe=rule["cwe"],
                            owasp_category=rule["owasp"],
                            remediation=rule["remediation"],
                        )
                    )

        # 2. Check deleted lines for removed security guards
        for del_line in file_info["deleted_lines"]:
            stripped_del = del_line.strip()
            if re.search(r"(@UseGuards|authMiddleware|tenant_id|verifyToken|checkPermission)", stripped_del):
                findings.append(
                    DiffFinding(
                        rule_id="SEC-DIFF-REGRESS-01",
                        title="Potentially Removed Authorization Guard / Tenancy Check",
                        severity="HIGH",
                        file_path=file_path,
                        line_number=0,
                        matched_line=stripped_del[:120],
                        description="An authorization decorator, middleware, or tenant check was removed in this diff.",
                        cwe="CWE-285",
                        owasp_category="A01:2021-Broken Access Control",
                        remediation="Verify whether the security guard was intentionally relocated or accidentally deleted.",
                    )
                )

    return findings


def get_git_diff(base: str, head: str, cwd: str = ".") -> str:
    """
    Executes git diff command and returns raw diff output.
    """
    cmd = ["git", "diff", "-U3", f"{base}...{head}"]
    try:
        res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True)
        return res.stdout
    except subprocess.CalledProcessError as e:
        # Fallback to direct diff if base...head fails (e.g. against single ref or uncommitted)
        try:
            res_fb = subprocess.run(["git", "diff", "-U3", base], cwd=cwd, capture_output=True, text=True, check=True)
            return res_fb.stdout
        except Exception:
            raise RuntimeError(f"Git diff failed: {e.stderr.strip()}")


def build_sarif_report(findings: List[DiffFinding]) -> Dict[str, Any]:
    """
    Exports findings in OASIS SARIF 2.1.0 format.
    """
    sarif_rules: Dict[str, Any] = {}
    sarif_results: List[Dict[str, Any]] = []

    for f in findings:
        if f.rule_id not in sarif_rules:
            sarif_rules[f.rule_id] = {
                "id": f.rule_id,
                "name": f.title.replace(" ", ""),
                "shortDescription": {"text": f.title},
                "fullDescription": {"text": f.description},
                "help": {"text": f.remediation},
                "properties": {"cwe": f.cwe, "owasp": f.owasp_category},
            }

        level = "error" if f.severity in ["CRITICAL", "HIGH"] else "warning" if f.severity == "MEDIUM" else "note"
        sarif_results.append(
            {
                "ruleId": f.rule_id,
                "level": level,
                "message": {"text": f"{f.title}: {f.description}"},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": f.file_path},
                            "region": {"startLine": max(1, f.line_number)},
                        }
                    }
                ],
            }
        )

    return {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "SecurityDiffScanner",
                        "version": "1.0.0",
                        "rules": list(sarif_rules.values()),
                    }
                },
                "results": sarif_results,
            }
        ],
    }


def format_markdown_report(findings: List[DiffFinding], files_count: int) -> str:
    """
    Formats the findings into a clean GitHub/GitLab PR Code Review comment.
    """
    status = "🔴 BLOQUEADO (Vulnerabilidades Encontradas)" if findings else "🟢 APROVADO (Nenhum Risco Detectado)"
    
    crit_count = sum(1 for f in findings if f.severity == "CRITICAL")
    high_count = sum(1 for f in findings if f.severity == "HIGH")
    med_count = sum(1 for f in findings if f.severity == "MEDIUM")
    low_count = sum(1 for f in findings if f.severity == "LOW")

    lines = [
        "# 🔍 Parecer de Segurança do Diff (Security Diff Scan)",
        "",
        f"**Arquivos Analisados no Diff:** {files_count}  ",
        f"**Veredito de Segurança:** {status}  ",
        f"**Total de Achados:** {len(findings)} ({crit_count} Críticos | {high_count} Altos | {med_count} Médios | {low_count} Baixos)",
        "",
        "---",
        "",
    ]

    if not findings:
        lines.append("✅ Nenhuma vulnerabilidade ou regressão de segurança foi introduzida nas linhas modificadas deste diff.")
        return "\n".join(lines)

    lines.extend([
        "## 📊 Matriz de Achados no Diff",
        "",
        "| Arquivo & Linha | Severidade | Regra / CWE | Descrição |",
        "| :--- | :---: | :--- | :--- |",
    ])

    for f in findings:
        loc = f"`{f.file_path}:{f.line_number}`" if f.line_number > 0 else f"`{f.file_path}`"
        lines.append(f"| {loc} | **{f.severity}** | {f.rule_id} ({f.cwe}) | {f.title} |")

    lines.extend(["", "---", "", "## 💥 Detalhamento & Ações de Correção", ""])

    for idx, f in enumerate(findings, 1):
        loc = f"{f.file_path}:{f.line_number}" if f.line_number > 0 else f"{f.file_path}"
        lines.extend([
            f"### #{idx} [{f.severity}] {f.title}",
            f"* **Localização:** `{loc}`",
            f"* **CWE:** {f.cwe} | **OWASP:** {f.owasp_category}",
            f"* **Trecho Identificado:** `{f.matched_line}`",
            f"* **Diagnóstico:** {f.description}",
            f"* **Ação Recomendada:** {f.remediation}",
            "",
        ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Security Diff Scanner for PRs and Git Diffs")
    parser.add_argument("--base", default="origin/main", help="Git base branch/commit (default: origin/main)")
    parser.add_argument("--head", default="HEAD", help="Git head commit (default: HEAD)")
    parser.add_argument("--patch", help="Path to raw .patch or .diff file instead of running git")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text", help="Output format")
    parser.add_argument("--output", help="Save output to file")
    parser.add_argument("--sarif", help="Export SARIF 2.1.0 output to specified path")

    args = parser.parse_args()

    if args.patch:
        if not os.path.isfile(args.patch):
            print(f"Error: Patch file not found: {args.patch}", file=sys.stderr)
            sys.exit(1)
        with open(args.patch, "r", encoding="utf-8") as f:
            diff_text = f.read()
    else:
        try:
            diff_text = get_git_diff(args.base, args.head)
        except Exception as e:
            print(f"Error extracting git diff: {e}", file=sys.stderr)
            sys.exit(1)

    parsed_files = parse_diff_content(diff_text)
    findings = scan_diff_files(parsed_files)

    if args.sarif:
        sarif_data = build_sarif_report(findings)
        with open(args.sarif, "w", encoding="utf-8") as f:
            json.dump(sarif_data, f, indent=2)
        print(f"✅ SARIF 2.1.0 salvo em: {args.sarif}", file=sys.stderr)

    if args.format == "json":
        output_str = json.dumps([asdict(f) for f in findings], indent=2)
    elif args.format == "markdown":
        output_str = format_markdown_report(findings, len(parsed_files))
    else:
        # Standard text output
        output_lines = [
            f"=== Security Diff Scan Results ({len(parsed_files)} files reviewed) ===",
            f"Findings: {len(findings)}",
            "",
        ]
        for f in findings:
            loc = f"{f.file_path}:{f.line_number}" if f.line_number > 0 else f"{f.file_path}"
            output_lines.append(f"[{f.severity}] {f.title} ({f.rule_id}) at {loc}")
            output_lines.append(f"  Snippet: {f.matched_line}")
            output_lines.append(f"  Fix: {f.remediation}")
            output_lines.append("")
        output_str = "\n".join(output_lines)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_str)
        print(f"✅ Relatório salvo em: {args.output}", file=sys.stderr)
    else:
        print(output_str)

    # Return exit code 1 if critical/high findings exist
    if any(f.severity in ["CRITICAL", "HIGH"] for f in findings):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
