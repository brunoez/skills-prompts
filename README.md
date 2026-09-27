# 🛡️ Suíte de Prompts & Agent Skills de Engenharia de Software, AppSec & Yellow Team

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Release](https://img.shields.io/github/v/release/brunoez/skills-prompts?color=blue)](https://github.com/brunoez/skills-prompts/releases/latest)
[![CI Status](https://github.com/brunoez/skills-prompts/actions/workflows/ci.yml/badge.svg)](https://github.com/brunoez/skills-prompts/actions)
[![GitLab CI](https://img.shields.io/badge/GitLab%20CI-Passing-22c55e?logo=gitlab)](.gitlab-ci.yml)
[![Language](https://img.shields.io/badge/Language-pt--BR-009c3b.svg)](README.md)

**A biblioteca definitiva de prompts estruturados e Agent Skills executáveis de auditoria profunda, arquitetura defensiva e metodologias *Driven Development* para desenvolvedores, arquitetos e agentes de Inteligência Artificial.**

[Instalação Rápida](#-instalação-rápida) • [Validação 360° (Destaque)](#-destaque-validação-completa-da-aplicação-zero-overkill--zero-overlap) • [Agent Skills](#-agent-skills-antigravity-claude-code-cursor--windsurf) • [Uso em CI/CD Privado](#-como-executar-os-prompts-em-cicd-no-seu-projeto-privado) • [Qual Prompt Usar?](#-qual-prompt-usar-guia-de-ação-rápida-com-exemplos) • [Catálogo Completo](#-catálogo-completo-de-prompts) • [Contribuição](CONTRIBUTING.md)

</div>

---

## 🇧🇷 Sobre o Projeto

Criado com foco na comunidade brasileira de desenvolvimento e AppSec, este repositório aberto reúne **prompts técnicos e Agent Skills de alto nível** projetados para serem executados por Engenheiros Principais ou Agentes de IA (**Claude Code**, **Google Antigravity**, **VSCode** / GitHub Copilot, **Cursor** e outros editores como Windsurf).

O objetivo é transformar a velocidade do **Vibe Coding** em software de **nível corporativo**: seguro contra vulnerabilidades (**OWASP ASTF 2023**, **WSTG v4.2**, **OWASP Top 10 Proactive Controls 2024**, **OWASP ASVS v4.0.3**, **OWASP DSOMM (DevSecOps Maturity Model)**, **OWASP Risk Rating Methodology** e **OWASP Cheat Sheet Series**), arquiteturalmente consistente (DDD/SDD), resiliente em produção (SRE) e 100% testado (TDD, BDD, SecDD).

---

## 🌟 Destaques: Validação Holística & Auditoria 360° da Aplicação

> [!TIP]
> ### 🎯 Escolha o tipo de avaliação 360° para o momento do seu projeto:
> 
> 1. **🏥 Full App Validator 360° (Saúde Geral, Arquitetura & SRE):**
>    - **Propósito:** Diagnóstico holístico da aplicação cobrindo as 5 fronteiras herméticas ([`domain-boundaries-matrix.md`](skills/full-app-validator/references/domain-boundaries-matrix.md)) sem redundâncias (*Zero Overlap*) e sem fadiga de tokens (*Zero Overkill* via [`anti-overkill-cascade.md`](skills/full-app-validator/references/anti-overkill-cascade.md)).
>    - **Entregável:** Health Card 360° com pontuação de maturidade (0-100) e Top 3 a 5 ações de maior impacto.
>    - **Prompt:** [`prompts/driven-development/full_app_validator.md`](prompts/driven-development/full_app_validator.md) | **Skill:** [`skills/full-app-validator`](skills/full-app-validator/SKILL.md) | **CLI:** `python3 skills/full-app-validator/scripts/health_card.py .`
>    ```markdown
>    @[.claude/prompts/driven-development/full_app_validator.md]
>    Faça a validação holística 360° desta aplicação e apresente o Health Card executivo.
>    ```
> 
> 2. **🛡️ AppSec Auditor 360° (Segurança em Profundidade & Pentest de Código):**
>    - **Propósito:** Auditoria minuciosa de vulnerabilidades e superfícies de ataque (**OWASP ASTF**, **ASVS v4.0.3 L2**), eliminando falsos positivos com Crítica de Viabilidade de Release (*Google Mantis Pattern*), cálculo determinístico de risco (*OWASP Risk Rating*) e PoCs de reprodução.
>    - **Entregável:** Matriz consolidada de vulnerabilidades, patches defensivos (*drop-in*) e relatórios **SARIF 2.1.0** para GitHub Code Scanning / GitLab SAST.
>    - **Prompt:** [`prompts/security/appsec_auditor.md`](prompts/security/appsec_auditor.md) | **Skill:** [`skills/appsec-auditor`](skills/appsec-auditor/SKILL.md) | **Scripts:** `sarif_builder.py` e `report_generator.py`
>    ```markdown
>    @[.claude/prompts/security/appsec_auditor.md]
>    Execute a auditoria de segurança em profundidade nesta aplicação e gere a matriz calibrada com SARIF.
>    ```

---

## ⚡ Instalação Rápida

Instale a suíte completa de prompts (41 arquivos) e Agent Skills (4 skills) no seu projeto com um único comando:

```bash
curl -sSL https://raw.githubusercontent.com/brunoez/skills-prompts/main/install.sh | bash
```

> **Dica de Ferramenta & IDE:** Por padrão, os prompts e as skills são instalados no diretório oficial do **Claude Code** (`.claude/prompts/` e `.claude/skills/`). Se você usa **VSCode**, **Cursor** ou outros editores:
> ```bash
> # Para Claude Code (padrão oficial em .claude/prompts/ e .claude/skills/):
> curl -sSL https://raw.githubusercontent.com/brunoez/skills-prompts/main/install.sh | bash
> 
> # Para VSCode (.agent/prompts/ e .agent/skills/):
> curl -sSL https://raw.githubusercontent.com/brunoez/skills-prompts/main/install.sh | bash -s -- . vscode
> 
> # Para Cursor (.cursor/rules/, .cursor/skills/ e .agent/skills/):
> curl -sSL https://raw.githubusercontent.com/brunoez/skills-prompts/main/install.sh | bash -s -- . cursor
> 
> # Para todas as ferramentas simultaneamente (.claude, .agent, .cursor, .windsurf):
> curl -sSL https://raw.githubusercontent.com/brunoez/skills-prompts/main/install.sh | bash -s -- . all
> ```

---

### 📁 Estrutura de Diretórios Gerada no Projeto

<details>
<summary><b>Clique para expandir a árvore completa de diretórios e arquivos gerados (70+ itens)</b></summary>
<br/>

```plaintext
seu-projeto/
├── .claude/prompts/              # Prompts oficiais para Claude Code (ou .agent/prompts/)
│   ├── driven-development/       # Metodologias & Testes
│   │   ├── bdd_behavior_driven.md     # BDD & Gherkin
│   │   ├── cdd_contract_driven.md     # Contratos & OpenAPI
│   │   ├── datadd_data_driven.md      # Data-Driven Design & Access Patterns
│   │   ├── ddd_domain_driven.md       # Domain-Driven Design & Aggregates
│   │   ├── full_app_validator.md      # Validação Holística 360° (Zero Overkill & Overlap)
│   │   ├── project_context.md         # Dicionário & Regras IA
│   │   ├── sdd_spec_driven.md         # SDD & Schemas Zod
│   │   ├── secdd_abuse_cases.md       # Casos de Abuso & SecDD
│   │   ├── tdd_test_driven.md         # TDD Red-Green-Refactor
│   │   ├── test_suite_generator.md    # Gerador de Testes QA
│   │   ├── technical_documentation.md # Docs-as-Code & C4
│   │   └── typedd_type_driven.md      # Type-Driven Design & Invariantes
│   ├── security/                 # Auditorias de AppSec (OWASP ASTF / WSTG / Proactive Controls)
│   │   ├── access_control.md          # Proactive C1 – Autorização & IDOR/BOLA
│   │   ├── adversarial_patching.md    # Protocolo Red/Blue com Re-Attack Loop (Mantis Pattern)
│   │   ├── ai_appsec.md               # OWASP LLM Top 10
│   │   ├── api.md                     # OWASP API Top 10 (ASTF)
│   │   ├── appsec_auditor.md          # Auditoria de Segurança 360° em Profundidade (OWASP ASTF/ASVS L2)
│   │   ├── authn_identity.md          # Proactive C7 – Autenticação, Sessão, MFA & OIDC
│   │   ├── business.md                # Fraudes & Idempotência
│   │   ├── db.md                      # OWASP DB & Concorrência
│   │   ├── exploit_chaining.md        # Composição de Kill Chains Multi-Stage
│   │   ├── frontend.md                # Trusted Types, CSP & SPAs
│   │   ├── input_validation.md        # Proactive C3 – Validação de Entrada & Exceções
│   │   ├── sec_advisor.md             # Developer Security Advisor (Shift-Left)
│   │   ├── secrets.md                 # TruffleHog3 & Argon2id
│   │   ├── secure_config.md           # Proactive C5 – Config Segura, Headers & CORS
│   │   ├── ssrf.md                    # Proactive C10 – Server-Side Request Forgery
│   │   ├── supply_chain.md            # SCVS, SBOM & Anti-Slopsquatting
│   │   ├── threat_modeling.md         # Modelagem STRIDE-per-Element
│   │   └── vcs_security_history.md    # Mineração de Segurança no Git (VCS History)
│   ├── devops/                   # Infraestrutura, CI/CD & SRE (OWASP DSOMM)
│   │   ├── cicd_pipeline.md           # Hardening de CI/CD, OIDC & DSOMM Build
│   │   ├── iac_docker_k8s.md          # Docker Rootless, K8s & DSOMM Implementation
│   │   └── resilience_observability.md# SRE, OpenTelemetry & DSOMM Info Gathering
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
│   ├── driven-development/       # Suíte Driven Design (DDD, DataDD, TypeDD, SDD, CDD, BDD, SecDD, TDD)
│   │   ├── SKILL.md              # Ciclo em 6 fases (Domínio -> Storage -> Tipos -> Contratos -> Aceite -> TDD)
│   │   ├── references/           # Guias modulares (DDD, DataDD, TypeDD, Pipeline Matrix, SDD, CDD, BDD, SecDD, TDD)
│   │   ├── scripts/              # test_runner.py (executor universal e detector de stack)
│   │   └── examples/             # Máquinas de estado TypeDD, DDL DataDD, Zod SDD, TDD e Gherkin
│   ├── full-app-validator/       # Validação Holística 360° (Zero Overkill & Zero Overlap)
│   │   ├── SKILL.md              # Workflow em 3 fases (Triagem, Fronteiras & Health Card)
│   │   ├── references/           # Matriz de fronteiras herméticas e triagem em cascata
│   │   └── scripts/              # health_card.py (gerador determinístico de Health Card)
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

</details>

---

## 🧠 Agent Skills (Antigravity, Claude Code, Cursor & Windsurf)

Além dos prompts estruturados invocados manualmente via `@`, este repositório disponibiliza **Agent Skills** nativas em conformidade com o padrão aberto [Agent Skills](https://agentskills.io/specification). As skills habilitam **ativação semântica autônoma** (`Use when...`), **Progressive Disclosure** (carregamento sob demanda para não estourar o contexto) e **scripts executáveis determinísticos**.

| Skill | Especialidade | Entregáveis & Ferramentas Integradas |
| :--- | :--- | :--- |
| [`skills/appsec-auditor`](skills/appsec-auditor/SKILL.md) | **Auditoria de Segurança AppSec (OWASP ASTF, ASVS L2 & Mantis-Enhanced)** | - Fluxo em 5 fases com **Crítica de Viabilidade de Release** e **Calibração de Risco Anti-Inflação (Score 1-10)**<br/>- `scripts/sarif_builder.py`: Gerador de relatórios SARIF 2.1.0 com metadados de calibração para GitHub Security<br/>- `scripts/report_generator.py`: Gerador de relatórios executivos em Markdown e Issues GitHub<br/>- `references/`: Guias modulares (ASTF, ASVS L2, BOLA, SSRF, Viability Critique, PoC Reproduction Harness)<br/>- `examples/`: Teste de abuso BOLA em pytest e cliente fetch seguro em TypeScript |
| [`skills/driven-development`](skills/driven-development/SKILL.md) | **Engenharia de Software & Suíte Driven Design (DDD, DataDD, TypeDD, SDD, CDD, BDD, SecDD, TDD)** | - Ciclo em 6 fases: Domínio (DDD) → Storage (DataDD) → Tipos (TypeDD) → Schemas/Contratos (SDD/CDD) → Aceite/Abuso (BDD/SecDD) → TDD<br/>- `scripts/test_runner.py`: Executor universal com detecção automática de stack (Node, Python, Go, Rust)<br/>- `references/`: Guias modulares de DDD, DataDD, TypeDD, Matriz de Pipeline, SDD, TDD, BDD, CDD, SecDD e Pirâmide<br/>- `examples/`: Máquinas de estado TypeDD, DDL DataDD com regra ESR, schemas Zod, fixtures TDD e Gherkin |
| [`skills/full-app-validator`](skills/full-app-validator/SKILL.md) | **Validação Holística 360° (Zero Overkill & Zero Overlap)** | - Avaliação 360° cobrindo Arquitetura, Segurança, Testes e SRE em 3 fases<br/>- `scripts/health_card.py`: Gerador determinístico de Health Card e métricas de maturidade (0-100)<br/>- `references/`: Matriz de 5 fronteiras herméticas e protocolo de triagem em cascata<br/>- Top 3 a 5 ações prioritárias sem sobreposição de escopo |
| [`skills/jev-system-one`](skills/jev-system-one/SKILL.md) | **Decisões Estruturadas & Guardrails System One (TypeSafe AI)** | - Padrão de Two-Model Cascade (System 1 para decisões <100ms + System 2 para raciocínio)<br/>- Primitivas `Choice`, `Score` e `Noul` com calibração de probabilidade<br/>- `references/`: HTTP API Reference, Primitivas e Jaggedness / Anti-Patterns<br/>- `examples/`: Guardrails LangChain, cascade em TypeScript, scanner híbrido de segredos, auditor de MCP e cálculo de CVSS |


### 💡 Como Usar as Agent Skills no seu Ambiente

As skills seguem o padrão aberto da indústria ([agentskills.io](https://agentskills.io/specification)) e funcionam de forma autônoma ou guiada:

* **Ativação Autônoma (Semântica):** O agente inspeciona o frontmatter YAML das skills e carrega o workflow automaticamente quando seu pedido corresponder aos gatilhos (ex: *"audite as APIs contra IDOR"* ou *"vamos criar essa funcionalidade aplicando TDD"*).
* **Instalação Automática (Recomendado):** O script `install.sh` instala automaticamente todas as Agent Skills e prompts no local oficial da sua IDE (`.claude/skills/`, `.agent/skills/` ou `.cursor/skills/`).
* **No Claude Code:** As skills instaladas em `.claude/skills/` são carregadas nativamente pelo Claude Code em cada sessão (ou globalmente em `~/.claude/skills/`).
* **No Antigravity / VSCode / Cursor:** Integradas automaticamente em `.agent/skills/` e `.cursor/skills/` (ou globalmente em `~/.gemini/antigravity-cli/skills/`).
* **Invocação Direta no Chat:**
  ```markdown
  Use a skill @[skills/appsec-auditor] para auditar este repositório e gerar os artefatos SARIF e Markdown.
  ```

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

<details>
<summary><b>Clique para expandir os comandos e prompts de Segurança & AppSec</b></summary>
<br/>

* **Para conduzir uma Auditoria de Segurança 360° em profundidade (OWASP ASTF, ASVS L2, Mantis Viability & SARIF):**
  * **Use:** [`prompts/security/appsec_auditor.md`](prompts/security/appsec_auditor.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/security/appsec_auditor.md]
    Execute a auditoria de segurança em profundidade nesta aplicação e gere a matriz calibrada com SARIF.
    ```

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

</details>

---

### 🎯 2. Arquitetura, Contexto & Testes (Driven Developments)

<details>
<summary><b>Clique para expandir os comandos e prompts de Driven Developments & Testes</b></summary>
<br/>

* **Para fazer uma validação completa 360° da aplicação sem overkill e sem sobreposição de escopo:**
  * **Use:** [`prompts/driven-development/full_app_validator.md`](prompts/driven-development/full_app_validator.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/driven-development/full_app_validator.md]
    Faça a validação holística 360° desta aplicação e gere o Health Card executivo.
    ```

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

* **Para modelar a arquitetura com Domain-Driven Design (Bounded Contexts, Aggregates e ACL):**
  * **Use:** [`prompts/driven-development/ddd_domain_driven.md`](prompts/driven-development/ddd_domain_driven.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/driven-development/ddd_domain_driven.md]
    Modele o domínio desta feature delimitando Aggregates, Value Objects e o Context Map.
    ```

* **Para eliminar estados ilegais em compilação e aplicar "Parse, Don't Validate" (TypeDD):**
  * **Use:** [`prompts/driven-development/typedd_type_driven.md`](prompts/driven-development/typedd_type_driven.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/driven-development/typedd_type_driven.md]
    Modele os tipos nominais (Branded Types) e a máquina de estados hermética com Discriminated Unions.
    ```

* **Para projetar esquemas de banco e índices orientados por Padrões de Acesso (DataDD):**
  * **Use:** [`prompts/driven-development/datadd_data_driven.md`](prompts/driven-development/datadd_data_driven.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/driven-development/datadd_data_driven.md]
    Mapeie a matriz de Access Patterns (Q1, Q2) e crie o DDL com índices seguindo a regra ESR.
    ```

</details>

---

### ⚙️ 3. DevOps, Infraestrutura & Resiliência (OWASP DSOMM)

<details>
<summary><b>Clique para expandir os comandos e prompts de DevOps, Infraestrutura & SRE</b></summary>
<br/>

* **Para auditar a esteira de CI/CD e avaliar a maturidade (OWASP CI/CD & DSOMM Build & Deployment):**
  * **Use:** [`prompts/devops/cicd_pipeline.md`](prompts/devops/cicd_pipeline.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/devops/cicd_pipeline.md]
    Audite os workflows contra script injection, configure OIDC, pinning SHA256, SBOM, Cosign e gere o scorecard DSOMM (Níveis 1 a 5).
    ```

* **Para checar a segurança de IaC, Docker (Distroless) e Kubernetes (DSOMM Implementation & Policy-as-Code):**
  * **Use:** [`prompts/devops/iac_docker_k8s.md`](prompts/devops/iac_docker_k8s.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/devops/iac_docker_k8s.md]
    Audite IaC, Dockerfiles e manifestos K8s aplicando Pod Security Standards, políticas OPA/Kyverno e gere o scorecard de maturidade DSOMM.
    ```

* **Para auditar filas, mensageria (DLQ), observabilidade (OTel), estabilidade SRE e logs append-only (DSOMM Info Gathering):**
  * **Use:** [`prompts/devops/resilience_observability.md`](prompts/devops/resilience_observability.md)
  * **Comando:**
    ```markdown
    @[.claude/prompts/devops/resilience_observability.md]
    Audite os workers de fila, configure retry com DLQ, tracing OTel, logs append-only WORM e gere o scorecard de resiliência DSOMM.
    ```

</details>

---

### ⚡ 4. Jev & System One (TypeSafe AI) – Decisões Estruturadas & Anti-Overkill

<details>
<summary><b>Clique para expandir os comandos e prompts de Jev System One</b></summary>
<br/>

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

</details>

---

## 📚 Catálogo Completo de Prompts

<details>
<summary><b>Clique para expandir as tabelas de referência técnica de todos os 41 prompts</b></summary>
<br/>

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
| [`full_app_validator.md`](prompts/driven-development/full_app_validator.md) | **Validação Holística 360° (Zero Overkill & Overlap)** | Avaliação integrada de maturidade em 5 fronteiras herméticas (API, Domínio, Banco, Testes e SRE) sem redundâncias analíticas e com Health Card consolidado. |
| [`ddd_domain_driven.md`](prompts/driven-development/ddd_domain_driven.md) | **Domain-Driven Design (DDD)** | Modelagem estratégica (Bounded Contexts, Context Map, ACL) e tática (Aggregates, Entities, Value Objects, Domain Events e Repositories). |
| [`typedd_type_driven.md`](prompts/driven-development/typedd_type_driven.md) | **Type-Driven Design (TypeDD)** | *"Make illegal states unrepresentable"* e *"Parse, Don't Validate"*, tipagem nominal com Branded Types e máquinas de estado por Discriminated Unions. |
| [`datadd_data_driven.md`](prompts/driven-development/datadd_data_driven.md) | **Data-Driven Design (DataDD)** | Modelagem de banco orientada por matriz de Padrões de Acesso (Access Patterns), regra ESR para índices compostos, covering indexes e Optimistic Locking. |

---

### 🛡️ 2. Segurança, Modelagem & AppSec (OWASP Standards)

| Prompt | Especialidade | Descrição & Escopo |
| :--- | :--- | :--- |
| [`appsec_auditor.md`](prompts/security/appsec_auditor.md) | **Auditoria AppSec 360° (OWASP ASTF/ASVS L2)** | Auditoria profunda em 5 fases (Superfície, Código, Viabilidade Mantis, Risco Calibrado 1-10 e PoCs) com eliminação de falsos positivos e SARIF. |
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
| [`adversarial_patching.md`](prompts/security/adversarial_patching.md) | **Correção Adversarial (Red/Blue Loop)** | Protocolo de remediação com separação estrita de deveres (Patcher vs. Re-Attacker), caça a bypasses de encoding/path e teste de regressão automatizado (Mantis Pattern). |
| [`exploit_chaining.md`](prompts/security/exploit_chaining.md) | **Exploit Chaining & Kill Chains** | Composição de múltiplos achados baixos/médios em cadeias de ataque multi-stage (Super Findings), diagramas de sequência e choke points defensivos. |
| [`vcs_security_history.md`](prompts/security/vcs_security_history.md) | **Mineração de Histórico Git (VCS Mining)** | Rastreamento de patches anteriores, detecção de regressões acidentais em merges/refatorações e mapeamento de invariantes históricos de segurança. |
| [`sec_advisor.md`](prompts/security/sec_advisor.md) | **Developer Security Advisor (Shift-Left)** | Pair programming de segurança em tempo real durante a escrita de código, consultando modelos de ameaça, invariantes e propondo alternativas defensivas idiomáticas. |

---

### ⚙️ 3. DevOps, Infraestrutura & Confiabilidade (SRE & OWASP DSOMM)

| Prompt | Especialidade | Descrição & Escopo |
| :--- | :--- | :--- |
| [`cicd_pipeline.md`](prompts/devops/cicd_pipeline.md) | **Hardening de CI/CD & DSOMM Build** | Prevenção de script injection, autenticação OIDC federada, pinning SHA256, geração de SBOM (CycloneDX), assinatura Sigstore/Cosign, proveniência SLSA e Scorecard de Maturidade DSOMM (Níveis 1-5). |
| [`iac_docker_k8s.md`](prompts/devops/iac_docker_k8s.md) | **IaC, Containers & DSOMM Implementation** | Terraform IAM least privilege e state security, imagens mínimas Distroless/Chainguard, triagem de CVEs (CISA KEV/EPSS), K8s Pod Security Standards, Policy-as-Code (OPA/Kyverno) e GitOps drift. |
| [`resilience_observability.md`](prompts/devops/resilience_observability.md) | **SRE, Resiliência & DSOMM Info Gathering** | Mensageria assíncrona com DLQ, Circuit Breakers, tracing distribuído OTel, logs append-only WORM (OWASP C9), canary rollbacks automatizados, Chaos Security Engineering e Scorecard DSOMM. |

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

</details>

---

## 🧭 Cobertura vs OWASP Top 10 Proactive Controls (2024)

<details>
<summary><b>Clique para expandir a matriz de cobertura dos Controles Proativos da OWASP</b></summary>
<br/>

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

</details>

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
