#!/usr/bin/env python3
"""
Unit tests for skills/full-app-validator/scripts/health_card.py.
Validates 360 health evaluation, non-overlap domain scoring, and markdown formatting.
"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "skills" / "full-app-validator" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from health_card import (
    DomainHealth,
    FullAppHealthReport,
    evaluate_repository_health,
    format_health_card_markdown,
)


class TestFullAppValidator(unittest.TestCase):
    def test_evaluate_health_on_empty_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            report = evaluate_repository_health(tmppath)

            self.assertIsInstance(report, FullAppHealthReport)
            self.assertEqual(len(report.domains), 5)
            self.assertIn("edge", report.domains)
            self.assertIn("core", report.domains)
            self.assertIn("persistence", report.domains)
            self.assertIn("quality", report.domains)
            self.assertIn("devops", report.domains)
            self.assertTrue(0 <= report.overall_score <= 100)

    def test_evaluate_health_on_structured_app(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            # Create minimal app structure
            (tmppath / "src" / "routes").mkdir(parents=True)
            (tmppath / "src" / "services").mkdir(parents=True)
            (tmppath / "prisma").mkdir(parents=True)
            (tmppath / "tests").mkdir(parents=True)
            (tmppath / ".github" / "workflows").mkdir(parents=True)
            (tmppath / "Dockerfile").touch()
            (tmppath / "openapi.yaml").touch()
            (tmppath / "CONTEXT.md").touch()
            (tmppath / "tests" / "test_sample.py").write_text("def test_ok(): pass\n")

            report = evaluate_repository_health(tmppath)

            # High scores expected due to proper boundary structure
            self.assertGreaterEqual(report.domains["edge"].score, 80)
            self.assertGreaterEqual(report.domains["core"].score, 80)
            self.assertGreaterEqual(report.domains["persistence"].score, 70)
            self.assertGreaterEqual(report.domains["quality"].score, 60)
            self.assertGreaterEqual(report.domains["devops"].score, 80)
            self.assertGreaterEqual(report.overall_score, 75)

    def test_format_health_card_markdown(self):
        report = FullAppHealthReport(
            project_name="test-app",
            overall_score=85,
            domains={
                "edge": DomainHealth("1. Borda & Contratos (API/Edge)", 90, "OPTIMAL", ["Rotas OK"], [], []),
                "core": DomainHealth("2. Domínio & Regras de Negócio", 85, "OPTIMAL", ["Services OK"], [], []),
                "persistence": DomainHealth("3. Persistência & Dados (DB)", 80, "ACCEPTABLE", ["Prisma OK"], [], []),
                "quality": DomainHealth("4. Qualidade & Testes (QA/TDD)", 85, "OPTIMAL", ["Pytest OK"], [], []),
                "devops": DomainHealth("5. DevOps, CI/CD & Resiliência", 85, "OPTIMAL", ["CI OK"], [], []),
            },
            top_priorities=["[Borda] Adicionar .strict() nos schemas Zod."],
        )

        md = format_health_card_markdown(report)
        self.assertIn("# 🏥 Health Card 360° da Aplicação: `test-app`", md)
        self.assertIn("Pontuação Geral de Maturidade:** `85/100`", md)
        self.assertIn("Borda & Contratos (API/Edge)", md)
        self.assertIn("🟢 OPTIMAL", md)
        self.assertIn("Principais Ações Recomendadas (Zero Overkill)", md)
        self.assertIn("[Borda] Adicionar .strict() nos schemas Zod.", md)


if __name__ == "__main__":
    unittest.main()
