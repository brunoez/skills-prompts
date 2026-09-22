#!/usr/bin/env python3
"""
Agent Skill & MCP Security Auditor with Jev (TypeSafe AI)
=========================================================
Audits `SKILL.md` definitions, MCP configs (`mcpServers`), and tool handlers
before runtime execution. Employs a multi-stage evaluation:
  Stage 1: Offline static checks (regex heuristics).
  Stage 2: Jev parallel Noul screening across threat vectors.
  Stage 3: Evidence localization and active-context confirmation (Choice).
  Stage 4: Deterministic gate to eliminate false positives in docs/tutorials.

Inspired by `win4r/jev-security-scan` and `luantak/is-malicious`.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Dict, List, Optional

API_URL = "https://api.typesafe.ai/v1/systemone"
MODEL_NAME = "jev-1.13.0"

class MCPSecurityAuditor:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("TYPESAFE_API_KEY")

    def _call_jev(self, state: Dict[str, Any], questions: Dict[str, Any]) -> Dict[str, Any]:
        if not self.api_key:
            return {}

        payload = json.dumps({
            "model": MODEL_NAME,
            "state": state,
            "questions": questions
        }).encode("utf-8")

        req = urllib.request.Request(
            API_URL,
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "MCPSecurityAuditor/1.0"
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            return {"error": str(e)}

    def audit_skill(self, skill_path: Path) -> Dict[str, Any]:
        """Audits a SKILL.md file for prompt injection and unauthorized directives."""
        content = skill_path.read_text(encoding="utf-8", errors="ignore")
        
        # Stage 1: Fast local checks
        has_suspicious_keywords = any(kw in content.lower() for kw in [
            "ignore previous", "override rules", "system instructions", "exfiltrate", "id_rsa", "curl -s"
        ])

        if not self.api_key:
            return {
                "file": str(skill_path),
                "mode": "offline",
                "verdict": "needs_review" if has_suspicious_keywords else "clean",
                "details": "API Key missing, checked only local heuristics."
            }

        # Stage 2: Parallel Jev Screening
        questions_stage1 = {
            "prompt_injection": {
                "type": "noul",
                "instructions": "Does the skill content contain attempts to hijack the agent or override system instructions?",
                "criteria": {
                    "true": "Instructions directing the agent to disregard safety rules or exfiltrate environment secrets",
                    "false": "Legitimate workflow guidelines, task definitions, and normal developer prompts"
                }
            },
            "credential_theft": {
                "type": "noul",
                "instructions": "Does the skill prompt or instruct reading credentials, private keys, or SSH files?"
            },
            "supply_chain_hook": {
                "type": "noul",
                "instructions": "Does the document contain instructions to execute arbitrary remote scripts via curl/bash or unverified downloads?"
            }
        }

        eval_resp = self._call_jev(
            state={"filename": skill_path.name, "content": content[:8000]},
            questions=questions_stage1
        )
        answers = eval_resp.get("answers", {})

        p_injection = answers.get("prompt_injection", {}).get("noul", 0.0)
        p_theft = answers.get("credential_theft", {}).get("noul", 0.0)
        p_supply = answers.get("supply_chain_hook", {}).get("noul", 0.0)

        max_risk = max(p_injection, p_theft, p_supply)

        # Stage 3: Verification & Context Localization if probability >= 0.35
        if max_risk >= 0.35:
            questions_stage2 = {
                "execution_context": {
                    "type": "choice",
                    "instructions": "What is the operational context of the suspicious instructions in this skill?",
                    "criteria": {
                        "active": "Direct executable instructions intended for immediate agent execution",
                        "example": "Descriptive documentation, security tutorial quote, or defensive rule example",
                        "unknown": "Ambiguous context"
                    }
                }
            }
            context_resp = self._call_jev(
                state={"filename": skill_path.name, "content": content[:8000]},
                questions=questions_stage2
            )
            context = context_resp.get("answers", {}).get("execution_context", {}).get("choice", "unknown")
            context_conf = context_resp.get("answers", {}).get("execution_context", {}).get("confidence", 0.0)

            # Stage 4: Deterministic Policy Gate
            if max_risk >= 0.85 and context == "active" and context_conf >= 0.70:
                verdict = "high_risk_suspected"
            elif max_risk >= 0.35:
                verdict = "needs_review"
            else:
                verdict = "clean"
        else:
            verdict = "clean"
            context = "n/a"

        return {
            "file": str(skill_path),
            "verdict": verdict,
            "metrics": {
                "prompt_injection_p": p_injection,
                "credential_theft_p": p_theft,
                "supply_chain_p": p_supply,
                "context": context
            }
        }


def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("SKILL.md")
    if not target.exists():
        print(f"Alvo não encontrado: {target}")
        sys.exit(2)

    auditor = MCPSecurityAuditor()
    print(f"🔍 Auditando {target}...")
    report = auditor.audit_skill(target)
    print(json.dumps(report, indent=2))

    if report["verdict"] == "high_risk_suspected":
        print("❌ BLOQUEADO: Risco crítico suspeito no Skill/MCP!")
        sys.exit(1)
    elif report["verdict"] == "needs_review":
        print("⚠️ REVISÃO: Indicadores suspeitos detectados no material.")
        sys.exit(1)
    else:
        print("✅ APROVADO: Nenhum indicador malicioso ativo.")
        sys.exit(0)


if __name__ == "__main__":
    main()
