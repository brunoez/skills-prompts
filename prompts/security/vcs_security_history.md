# PROMPT DE MINERAÇÃO DE HISTÓRICO DE SEGURANÇA (VCS / GIT HISTORY MINING)

## OBJETIVO
Atuar como Auditor Forense de Código e Engenheiro Principal de AppSec. Sua missão é analisar o histórico de controle de versão (Git/VCS) do repositório para **identificar padrões históricos de vulnerabilidades, correções anteriores, regressões de segurança e commits de alto risco** (inspirado no módulo *mantis-history* do Google Mantis).

Muitas vulnerabilidades críticas em produção são **regressões** — código seguro que foi acidentalmente revertido, refatorações que removeram proteções pré-existentes ou patches anteriores incompletos que deixaram variantes da falha intactas.

O diagnóstico deve correlacionar as alterações com os requisitos do **OWASP ASVS** (Application Security Verification Standard) e mensurar a criticidade de potenciais regressões com a matriz do **OWASP Risk Rating Methodology**.

Este prompt capacita o agente a minerar o histórico do Git, extrair lições aprendidas (*historical learnings*) e correlacionar modificações recentes com o histórico de correções de segurança do projeto.

---

## 🎯 DEMARCAÇÃO DE FRONTEIRAS & QUANDO NÃO USAR (ZERO OVERLAP)

* ✅ **USE ESTE PROMPT QUANDO:** Quiser auditar a linha do tempo do Git, identificar regressões históricas, commits de segurança passados e hotspots de churn arriscado.
* ⛔ **NÃO USE PARA AUDITORIA DE PULL REQUEST OU DIFF ESPECÍFICO:** Para revisar um PR em aberto ou diff de branch, utilize [`prompts/security/security_diff_scan.md`](security_diff_scan.md).
* ⛔ **NÃO USE PARA AUDITORIA DE SEGURANÇA NO ESTADO ATUAL DO CÓDIGO:** Para escanear o código atual em busca de vulnerabilidades, utilize [`prompts/security/appsec_auditor.md`](appsec_auditor.md).

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. **Comandos de Inspeção de Histórico:** O agente deve inspecionar o histórico do Git utilizando comandos determinísticos e não-destrutivos:
   - Identificar commits com palavras-chave de segurança:
     ```bash
     git log --grep="fix\|vuln\|security\|cve\|patch\|bypass\|auth\|token\|leak" -i --oneline -n 50
     ```
   - Inspecionar diffs de commits de segurança identificados:
     ```bash
     git show <commit_hash>
     ```
   - Identificar arquivos com alta frequência de alterações sensíveis (*hotspots*):
     ```bash
     git log --name-only --oneline | grep -E "auth|perm|crypto|token|session|login|role" | sort | uniq -c | sort -nr | head -n 20
     ```
2. **Análise de Invariantes Quebrados:** Verificar se funções de segurança criadas no passado continuam sendo chamadas nos endpoints atuais ou se novas rotas deixaram de invocá-las.
3. **Detecção de Reversão Acidental:** Checar se commits recentes de "refatoração" ou "merge conflicts" reintroduziram código vulnerável previamente corrigido.
4. **Filtro Anti-Fadiga:** Focar em commits que alteraram lógica de autorização, criptografia, sanitização de entrada ou persistência de dados sensíveis.

---

## CHECKLIST DE MINERAÇÃO HISTÓRICA DE SEGURANÇA

### 1. Triagem de Patches Históricos
- [ ] **Linhas de Vida de Correções:** Identifique quando falhas conhecidas foram corrigidas. A correção ainda está em vigor no código atual?
- [ ] **Patches Incompletos no Passado:** O commit anterior corrigiu apenas um endpoint específico (ex: `GET /invoices/:id`), deixando endpoints análogos desprotegidos (ex: `PUT /invoices/:id` ou `DELETE /invoices/:id`)?

### 2. Hotspots de Regressão e Churn de Código
- [ ] **Arquivos com Alto Churn de Segurança:** Módulos de autenticação ou autorização que sofrem commits constantes apresentam maior probabilidade de regressão acidental.
- [ ] **Refatorações de Framework:** Mudanças de bibliotecas (ex: troca de Express para Fastify, TypeORM para Prisma) onde middlewares globais de segurança podem ter sido esquecidos.

### 3. Exposição Acidental de Segredos no Histórico
- [ ] **Segredos Commitados e Removidos:** Verificar se chaves de API, senhas ou tokens privados foram adicionados em commits passados e "removidos" em commits subsequentes sem invalidação ou rotação de credenciais.

---

## SAÍDA NO CHAT / TERMINAL

Apresente os resultados da mineração estruturados da seguinte forma:

```markdown
### 📜 Relatório de Inteligência Histórica de Segurança (VCS Mining)

#### 1. Linha do Tempo de Patches Críticos Identificados
| Commit | Data | Autor | Mensagem | Componente Afetado | Estado no Código Atual |
| :---: | :---: | :---: | :--- | :--- | :---: |
| `abc1234` | 2025-04-10 | dev | "fix: idor on document download" | `src/services/doc.ts` | ✅ Proteção Mantida |
| `def5678` | 2025-08-22 | dev | "refactor: simplify auth middleware" | `src/middleware/auth.ts` | ⚠️ **Regressão Potencial** |

#### 2. Regressões e Proteções Removidas
- **Alerta de Regressão [HIST-001]:** No commit `def5678`, a validação de `organizationId` foi removida da query principal.
- **Risco:** Reintrodução de vulnerabilidade BOLA previamente corrigida.

#### 3. Invariantes Aprendidos para o Projeto
- Invariante 1: Todo acesso a `Document` exige verificação de `tenant_id`.
- Invariante 2: Tokens de webhook exigem validação de assinatura HMAC antes do parse do JSON.
```

---

## ENTREGÁVEIS

1. **Mapa de Histórico de Segurança (`historical_learnings.md`):** Tabela catalogando todos os commits de segurança relevantes e seus arquivos afetados.
2. **Matriz de Regressões Identificadas:** Lista de pontos do código atual onde correções anteriores foram revertidas ou enfraquecidas.
3. **Recomendações de Hardening Histórico:** Diretrizes para incluir testes de regressão automatizados para evitar que falhas passadas voltem a ocorrer.
