#!/usr/bin/env python3
"""
Full App Validator - 360° Health Card Generator.
Analyzes application boundaries (Edge, Core, Persistence, Tests, DevOps)
and produces a consolidated 360° Health Card without overlap or overkill.
Standard library only (zero external pip dependencies).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class DomainHealth:
    name: str
    score: int  # 0 to 100
    status: str  # OPTIMAL, ACCEPTABLE, ATTENTION, CRITICAL
    strengths: List[str] = field(default_factory=list)
    gaps: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class FullAppHealthReport:
    project_name: str
    overall_score: int
    domains: Dict[str, DomainHealth] = field(default_factory=dict)
    top_priorities: List[str] = field(default_factory=list)


def evaluate_repository_health(root_dir: Path) -> FullAppHealthReport:
    """Performs deterministic, non-overkill structural inspection of the application."""
    root = root_dir.resolve()
    project_name = root.name

    # 1. Edge & Contracts Boundary (Borda / API)
    edge_strengths = []
    edge_gaps = []
    edge_recs = []
    edge_score = 70

    has_openapi = any((root / f).is_file() for f in ["openapi.yaml", "openapi.json", "swagger.yaml", "swagger.json"])
    has_routes = any((root / d).is_dir() for d in ["src/routes", "src/controllers", "app/api", "routes", "controllers"])
    has_zod_or_pydantic = False

    # Shallow scan for schema validation
    for p in root.glob("**/schema*.ts"):
        has_zod_or_pydantic = True
        break
    if not has_zod_or_pydantic:
        for p in root.glob("**/models.py"):
            has_zod_or_pydantic = True
            break

    if has_routes:
        edge_strengths.append("Camada de roteamento e controllers identificada.")
    else:
        edge_gaps.append("Rotas ou controllers não encontrados em diretórios padronizados.")
        edge_score -= 20

    if has_openapi or has_zod_or_pydantic:
        edge_strengths.append("Contratos de interface tipados / OpenAPI presentes.")
        edge_score += 15
    else:
        edge_gaps.append("Ausência de especificações OpenAPI ou schemas estritos de validação (Zod/Pydantic).")
        edge_recs.append("Adotar validação de schema na borda com .strict() para bloquear Mass Assignment.")
        edge_score -= 15

    edge_score = max(10, min(100, edge_score))
    edge_status = "OPTIMAL" if edge_score >= 85 else ("ACCEPTABLE" if edge_score >= 70 else ("ATTENTION" if edge_score >= 50 else "CRITICAL"))

    # 2. Core Business Domain (Regras de Negócio)
    core_strengths = []
    core_gaps = []
    core_recs = []
    core_score = 65

    has_services = any((root / d).is_dir() for d in ["src/services", "src/domain", "app/services", "domain", "core"])
    has_context = (root / "CONTEXT.md").is_file() or (root / "docs").is_dir()

    if has_services:
        core_strengths.append("Separação de regras de negócio em camada de serviços/domínio.")
        core_score += 20
    else:
        core_gaps.append("Lógica de negócio acoplada diretamente em controllers ou sem camada de serviço.")
        core_recs.append("Desacoplar invariantes de negócio dos handlers de protocolo HTTP.")
        core_score -= 20

    if has_context:
        core_strengths.append("Documentação de contexto de domínio / CONTEXT.md disponível.")
        core_score += 15
    else:
        core_recs.append("Documentar termos e invariantes de domínio em CONTEXT.md.")
        core_score -= 10

    core_score = max(10, min(100, core_score))
    core_status = "OPTIMAL" if core_score >= 85 else ("ACCEPTABLE" if core_score >= 70 else ("ATTENTION" if core_score >= 50 else "CRITICAL"))

    # 3. Persistence & Data Boundary (Banco de Dados)
    db_strengths = []
    db_gaps = []
    db_recs = []
    db_score = 65

    has_prisma = (root / "prisma").is_dir() or (root / "schema.prisma").is_file()
    has_migrations = any(len(list(root.glob(f"**/{m}"))) > 0 for m in ["migrations", "alembic"])
    has_db_layer = has_prisma or any((root / d).is_dir() for d in ["src/models", "src/db", "app/models", "database"])

    if has_db_layer:
        db_strengths.append("Camada de persistência / ORM configurada.")
        db_score += 20
    else:
        db_gaps.append("Camada de persistência explícita não localizada.")
        db_score -= 20

    if has_migrations:
        db_strengths.append("Histórico de migrações versionado.")
        db_score += 15
    else:
        db_recs.append("Versionar migrações de banco de dados para evitar schema drift.")
        db_score -= 10


    db_score = max(10, min(100, db_score))
    db_status = "OPTIMAL" if db_score >= 85 else ("ACCEPTABLE" if db_score >= 70 else ("ATTENTION" if db_score >= 50 else "CRITICAL"))

    # 4. Quality & Test Pyramid (Testes & Confiabilidade)
    test_strengths = []
    test_gaps = []
    test_recs = []
    test_score = 50

    has_tests = any((root / d).is_dir() for d in ["tests", "__tests__", "test", "spec"])
    test_files_count = len(list(root.glob("**/*.test.*"))) + len(list(root.glob("**/*.spec.*"))) + len(list(root.glob("**/test_*.py")))

    if has_tests or test_files_count > 0:
        test_strengths.append(f"Suíte de testes presente ({test_files_count} arquivos de teste detectados).")
        test_score = 80 if test_files_count >= 5 else 65
    else:
        test_gaps.append("Nenhum arquivo de teste automatizado detectado no repositório.")
        test_recs.append("Adotar TDD/SecDD e implementar testes unitários e de integração mínimos.")
        test_score = 25

    test_score = max(10, min(100, test_score))
    test_status = "OPTIMAL" if test_score >= 85 else ("ACCEPTABLE" if test_score >= 70 else ("ATTENTION" if test_score >= 50 else "CRITICAL"))

    # 5. DevOps, SRE & CI/CD (Operações & Resiliência)
    ops_strengths = []
    ops_gaps = []
    ops_recs = []
    ops_score = 60

    has_ci = (root / ".github/workflows").is_dir() or (root / ".gitlab-ci.yml").is_file()
    has_docker = (root / "Dockerfile").is_file() or (root / "docker-compose.yml").is_file()

    if has_ci:
        ops_strengths.append("Pipeline de CI/CD automatizado configurado.")
        ops_score += 20
    else:
        ops_gaps.append("Ausência de esteira de CI/CD automatizada.")
        ops_recs.append("Configurar pipeline de CI/CD para execução contínua de linters e testes.")
        ops_score -= 20

    if has_docker:
        ops_strengths.append("Definição de containerização (Dockerfile/Compose) presente.")
        ops_score += 15
    else:
        ops_recs.append("Padronizar ambiente com Dockerfile multi-stage e usuário rootless.")

    ops_score = max(10, min(100, ops_score))
    ops_status = "OPTIMAL" if ops_score >= 85 else ("ACCEPTABLE" if ops_score >= 70 else ("ATTENTION" if ops_score >= 50 else "CRITICAL"))

    domains = {
        "edge": DomainHealth("1. Borda & Contratos (API/Edge)", edge_score, edge_status, edge_strengths, edge_gaps, edge_recs),
        "core": DomainHealth("2. Domínio & Regras de Negócio", core_score, core_status, core_strengths, core_gaps, core_recs),
        "persistence": DomainHealth("3. Persistência & Dados (DB)", db_score, db_status, db_strengths, db_gaps, db_recs),
        "quality": DomainHealth("4. Qualidade & Testes (QA/TDD)", test_score, test_status, test_strengths, test_gaps, test_recs),
        "devops": DomainHealth("5. DevOps, CI/CD & Resiliência", ops_score, ops_status, ops_strengths, ops_gaps, ops_recs),
    }

    overall_score = round(sum(d.score for d in domains.values()) / len(domains))

    # Top Priorities (Quick Wins & Strategic Actions)
    top_priorities = []
    for d in domains.values():
        for rec in d.recommendations[:1]:
            top_priorities.append(f"[{d.name.split('.')[1].strip().split('(')[0].strip()}] {rec}")

    return FullAppHealthReport(
        project_name=project_name,
        overall_score=overall_score,
        domains=domains,
        top_priorities=top_priorities[:4],
    )


def format_health_card_markdown(report: FullAppHealthReport) -> str:
    status_emoji = {
        "OPTIMAL": "🟢",
        "ACCEPTABLE": "🟡",
        "ATTENTION": "🟠",
        "CRITICAL": "🔴",
    }

    lines = [
        f"# 🏥 Health Card 360° da Aplicação: `{report.project_name}`",
        "",
        f"**Pontuação Geral de Maturidade:** `{report.overall_score}/100`",
        "",
        "---",
        "",
        "## 📊 Visão Geral por Fronteira de Domínio (Zero Overlap)",
        "",
        "| Fronteira de Arquitetura | Score | Status | Diagnóstico Resumido |",
        "| :--- | :---: | :---: | :--- |",
    ]

    for d in report.domains.values():
        emoji = status_emoji.get(d.status, "⚪")
        diag = d.strengths[0] if d.strengths else (d.gaps[0] if d.gaps else "Análise concluída.")
        lines.append(f"| **{d.name}** | `{d.score}/100` | {emoji} {d.status} | {diag} |")

    lines.extend([
        "",
        "---",
        "",
        "## 🎯 Principais Ações Recomendadas (Zero Overkill)",
        "",
    ])

    for i, prio in enumerate(report.top_priorities, 1):
        lines.append(f"{i}. {prio}")

    lines.extend([
        "",
        "---",
        "",
        "## 🔍 Detalhamento por Fronteira de Responsabilidade",
        "",
    ])

    for d in report.domains.values():
        lines.append(f"### {d.name} (`{d.score}/100`)")
        if d.strengths:
            lines.append("**Pontos Fortes:**")
            for s in d.strengths:
                lines.append(f"- ✅ {s}")
        if d.gaps:
            lines.append("**Lacunas Identificadas:**")
            for g in d.gaps:
                lines.append(f"- ⚠️ {g}")
        if d.recommendations:
            lines.append("**Recomendações Práticas:**")
            for r in d.recommendations:
                lines.append(f"- 💡 {r}")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Full App Validator - Generate 360° Health Card without overlap or overkill.")
    parser.add_argument("-r", "--root", default=".", help="Root directory of the application to validate (default: .)")
    parser.add_argument("-o", "--output", help="Optional path to write output markdown report")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()
    report = evaluate_repository_health(Path(args.root))

    if args.json:
        data = {
            "project_name": report.project_name,
            "overall_score": report.overall_score,
            "domains": {k: asdict(v) for k, v in report.domains.items()},
            "top_priorities": report.top_priorities,
        }
        output_str = json.dumps(data, indent=2, ensure_ascii=False)
    else:
        output_str = format_health_card_markdown(report)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_str, encoding="utf-8")
        print(f"✅ Health Card 360° gerado com sucesso em: {args.output}")
    else:
        print(output_str)

    return 0


if __name__ == "__main__":
    sys.exit(main())
