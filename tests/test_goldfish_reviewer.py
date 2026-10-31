#!/usr/bin/env python3
"""
Unit tests for skills/goldfish-reviewer/scripts/run_review.py.
Validates the Zero-Decision Rule, Heilmeier checks, Semantic Split, and Anti-Glazing checks.
"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "skills" / "goldfish-reviewer" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from run_review import audit_document


class TestGoldfishReviewer(unittest.TestCase):
    def test_compliant_spec_passes(self):
        doc = """# Feature: Webhook Delivery

## Overview & Architecture
Objetivo: Implementar entrega de webhooks com garantia de entrega at-least-once.
Hoje as notificações são feitas por polling, o que gera latência e sobrecarga.
Risco: Falhas transitórias no endpoint de destino podem causar sobrecarga de retries.
Métrica: Taxa de entrega com sucesso > 99.9% e testes de concorrência automatizados.

## Plano de Implementação
Fase 1: Criar schema de dados para eventos de webhook em `src/webhooks/schema.ts`.
Fase 2: Implementar serviço de envio com retry exponencial em `src/webhooks/sender.ts`.
Fase 3: Criar suíte de testes em `tests/test_webhooks.py`.
"""
        with tempfile.NamedTemporaryFile("w+", suffix=".md", encoding="utf-8") as f:
            f.write(doc)
            f.flush()
            res = audit_document(Path(f.name))
            self.assertTrue(res["passed"])
            self.assertEqual(res["status"], "PASS")
            self.assertEqual(res["summary"]["critical"], 0)

    def test_undecided_marker_fails_zero_decision_rule(self):
        doc = """# Feature: Nova Autenticação

## Arquitetura
Objetivo: Migrar para JWT com rotação de chaves. Hoje usamos sessões em memória.
Risco: Desconexão de sessões ativas. Métrica de sucesso: zero downtime.

## Plano de Implementação
Fase 1: Atualizar `src/auth/service.ts`.
Fase 2: Escolher biblioteca de JWT a definir depois. TODO: decidir algoritmo de hash.
"""
        with tempfile.NamedTemporaryFile("w+", suffix=".md", encoding="utf-8") as f:
            f.write(doc)
            f.flush()
            res = audit_document(Path(f.name))
            self.assertFalse(res["passed"])
            self.assertEqual(res["status"], "FAIL")
            self.assertGreater(res["summary"]["critical"], 0)
            critical_msgs = [finding["message"] for finding in res["findings"] if finding["severity"] == "CRITICAL"]
            self.assertTrue(any("Open design decision" in msg for msg in critical_msgs))

    def test_missing_semantic_split_flagged(self):
        doc = """# Simple Note
Apenas uma nota sem seções formais de arquitetura ou plano.
"""
        with tempfile.NamedTemporaryFile("w+", suffix=".md", encoding="utf-8") as f:
            f.write(doc)
            f.flush()
            res = audit_document(Path(f.name))
            self.assertFalse(res["passed"])
            self.assertTrue(any(f["category"] == "Semantic Split" for f in res["findings"]))

    def test_banned_adjectives_flagged(self):
        doc = """# Feature: Ultra Fast Cache

## Arquitetura
Objetivo: Adicionar um cache blazingly fast e seamless para acelerar queries.
Hoje é lento. Risco: cache stampede. Métricas: latência P99 < 5ms.

## Plano de Implementação
Modificar `src/cache.ts` com TTL fixo.
"""
        with tempfile.NamedTemporaryFile("w+", suffix=".md", encoding="utf-8") as f:
            f.write(doc)
            f.flush()
            res = audit_document(Path(f.name))
            glazing_findings = [f for f in res["findings"] if f["category"] == "Anti-Glazing"]
            self.assertGreater(len(glazing_findings), 0)


if __name__ == "__main__":
    unittest.main()
