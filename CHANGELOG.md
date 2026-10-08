# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico (SemVer)](https://semver.org/lang/pt-BR/).

## [2.6.1] - 2026-10-08

### Aprimorado (Instalação Modular por LLM e Matriz Local vs. Global)

- **Instalador com Flags Específicas por Assistente (`install.sh`):**
  - Adicionadas flags dedicadas para cada ferramenta/LLM: `--claude`, `--gemini` (alias `--antigravity`), e `--codex` (aliases `--chatgpt`, `--openai`).
  - Compatibilidade com escopo local (`./install.sh --<llm>`) e escopo global (`./install.sh --global --<llm>`), além de instalação completa (`--all` / `--global --all`).
  - Respeito à estrutura canônica de cada ferramenta: `.claude/` e `~/.claude/` para Claude Code; `.gemini/` e `~/.gemini/` para Gemini CLI; `.codex/`, `.agents/skills/` e `~/.agents/skills/` para OpenAI Codex / ChatGPT.
- **Documentação e Guia de Instalação (`README.md`):**
  - Reorganização didática em 4 partes essenciais: (1) Instalação rápida padrão, (2) Instalação local por LLM, (3) Instalação global por LLM e (4) Arquitetura de diretórios.
  - Inclusão das tabelas comparativas "Local vs. Global" e "Arquivos padrão por ferramenta" para Claude Code, Gemini CLI e OpenAI Codex.
  - Esclarecimento sobre o compartilhamento nativo de skills entre Gemini e Codex via `.agents/skills/` e symlinks no Claude Code.

## [2.6.0] - 2026-10-08

### Adicionado (Instalação Global, Suporte Universal ChatGPT & Modelos Agnósticos)

- **Instalação Global (`install.sh --global`):**
  - Adicionado suporte nativo à flag `--global` (ou `-g`) para instalação centralizada no sistema operacional do usuário (`$HOME`).
  - **Claude Code:** Mapeamento automático dos prompts como *Slash Commands* em `~/.claude/commands/`, permitindo invocar `/appsec-auditor`, `/full-app-validator`, `/tdd`, `/bdd`, `/sec-api`, `/threat-modeling`, etc., em qualquer pasta/repositório diretamente no terminal. Instalação global de Agent Skills em `~/.claude/skills/`.
  - **Google Antigravity:** Instalação global de Agent Skills em `~/.gemini/skills/` e `~/.gemini/antigravity-cli/skills/`, ativando o carregamento autônomo e semântico em qualquer workspace.
- **Suíte Universal para ChatGPT, Web Chats & Modelos Locais (`chatgpt/`):**
  - Criação da pasta oficial `chatgpt/` projetada para interfaces de chat web/desktop e 100% agnóstica de fornecedor (compatível com OpenAI, Claude Web, Gemini Web, DeepSeek e modelos locais via Ollama/Open WebUI).
  - `chatgpt/SYSTEM_INSTRUCTIONS.md`: Instrução de sistema mestra universal para colar em *Custom Instructions* ou System Prompts.
  - `chatgpt/custom-gpts/`: Templates pré-configurados para criação de assistentes personalizados no GPT Builder, Gemini Gems ou Claude Projects (`1-appsec-auditor.md`, `2-driven-development.md` e `3-full-app-validator.md`).
  - `chatgpt/prompts-condensed/`: Prompts autocontidos (sem dependência de imports `@` locais) prontos para copiar e colar com código.
  - `chatgpt/README.md`: Guia completo ilustrado de utilização e critérios agnósticos para escolha de perfis de modelos (Fronteira, Raciocínio, Produção e Local Open-Weight).
- **Foco Arquitetural e Descontinuação do Windsurf:**
  - Remoção de referências ao editor Windsurf em documentação, instaladores e testes, consolidando o foco do projeto na tríade: **Claude Code**, **AntiGravity** e **ChatGPT**.
- **Qualidade & Testes Automatizados:**
  - Inclusão dos testes `test_global_installer_execution` e `test_chatgpt_suite_integrity` em `tests/test_integrity.py`.
  - 100% dos 41 testes unitários e de integridade passando com sucesso.

## [2.5.0] - 2026-09-27

### Aprimorado (Integração do OWASP DSOMM na Suíte DevOps, CI/CD & SRE)

- **Adoção do OWASP DevSecOps Maturity Model (DSOMM):**
  - Integração do modelo de maturidade progressivo (Níveis 1 a 5) em toda a Parte 3 (DevOps, Infraestrutura e SRE), transformando checklists estáticos em roadmaps evolutivos.
- **Hardening de CI/CD (`prompts/devops/cicd_pipeline.md`):**
  - Mapeamento para a dimensão **Build and Deployment** do DSOMM.
  - Adição de verificações para atestações de proveniência **SLSA Level 2+/3+**, geração automatizada de **SBOM (CycloneDX/SPDX)**, assinatura criptográfica de artefatos com **Sigstore / Cosign** (keyless OIDC), proteção de branches com multi-party approvals e **Scorecard de Maturidade DSOMM (Níveis 1 a 5)**.
- **IaC, Containers & Kubernetes (`prompts/devops/iac_docker_k8s.md`):**
  - Mapeamento para as dimensões **Implementation** (Infrastructure Hardening, IAM, Container Security) e **Build and Deployment** (Policy Enforcement).
  - Adição de verificações para imagens mínimas **Distroless / Chainguard**, triagem de CVEs com critérios **CISA KEV / EPSS**, proteção e criptografia de estado `tfstate`, Shift-Left IaC scanning (Checkov/Trivy), **Policy-as-Code na admissão (OPA Gatekeeper / Kyverno)**, reconciliação de drift via **GitOps (ArgoCD/Flux)** e **Scorecard de Maturidade DSOMM**.
- **Resiliência, Observabilidade & SRE (`prompts/devops/resilience_observability.md`):**
  - Mapeamento para a dimensão **Information Gathering** (Logging, Monitoring, Alerting, Correlation).
  - Adição de verificações para armazenamento de logs imutável append-only (WORM / Object Lock), deploys canary com rollback automatizado baseado em violação de SLOs, correlação de eventos de segurança com traces OTel, práticas de **Chaos Security Engineering** e **Scorecard de Maturidade DSOMM**.
- **Documentação & Relatórios:**
  - Atualização do `README.md` com menções ao framework OWASP DSOMM, comandos atualizados e nova visão por níveis nos relatórios em PDF.

## [2.4.0] - 2026-09-27

### Adicionado (Novo Prompt Orquestrador Mestre: AppSec Auditor 360°)

- **Novo Prompt Oficial [`prompts/security/appsec_auditor.md`](prompts/security/appsec_auditor.md):**
  - Orquestrador de pentest e auditoria de segurança em profundidade de ponta a ponta, espelhando integralmente as 5 fases da Agent Skill `appsec-auditor` (Descoberta de Superfície, Inspeção de Código, Crítica de Viabilidade Mantis, Risco Calibrado 1-10 e PoCs com SARIF).
  - Permite invocar a auditoria completa de segurança via `@` no Claude Code, Cursor, VSCode e Windsurf (`@[.claude/prompts/security/appsec_auditor.md]`).
  - Alinhamento rigoroso com **OWASP ASTF 2023**, **OWASP ASVS v4.0.3 Nível 2** e **OWASP Risk Rating Methodology**.
  - Detecção de Shadow/Zombie APIs (ASVS V13.2.2), BOLA/IDOR (API1:2023), SSRF (API7:2023), Mass Assignment (API3:2023) e Injeções.
  - Eliminação de falsos positivos teóricos via *Mantis Viability Critique* (Reachability, Release Build Viability e Upstream Neutralization).
- **Documentação & Destaques (`README.md`):**
  - Seção de Destaques principais atualizada para apresentar as duas ferramentas 360° em conjunto: **Full App Validator 360°** (saúde geral, arquitetura e SRE) e **AppSec Auditor 360°** (segurança em profundidade, pentest e SARIF).
  - Guia de Ação Rápida e Catálogo Geral de Prompts atualizados para 41 prompts.
- **Automação & Qualidade (`install.sh` & `tests/test_integrity.py`):**
  - Catálogo expandido para 41 prompts no `install.sh` e `tests/test_integrity.py`.
  - 100% dos testes de integridade e regressão passando.

## [2.3.1] - 2026-09-27

### Aprimorado (Instalação Unificada de Prompts & Agent Skills no `install.sh`)

- **Instalação Automatizada Completa de Agent Skills:**
  - O script de instalação `install.sh` agora instala tanto os **40 prompts** quanto as **4 Agent Skills** (`appsec-auditor`, `driven-development`, `full-app-validator` e `jev-system-one`) em um único comando unificado.
  - Mapeamento nativo por IDE / ferramenta:
    - **Claude Code:** `.claude/prompts/` e `.claude/skills/`
    - **VSCode / Copilot:** `.agent/prompts/` e `.agent/skills/`
    - **Cursor:** `.cursor/rules/`, `.cursor/skills/` e `.agent/skills/`
    - **Windsurf:** `.windsurf/rules/`, `.windsurf/skills/` e `.agent/skills/`
    - **Universal (`all`):** instala em todas as pastas correspondentes.
  - Suporte ao argumento seletivo opcional de componente (`all`, `prompts` ou `skills`): `bash install.sh <target> <ide> <component>`.
  - Download rápido e atômico via tarball (`main.tar.gz`) com fallback resiliente para clone raso (`git clone --depth 1`) e limpeza automática via `trap`.
  - Preservação 100% não-destrutiva de diretórios pré-existentes e exclusão preventiva de artefatos de compilação Python (`__pycache__` e `*.pyc`).
- **Testes & Qualidade (`tests/test_integrity.py`):**
  - Adicionado `EXPECTED_SKILLS` e validação funcional de instalação em `test_installer_execution`.
  - `test_install_script_sync` atualizado para verificar a sincronia estrita de prompts e skills no `install.sh`.

## [2.3.0] - 2026-09-27

### Adicionado & Aprimorado (Expansão da Suíte Driven Design: DDD, TypeDD & DataDD)

Evolução arquitetural inspirada no artigo *"The Definitive Guide to ‘Driven’ Design: 8 Methodologies Every Engineer and Architect Must Master"*, cobrindo 100% das metodologias "Driven" da indústria de software corporativo:

- **Novos Prompts Oficiais (`prompts/driven-development/`):**
  - [`ddd_domain_driven.md`](prompts/driven-development/ddd_domain_driven.md): Domain-Driven Design completo cobrindo design estratégico (Bounded Contexts, Context Map, ACL) e tático (Aggregates com regra de 1 aggregate por transação, Entities, Value Objects imutáveis e Domain Events).
  - [`typedd_type_driven.md`](prompts/driven-development/typedd_type_driven.md): Type-Driven Design aplicando as regras de ouro de Yaron Minsky (*"Make illegal states unrepresentable"*) e Alexis King (*"Parse, don't validate"*), tipagem nominal com Branded Types e máquinas de estado por Discriminated Unions com checagem exaustiva (`assertNever`).
  - [`datadd_data_driven.md`](prompts/driven-development/datadd_data_driven.md): Data-Driven Design modelando esquemas a partir da Matriz de Padrões de Acesso (Access Patterns Matrix Q1/Q2/Q3), regra ESR (Equality, Sort, Range) para índices compostos, covering indexes (`INCLUDE`) e controle de concorrência com Optimistic Locking.

- **Evolução da Agent Skill `skills/driven-development`:**
  - `SKILL.md` atualizado para orquestrar o ciclo de vida completo em 6 fases (Domínio → Storage → Tipos → Contratos → Aceite/Abuso → TDD).
  - Novos guias modulares sob demanda em `references/`: `ddd-domain-driven.md`, `typedd-type-driven.md`, `datadd-data-driven.md` e `driven-pipeline-matrix.md` (composição de 3 a 5 metodologias por arquétipo de arquitetura: Fintech, B2B SaaS, Streaming e E-commerce).
  - Novos exemplos práticos em `examples/`: `typedd-state-machine.ts` e `datadd-access-patterns.sql`.

- **Testes & Integridade:**
  - Catálogo expandido para 40 prompts em `tests/test_integrity.py`, `install.sh` e `README.md`.
  - Novos testes unitários em `tests/test_driven_development.py` cobrindo TypeDD, DataDD e completude das referências da skill.

## [2.2.0] - 2026-09-27

### Adicionado (Full App Validator 360° – Zero Overkill & Zero Overlap)

- **Nova Agent Skill `skills/full-app-validator`:**
  - Avaliação holística da aplicação sem sobreposição (*zero overlap*) e sem desperdício analítico (*zero overkill*).
  - `SKILL.md`: Frontmatter YAML com acionamento semântico para diagnósticos completos de ponta a ponta em conformidade com o padrão aberto [Agent Skills](https://agentskills.io/specification).
  - `scripts/health_card.py`: Ferramenta CLI determinística que inspeciona a estrutura física da aplicação e gera o **Health Card 360°** com pontuações por fronteira (Borda, Domínio, Persistência, Qualidade e DevOps).
  - `references/domain-boundaries-matrix.md`: Matriz de demarcação estrita das 5 fronteiras herméticas, garantindo que nenhum conceito seja auditado duas vezes.
  - `references/anti-overkill-cascade.md`: Protocolo de triagem progressiva em 3 camadas (System 1 determinístico $\rightarrow$ System 2 focado).
- **Novo Prompt Orquestrador de Validação Holística:**
  - [`prompts/driven-development/full_app_validator.md`](prompts/driven-development/full_app_validator.md): Prompt orquestrador mestre para invocação direta via `@` no Claude Code, Cursor, VSCode e Windsurf.
- **Qualidade, Integridade & Testes:**
  - Sincronização automática em `install.sh`, `tests/test_integrity.py` e `README.md`.
  - Novos testes unitários dedicados em `tests/test_full_app_validator.py`.

## [2.1.0] - 2026-09-27

### Adicionado & Aprimorado (Integração das Inovações do Google Mantis)

Evolução metodológica e tática inspirada no projeto [Google Mantis](https://github.com/google/mantis) (*A modular, stack-agnostic toolkit for AI coding agents to autonomously find, reproduce, and patch vulnerabilities*):

- **Evolução da Skill `skills/appsec-auditor` (Fluxo em 5 Fases):**
  - **Crítica de Viabilidade de Release (`references/viability-critique.md`):** Protocolo anti-alucinação inspirado no `mantis-critic` e `mantis-review` para descartar código inalcançável (dead code), filtrar falhas restritas a `assert` de debug (que somem em release/produção com `python -O`), e verificar neutralização por gateways/DTO pipes.
  - **Calibração de Severidade Anti-Inflação (`references/risk-rating-methodology.md`):** Adoção da rubrica de calibração numérica do Mantis (Score 1-10) com multiplicadores de evidência e viabilidade para conter a inflação de severidade em LLMs.
  - **PoC Reproduction Harness (`references/poc-reproduction-harness.md`):** Estratégia em 3 camadas de reprodução (Tier 1: micro-harness unitário em memória $\rightarrow$ Tier 2: teste funcional com mock $\rightarrow$ Tier 3: sandbox isolada com gVisor `runsc --network=none`).
  - **Atualização dos Scripts e Relatórios (`sarif_builder.py` & `report_generator.py`):** Suporte nativo aos campos `risk_score`, `viability` e `poc_tier` nos relatórios SARIF 2.1.0, Markdown e templates de Issue.

- **Novos Prompts Táticos de AppSec (`prompts/security/`):**
  - [`adversarial_patching.md`](prompts/security/adversarial_patching.md): Protocolo de correção com separação de deveres (Blue Team patcher vs. Red Team re-attacker), caça a bypasses de encoding/path e teste de regressão automatizado (inspirado no `mantis-patch`).
  - [`exploit_chaining.md`](prompts/security/exploit_chaining.md): Metodologia para correlacionar múltiplos achados baixos/médios em cadeias de exploração de alto impacto (Super Findings / Kill Chains), com mapeamento de *choke points* defensivos (inspirado no `mantis-chain`).
  - [`vcs_security_history.md`](prompts/security/vcs_security_history.md): Mineração de histórico Git para rastrear CVEs passados, evitar regressões em refatorações e mapear invariantes históricos (inspirado no `mantis-history`).
  - [`sec_advisor.md`](prompts/security/sec_advisor.md): Assistente de codificação segura em tempo real (Shift-Left Pair Programming) para orientar o desenvolvedor durante a escrita de código (inspirado no `mantis-advise`).

- **Qualidade, Integridade & Testes:**
  - Atualização do catálogo em `install.sh`, `tests/test_integrity.py` e `README.md`.
  - Novos testes unitários em `tests/test_appsec_auditor.py`.


## [2.0.0] - 2026-09-22


### Adicionado & Aprimorado (Lançamento do Ecossistema de Agent Skills & Suíte Jev System One)

Evolução arquitetural da suíte para uma plataforma completa de **Prompts Estruturados + Agent Skills Executáveis**, em total conformidade com o padrão aberto [Agent Skills](https://agentskills.io/specification) para agentes de IA modernos (**Claude Code**, **Google Antigravity**, **Cursor**, **Windsurf** e **VSCode Copilot**).

- **Ecossistema de Agent Skills (`skills/`):**
  - **`skills/appsec-auditor`**: Skill completa de auditoria de segurança em 4 fases baseada no OWASP ASTF, ASVS v4.0.3 e OWASP Risk Rating:
    - `SKILL.md`: Frontmatter YAML com acionamento semântico (`Use when...`), diretrizes anti-fadiga e fluxo operacional.
    - `references/`: Documentação modular sob demanda (`owasp-api-astf.md`, `asvs-v4-checklist.md`, `access-control-bola.md`, `ssrf-prevention.md`, `risk-rating-methodology.md`).
    - `scripts/sarif_builder.py`: Ferramenta CLI e módulo nativo em Python (sem dependências externas) para conversão de achados em SARIF 2.1.0 para o GitHub Code Scanning / GitLab SAST.
    - `scripts/report_generator.py`: Gerador de relatórios Markdown executivos e templates de Issues GitHub prontas para rastreamento.
    - `examples/`: Fixtures práticas executáveis incluindo teste BOLA em pytest (`bola_idor_test.py`) e cliente TypeScript seguro contra SSRF (`ssrf_safe_fetch.ts`).
  - **`skills/driven-development`**: Skill de engenharia de software orientada por testes, especificações e contratos:
    - `SKILL.md`: Ciclo em 4 fases cobrindo SDD, BDD, SecDD, TDD (Red-Green-Refactor) e automação de pirâmide de testes.
    - `references/`: Guias modulares (`sdd-spec-driven.md`, `tdd-red-green-refactor.md`, `bdd-gherkin-scenarios.md`, `cdd-contract-testing.md`, `secdd-abuse-cases.md`, `test-pyramid-strategy.md`).
    - `scripts/test_runner.py`: Executor universal de testes com detecção automática de ecossistemas (Node, Python, Go, Rust) e saída estruturada em JSON ou terminal.
    - `examples/`: Schemas Zod com inferência e `.strict()`, fixtures de ciclo TDD com padrão AAA e especificações executáveis Gherkin (`.feature`).
  - **`skills/jev-system-one`**: Skill para integração e arquitetura com modelos System One (TypeSafe AI / Jev):
    - `SKILL.md`: Guia de arquitetura em cascata (System 1 + System 2), primitivas `Choice`, `Score` e `Noul` e aprovação gated por confiança.
    - `references/`: API Reference HTTP/REST, Guia Avançado de Primitivas e Mapeamento de Jaggedness / Anti-Patterns.
    - `examples/`: Implementações de guardrails LangChain, cascade em TypeScript, scanner híbrido de segredos, auditor de MCP/skills, sanitizador de PII e cálculo determinístico de CVSS.

- **Nova Categoria de Prompts (`prompts/jev/`):**
  - Adição de 8 prompts especializados para decisões e guardrails de alta velocidade (<100ms):
    - `system_one_architecture.md`: Arquitetura em cascata e eliminação de overkill de LLMs.
    - `agent_guardrails_safety.md`: Guardrails pré-execução de tools para agentes (OWASP LLM06).
    - `intent_routing_dispatch.md`: Roteamento de intenção e speculative fan-out.
    - `rag_verification_guardrails.md`: Verificação de fidedignidade e citações em RAG (OWASP LLM09).
    - `secret_detection_triage.md`: Triagem semântica de segredos e redução de falsos positivos.
    - `mcp_agent_security_scan.md`: Auditoria de segurança de MCP servers e Agent Skills.
    - `pii_sanitization_guardrail.md`: Sanitização e mascaramento de PII em três camadas.
    - `vulnerability_triage_cvss.md`: Triagem de falhas e cálculo determinístico de CVSS v3.1/v4.0.

- **Automação & Qualidade (`tests/` e `install.sh`):**
  - `tests/test_integrity.py`: Adição do teste `test_skills_integrity` (etapa 8/8) validando YAML frontmatter, campos obrigatórios e suítes unitárias de todas as skills.
  - `tests/test_appsec_auditor.py`: 6 testes unitários cobrindo o construtor SARIF 2.1.0, gerador de relatórios e ordenação de achados.
  - `tests/test_driven_development.py`: 5 testes unitários validando detecção de frameworks de teste e parsing de métricas.
  - `install.sh`: Suporte estendido para instalação da categoria `jev/`.

## [1.9.0] - 2026-09-15

### Adicionado & Aprimorado (Integração do OWASP ASVS v4.0.3 & OWASP Risk Rating Methodology)

Enriquecimento estritamente aditivo de todos os 13 prompts de segurança e do prompt de SecDD / Abuse Cases com requisitos formais de verificação e cálculo quantitativo de risco, mantendo 100% dos padrões, frameworks e controles existentes.

- **OWASP Application Security Verification Standard (ASVS v4.0.3):**
  - Mapeamento explícito de capítulos (V1 a V14) e Níveis de Verificação (L1: Oportunístico/Automático, L2: Aplicações com dados sensíveis, L3: Sistemas críticos) em todos os checklists e relatórios:
    - `api.md`: Capítulos V13 (API & Web Service), V1 (Architecture) e V14 (Configuration).
    - `authn_identity.md`: Capítulos V2 (Authentication) e V3 (Session Management).
    - `access_control.md`: Capítulo V4 (Access Control Verification).
    - `input_validation.md`: Capítulos V5 (Validation, Sanitization and Encoding) e V7 (Error Handling and Logging).
    - `db.md`: Capítulos V5 (SQLi), V8 (Data Protection) e V6 (Stored Cryptography).
    - `frontend.md`: Capítulos V5 (Output Encoding/XSS), V3 (Client Session) e V14 (Configuration).
    - `business.md`: Capítulos V11 (Business Logic) e V1 (Architecture & Design).
    - `secrets.md`: Capítulos V6 (Stored Cryptography), V8 (Data Protection) e V14 (Configuration).
    - `secure_config.md`: Capítulos V14 (Configuration), V7 (Logging/Errors) e V9 (Communications/TLS).
    - `ssrf.md`: Capítulos V12 (File & Resources - SSRF Protection) e V5 (Input Validation).
    - `supply_chain.md`: Capítulos V10 (Malicious Code) e V14 (Third-Party Components).
    - `threat_modeling.md`: Capítulo V1 (Architecture, Design and Threat Modeling).
    - `ai_appsec.md`: Capítulos V1 (Modelagem), V5 (Validação de Prompts/Inputs) e V10 (Malicious Code).
    - `secdd_abuse_cases.md`: Capítulos V1 (Architecture) e V11 (Business Logic Testing).
- **OWASP Risk Rating Methodology (RRM):**
  - Substituição da severidade intuitiva pelo cálculo formal padronizado pela OWASP: $\text{Severidade} = \text{Probabilidade (Likelihood)} \times \text{Impacto (Impact)}$.
  - Matriz determinística 3x3 (Alta/Média/Baixa Probabilidade $\times$ Alto/Médio/Baixo Impacto).
  - Adição de colunas de Probabilidade e Impacto nas tabelas de priorização de todos os prompts.
  - Card de achado enriquecido com justificativas formais de Agente de Ameaça, Facilidade de Descoberta/Exploração, Impacto Técnico e Impacto de Negócio (financeiro, conformidade regulatória/LGPD e reputação).
- **Entregáveis Automatizados (PDF, SARIF & GitHub Issues):**
  - Especificação de inclusão de Matriz de Calor 3x3 (Heatmap Likelihood × Impact) e tabelas de conformidade por capítulo ASVS nos relatórios PDF.
  - Inclusão de tags `ASVS-V*` e scores de risco no SARIF v2.1.0 para o GitHub Code Scanning.
  - Templates de issues no GitHub com justificativa de risco quantificada.
- **Engenharia de Software (SDD & BDD):**
  - Criação do documento formal de especificação arquitetural (SDD) e cenários executáveis Gherkin (BDD) para a integração de ASVS e Risk Rating.
- **Validação Automatizada de CI/CD (`tests/test_integrity.py`):**
  - Nova bateria `test_security_standards_coexistence` validando continuamente a coexistência de `OWASP ASVS` e `OWASP Risk Rating Methodology` em todos os 14 prompts de segurança.

## [1.8.0] - 2026-09-10

### Adicionado & Aprimorado (Cobertura Completa do OWASP Top 10 Proactive Controls 2024)

Fechamento das lacunas da suíte frente aos [OWASP Top 10 Proactive Controls (2024)](https://top10proactive.owasp.org/) e à [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/).

- **Novos prompts de auditoria em `prompts/security/`:**
  - **`authn_identity.md` (C7 – Secure Digital Identities):** hashing de senha (`Argon2id`), comparação em tempo constante, anti-enumeração, regeneração de sessão (*Session Fixation*), atributos de cookie, MFA/2FA + backup codes, JWT (rejeição de `alg:none`, validação de `iss`/`aud`/`exp`, rotação e revogação de refresh token), OAuth2/OIDC com Authorization Code + PKCE, `state`/`nonce` e allow-list de `redirect_uri`, e fluxos de reset/verificação de conta sem *Account Takeover*.
  - **`access_control.md` (C1 – Implement Access Control / A01:2021):** *deny-by-default*, centralização da decisão de autorização, *enforcement* server-side, IDOR/BOLA com checagem de titularidade e escopo na query (RLS), escalada vertical/BFLA, bypass por verbo HTTP, isolamento multi-tenant, testes negativos de autorização e *fail closed*.
  - **`ssrf.md` (C10 – Stop SSRF / A10:2021):** mapa de *sinks* de saída (webhooks, HTML→PDF, proxies de imagem, `$ref` remoto, XXE), *allow-list* de destino, validação pós-resolução DNS + *pinning* (anti DNS rebinding), bloqueio de faixas privadas/link-local, proteção do endpoint de metadata de nuvem (`169.254.169.254`, IMDSv2), *egress filtering* e tratamento de resposta anti-exfiltração.
  - **`secure_config.md` (C5 – Secure by Default / A05:2021):** estado default seguro, debug/stack traces desligados em produção, ausência de credenciais padrão, headers defensivos (`HSTS`, `CSP`, `X-Content-Type-Options`, `frame-ancestors`, `Referrer-Policy`, `Permissions-Policy`), CORS com *allow-list* estrita, atributos de cookie + CSRF, TLS 1.2+/1.3 obrigatório e *hardening* de container.
  - **`input_validation.md` (C3 – Validate Input & Handle Exceptions):** validação positiva (*allow-list*) em toda fronteira de confiança (incluindo consumidores de fila e webhooks), canonicalização Unicode antes da validação, schema estrito anti *Mass Assignment*, deserialização segura (XXE, *zip slip*, *zip bomb*, *formula injection*), parametrização de *sinks* e tratamento centralizado de exceções sem vazamento de stack trace.
- **Estendido — `devops/resilience_observability.md` (C9 – Security Logging & Monitoring):**
  - Nova seção **"Logging de Segurança e Monitoramento de Detecção"**: eventos de segurança auditados com contexto, redação obrigatória de segredos/PII em todos os *appenders*, integridade e retenção de logs *append-only*, prevenção de *Log Injection* (CR/LF), vocabulário de eventos padronizado, regras de alerta acionáveis e monitoramento da disponibilidade do próprio *pipeline* de logs.
- **Documentação (`README.md`):**
  - Nova seção **"🧭 Cobertura vs OWASP Top 10 Proactive Controls (2024)"** com matriz C1–C10 → prompt(s) responsável(is) → Cheat Sheets aplicados.
  - Catálogo de Segurança e árvore de diretórios atualizados com os 5 novos prompts.
- **Validação Automatizada (`tests/test_integrity.py` & `install.sh`):**
  - Registro dos 5 novos prompts em `EXPECTED_PROMPTS` e `PROMPT_FILES` (catálogo total: **24 prompts**).
  - Contagem de prompts na bateria de testes passou a ser dinâmica (`len(EXPECTED_PROMPTS)`), eliminando *drift* de números fixos.

## [1.7.0] - 2026-09-03

### Adicionado & Aprimorado (Suporte Nativo ao Claude Code & Multi-IDE Sync)
- **Suporte Oficial a `.claude/prompts/` (Padrão Nativo Anthropic):**
  - O instalador `install.sh` agora adota `.claude/prompts/` como diretório oficial padrão para o Claude Code.
  - O comando rápido `curl -sSL ... | bash` instala diretamente na árvore nativa `.claude/`.
- **Matriz de Instalação Modular por IDE (`install.sh`):**
  - Modo `claude` (padrão oficial): `.claude/prompts/`
  - Modo `vscode` / `agent`: `.agent/prompts/`
  - Modo `cursor`: `.cursor/rules/`
  - Modo `windsurf`: `.windsurf/rules/`
  - Modo `all`: sincronização simultânea nas 4 árvores de diretórios (`.claude`, `.agent`, `.cursor`, `.windsurf`).
- **Documentação e Exemplos de Invocação (`README.md`):**
  - Atualização dos 19 comandos de invocação rápida para a sintaxe nativa `@[.claude/prompts/...]`.
  - Instruções de uso claras diferenciando Claude Code, VSCode e Cursor.
- **Validação Automatizada de Multi-IDE (`tests/test_integrity.py`):**
  - Expansão do teste `test_installer_execution` para validar a presença física dos 19 prompts nas 4 pastas suportadas.

## [1.6.0] - 2026-09-03

### Aprimorado (Alinhamento com AI-Native Playbook & Priorização de Ferramentas)
- **Priorização de Ferramentas (Claude Code ➔ VSCode ➔ Cursor):**
  - Reestruturação de documentação, `README.md`, `project_context.md` e `install.sh` definindo **Claude Code** como ferramenta principal, seguido de **VSCode** e **Cursor**.
  - Menções isoladas ao Windsurf unificadas junto aos outros editores suportados.
- **Diretriz Anti-Fadiga e Anti-Alucinação (Filtro Factual):**
  - Inserida cláusula estrita em prompts de auditoria (`api.md`, `db.md`) proibindo achados hipotéticos sem evidência factual e separando recomendações cosméticas (`[NIT]`).
- **Prova de Conceito (PoC) & Comando de Verificação nos Achados:**
  - Cada achado de segurança agora inclui obrigatoriamente um comando de reprodução (`curl`, script, query) e um comando de verificação para validar a correção em 1 linha.
- **Regra Inviolável do Teste Travado (*Failing-Test-First*):**
  - Inserida em `tdd_test_driven.md` e `test_suite_generator.md` regra que proíbe expressamente que a IA enfraqueça asserções ou ignore testes para fazê-los passar; a correção deve ser 100% no código de produção.
- **Mapeamento em Memória (Passo Zero):**
  - Adicionada orientação de ordenação mental de dependências antes da escrita física de testes ou código.
- **Modernização do `CLAUDE.md` em `project_context.md`:**
  - Modelo atualizado com diretrizes modernas da Anthropic: regra de sub-1-página, bloco "Como Verificar seu Trabalho (Proof of Done)" com saídas literais esperadas e bloco "Erros Recorrentes (Regra do Erro Repetido)".

## [1.5.0] - 2026-09-02

### Adicionado (Suíte de Testes Unitários com Mocks para Sincronizadores)
- **Bateria de Testes Unitários (`tests/test_sync_scripts.py`):**
  - 12 testes automatizados usando `unittest` e `unittest.mock` da biblioteca padrão.
  - Validação de parsing do padrão OASIS SARIF v2.1.0, checagem de variáveis de ambiente obrigatórias, construção de payloads ricos em Atlassian Document Format (ADF) e Markdown.
  - Testes de algoritmos de deduplicação remota e cache em memória para Jira, GitHub Issues e GitLab Boards.
- **Integração na Bateria Central (`tests/test_integrity.py`):**
  - Adicionado o passo `[6/6]` executando a suíte unitária em CI/CD e localmente.

## [1.4.0] - 2026-09-02

### Adicionado (Sincronização Nativa com GitHub Issues e GitLab Boards)
- **Sincronizador com GitHub Issues (`examples/ci-cd/github_issues_sync.py`):**
  - Script autônomo em Python que consome o arquivo `results.sarif` e cria automaticamente Issues no GitHub para vulnerabilidades Críticas e Altas com zero duplicatas.
  - Formatação rica em GitHub Markdown contendo arquivo, linha, regra OWASP, evidência e labels escopadas (`severity:critical`, `appsec`, `bug`).
- **Sincronizador com GitLab Issues & Boards (`examples/ci-cd/gitlab_issues_sync.py`):**
  - Script autônomo em Python para integração com a API v4 do GitLab, criando issues com scoped labels (`severity::critical`) prontas para os Issue Boards da organização.
- **Workflows Atualizados (`github-actions-audit.yml` & `gitlab-ci-audit.yml`):**
  - Pipelines de clientes configurados com suporte completo a tickets em GitHub Issues, GitLab Boards e Jira.

## [1.3.0] - 2026-09-02

### Adicionado (Integração com Jira REST API v3 para CI/CD)
- **Sincronizador Automático com Jira (`examples/ci-cd/jira_sync.py`):**
  - Script autônomo em Python que consome o arquivo `results.sarif` e cria automaticamente cards no Jira para vulnerabilidades Críticas e Altas com prevenção de duplicatas via JQL.
- **Guia de Configuração (`examples/ci-cd/README.md`):**
  - Documentação completa para geração de tokens no Atlassian e configuração de Secrets de CI/CD.

## [1.2.0] - 2026-09-02

### Adicionado & Aprimorado (Pronto para CI/CD & Modelos para Clientes)
- **Modelos de CI/CD para Clientes (`examples/ci-cd/`):**
  - Adicionado template de **GitHub Actions** (`examples/ci-cd/github-actions-audit.yml`) para execução automática de auditoria de segurança com IA em Pull Requests, publicação de vulnerabilidades no **GitHub Code Scanning via SARIF** e upload do relatório em PDF como artefato de build.
  - Adicionado template de **GitLab CI** (`examples/ci-cd/gitlab-ci-audit.yml`) com integração nativa ao GitLab SAST reports.
- **Esteira de CI/CD do Repositório (`.github/workflows/ci.yml` & `.gitlab-ci.yml`):**
  - Implementado pipeline do GitHub Actions com validação de ShellCheck, bateria de testes de integridade e scanner de segredos (Gitleaks).
  - Corrigido e aprimorado o pipeline do GitLab CI.
- **Bateria de Testes Automatizados de Integridade (`tests/test_integrity.py`):**
  - Script autônomo em Python validando a existência física dos 19 prompts, contrato estrutural de seções obrigatórias, integridade do `install.sh`, referências no `README.md` e testes funcionais de instalação.
- **Inclusões Cirúrgicas do OWASP WSTG v4.2:**
  - Validação de Magic Bytes e anti-path traversal em uploads (`api.md` e `business.md`).
  - Directory / Path Traversal em leitura de arquivos (`api.md`).
  - Server-Side Template Injection / SSTI em SSR (`api.md` e `frontend.md`).
  - Segurança de WebSockets e prevenção de CSWSH (`api.md` e `frontend.md`).
  - Fixação de sessão e mitigação de enumeração de contas (`secrets.md` e `api.md`).

## [1.1.0] - 2026-09-02

### Adicionado & Aprimorado (Alinhamento OWASP ASTF 2023 & OWASP Cheat Sheet Series)
- **Segurança de APIs (`api.md`):** Alinhamento a 16 módulos ASTF 2023, GraphQL, gRPC, LLM APIs e exportação SARIF.
- **Banco de Dados (`db.md`):** Menor privilégio no DB, TLS obrigatório, criptografia de campos sensíveis (KMS) e NoSQL injection.
- **Gestão de Segredos (`secrets.md`):** Padrão ouro Argon2id, Salt+Pepper com KMS, Timing Attacks e Zeroization.
- **Lógica de Negócio (`business.md`):** Chaves de idempotência (`Idempotency-Key`), TOCTOU, HPP e trilhas de auditoria.
- **Modelagem de Ameaças (`threat_modeling.md`):** Manifesto de Threat Modeling e decomposição STRIDE-per-Element.
- **SecDD (`secdd_abuse_cases.md`):** Testes automatizados de invasão, BOLA cross-tenant e concorrência maliciosa.
- **Frontend (`frontend.md`):** Trusted Types API, segurança de `postMessage`, cookies seguros e CSP estrito.
- **Supply Chain (`supply_chain.md`):** OWASP SCVS, geração de SBOM (CycloneDX/SPDX) e anti-slopsquatting.
- **Segurança em CI/CD (`cicd_pipeline.md`):** Hardening de esteiras, OIDC e pinning SHA-256.

## [1.0.0] - 2026-09-01

### Adicionado
- Versão inicial com os 19 prompts estruturados nas categorias Driven Development, Security e DevOps.
