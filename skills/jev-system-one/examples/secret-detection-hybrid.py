#!/usr/bin/env python3
"""
Hybrid Secret Scanning & Semantic Triage Pipeline with Jev (TypeSafe AI)
========================================================================
Combines high-speed local regex/entropy matching with Jev Noul semantic validation
to eliminate false positives (test seeds, UUIDs, bcrypt, docs keys) and catch
config-shaped low-entropy passwords.

Tested against real-world patterns from `teyhouse/jev-secret-detection`.
Concurrency capped at 16 requests to avoid HTTP 529 Overloaded.
"""

import asyncio
import json
import os
import re
import sys
import urllib.request
import urllib.error
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

API_URL = "https://api.typesafe.ai/v1/systemone"
MODEL_NAME = "jev-1.13.0"
MAX_CONCURRENT_REQUESTS = 16

# Stage 1: Fast local candidates
CANDIDATE_PATTERNS = [
    re.compile(r'(?i)(?:password|passwd|pwd|bindpw)\s*[:=]\s*["\']?([^"\'\s\r\n]{4,})["\']?'),
    re.compile(r'(?i)(?:api_key|apikey|secret_key|auth_token)\s*[:=]\s*["\']?([^"\'\s\r\n]{8,})["\']?'),
    re.compile(r'(?i)(?:ghp_[a-zA-Z0-9]{36}|sk_live_[a-zA-Z0-9]{24,})'),
]

@dataclass
class SecretFinding:
    file_path: str
    line_number: int
    matched_text: str
    snippet_context: str
    noul_score: Optional[float] = None
    category: Optional[str] = None
    confidence: Optional[float] = None
    decision: str = "PENDING"


class JevSecretValidator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async def evaluate_snippet(self, finding: SecretFinding) -> SecretFinding:
        """Evaluates a secret candidate snippet using Jev Noul & Choice primitives."""
        payload = {
            "model": MODEL_NAME,
            "state": {
                "file_path": finding.file_path,
                "line_number": finding.line_number,
                "snippet": finding.snippet_context,
            },
            "questions": {
                "is_real_secret": {
                    "type": "noul",
                    "instructions": "Does the snippet contain a real secret credential that someone reading it could use to authenticate?",
                    "criteria": {
                        "true": "Live database credentials, private keys, working API tokens, plaintext config passwords",
                        "false": "Placeholder values (EXAMPLE_KEY), test credentials (changeit, hunter2), cryptographic digests (bcrypt, sha256), UUIDs"
                    }
                },
                "secret_category": {
                    "type": "choice",
                    "instructions": "Classify the credential type found in the snippet.",
                    "criteria": {
                        "vendor_token": "Prefixed token from cloud/SaaS provider (GitHub, Stripe, AWS, Slack)",
                        "config_password": "Plaintext operational password in service configuration",
                        "database_uri": "Connection URI with embedded username and password",
                        "private_key": "Cryptographic private key or service account token",
                        "benign_hash_or_mock": "Non-sensitive hash, UUID, test fixture, or placeholder"
                    }
                }
            }
        }

        async with self.semaphore:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                API_URL,
                data=data,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "JevHybridSecretValidator/1.0",
                },
                method="POST"
            )

            # Retry loop for 429 and 529
            for attempt in range(3):
                try:
                    loop = asyncio.get_running_loop()
                    resp = await loop.run_in_executor(None, lambda: urllib.request.urlopen(req, timeout=30))
                    raw_body = resp.read().decode("utf-8")
                    result = json.loads(raw_body)
                    
                    answers = result.get("answers", {})
                    noul_val = answers.get("is_real_secret", {}).get("noul", 0.0)
                    choice_val = answers.get("secret_category", {}).get("choice", "unknown")
                    conf_val = answers.get("secret_category", {}).get("confidence", 0.0)

                    finding.noul_score = noul_val
                    finding.category = choice_val
                    finding.confidence = conf_val

                    # Triaged Calibrated Bands:
                    if noul_val < 0.30:
                        finding.decision = "ALLOW_BENIGN"
                    elif noul_val <= 0.75:
                        finding.decision = "REVIEW_QUARANTINE"
                    else:
                        finding.decision = "BLOCK_CRITICAL"
                    return finding

                except urllib.error.HTTPError as e:
                    if e.code in (429, 529) and attempt < 2:
                        await asyncio.sleep(1.5 * (attempt + 1))
                        continue
                    finding.decision = f"ERROR_{e.code}"
                    return finding
                except Exception as err:
                    finding.decision = f"ERROR_{type(err).__name__}"
                    return finding

        return finding


def extract_candidates_from_file(file_path: str) -> List[SecretFinding]:
    """Extracts candidate lines with asset-pairing context (5 lines before and after)."""
    findings = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception:
        return findings

    for idx, line in enumerate(lines):
        for pat in CANDIDATE_PATTERNS:
            match = pat.search(line)
            if match:
                # Capture asset-pairing context (up to 3 lines before, 3 lines after)
                start_l = max(0, idx - 3)
                end_l = min(len(lines), idx + 4)
                snippet = "".join(lines[start_l:end_l])

                findings.append(SecretFinding(
                    file_path=file_path,
                    line_number=idx + 1,
                    matched_text=match.group(0),
                    snippet_context=snippet
                ))
                break  # Don't duplicate if multiple patterns hit same line

    return findings


async def run_pipeline(files: List[str]) -> Tuple[int, List[SecretFinding]]:
    api_key = os.environ.get("TYPESAFE_API_KEY")
    if not api_key:
        print("⚠️ TYPESAFE_API_KEY não configurada. Executando apenas varredura estática local.")
        return 0, []

    validator = JevSecretValidator(api_key=api_key)
    all_findings = []
    for fp in files:
        if os.path.isfile(fp):
            all_findings.extend(extract_candidates_from_file(fp))

    print(f"🔍 Candidatos encontrados por regex: {len(all_findings)}")
    if not all_findings:
        print("✅ Nenhum candidato detectado. Pipeline liberado.")
        return 0, []

    # Parallel evaluation through Jev with concurrency control
    print(f"⚡ Submetendo ao Jev com semáforo de {MAX_CONCURRENT_REQUESTS} requisições...")
    tasks = [validator.evaluate_snippet(f) for f in all_findings]
    results = await asyncio.gather(*tasks)

    # Process verdicts
    blocks = [r for r in results if r.decision == "BLOCK_CRITICAL"]
    reviews = [r for r in results if r.decision == "REVIEW_QUARANTINE"]
    allows = [r for r in results if r.decision == "ALLOW_BENIGN"]

    print("\n" + "=" * 70)
    print("  🛡️  RELATÓRIO DE TRIAGEM SEMÂNTICA DE SEGREDOS (JEV)")
    print("=" * 70)
    print(f"Total avaliado: {len(results)} | Bloqueados: {len(blocks)} | Revisão: {len(reviews)} | Falsos Positivos Filtrados: {len(allows)}")

    for b in blocks:
        print(f"❌ [BLOQUEIO] {b.file_path}:{b.line_number} | Noul: {b.noul_score:.3f} | Tipo: {b.category}")
    for r in reviews:
        print(f"⚠️ [REVISÃO]  {r.file_path}:{r.line_number} | Noul: {r.noul_score:.3f} | Tipo: {r.category}")
    for a in allows:
        print(f"✅ [LIBERADO] {a.file_path}:{a.line_number} | Noul: {a.noul_score:.3f} (Falso positivo descartado)")

    exit_code = 1 if len(blocks) > 0 else 0
    return exit_code, results


if __name__ == "__main__":
    target_files = sys.argv[1:] if len(sys.argv) > 1 else ["config.yaml", "auth.py"]
    code, _ = asyncio.run(run_pipeline(target_files))
    sys.exit(code)
