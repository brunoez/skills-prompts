#!/usr/bin/env python3
"""
Three-Layer PII Sanitization Guardrail with Jev (TypeSafe AI)
============================================================
Detects, disambiguates, and masks Personally Identifiable Information (PII)
using a hybrid 3-layer architecture:
  Layer 1: Deterministic local regex + corporate allowlist.
  Layer 2: Jev parallel Gate (13 PII Nouls + 3-level sensitivity Score).
  Layer 3: Semantic disambiguation (Credit Cards vs Order Numbers vs Serials).

Inspired by `coo-quack/jev-pii-checker` and IBM PII taxonomy.
"""

import json
import os
import re
import sys
import urllib.request
from typing import Any, Dict, List, Tuple

API_URL = "https://api.typesafe.ai/v1/systemone"
MODEL_NAME = "jev-1.13.0"

# Layer 1: Deterministic Regex
EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
PHONE_REGEX = re.compile(r'(?:\+?55\s?)?(?:\(?\d{2}\)?\s?)?(?:9\d{4}[-.\s]?\d{4}|\d{4}[-.\s]?\d{4})')
DIGITS_REGEX = re.compile(r'\b\d{9,16}\b')

# Regexes específicos para documentos brasileiros formatados
CPF_REGEX = re.compile(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b')
RG_REGEX = re.compile(r'\b\d{1,2}\.\d{3}\.\d{3}-[0-9Xx]\b')
CNH_REGEX = re.compile(r'\b(?:CNH\s*[:=]?\s*)(\d{11})\b', re.IGNORECASE)

CORPORATE_EMAILS = {"noreply@", "support@", "contato@", "info@", "alerts@"}


def validate_cpf(cpf: str) -> bool:
    """Valida matematicamente os dígitos verificadores do CPF via Módulo 11."""
    digits = [int(c) for c in re.sub(r'\D', '', cpf)]
    if len(digits) != 11 or len(set(digits)) == 1:
        return False
    # Primeiro dígito verificador
    s1 = sum(digits[i] * (10 - i) for i in range(9))
    d1 = 0 if (s1 % 11) < 2 else 11 - (s1 % 11)
    if digits[9] != d1:
        return False
    # Segundo dígito verificador
    s2 = sum(digits[i] * (11 - i) for i in range(10))
    d2 = 0 if (s2 % 11) < 2 else 11 - (s2 % 11)
    return digits[10] == d2


def mask_cpf(cpf: str) -> str:
    """Aplica máscara LGPD de CPF mantendo contorno: 123.***.***-00."""
    clean = re.sub(r'\D', '', cpf)
    if len(clean) == 11:
        return f"{clean[:3]}.***.***-{clean[-2:]}"
    return f"{cpf[:3]}...{cpf[-2:]}"


def mask_string(val: str) -> str:
    """Masks a generic sensitive string using first2...last1 notation."""
    if len(val) <= 4:
        return "****"
    return f"{val[:2]}...{val[-1]}"


class PIISanitizer:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def _call_jev(self, state: Dict[str, Any], questions: Dict[str, Any]) -> Dict[str, Any]:
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
                "User-Agent": "PIISanitizer/1.0"
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            return {"error": str(e)}

    def sanitize_text(self, text: str) -> Tuple[str, Dict[str, Any]]:
        # Layer 1: Local Regex Extraction & Validation
        extracted_emails = [e for e in EMAIL_REGEX.findall(text) if not any(c in e.lower() for c in CORPORATE_EMAILS)]
        extracted_phones = PHONE_REGEX.findall(text)
        
        # Documentos Brasileiros Formatados
        extracted_cpfs = [cpf for cpf in CPF_REGEX.findall(text) if validate_cpf(cpf)]
        extracted_rgs = RG_REGEX.findall(text)
        extracted_cnhs = CNH_REGEX.findall(text)
        
        # Dígitos numéricos não formatados (10 a 16 dígitos)
        candidate_digits = [d for d in DIGITS_REGEX.findall(text) if d not in extracted_cpfs and d not in extracted_cnhs]

        # Layer 2: Jev Parallel Gate
        gate_questions = {
            "sensitivity_level": {
                "type": "score",
                "instructions": "Rate the overall privacy sensitivity of the personal information in this text based on the IBM PII taxonomy.",
                "criteria": [
                    "none - No personal data or only generic public company information",
                    "low - Business contact details or public event attendees",
                    "high - Medical diagnosis, government ID (CPF, RG, CNH), credit card, or sensitive personal data"
                ]
            },
            "has_person_name": {
                "type": "noul",
                "instructions": "Does the text contain the real personal name of an identifiable human?"
            },
            "has_brazilian_gov_id": {
                "type": "noul",
                "instructions": "Does the text mention or contain a Brazilian government identification document (CPF, RG, CNH, Titulo de Eleitor)?"
            }
        }

        # Layer 3: Se houver sequências numéricas não formatadas, desambiguar com Jev Choice
        if candidate_digits:
            gate_questions["digit_classification"] = {
                "type": "choice",
                "instructions": f"Classify the semantic nature of the numeric sequence `{candidate_digits[0]}` in the text context.",
                "criteria": {
                    "cpf_sem_mascara": "Unformatted 11-digit Brazilian CPF number",
                    "cnh_document": "11-digit Brazilian Driver's License (CNH)",
                    "credit_card": "Payment credit card number (13-16 digits)",
                    "order_or_serial": "Ecommerce order number, invoice tracking, or hardware product serial",
                    "other_numeric": "Unspecified numeric sequence"
                }
            }

        jev_resp = self._call_jev(state={"text": text}, questions=gate_questions)
        answers = jev_resp.get("answers", {})

        score_info = answers.get("sensitivity_level", {})
        sensitivity_score = score_info.get("score", 0.0)
        p_name = answers.get("has_person_name", {}).get("noul", 0.0)
        p_gov_id = answers.get("has_brazilian_gov_id", {}).get("noul", 0.0)
        digit_type = answers.get("digit_classification", {}).get("choice", "other_numeric")

        # Layer 4: Mascaramento Determinístico
        sanitized = text
        for email in extracted_emails:
            sanitized = sanitized.replace(email, mask_string(email))
        for phone in extracted_phones:
            sanitized = sanitized.replace(phone, mask_string(phone))
        for cpf in extracted_cpfs:
            sanitized = sanitized.replace(cpf, mask_cpf(cpf))
        for rg in extracted_rgs:
            sanitized = sanitized.replace(rg, mask_string(rg))
        for cnh in extracted_cnhs:
            sanitized = sanitized.replace(cnh, mask_string(cnh))

        # Mascarar dígitos não formatados se Jev classificou como documento ou cartão
        if digit_type in ("cpf_sem_mascara", "cnh_document", "credit_card"):
            for d in candidate_digits:
                if digit_type == "cpf_sem_mascara" and validate_cpf(d):
                    sanitized = sanitized.replace(d, mask_cpf(d))
                else:
                    sanitized = sanitized.replace(d, mask_string(d))

        report = {
            "sensitivity_score": sensitivity_score,
            "sensitivity_tier": "high" if sensitivity_score >= 1.8 else ("low" if sensitivity_score >= 0.8 else "none"),
            "probabilities": {
                "person_name": p_name,
                "brazilian_gov_id": p_gov_id,
            },
            "digit_classification": digit_type,
            "detected_brazilian_docs": {
                "cpf_count": len(extracted_cpfs) + (1 if digit_type == "cpf_sem_mascara" else 0),
                "rg_count": len(extracted_rgs),
                "cnh_count": len(extracted_cnhs) + (1 if digit_type == "cnh_document" else 0)
            },
            "masked_items_count": (
                len(extracted_emails) + len(extracted_phones) +
                len(extracted_cpfs) + len(extracted_rgs) + len(extracted_cnhs) +
                (len(candidate_digits) if digit_type in ("cpf_sem_mascara", "cnh_document", "credit_card") else 0)
            )
        }

        return sanitized, report


def main():
    api_key = os.environ.get("TYPESAFE_API_KEY")
    if not api_key:
        print("⚠️ TYPESAFE_API_KEY não configurada. Executando validação local de documentos brasileiros.")
        sample_cpf_valid = "123.456.789-09"
        is_valid = validate_cpf(sample_cpf_valid)
        print(f"Validação matemática local do CPF '{sample_cpf_valid}': {is_valid}")
        masked = mask_cpf(sample_cpf_valid)
        print(f"Máscara LGPD do CPF: {masked}")
        sys.exit(0)

    sample = (
        "Olá, favor confirmar a internação do paciente Carlos Drummond de Andrade, "
        "CPF 123.456.789-09, RG 12.345.678-9, CNH 12345678901, "
        "contato carlos.drummond@email.com.br, telefone (11) 98765-4321."
    )

    sanitizer = PIISanitizer(api_key=api_key)
    masked_text, report = sanitizer.sanitize_text(sample)

    print("=== TEXTO SANITIZADO (LGPD) ===")
    print(masked_text)
    print("\n=== RELATÓRIO DE PII BRASILEIRO ===")
    print(json.dumps(report, indent=2, ensure_ascii=False))

    if report["sensitivity_tier"] == "high":
        print("\n❌ ALERTA: Documentos pessoais brasileiros de alta criticidade detectados!")
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()

