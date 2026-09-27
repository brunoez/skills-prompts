# Matriz de Fronteiras de Domínio (Zero Overlap)

A causa primária de lentidão, estouro de contexto e análises conflitantes em IA é a **sobreposição de escopo (*overlap*)** — múltiplos prompts ou etapas tentando auditar o mesmo arquivo ou conceito (ex: validar parâmetros no controller, no service e na query SQL).

Esta matriz define contratos herméticos de responsabilidade exclusiva: cada camada é inspecionada uma única vez pelo seu vetor específico.

---

## 1. As 5 Fronteiras Herméticas da Aplicação

```mermaid
flowchart LR
    F1["1. Borda / Edge<br/>(API, Contratos & DTOs)"] --> F2["2. Core / Domínio<br/>(Regras, Invariantes & DDD)"]
    F2 --> F3["3. Persistência<br/>(Queries, RLS & Transações)"]
    F1 -.-> F4["4. Qualidade & Testes<br/>(test_runner & Cobertura)"]
    F3 -.-> F5["5. DevOps & SRE<br/>(CI/CD, Docker & Logs)"]
```

| Fronteira | Responsabilidade EXCLUSIVA | O que NÃO deve ser auditado aqui (Evita Overlap) |
| :--- | :--- | :--- |
| **1. Borda & Contratos (API/Edge)** | - Roteamento HTTP/gRPC/GraphQL.<br/>- Parsing e validação de schema de entrada (Zod, Pydantic, OpenAPI).<br/>- Rejeição de campos extras com `.strict()` (Anti Mass Assignment).<br/>- Autenticação e extração de identidade de sessão (`req.user`).<br/>- Headers de segurança (CORS, CSP, HSTS). | ❌ Não audita queries de banco de dados.<br/>❌ Não audita regras de negócio de checkout/cálculo.<br/>❌ Não analisa Dockerfiles ou CI/CD. |
| **2. Domínio & Core de Negócio** | - Invariantes e regras de negócio essenciais (DDD).<br/>- Chaves de idempotência em transações financeiras (`Idempotency-Key`).<br/>- Prevenção de condições de corrida (TOCTOU) e pulo de etapas.<br/>- Modelagem semântica documentada (`CONTEXT.md`). | ❌ Não audita formatação de JSON ou rotas HTTP.<br/>❌ Não audita dialetos de SQL.<br/>❌ Não audita pipelines de deploy. |
| **3. Persistência & Dados (DB)** | - Parametrização estrita de queries (Prevenção de SQLi/NoSQLi).<br/>- Restrição de escopo multitenant (`where: { tenant_id }`) e RLS.<br/>- Controle transacional (ACID) e isolamento em operações concorrentes.<br/>- Versionamento de migrações e criptografia de campos sensíveis (KMS). | ❌ Não audita validação de input de controllers (já feito na Borda).<br/>❌ Não re-audita tokens JWT de usuário.<br/>❌ Não audita arquivos de teste unitário. |
| **4. Qualidade & Testes (QA/TDD)** | - Execução real de testes locais (`pytest`, `npm test`, `test_runner.py`).<br/>- Distribuição da pirâmide de testes (Unitários AAA > Integração > E2E).<br/>- Presença de testes de abuso (SecDD) para cenários negativos.<br/>- Saúde de dependências e cobertura de código. | ❌ Não faz code review de estilo de código.<br/>❌ Não audita infraestrutura de nuvem.<br/>❌ Não repete testes funcionais manuais. |
| **5. DevOps, SRE & Resiliência** | - Hardening de containers (Docker rootless, multi-stage builds).<br/>- Segurança em CI/CD (OIDC federado, pinning SHA-256 de actions, sem secrets).<br/>- Circuit Breakers, retries com jitter e Graceful Shutdown.<br/>- Observabilidade (OpenTelemetry, logs estruturados sem PII). | ❌ Não audita regras de negócio da aplicação.<br/>❌ Não audita DTOs de APIs.<br/>❌ Não audita schemas do banco. |

---

## 2. Princípio de Não-Interferência

Se um problema for detectado na **Borda** (ex: endpoint aceita campo arbitrário sem validação Zod), ele deve ser registrado como **Falha de Borda**.
O auditor NÃO deve registrar a mesma falha na camada de **Persistência** alegando que o campo pode atingir o banco; cada fronteira possui seu próprio mecanismo de contenção em Defesa em Profundidade.
