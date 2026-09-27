# PROMPT DE AUDITORIA COMPLETA: SEGURANÇA EM CI/CD, PIPELINES (OWASP CI/CD SECURITY & OWASP DSOMM) E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de DevSecOps e Especialista em Segurança de Pipelines (CI/CD Security & Pipeline Hardening Lead). Sua missão é realizar uma varredura rigorosa em todas as configurações de **CI/CD e automação** do repositório (GitHub Actions, GitLab CI, CircleCI, Bitbucket Pipelines, Jenkinsfiles, Azure Pipelines), aplicando conjuntamente:
1. **OWASP Top 10 CI/CD Security Risks** e **OWASP CI/CD Security Cheat Sheet**;
2. **OWASP DevSecOps Maturity Model (DSOMM)** — Dimensão **Build and Deployment** (Subdimensões: *Build Security*, *Artifact Security*, *Deployment*, *Secret Management*).

A auditoria deve avaliar não apenas falhas pontuais nos arquivos de configuração, mas também o **Nível de Maturidade DevSecOps (Níveis 1 a 5 do DSOMM)** do repositório, cobrindo injeção de comandos em runners (*Workflow Script Injection*), vazamento de credenciais na esteira, ausência de SHA Pinning em Actions, abuso de gatilhos em pull requests de forks (`pull_request_target`), permissões excessivas de tokens de CI, atestações de proveniência **SLSA Level 2+/3+**, geração de **SBOM (Software Bill of Materials)**, assinatura criptográfica com **Cosign/Sigstore** e políticas de proteção de branches e deploys.

Ao final da auditoria, você deve listar os achados no chat/terminal, apresentar o **Scorecard de Maturidade DSOMM** e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie todos os arquivos de configuração de automação e esteira:
   - **GitHub Actions:** `.github/workflows/*.yml`, `.github/workflows/*.yaml`, `.github/actions/`.
   - **GitLab CI:** `.gitlab-ci.yml`, arquivos incluídos em `ci/`.
   - **Outros:** `Jenkinsfile`, `.circleci/config.yml`, `bitbucket-pipelines.yml`, `azure-pipelines.yml`.
2. Identifique os gatilhos (*triggers*), matriz de execução, permissões de tokens, segredos referenciados, scripts executados nos jobs e políticas de publicação/deploy de artefatos.
3. Você DEVE ler e analisar cada workflow linha por linha. Não faça suposições sem validar o código-fonte correspondente.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (OWASP CI/CD & DSOMM BUILD AND DEPLOYMENT)

### 1. Injeção de Expressões e Comandos (Workflow Script Injection)
- [ ] **Uso Inseguro de Contextos em Scripts Inline:** Identifique o uso direto de variáveis de contexto controladas pelo usuário (ex: `${{ github.event.issue.title }}`, `${{ github.head_ref }}`, `${{ github.event.comment.body }}`, `${{ github.event.pull_request.title }}`) dentro de comandos `run:`, permitindo execução arbitrária de código (`eval/bash injection`).
- [ ] **Uso de Variáveis de Ambiente Intermediárias:** Verifique se os inputs dinâmicos são passados de forma segura como variáveis de ambiente (`env: PR_TITLE: ${{ github.event.issue.title }}`) antes de serem lidos pelo script shell.
- [ ] **Gatilhos Inseguros em PRs de Forks (`pull_request_target`):** Verifique se workflows com `pull_request_target` realizam `checkout` de código de forks não confiáveis com privilégios de gravação ou acesso a segredos do repositório.

### 2. Permissões de Tokens e Princípio do Menor Privilégio (OWASP CI Token Hardening & DSOMM Level 2-3)
- [ ] **Escopo de `GITHUB_TOKEN` / CI Tokens:** Verifique se os workflows definem permissões mínimas explícitas no nível de arquivo ou job (ex: `permissions: contents: read` ou `permissions: {}`), evitando o padrão perigoso de `permissions: write-all` ou permissões implícitas de escrita.
- [ ] **Autenticação OIDC vs Chaves Estáticas de Nuvem:** Verifique se as integrações com AWS, GCP ou Azure utilizam autenticação federada via **OpenID Connect (OIDC)** com assunção de Roles temporárias, em vez de chaves de acesso estáticas de longa duração (`AWS_SECRET_ACCESS_KEY`, `GOOGLE_APPLICATION_CREDENTIALS`) salvas em segredos de CI.

### 3. Imutabilidade, Pinning e Cadeia de Suprimentos (DSOMM Build - Artifact Security Level 3-4)
- [ ] **Pinning por SHA-256 (Full Commit Hash):** Identifique o uso de Actions de terceiros apontando para tags mutáveis de versão (ex: `uses: actions/checkout@v4` ou `uses: third-party/action@master`) em vez do SHA imutável do commit (`uses: actions/checkout@2541b1294d2704b0964813337f33b291d3f8596b # v4.0.0`), prevenindo ataques de sequestro de repositório de Actions.
- [ ] **Auditoria de Reputação de Ações:** Identifique Actions mantidas por forks ou criadores anônimos sem verificação oficial da plataforma ou sem histórico confiável.
- [ ] **Geração Automatizada de SBOM (DSOMM Level 3):** Verifique se o pipeline gera automaticamente um **Software Bill of Materials (SBOM)** em padrão CycloneDX ou SPDX para rastreabilidade de bibliotecas e componentes (ex: via Syft, Trivy ou cdxgen).
- [ ] **Assinatura e Atestação de Proveniência SLSA (DSOMM Level 4):** Verifique se pacotes, binários e imagens OCI gerados no pipeline são assinados criptograficamente via **Sigstore / Cosign** (usando OIDC keyless signing) e se possuem atestados de proveniência em conformidade com **SLSA Level 2+ ou 3+**.

### 4. Gestão de Segredos, Isolamento de Runners e Deploys (DSOMM Deployment Level 3-5)
- [ ] **Exposição de Segredos em Logs:** Verifique se comandos de echo, dumps de ambiente (`printenv`, `env`) ou scripts de debug podem imprimir segredos desmascarados nos logs de execução do pipeline.
- [ ] **Runners Efêmeros e Isolados (DSOMM Build Level 3):** Verifique se os runners auto-hospedados (self-hosted) operam de modo efêmero (recriados a cada execução) ou se há risco de persistência de artefatos maliciosos entre builds de branches/PRs distintos.
- [ ] **Proteção de Branches e Gates de Aprovação (DSOMM Deployment Level 3-4):** Verifique a existência de regras de proteção de branch (`main`/`release`) exigindo PRs com revisão obrigatória de código (*multi-party approval*), bloqueio de force push e status checks com testes de segurança verdes antes do merge.
- [ ] **Gating Automatizado de Políticas no Deploy (DSOMM Deployment Level 4):** Verifique se etapas de deploy contam com validação de políticas pré-deploy (ex: Open Policy Agent, Conftest, Cosign verify) bloqueando qualquer artefato que não possua atestado válido.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a auditoria estruturada:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados encontrados:

| ID | Arquivo / Ponto | Categoria | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `.github/workflows/deploy.yml:15` | Script Injection via Context | CRÍTICA | Baixo (15 min) | **SIM** |
| #2 | `.github/workflows/ci.yml:3` | Permissão Excessiva (Write-All) | ALTA | Baixo (5 min) | **SIM** |
| #3 | `.github/workflows/release.yml:22` | Falta de SHA Pinning | MÉDIA | Baixo (10 min) | **SIM** |

*(Quick Win: Problema de Severidade ALTA ou CRÍTICA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome da Vulnerabilidade em CI/CD]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/workflow.yml:linha`
- **Categoria:** [Script Injection / Token Permissions / Action Pinning / OIDC Hardening / Log Leakage / Runner Security / Supply Chain & SBOM]
- **Mapeamento DSOMM:** [Dimensão / Subdimensão / Nível atingido vs Nível esperado]
- **Vetor de Exploração:** Explicação direta de como um atacante pode comprometer a esteira, roubar segredos de produção ou injetar código malicioso no build.
- **Evidência:** Trecho do arquivo YAML de workflow.
- **Correção Recomendada:** Código YAML corrigido e seguro.

### PARTE 3: SCORECARD DE MATURIDADE DSOMM (BUILD AND DEPLOYMENT)
Apresente uma tabela de avaliação da maturidade DevSecOps do repositório:

| Subdimensão DSOMM | Nível Atual (1-5) | Status | Requisito para Próximo Nível |
|---|:---:|---|---|
| **Build Security** (Automação & Runners) | Nível [X] | [Em progresso/Adequado] | [Ação necessária] |
| **Artifact Security** (Pinning, SBOM, Cosign) | Nível [X] | [Crítico/Em progresso] | [Ação necessária] |
| **Deployment Security** (Branch Protection & Gates) | Nível [X] | [Em progresso/Adequado] | [Ação necessária] |
| **Secret Management** (OIDC & Token Hardening) | Nível [X] | [Crítico/Adequado] | [Ação necessária] |

**Nível Geral de Maturidade em CI/CD:** `Nível X / 5`
**Roadmap de Evolução:** Resumo em 3 passos para atingir o nível superior na escala DSOMM.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/cicd-audit/relatorio-auditoria-cicd.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria de Segurança em CI/CD e Pipelines (OWASP CI/CD & DSOMM Standards) — <nome do projeto>", data, esteiras mapeadas e pontuação geral de maturidade DevSecOps.
b) **Resumo Executivo:** Total de achados por severidade, gráfico de rosca de severidade e gráfico de barras por categoria de risco de pipeline.
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Scorecard e Radar de Maturidade DSOMM:** Gráfico de teia/radar ou tabela comparativa exibindo os Níveis 1 a 5 da dimensão *Build and Deployment*.
d) **Pontos Fortes** (uso de OIDC, permissões restritas) e **Pontos Fracos** (injeções potenciais, pinning ausente, falta de SBOM/Cosign).
e) **Matriz de Conformidade OWASP CI/CD & DSOMM:** Tabela indicando status para Script Injection, Tokens, Pinning, OIDC, SBOM e Assinatura.
f) **Tabela de Achados Detalhados:** Severidade | Workflow:Linha | Risco Identificado | Nível DSOMM | Correção.
g) **Diretrizes de Pipeline Hardening e Roadmap de Maturidade para o Time.**
h) **Seção Final "ISSUES PARA O GITHUB":** Para cada workflow inseguro, o template completo de issue com o código corrigido.

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Use um ambiente isolado (`venv` Python com `reportlab` + `matplotlib`).
- Salve o script gerador em `docs/cicd-audit/generate_report.py`.
- Formatação das páginas: tamanho A4, margens de 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS
Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2) e o Scorecard DSOMM (Parte 3).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/cicd-audit/relatorio-auditoria-cicd.pdf`, `docs/cicd-audit/generate_report.py`).
