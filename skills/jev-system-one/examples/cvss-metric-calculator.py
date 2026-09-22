#!/usr/bin/env python3
"""
CVSS v3.1 Metric Extraction and Deterministic Calculation with Jev (TypeSafe AI)
================================================================================
Elicits CVSS v3.1 Base Metrics from unstructured vulnerability descriptions via
Jev Choice questions, then calculates the exact numeric score using deterministic
closed-form equations from the official FIRST specification (Section 7).

Inspired by `Red5d/jev-cvss`.
"""

import json
import math
import os
import sys
import urllib.request
from typing import Any, Dict, Tuple

API_URL = "https://api.typesafe.ai/v1/systemone"
MODEL_NAME = "jev-1.13.0"

# Official FIRST CVSS v3.1 Weights
WEIGHTS = {
    "AV": {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.20},
    "AC": {"L": 0.77, "H": 0.44},
    "PR_U": {"N": 0.85, "L": 0.62, "H": 0.27},  # Scope Unchanged
    "PR_C": {"N": 0.85, "L": 0.68, "H": 0.50},  # Scope Changed
    "UI": {"N": 0.85, "R": 0.62},
    "C": {"H": 0.56, "L": 0.22, "N": 0.0},
    "I": {"H": 0.56, "L": 0.22, "N": 0.0},
    "A": {"H": 0.56, "L": 0.22, "N": 0.0},
}


def roundup(val: float) -> float:
    """Official FIRST CVSS v3.1 Roundup function."""
    int_val = round(val * 100000)
    if int_val % 10000 == 0:
        return int_val / 100000.0
    return (math.floor(int_val / 10000) + 1) / 10.0


def calculate_cvss31_base_score(m: Dict[str, str]) -> float:
    """Computes exact CVSS v3.1 Base Score per FIRST Section 7 specification."""
    scope_changed = m["S"] == "C"
    
    # Impact Sub-Score (ISS)
    iss = 1.0 - ((1.0 - WEIGHTS["C"][m["C"]]) * (1.0 - WEIGHTS["I"][m["I"]]) * (1.0 - WEIGHTS["A"][m["A"]]))
    
    if scope_changed:
        impact = 7.52 * (iss - 0.029) - 3.25 * math.pow(iss - 0.02, 15)
        pr_weight = WEIGHTS["PR_C"][m["PR"]]
    else:
        impact = 6.42 * iss
        pr_weight = WEIGHTS["PR_U"][m["PR"]]

    # Exploitability Sub-Score
    exploitability = 8.22 * WEIGHTS["AV"][m["AV"]] * WEIGHTS["AC"][m["AC"]] * pr_weight * WEIGHTS["UI"][m["UI"]]

    if impact <= 0.0:
        return 0.0

    if scope_changed:
        return roundup(min(1.08 * (impact + exploitability), 10.0))
    else:
        return roundup(min(impact + exploitability, 10.0))


def elicit_cvss_metrics(description: str, api_key: str) -> Tuple[Dict[str, str], Dict[str, float]]:
    """Elicits all 8 Base Metrics from description in a single parallel Jev call."""
    questions = {
        "AV": {
            "type": "choice",
            "instructions": "Determine the Attack Vector (AV) per CVSS v3.1.",
            "criteria": {
                "N": "Network: Remotely exploitable across L3 boundaries or from browser web clients",
                "A": "Adjacent: Local subnet, Bluetooth, or cellular proximity required",
                "L": "Local: Attacker has local shell/account or relies on local file read/write",
                "P": "Physical: Requires physical touch of hardware"
            }
        },
        "AC": {
            "type": "choice",
            "instructions": "Determine Attack Complexity (AC).",
            "criteria": {
                "L": "Low: Standard deployment, repeatable exploit without race conditions",
                "H": "High: Rare configuration, race condition, or cryptographic secret required"
            }
        },
        "PR": {
            "type": "choice",
            "instructions": "Determine Privileges Required (PR) before attack.",
            "criteria": {
                "N": "None: Unauthenticated attacker",
                "L": "Low: Standard authenticated user credentials",
                "H": "High: Administrative or root privileges required"
            }
        },
        "UI": {
            "type": "choice",
            "instructions": "Determine User Interaction (UI).",
            "criteria": {
                "N": "None: Autonomous exploit without victim involvement",
                "R": "Required: Victim must click link, open file, or navigate to page"
            }
        },
        "S": {
            "type": "choice",
            "instructions": "Determine Scope (S).",
            "criteria": {
                "U": "Unchanged: Vulnerability affects only the security authority of the component",
                "C": "Changed: Exploit breaches container, sandbox, hypervisor, or browser origin"
            }
        },
        "C": {
            "type": "choice",
            "instructions": "Confidentiality Impact (C). Note: Arbitrary Code Execution implies High.",
            "criteria": {"N": "None", "L": "Low / Partial", "H": "High / Total read"}
        },
        "I": {
            "type": "choice",
            "instructions": "Integrity Impact (I). Note: Arbitrary Code Execution or validation bypass implies High.",
            "criteria": {"N": "None", "L": "Low / Partial", "H": "High / Total write"}
        },
        "A": {
            "type": "choice",
            "instructions": "Availability Impact (A). Note: Arbitrary Code Execution or service crash implies High.",
            "criteria": {"N": "None", "L": "Low / Partial", "H": "High / Total denial of service"}
        }
    }

    payload = json.dumps({
        "model": MODEL_NAME,
        "state": {"vulnerability_description": description},
        "questions": questions
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode("utf-8"))

    selected_metrics = {}
    spreads = {}

    for metric_id, ans in res.get("answers", {}).items():
        chosen = ans.get("choice", "N")
        selected_metrics[metric_id] = chosen
        
        # Calculate Top-2 Probability Spread
        probs = sorted(ans.get("probabilities", {}).values(), reverse=True)
        spread = probs[0] - (probs[1] if len(probs) > 1 else 0.0)
        spreads[metric_id] = spread

    return selected_metrics, spreads


def main():
    api_key = os.environ.get("TYPESAFE_API_KEY")
    if not api_key:
        print("⚠️ TYPESAFE_API_KEY não configurada. Executando teste determinístico com vetor NVD 9.8.")
        mock_metrics = {"AV": "N", "AC": "L", "PR": "N", "UI": "N", "S": "U", "C": "H", "I": "H", "A": "H"}
        score = calculate_cvss31_base_score(mock_metrics)
        print(f"Mock Score: {score} (Esperado: 9.8)")
        sys.exit(0)

    advisory = sys.argv[1] if len(sys.argv) > 1 else (
        "An unauthenticated remote code execution vulnerability exists in Apache Tomcat "
        "allowing remote attackers to send a crafted HTTP PUT request and execute arbitrary code."
    )

    print(f"🔍 Avaliando Advisory:\n{advisory}\n")
    metrics, spreads = elicit_cvss_metrics(advisory, api_key)
    score = calculate_cvss31_base_score(metrics)
    
    vector = f"CVSS:3.1/AV:{metrics['AV']}/AC:{metrics['AC']}/PR:{metrics['PR']}/UI:{metrics['UI']}/S:{metrics['S']}/C:{metrics['C']}/I:{metrics['I']}/A:{metrics['A']}"
    
    severity = "CRITICAL" if score >= 9.0 else ("HIGH" if score >= 7.0 else ("MEDIUM" if score >= 4.0 else "LOW"))

    print("=" * 60)
    print(f"  Vetor CVSS v3.1 : {vector}")
    print(f"  Score Calculado : {score} ({severity})")
    print("=" * 60)
    print("Top-2 Spreads de Certeza por Métrica:")
    for k, v in spreads.items():
        status = "⚠️ AMBÍGUO" if v < 0.20 else "✅ SEGURO"
        print(f"  - {k}: {metrics[k]} (ΔP = {v:.3f}) {status}")


if __name__ == "__main__":
    main()
