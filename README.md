# 🛡️ Suíte de Prompts & Agent Skills de Engenharia de Software, AppSec & Yellow Team

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Release](https://img.shields.io/github/v/release/brunoez/prompts?color=blue)](https://github.com/brunoez/prompts/releases/latest)
[![CI Status](https://github.com/brunoez/prompts/actions/workflows/ci.yml/badge.svg)](https://github.com/brunoez/prompts/actions)
[![GitLab CI](https://img.shields.io/badge/GitLab%20CI-Passing-22c55e?logo=gitlab)](.gitlab-ci.yml)
[![Language](https://img.shields.io/badge/Language-pt--BR-009c3b.svg)](README.md)

**A biblioteca definitiva de prompts estruturados e Agent Skills executáveis de auditoria profunda, arquitetura defensiva e metodologias *Driven Development* para desenvolvedores, arquitetos e agentes de Inteligência Artificial.**

[Instalação Rápida](#-instalação-rápida) • [Agent Skills](#-agent-skills-antigravity-claude-code-cursor--windsurf) • [Uso em CI/CD Privado](#-como-executar-os-prompts-em-cicd-no-seu-projeto-privado) • [Qual Prompt Usar?](#-qual-prompt-usar-guia-de-ação-rápida-com-exemplos) • [Catálogo Completo](#-catálogo-completo-de-prompts) • [Contribuição](CONTRIBUTING.md)

</div>

---

## 🇧🇷 Sobre o Projeto

Criado com foco na comunidade brasileira de desenvolvimento e AppSec, este repositório aberto reúne **prompts técnicos e Agent Skills de alto nível** projetados para serem executados por Engenheiros Principais ou Agentes de IA (**Claude Code**, **Google Antigravity**, **VSCode** / GitHub Copilot, **Cursor** e outros editores como Windsurf).

O objetivo é transformar a velocidade do **Vibe Coding** em software de **nível corporativo**: seguro contra vulnerabilidades (**OWASP ASTF 2023**, **WSTG v4.2**, **OWASP Top 10 Proactive Controls 2024**, **OWASP ASVS v4.0.3**, **OWASP Risk Rating Methodology** e **OWASP Cheat Sheet Series**), arquiteturalmente consistente (DDD/SDD), resiliente em produção (SRE) e 100% testado (TDD, BDD, SecDD).

---

## ⚡ Instalação Rápida

Instale a suíte de prompts no seu projeto com um único comando:

```bash
curl -sSL https://raw.githubusercontent.com/brunoez/prompts/main/install.sh | bash
```

> **Dica de Ferramenta & IDE:** Por padrão, os prompts são instalados no diretório oficial do **Claude Code** (`.claude/prompts/`). Se você usa **VSCode**, **Cursor** ou outros editores:
> ```bash
> # Para Claude Code (padrão oficial em .claude/prompts/):
> curl -sSL https://raw.githubusercontent.com/brunoez/prompts/main/install.sh | bash
> 
> # Para VSCode (.agent/prompts/):
> curl -sSL https://raw.githubusercontent.com/brunoez/prompts/main/install.sh | bash -s -- . vscode
> 
> # Para Cursor (.cursor/rules/):
> curl -sSL https://raw.githubusercontent.com/brunoez/prompts/main/install.sh | bash -s -- . cursor
> 
> # Para todas as ferramentas simultaneamente (.claude, .agent, .cursor, .windsurf):
> curl -sSL https://raw.githubusercontent.com/brunoez/prompts/main/install.sh | bash -s -- . all
> ```

---

### 📁 Estrutura de Diretórios Gerada no Projeto

```plaintext
seu-projeto/
├── .claude/prompts/              # Prompts oficiais para Claude Code (ou .agent/prompts/)
│   ├── driven-development/       # Metodologias & Testes
│   │   ├── bdd_behavior_driven.md     # BDD & Gherkin
│   │   ├── cdd_contract_driven.md     # Contratos & OpenAPI
│   │   ├── project_context.md         # Dicionário & Regras IA
│   │   ├── sdd_spec_driven.md         # SDD & Schemas Zod
│   │   ├── secdd_abuse_cases.md       # Casos de Abuso & SecDD
│   │   ├── tdd_test_driven.md         # TDD Red-Green-Refactor
│   │   ├── test_suite_generator.md    # Gerador de Testes QA
│   │   └── technical_documentation.md # Docs-as-Code & C4
│   ├── security/                 # Auditorias de AppSec (OWASP ASTF / WSTG / Proactive Controls)
│   │   ├── access_control.md          # Proactive C1 – Autorização & IDOR/BOLA
│   │   ├── ai_appsec.md               # OWASP LLM Top 10
│   │   ├── api.md                     # OWASP API Top 10 (ASTF)
│   │   ├── authn_identity.md          # Proactive C7 – Autenticação, Sessão, MFA & OIDC
│   │   ├── business.md                # Fraudes & Idempotência
│   │   ├── db.md                      # OWASP DB & Concorrência
│   │   ├── frontend.md                # Trusted Types, CSP & SPAs
│   │   ├── input_validation.md        # Proactive C3 – Validação de Entrada & Exceções
│   │   ├── secrets.md                 # TruffleHog3 & Argon2id
│   │   ├── secure_config.md           # Proactive C5 – Config Segura, Headers & CORS
│   │   ├── ssrf.md                    # Proactive C10 – Server-Side Request Forgery
│   │   ├── supply_chain.md            # SCVS, SBOM & Anti-Slopsquatting
│   │   └── threat_modeling.md         # Modelagem STRIDE-per-Element
│   ├── devops/                   # Infraestrutura & SRE
│   │   ├── cicd_pipeline.md           # Hardening de CI/CD & OIDC
│   │   ├── iac_docker_k8s.md          # Docker Rootless & K8s
│   │   └── resilience_observability.md# SRE & OpenTelemetry
│   └── jev/                      # TypeSafe AI – Decisões System One & Anti-Overkill
│       ├── system_one_architecture.md # Arquitetura em Cascata & Refatoração System 1
│       ├── agent_guardrails_safety.md # Guardrails Pré-Execução de Tools em Agentes
│       ├── intent_routing_dispatch.md # Roteamento de Intenção & Speculative Fan-out
│       ├── rag_verification_guardrails.md # Verificação de RAG & Fidedignidade de Citações
│       ├── secret_detection_triage.md # Triagem Semântica de Segredos & Redução de Falsos Positivos
│       ├── mcp_agent_security_scan.md # Auditoria de Segurança de Agent Skills & Servidores MCP
│       ├── pii_sanitization_guardrail.md # Sanitização e Mascaramento de PII em Três Camadas
│       └── vulnerability_triage_cvss.md # Triagem de Falhas e Cálculo Determinístico de CVSS v3.1/v4.0
├── skills/                       # Agent Skills Executáveis (Padrão aberto agentskills.io)
│   ├── appsec-auditor/           # Auditoria completa OWASP com geradores SARIF & relatórios
│   │   ├── SKILL.md              # Workflow em 4 fases e gatilhos autônomos
│   │   ├── references/           # Guias técnicos sob demanda (ASTF, ASVS, BOLA, SSRF)
│   │   ├── scripts/              # sarif_builder.py & report_generator.py
│   │   └── examples/             # Teste BOLA pytest & fetch seguro TypeScript
│   └── jev-system-one/           # Decisões e Guardrails de Alta Velocidade (<100ms)
│       ├── SKILL.md              # Primitivas Choice, Score, Noul e cascades
│       ├── references/           # API Reference, Primitivas e Anti-Patterns
│       └── examples/             # Guardrails LangChain, TS Cascade, CVSS e PII
├── src/                          # Código da sua aplicação
├── tests/                        # Testes automatizados
├── docs/                         # Relatórios em PDF e SARIF
├── CONTEXT.md                    # Dicionário do negócio
└── CLAUDE.md / .github/copilot-instructions.md / .cursorrules # Regras de IA do projeto
```

---

## 🧠 Agent Skills (Antigravity, Claude Code, Cursor & Windsurf)

Além dos prompts estruturados invocados manualmente via `@`, este repositório disponibiliza **Agent Skills** nativas em conformidade com o padrão aberto [Agent Skills](https://agentskills.io/specification). As skills habilitam **ativação semântica autônoma** (`Use when...`), **Progressive Disclosure** (carregamento sob demanda para não estourar o contexto) e **scripts executáveis determinísticos**.

| Skill | Especialidade | Entregáveis & Ferramentas Integradas |
| :--- | :--- | :--- |
| [`skills/appsec-auditor`](skills/appsec-auditor/SKILL.md) | **Auditoria de Segurança AppSec (OWASP ASTF / ASVS L2)** | - Fluxo de auditoria em 4 fases com filtro anti-fadiga e cálculo OWASP Risk Rating<br/>- `scripts/sarif_builder.py`: Gerador de relatórios SARIF 2.1.0 para GitHub Security<br/>- `scripts/report_generator.py`: Gerador de relatórios executivos em Markdown e Issues GitHub<br/>- `references/`: Guias modulares (ASTF API, ASVS L2, BOLA/IDOR, SSRF & Egress)<br/>- `examples/`: Teste de abuso BOLA em pytest e cliente fetch seguro em TypeScript |
| [`skills/jev-system-one`](skills/jev-system-one/SKILL.md) | **Decisões Estruturadas & Guardrails System One (TypeSafe AI)** | - Padrão de Two-Model Cascade (System 1 para decisões <100ms + System 2 para raciocínio)<br/>- Primitivas `Choice`, `Score` e `Noul` com calibração de probabilidade<br/>- `references/`: HTTP API Reference, Primitivas e Jaggedness / Anti-Patterns<br/>- `examples/`: Guardrails LangChain, cascade em TypeScript, scanner híbrido de segredos, auditor de MCP e cálculo de CVSS |

---

## 🤖 Como Executar os Prompts em CI/CD no seu Projeto Privado

Você pode integrar a suíte de prompts na esteira de CI/CD da sua empresa para que um **Agente de IA audite automaticamente cada Pull Request**, gere o relatório em PDF, publique vulnerabilidades na aba **Security / Code Scanning** do GitHub via **SARIF** e abra tickets automáticos no seu gerenciador de tarefas.

Disponibilizamos modelos prontos para copiar e colar na pasta [`examples/ci-cd/`](examples/ci-cd/):

### 📋 Pipelines Prontos
* **GitHub Actions:** [`examples/ci-cd/github-actions-audit.yml`](examples/ci-cd/github-actions-audit.yml)  
  *Executa o agente em Pull Requests, publica o arquivo `results.sarif` na aba Security, salva o PDF como artefato de build e sincroniza com GitHub Issues / Jira.*
* **GitLab CI:** [`examples/ci-cd/gitlab-ci-audit.yml`](examples/ci-cd/gitlab-ci-audit.yml)  
  *Integração nativa com GitLab SAST reports, retenção de relatórios PDF e sincronização com GitLab Issues & Boards.*

### 🎫 Sincronizadores Automáticos de Tickets (Zero Duplicatas)
* **GitHub Issues:** [`examples/ci-cd/github_issues_sync.py`](examples/ci-cd/github_issues_sync.py) — Cria issues detalhadas com labels `severity:critical`/`high` de forma nativa via `${{ secrets.GITHUB_TOKEN }}`.
* **GitLab Issues & Boards:** [`examples/ci-cd/gitlab_issues_sync.py`](examples/ci-cd/gitlab_issues_sync.py) — Cria issues no GitLab com scoped labels (`severity::critical`) para quadros de gestão.
* **Jira (Atlassian):** [`examples/ci-cd/jira_sync.py`](examples/ci-cd/jira_sync.py) — Cria cards de Bug via Jira REST API v3 com formatação rica ADF e consulta JQL anti-duplicação.
* 📖 **Guia Completo de Configuração:** Consulte o [`examples/ci-cd/README.md`](examples/ci-cd/README.md) para o passo a passo de configuração de tokens e secrets.

---

## 💡 Qual Prompt Usar? (Guia de Ação Rápida com Exemplos)

### 🛡️ 1. Segurança & AppSec

* **Para auditar a segurança de APIs (OWASP API Top 10 2023, ASTF, GraphQL e gRPC):**
  * **Use:** [`prompts/security/api.md`](prompts/security/api.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/security/api.md]
    Execute a auditoria de APIs neste repositório e gere o relatório em PDF e SARIF.
    ```

* **Para encontrar fraudes, falhas em regras de negócio, pulo de etapas e idempotência:**
  * **Use:** [`prompts/security/business.md`](prompts/security/business.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/security/business.md]
    Audite as regras de negócio contra fraudes, race conditions (TOCTOU) e falta de idempotência.
    ```

* **Para checar vazamento de senhas, chaves de API e padrões de hashing (Argon2id/TruffleHog3):**
  * **Use:** [`prompts/security/secrets.md`](prompts/security/secrets.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/security/secrets.md]
    Configure o venv, execute o TruffleHog3 e faça a triagem de segredos e hashing.
    ```

* **Para auditar a segurança do frontend, SPAs, Trusted Types, postMessage e CSP:**
  * **Use:** [`prompts/security/frontend.md`](prompts/security/frontend.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/security/frontend.md]
    Audite os componentes frontend contra DOM XSS, vazamento de tokens e CWV.
    ```

* **Para auditar a segurança do banco de dados, menor privilégio, TLS e injeções SQL/NoSQL:**
  * **Use:** [`prompts/security/db.md`](prompts/security/db.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/security/db.md]
    Audite as queries, conexões e migrações contra SQLi, permissões de superuser e deadlocks.
    ```

* **Para identificar alucinações de pacotes por IA (*Slopsquatting*), gerar SBOM e auditar CVEs:**
  * **Use:** [`prompts/security/supply_chain.md`](prompts/security/supply_chain.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/security/supply_chain.md]
    Audite as dependências contra pacotes alucinados, gere o SBOM e verifique CVEs.
    ```

* **Para mapear ameaças (STRIDE-per-Element) e fronteiras de confiança antes de codificar:**
  * **Use:** [`prompts/security/threat_modeling.md`](prompts/security/threat_modeling.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/security/threat_modeling.md]
    Faça a modelagem de ameaças STRIDE e DFD para a arquitetura desta aplicação.
    ```

* **Para auditar aplicações que usam IA (LLMs, RAG e Agentes) contra injeção de prompt:**
  * **Use:** [`prompts/security/ai_appsec.md`](prompts/security/ai_appsec.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/security/ai_appsec.md]
    Audite as integrações de IA contra Prompt Injection e Insecure Output.
    ```

---

### 🎯 2. Arquitetura, Contexto & Testes (Driven Developments)

* **Para ensinar o vocabulário do seu negócio à IA e gerar `CLAUDE.md`, `.github/copilot-instructions.md`, `.cursorrules` e `CONTEXT.md`:**
  * **Use:** [`prompts/driven-development/project_context.md`](prompts/driven-development/project_context.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/driven-development/project_context.md]
    Crie o CONTEXT.md com o dicionário do projeto e os arquivos de regras de IA.
    ```

* **Para gerar a documentação técnica completa da aplicação (Stack, C4 Model, DER do Banco e APIs):**
  * **Use:** [`prompts/driven-development/technical_documentation.md`](prompts/driven-development/technical_documentation.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/driven-development/technical_documentation.md]
    Mapeie o projeto e gere o docs/architecture/ARCHITECTURE.md completo.
    ```

* **Para gerar, escrever e rodar a suíte completa de testes (Unitários, Integração e E2E):**
  * **Use:** [`prompts/driven-development/test_suite_generator.md`](prompts/driven-development/test_suite_generator.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/driven-development/test_suite_generator.md]
    Crie os testes que faltam neste projeto e execute até ficarem 100% verdes.
    ```

* **Para planejar uma nova funcionalidade com especificação técnica (SDD) e Schemas Zod:**
  * **Use:** [`prompts/driven-development/sdd_spec_driven.md`](prompts/driven-development/sdd_spec_driven.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/driven-development/sdd_spec_driven.md]
    Crie o Software Design Document e os Schemas Zod para a nova feature.
    ```

* **Para criar testes automáticos de invasão, BOLA/IDOR, Mass Assignment e concorrência:**
  * **Use:** [`prompts/driven-development/secdd_abuse_cases.md`](prompts/driven-development/secdd_abuse_cases.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/driven-development/secdd_abuse_cases.md]
    Escreva testes de abuso simulando invasões e concorrência maliciosa.
    ```

* **Para documentar o comportamento do sistema em Gherkin (`Given/When/Then`):**
  * **Use:** [`prompts/driven-development/bdd_behavior_driven.md`](prompts/driven-development/bdd_behavior_driven.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/driven-development/bdd_behavior_driven.md]
    Modele os fluxos de negócio em arquivos .feature com sintaxe Gherkin.
    ```

* **Para aplicar o ciclo TDD (Red-Green-Refactor) e cobrir casos de borda:**
  * **Use:** [`prompts/driven-development/tdd_test_driven.md`](prompts/driven-development/tdd_test_driven.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/driven-development/tdd_test_driven.md]
    Aplique TDD para criar os testes unitários antes de codificar a lógica.
    ```

* **Para garantir contratos de API entre serviços e frontend sem quebras:**
  * **Use:** [`prompts/driven-development/cdd_contract_driven.md`](prompts/driven-development/cdd_contract_driven.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/driven-development/cdd_contract_driven.md]
    Valide as rotas com a spec OpenAPI e configure testes de contrato Pact.
    ```

---

### ⚙️ 3. DevOps, Infraestrutura & Resiliência

* **Para auditar e proteger a esteira de CI/CD (GitHub Actions / GitLab CI):**
  * **Use:** [`prompts/devops/cicd_pipeline.md`](prompts/devops/cicd_pipeline.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/devops/cicd_pipeline.md]
    Audite os workflows contra script injection, configure OIDC e pinning SHA256.
    ```

* **Para checar a segurança do Docker (rootless/multi-stage) e manifestos Kubernetes:**
  * **Use:** [`prompts/devops/iac_docker_k8s.md`](prompts/devops/iac_docker_k8s.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/devops/iac_docker_k8s.md]
    Audite Dockerfiles e K8s garantindo securityContext restrito e limites.
    ```

* **Para auditar filas, mensageria (DLQ), observabilidade (OTel) e estabilidade SRE:**
  * **Use:** [`prompts/devops/resilience_observability.md`](prompts/devops/resilience_observability.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/devops/resilience_observability.md]
    Audite os workers de fila, configure retry com DLQ e graceful shutdown.
    ```

---

### ⚡ 4. Jev & System One (TypeSafe AI) – Decisões Estruturadas & Anti-Overkill

* **Para eliminar overkill de LLMs e refatorar fluxos para arquitetura em cascata (System 1 + System 2):**
  * **Use:** [`prompts/jev/system_one_architecture.md`](prompts/jev/system_one_architecture.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/jev/system_one_architecture.md]
    Audite a base de código identificando onde LLMs estão sendo usados para decisões simples e proponha a cascata com Jev.
    ```

* **Para interceptar e bloquear chamadas perigosas de ferramentas em agentes (Pre-Execution Tool Guardrails):**
  * **Use:** [`prompts/jev/agent_guardrails_safety.md`](prompts/jev/agent_guardrails_safety.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/jev/agent_guardrails_safety.md]
    Implemente um guardrail de execução de tools em tempo real com Jev antes de comandos bash, SQL ou de exclusão.
    ```

* **Para criar roteadores de intenção e despacho dinâmico de alta velocidade com Speculative Fan-out:**
  * **Use:** [`prompts/jev/intent_routing_dispatch.md`](prompts/jev/intent_routing_dispatch.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/jev/intent_routing_dispatch.md]
    Projete uma camada de despacho dinâmico para triagem de requisições com Jev e roteamento baseado em confiança.
    ```

* **Para validar fidedignidade de RAG, verificar citações e filtrar ruído sem custo de LLM-as-a-judge:**
  * **Use:** [`prompts/jev/rag_verification_guardrails.md`](prompts/jev/rag_verification_guardrails.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/jev/rag_verification_guardrails.md]
    Audite o pipeline de RAG adicionando re-ranking de passagens e verificação de citações pós-geração com Jev.
    ```

* **Para eliminar falsos positivos em detecção de segredos e capturar senhas de baixa entropia em configurações:**
  * **Use:** [`prompts/jev/secret_detection_triage.md`](prompts/jev/secret_detection_triage.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/jev/secret_detection_triage.md]
    Construa um pipeline híbrido de pre-commit e CI/CD combinando regex e validação semântica com Jev para triagem de credenciais.
    ```

* **Para auditar Agent Skills (`SKILL.md`) e configurações MCP contra prompt injection e tool poisoning:**
  * **Use:** [`prompts/jev/mcp_agent_security_scan.md`](prompts/jev/mcp_agent_security_scan.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/jev/mcp_agent_security_scan.md]
    Escaneie os diretórios de Agent Skills e arquivos de configuração MCP com Jev para detectar comportamentos suspeitos antes da instalação.
    ```

* **Para sanitizar, desambiguar e mascarar dados pessoais (PII) antes de enviar para LLMs ou persistência:**
  * **Use:** [`prompts/jev/pii_sanitization_guardrail.md`](prompts/jev/pii_sanitization_guardrail.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/jev/pii_sanitization_guardrail.md]
    Implemente um guardrail de PII em três camadas com Jev (portão multicategórico + score de sensibilidade IBM + mascaramento).
    ```

* **Para triagem automatizada de vulnerabilidades/CVEs e cálculo determinístico de CVSS v3.1/v4.0:**
  * **Use:** [`prompts/jev/vulnerability_triage_cvss.md`](prompts/jev/vulnerability_triage_cvss.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/jev/vulnerability_triage_cvss.md]
    Construa uma esteira de triagem de segurança extraindo métricas qualitativas com Jev e calculando a pontuação CVSS determinística em código.
    ```

---

## 📚 Catálogo Completo de Prompts

### 🎯 1. Driven Developments, Contexto & Testes (Guardrails contra Alucinação)

| Prompt | Especialidade | Descrição & Escopo |
| :--- | :--- | :--- |
| [`project_context.md`](prompts/driven-development/project_context.md) | **Engenheiro de Contexto & Onboarding de IA** | Mapeia o vocabulário e regras do projeto e gera os arquivos de contexto para IAs: **`CLAUDE.md`** (Claude Code), **`.github/copilot-instructions.md`** (VSCode), **`.cursorrules`** (Cursor) e **`CONTEXT.md`** (glossário universal). |
| [`technical_documentation.md`](prompts/driven-development/technical_documentation.md) | **Arquiteto de Software (Docs-as-Code)** | Mapeia e gera a documentação técnica completa: **Stack & Versões, Diagramas C4 Model, Diagrama ERD do Banco de Dados, Catálogo de Endpoints/Entrypoints, Mensageria, Guia de Onboarding/Setup Local e Deploy/Observabilidade**. |
| [`test_suite_generator.md`](prompts/driven-development/test_suite_generator.md) | **Engenheiro de QA & Test Automation** | Varre a aplicação, identifica código sem testes e **gera, implementa e executa fisicamente** a Pirâmide de Testes completa (Unitários, Integração com Supertest/Testcontainers, E2E com Playwright e carga com K6). |
| [`sdd_spec_driven.md`](prompts/driven-development/sdd_spec_driven.md) | **Spec & Schema-Driven** | Especificação técnica formal prévia (SDD/RFC), Schemas Zod/TypeBox como fonte única da verdade, inferência estrita de tipos e prevenção de *Spec Drift*. |
| [`secdd_abuse_cases.md`](prompts/driven-development/secdd_abuse_cases.md) | **Security-Driven (SecDD)** | Criação de testes automatizados de *Abuse Cases*, simulações de BOLA/IDOR cross-tenant, injeção de Mass Assignment, testes de concorrência em saldo e ReDoS. |
| [`bdd_behavior_driven.md`](prompts/driven-development/bdd_behavior_driven.md) | **Behavior-Driven (BDD)** | Documentação viva em linguagem Gherkin (`.feature`), validação de transições ilegais em máquinas de estado e critérios de aceite executáveis. |
| [`tdd_test_driven.md`](prompts/driven-development/tdd_test_driven.md) | **Test-Driven (TDD)** | Ciclo Red-Green-Refactor, cobertura rigorosa de *Edge Cases*, eliminação de over-mocking e testes determinísticos ultrarrápidos. |
| [`cdd_contract_driven.md`](prompts/driven-development/cdd_contract_driven.md) | **Contract-Driven (CDD)** | OpenAPI, AsyncAPI, validação com Pact (Consumer-Driven Contracts), prevenção de *Breaking Changes* e schema registry de eventos. |

---

### 🛡️ 2. Segurança, Modelagem & AppSec (OWASP Standards)

| Prompt | Especialidade | Descrição & Escopo |
| :--- | :--- | :--- |
| [`threat_modeling.md`](prompts/security/threat_modeling.md) | **Modelagem de Ameaças (STRIDE/PASTA)** | Mapeamento formal de fronteiras de confiança (*Trust Boundaries*), decomposição STRIDE-per-Element e matriz de contramedidas arquiteturais. |
| [`supply_chain.md`](prompts/security/supply_chain.md) | **Supply Chain & SCA (OWASP SCVS)** | Prevenção contra **alucinação de pacotes (*Slopsquatting*)**, geração de SBOM (CycloneDX/SPDX), scripts de `postinstall` maliciosos e CVEs. |
| [`api.md`](prompts/security/api.md) | **OWASP API Top 10 (ASTF Suite)** | 16 módulos de teste ASTF, autorização cruzada multi-tenant, GraphQL, gRPC, AI APIs, SSRF, BOLA, BOPLA e exportação SARIF. |
| [`business.md`](prompts/security/business.md) | **Business Logic & Idempotência** | Manipulação de preço/quantidade, chaves de idempotência (`Idempotency-Key`), pulo de etapas no checkout (*skip-step*), TOCTOU e trilhas de auditoria. |
| [`db.md`](prompts/security/db.md) | **Banco de Dados (OWASP DB Security)** | Menor privilégio no DB, TLS obrigatório, criptografia de campos sensíveis (KMS), injeções em procedures dinâmicas, NoSQL operator injection e deadlocks. |
| [`frontend.md`](prompts/security/frontend.md) | **Frontend (OWASP Client-Side)** | DOM XSS, Trusted Types API, segurança de `window.postMessage`, prefixos de cookies seguros (`__Host-`), CSP, Clickjacking e Core Web Vitals. |
| [`secrets.md`](prompts/security/secrets.md) | **Gestão de Segredos & Criptografia** | Scanner automatizado com `trufflehog3`, padrão ouro de hashing de senhas (`Argon2id`), prevenção de Timing Attacks e limpeza de memória (*zeroization*). |
| [`ai_appsec.md`](prompts/security/ai_appsec.md) | **Aplicações de IA (OWASP LLM)** | Injeção direta/indireta de prompt, Insecure Output Handling, Excessive Agency e isolamento de tenants em RAG/vetores. |
| [`authn_identity.md`](prompts/security/authn_identity.md) | **Identidades Digitais (OWASP Proactive C7)** | Autenticação e hashing de senha (`Argon2id`), regeneração de sessão (Session Fixation), MFA/2FA e backup codes, JWT (rejeição de `alg:none`), OAuth2/OIDC com PKCE + `state`/`nonce`, fluxos de reset/verificação de conta sem enumeração e sem ATO. |
| [`access_control.md`](prompts/security/access_control.md) | **Controle de Acesso (OWASP Proactive C1 / A01)** | Deny-by-default, autorização centralizada, IDOR/BOLA com checagem de titularidade e escopo na query, escalada vertical/BFLA, isolamento multi-tenant, testes negativos de autorização e fail-closed. |
| [`ssrf.md`](prompts/security/ssrf.md) | **SSRF (OWASP Proactive C10 / A10)** | Mapa de sinks de saída (webhooks, HTML→PDF, proxies de imagem, `$ref` remoto, XXE), allow-list de destino, validação pós-DNS + pinning (anti DNS rebinding), bloqueio de metadata cloud (`169.254.169.254`), egress filtering e IMDSv2. |
| [`secure_config.md`](prompts/security/secure_config.md) | **Configuração Segura por Padrão (OWASP Proactive C5 / A05)** | Secure-by-default, debug/stack traces off, credenciais default, headers (`HSTS`, `CSP`, `nosniff`, `frame-ancestors`), CORS com allow-list estrita, atributos de cookie + CSRF, TLS 1.2+/1.3 e hardening de container. |
| [`input_validation.md`](prompts/security/input_validation.md) | **Validação de Entrada & Exceções (OWASP Proactive C3)** | Validação positiva (allow-list) em toda fronteira de confiança, canonicalização Unicode, schema estrito anti Mass Assignment, deserialização segura (XXE, zip slip), parametrização de sinks e tratamento centralizado de erros sem vazamento de stack trace. |

---

### ⚙️ 3. DevOps, Infraestrutura & Confiabilidade (SRE)

| Prompt | Especialidade | Descrição & Escopo |
| :--- | :--- | :--- |
| [`cicd_pipeline.md`](prompts/devops/cicd_pipeline.md) | **Hardening de CI/CD (OWASP CI/CD)** | Prevenção de script injection em GitHub Actions/GitLab CI, autenticação OIDC federada, pinning de actions por SHA256 e runners isolados. |
| [`iac_docker_k8s.md`](prompts/devops/iac_docker_k8s.md) | **IaC, Containers & K8s** | Terraform IAM least privilege, Docker rootless e multi-stage, K8s securityContext, NetworkPolicies e Probes. |
| [`resilience_observability.md`](prompts/devops/resilience_observability.md) | **Resiliência & Observabilidade** | Mensageria assíncrona, Dead Letter Queues (DLQ), Circuit Breakers, tracing distribuído com OpenTelemetry e Graceful Shutdown. |

---

### ⚡ 4. Jev & System One Models (TypeSafe AI)

| Prompt | Especialidade | Descrição & Escopo |
| :--- | :--- | :--- |
| [`system_one_architecture.md`](prompts/jev/system_one_architecture.md) | **Arquitetura System One & Anti-Overkill** | Diagnóstico de gargalos de LLMs, substituição de parsing de JSON por primitivas tipadas (`Choice`, `Score`, `Noul`) e design de Two-Model Cascades. |
| [`agent_guardrails_safety.md`](prompts/jev/agent_guardrails_safety.md) | **Guardrails de Agentes & Excessive Agency (OWASP LLM06)** | Interceptação de ferramentas em <100ms, detecção de injeção indireta e aprovação de execução com Confidence-Gated Approval. |
| [`intent_routing_dispatch.md`](prompts/jev/intent_routing_dispatch.md) | **Roteamento de Intenção & Speculative Fan-out** | Despacho dinâmico de eventos e requisições para lógica determinística, modelos leves ou modelos frontier, com amostragem paralela. |
| [`rag_verification_guardrails.md`](prompts/jev/rag_verification_guardrails.md) | **Verificação de RAG & Citações (OWASP LLM09)** | Re-ranking de passagens recuperadas, descarte de ruído pré-geração e verificação factual de citações sem custo de LLM-as-a-judge. |
| [`secret_detection_triage.md`](prompts/jev/secret_detection_triage.md) | **Triagem Semântica de Segredos (ASVS V14)** | Eliminação de falsos positivos (hashes/test seeds) e captura de senhas em configs de baixa entropia com bandas calibradas. |
| [`mcp_agent_security_scan.md`](prompts/jev/mcp_agent_security_scan.md) | **Auditoria de Agent Skills & MCP (OWASP LLM01/06)** | Varredura estática e semântica de `SKILL.md` e `mcpServers` contra prompt injection, tool description poisoning e supply chain. |
| [`pii_sanitization_guardrail.md`](prompts/jev/pii_sanitization_guardrail.md) | **Sanitização & Mascaramento de PII (ASVS V8)** | Portão multicategórico de 13 PIIs, score de sensibilidade IBM, desambiguação de dígitos e mascaramento determinístico. |
| [`vulnerability_triage_cvss.md`](prompts/jev/vulnerability_triage_cvss.md) | **Triagem de Falhas & Cálculo CVSS (ASVS V1.14)** | Elicitação paralela de métricas Base com Jev Choice, Top-2 Probability Spread ($\Delta P$) e cálculo oficial FIRST. |

---

## 🧭 Cobertura vs OWASP Top 10 Proactive Controls (2024)

Mapa de qual prompt exerce cada [Proactive Control](https://top10proactive.owasp.org/) e quais [Cheat Sheets](https://cheatsheetseries.owasp.org/) ele aplica.

| Proactive Control | Prompt(s) principal(is) | Cheat Sheets aplicados |
| :--- | :--- | :--- |
| **C1** – Implement Access Control | [`access_control.md`](prompts/security/access_control.md), `business.md`, `secdd_abuse_cases.md` | Authorization, Access Control, IDOR Prevention, Transaction Authorization |
| **C2** – Use Cryptography Properly | [`secrets.md`](prompts/security/secrets.md), `db.md` | Cryptographic Storage, Key Management, Password Storage |
| **C3** – Validate Input & Handle Exceptions | [`input_validation.md`](prompts/security/input_validation.md), `api.md`, `db.md`, `frontend.md` | Input Validation, Mass Assignment, Deserialization, Error Handling, Injection Prevention, XXE Prevention |
| **C4** – Address Security from the Start | [`threat_modeling.md`](prompts/security/threat_modeling.md), `sdd_spec_driven.md` | Threat Modeling, Attack Surface Analysis, Abuse Case |
| **C5** – Secure by Default Configurations | [`secure_config.md`](prompts/security/secure_config.md), `iac_docker_k8s.md`, `frontend.md` | HTTP Security Response Headers, CSP, TLS, HSTS, CSRF Prevention, Docker Security |
| **C6** – Keep Components Secure | [`supply_chain.md`](prompts/security/supply_chain.md) | Vulnerable Dependency Management, SCVS, NPM Security |
| **C7** – Secure Digital Identities | [`authn_identity.md`](prompts/security/authn_identity.md), `secrets.md` | Authentication, Session Management, JWT, Forgot Password, MFA, Credential Stuffing Prevention |
| **C8** – Leverage Browser Security Features | [`frontend.md`](prompts/security/frontend.md) | XSS Prevention, DOM XSS, Content Security Policy, Clickjacking Defense |
| **C9** – Security Logging & Monitoring | [`resilience_observability.md`](prompts/devops/resilience_observability.md), `business.md` | Logging, Application Logging Vocabulary |
| **C10** – Stop Server-Side Request Forgery | [`ssrf.md`](prompts/security/ssrf.md), `api.md` | SSRF Prevention, XXE Prevention |

---

## 📊 Entregáveis Padrão Gerados pelos Prompts

Todos os prompts são padronizados para entregar:
1. **Matriz de Priorização no Terminal:** Tabela com ordenação por Severidade x Esforço, cálculo pela **OWASP Risk Rating Methodology** (Likelihood x Impact) e chips de **Quick Wins**.
2. **Detalhamento Completo dos Achados com PoC & Verificação:** Arquivo/linha, evidência factual, mapeamento de conformidade **OWASP ASVS v4.0.3 (L1/L2/L3)**, Prova de Conceito (PoC de reprodução), código seguro pronto e comando de verificação pós-correção.
3. **Filtro Anti-Fadiga e Anti-Alucinação:** Foco exclusivo no raio de impacto real (*Blast Radius*), descartando falso-positivo teórico e separando sugestões cosméticas (*nits*).
4. **Relatório em PDF com Gráficos:** Salvo na pasta `docs/<modulo>-audit/`, com design profissional (paleta `#B91C1C` Crítica, `#EA580C` Alta, `#D97706` Média, `#2563EB` Baixa, `#059669` Pontos Fortes).
5. **Exportação SARIF (quando aplicável):** Arquivos compatíveis com o GitHub Code Scanning / Advanced Security.
6. **Issues Formatadas para GitHub/GitLab:** Blocos em Markdown prontos para copiar com critérios de aceite verificáveis.

---

## 🤝 Como Contribuir

Contribuições da comunidade brasileira e internacional são muito bem-vindas!
* Leia nosso [Guia de Contribuição (CONTRIBUTING.md)](CONTRIBUTING.md) para entender o padrão de criação de novos prompts.
* Consulte o [Código de Conduta](CODE_OF_CONDUCT.md).
* Reporte vulnerabilidades de acordo com a [Política de Segurança (SECURITY.md)](SECURITY.md).

---

## 📄 Licença

Distribuído sob a licença **MIT**. Veja [`LICENSE`](LICENSE) para mais informações.

<div align="center">
Desenvolvido com 💚 para a comunidade de tecnologia brasileira por <a href="https://github.com/brunoez">@brunoez</a>
</div>
