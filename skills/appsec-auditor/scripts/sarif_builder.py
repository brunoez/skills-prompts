#!/usr/bin/env python3
"""
SARIF 2.1.0 Builder & Exporter for AppSec Auditor.
Generates compliant OASIS SARIF v2.1.0 files for GitHub Code Scanning / Advanced Security.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Finding:
    id: str
    title: str
    description: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    file_path: str
    start_line: int
    end_line: Optional[int] = None
    start_column: int = 1
    end_column: Optional[int] = None
    cwe: Optional[str] = None
    asvs: Optional[str] = None
    owasp: Optional[str] = None
    likelihood: Optional[str] = None
    impact: Optional[str] = None
    remediation: Optional[str] = None
    properties: Dict[str, Any] = field(default_factory=dict)


SEVERITY_TO_SARIF_LEVEL = {
    "CRITICAL": "error",
    "HIGH": "error",
    "MEDIUM": "warning",
    "LOW": "note",
    "INFO": "note",
    "NIT": "note",
}


def build_sarif(
    findings: List[Finding],
    tool_name: str = "AppSec Auditor",
    tool_version: str = "1.0.0",
    information_uri: str = "https://github.com/brunoez/skills-prompts",
) -> Dict[str, Any]:
    """Converts a list of Finding objects into a compliant SARIF 2.1.0 dictionary."""
    rules_map: Dict[str, Dict[str, Any]] = {}
    results: List[Dict[str, Any]] = []

    for f in findings:
        rule_id = f.owasp or f.cwe or f.id
        norm_severity = f.severity.upper()
        sarif_level = SEVERITY_TO_SARIF_LEVEL.get(norm_severity, "warning")

        if rule_id not in rules_map:
            rule_def: Dict[str, Any] = {
                "id": rule_id,
                "name": f.title,
                "shortDescription": {"text": f.title},
                "fullDescription": {"text": f.description},
                "defaultConfiguration": {"level": sarif_level},
                "properties": {
                    "tags": ["security", "appsec"],
                    "precision": "high",
                },
            }
            if f.cwe:
                rule_def["properties"]["cwe"] = f.cwe
                rule_def["properties"]["tags"].append(f"external/cwe/{f.cwe.lower()}")
            if f.asvs:
                rule_def["properties"]["asvs"] = f.asvs
            if f.owasp:
                rule_def["properties"]["owasp"] = f.owasp
                rule_def["properties"]["tags"].append(f.owasp.lower())

            if f.remediation:
                rule_def["help"] = {
                    "text": f"Remediation Recommendation:\n{f.remediation}",
                    "markdown": f"### Remediation Recommendation\n{f.remediation}",
                }

            rules_map[rule_id] = rule_def

        # Result item
        end_line = f.end_line if f.end_line and f.end_line >= f.start_line else f.start_line

        region: Dict[str, Any] = {
            "startLine": f.start_line,
            "endLine": end_line,
            "startColumn": f.start_column,
        }
        if f.end_column is not None:
            region["endColumn"] = f.end_column

        # Normalize relative file path for SARIF
        clean_path = str(f.file_path).lstrip("./")

        result: Dict[str, Any] = {
            "ruleId": rule_id,
            "level": sarif_level,
            "message": {
                "text": f"[{norm_severity}] {f.title}: {f.description}"
            },
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": clean_path,
                            "uriBaseId": "%SRCROOT%",
                        },
                        "region": region,
                    }
                }
            ],
            "properties": {
                "severity": norm_severity,
                "likelihood": f.likelihood or "N/A",
                "impact": f.impact or "N/A",
                **f.properties,
            },
        }

        if f.remediation:
            result["fixes"] = [
                {
                    "description": {"text": f.remediation}
                }
            ]

        results.append(result)

    sarif_doc = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": tool_name,
                        "version": tool_version,
                        "informationUri": information_uri,
                        "rules": list(rules_map.values()),
                    }
                },
                "results": results,
                "invocations": [
                    {
                        "executionSuccessful": True,
                        "endTimeUtc": datetime.now(timezone.utc).isoformat(),
                    }
                ],
            }
        ],
    }

    return sarif_doc


def load_findings_from_dict(data: List[Dict[str, Any]]) -> List[Finding]:
    findings: List[Finding] = []
    for item in data:
        finding = Finding(
            id=item.get("id", "SEC-UNKNOWN"),
            title=item.get("title", "Security Finding"),
            description=item.get("description", ""),
            severity=item.get("severity", "MEDIUM"),
            file_path=item.get("file_path", "unknown"),
            start_line=int(item.get("start_line", 1)),
            end_line=int(item["end_line"]) if item.get("end_line") else None,
            start_column=int(item.get("start_column", 1)),
            end_column=int(item["end_column"]) if item.get("end_column") else None,
            cwe=item.get("cwe"),
            asvs=item.get("asvs"),
            owasp=item.get("owasp"),
            likelihood=item.get("likelihood"),
            impact=item.get("impact"),
            remediation=item.get("remediation"),
            properties=item.get("properties", {}),
        )
        findings.append(finding)
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert AppSec findings JSON into standard SARIF 2.1.0 report."
    )
    parser.add_argument(
        "-i", "--input", help="Path to findings JSON file (reads stdin if omitted)"
    )
    parser.add_argument(
        "-o", "--output", default="results.sarif", help="Path to write output SARIF (default: results.sarif)"
    )
    parser.add_argument(
        "--tool-name", default="AppSec Auditor", help="Name of the reporting tool"
    )

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
        if not isinstance(data, list):
            print("Error: Input must be a JSON array of findings or an object with 'findings' key.", file=sys.stderr)
            return 1
    except Exception as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        return 1

    findings = load_findings_from_dict(data)
    sarif = build_sarif(findings, tool_name=args.tool_name)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(sarif, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ Generated SARIF 2.1.0 with {len(findings)} findings at {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
