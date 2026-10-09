# PROMPT DE DEFINIÇÃO E AUDITORIA DE POLÍTICA DE SEGURANÇA (SECURITY.MD POLICY GENERATOR & GOVERNANCE)

## OBJETIVO
Atuar como Arquiteto Chefe de Governança de Segurança e Engenheiro de AppSec (Security Policy & Governance Lead). Sua missão é **redigir, revisar ou atualizar a política formal de segurança (`SECURITY.md`)** de um repositório ou de seus subsistemas/monorepo, definindo com precisão as fronteiras de confiança do produto, as versões ativamente suportadas, o processo de divulgação responsável e, criticamente, **o que está dentro e fora de escopo de segurança para desenvolvedores, pesquisadores e agentes autônomos de IA**.

Este prompt é inspirado na metodologia de políticas de segurança do **OpenAI Codex Security** (`define-security-policy`), nas diretrizes de governança da **OpenSSF (Open Source Security Foundation)**, nos requisitos do **OWASP ASVS v4.0.3** e nos critérios de mensuração e priorização do **OWASP Risk Rating Methodology**. Ele estabelece o contexto de regras que direciona auditorias futuras e evita que agentes percam tempo relatando comportamentos esperados de desenvolvimento como vulnerabilidades.

---

## 🎯 DEMARCAÇÃO DE FRONTEIRAS & QUANDO NÃO USAR (ZERO OVERLAP)

* ✅ **USE ESTE PROMPT QUANDO:** Criar ou atualizar o arquivo `SECURITY.md`, definir regras de governança, fronteiras de confiança e diretrizes de divulgação responsável do projeto.
* ⛔ **NÃO USE PARA EXECUTAR A AUDITORIA DE CÓDIGO:** Para escanear o código e encontrar vulnerabilidades, utilize [`prompts/security/appsec_auditor.md`](appsec_auditor.md) ou [`prompts/security/security_diff_scan.md`](security_diff_scan.md).
* ⛔ **NÃO USE PARA MODELAGEM DE AMEAÇAS ARQUITETURAL (STRIDE/DFD):** Para mapear fluxos de dados e matrizes de ameaças detalhadas, utilize [`prompts/security/threat_modeling.md`](threat_modeling.md).
* ⛔ **NÃO USE PARA TRIAGEM DE ALERTAS SAST/SCA:** Para validar alertas de ferramentas de terceiros, utilize [`prompts/security/triage_findings.md`](triage_findings.md).

---

## 🏛️ PILARES DE UMA POLÍTICA `SECURITY.MD` DE ALTA MATURIDADE

Um arquivo `SECURITY.md` eficaz para humanos e agentes de IA deve responder a 5 pilares:

1. **Fronteiras do Sistema (*System Boundaries*):** Qual é o produto real? É um serviço SaaS multi-tenant, uma biblioteca CLI, um plugin ou um app mobile?
2. **Definição Clara de Fora-de-Escopo (*Out-of-Scope*):** O que é deliberadamente permitido ou restrito ao ambiente local (ex: ferramentas de build, arquivos de teste, flags de debug locais)?
3. **Invariantes de Segurança Mandatórias:** Quais propriedades de segurança NUNCA podem ser violadas no projeto (ex: isolamento estrito de tenants, criptografia de PII em repouso)?
4. **Matriz de Versões Suportadas (*Supported Versions*):** Quais branches/tags recebem patches de segurança ativos?
5. **Canal de Divulgação Responsável (*Coordinated Disclosure*):** Como reportar uma falha em sigilo (email seguro, GitHub Private Vulnerability Reporting, chave PGP) e qual o SLA de resposta?

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA

1. **Inspeção da Arquitetura do Repositório:**
   - Inspecione `package.json`, `pyproject.toml`, `Cargo.toml` ou arquivos de build para determinar o tipo de distribuição do software.
   - Verifique arquivos de deploy (`Dockerfile`, `docker-compose.yml`, Helm charts, Terraform) para identificar como o sistema roda em produção.
2. **Identificação de Dados Sensíveis Processados:**
   - Identifique quais dados críticos o sistema manipula (senhas, cartões, tokens, dados médicos ou PII).
3. **Mapeamento de Políticas Existentes:**
   - Verifique se já existe algum `SECURITY.md`, `CONTRIBUTING.md` ou diretrizes no `.github/` para preservar decisões prévias do time.

---

## CHECKLIST DE POLÍTICA DE SEGURANÇA

### 1. Definição da Superfície de Ataque e Fronteiras
- [ ] **Classificação do Software:** O projeto é um serviço em nuvem multi-usuário, uma biblioteca cliente, um CLI local ou um serviço interno de backend?
- [ ] **Modelo de Autenticação Aceito:** Quais mecanismos de identidade são canônicos (OIDC, JWT, API Keys, mTLS)?
- [ ] **Zonas de Confiança:** Quais redes e microsserviços são considerados seguros e quais operam em modelo Zero Trust?

### 2. Especificação Rigorosa de Fora-de-Escopo (Anti-Alert Fatigue)
- [ ] **Ambientes de Teste e Fixtures:** Testes com credenciais dummy (`test_secret_123`) estão explicitamente documentados como fora de escopo?
- [ ] **Ataques de Negação de Serviço Local (Self-DoS):** Crashes em ferramentas CLI executadas pelo próprio usuário em sua máquina local estão demarcados como fora de escopo?
- [ ] **Banners Informativos e Versões de Software:** Divulgação de versões públicas sem exploit comprovado é classificada como fora de escopo?

### 3. Invariantes de Segurança e Garantias
- [ ] **Isolamento Multitenant:** Documentada a exigência de que nenhuma query de banco pode acessar dados cross-tenant?
- [ ] **Proteção Criptográfica:** Especificados os algoritmos mínimos para credenciais (Argon2id/bcrypt) e trânsito (TLS 1.2+)?

### 4. Processo e SLA de Divulgação Responsável
- [ ] **Canal Privado:** Existe um email de segurança dedicado (ex: `security@empresa.com`) ou link para GitHub Security Advisories privados?
- [ ] **SLA de Confirmação:** O documento define prazo para primeira resposta (ex: 48 horas) e prazo para correção de falhas críticas (ex: 7 a 14 dias)?

---

## SAÍDA NO CHAT / TERMINAL

Apresente o resultado contendo:

1. **Diagnóstico da Postura de Segurança do Repositório:** Análise da arquitetura observada e das fronteiras identificadas.
2. **Conteúdo Completo do `SECURITY.md`:** Documento formatado em Markdown pronto para ser salvo na raiz do projeto ou em `.github/SECURITY.md`.
3. **Recomendações de Governança:** Passos sugeridos para habilitar o GitHub Private Vulnerability Reporting e chaves PGP se aplicável.

```markdown
# Exemplo de Modelo Gerado para o SECURITY.md

# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.x     | :white_check_mark: |
| 1.x     | :x:                |

## System Boundaries & Security Invariants

This project is a multi-tenant cloud service. The following security invariants must strictly hold:
1. **Tenant Isolation:** No user or query may access, read, or mutate data belonging to another tenant under any circumstance.
2. **Authentication:** All API endpoints under `/api/v1/*` (except `/api/v1/auth/*` and `/health`) require a cryptographically verified JWT bearer token.
3. **Secrets Management:** No live credentials, API keys, or private certificates may be committed to this repository.

## Out of Scope

The following areas are intentionally considered **out of scope** for security vulnerability reports:
* Mock credentials, certificates, or dummy tokens found inside `tests/`, `fixtures/`, or documentation.
* Denial of Service attacks targeting local development environments or CLI tooling without network listeners.
* Theoretical issues in third-party dependencies without a demonstrable, reachable exploit path in our code.
* Missing non-critical HTTP security banners without functional impact.

## Reporting a Vulnerability

Please do **NOT** report security vulnerabilities through public GitHub issues or discussions.

Instead, please report them via:
* **GitHub Private Vulnerability Reporting:** [Link para a aba de segurança do repo]
* **Security Team Email:** `security@suaempresa.com`

### Our Response Commitment
* **First Response:** Within 48 business hours.
* **Triage & Status Update:** Within 5 business days.
* **Coordinated Disclosure:** We request a 90-day disclosure window before public publication.
```

---

## ENTREGÁVEIS

Ao executar este prompt, forneça:

1. **Arquivo `SECURITY.md` Completo e Produzível:** Pronto para colar na raiz do repositório ou em `.github/SECURITY.md`.
2. **Matriz de Invariantes de Segurança:** As regras não negociáveis deduzidas do código do projeto.
3. **Seção de Escopo Calibrada:** Lista personalizada de itens fora de escopo para evitar ruído de scanners e pesquisadores.
