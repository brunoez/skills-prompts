# PROMPT DE AUDITORIA COMPLETA: INFRAESTRUTURA COMO CÓDIGO (IaC), CONTAINERS & KUBERNETES (DEVSECOPS & OWASP DSOMM) E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de DevSecOps e Especialista em Cloud Security. Sua missão é realizar uma varredura completa no repositório para identificar falhas de segurança, conformidade e resiliência em **Infraestrutura como Código (Terraform, OpenTofu, CloudFormation, Pulumi, Ansible)**, **Containers (Dockerfiles, Compose)** e **Orquestração Kubernetes (Manifestos, Helm Charts, Kustomize)**, aplicando conjuntamente:
1. **CIS Benchmarks**, **NSA/CISA Kubernetes Hardening Guidance** e **Cloud Best Practices**;
2. **OWASP DevSecOps Maturity Model (DSOMM)** — Dimensões:
   - **Implementation** (Subdimensões: *Infrastructure Hardening*, *Container Security*, *Identity and Access Management*);
   - **Build and Deployment** (Subdimensão: *Policy Enforcement*).

A auditoria deve avaliar tanto vulnerabilidades estáticas de configuração quanto a postura de **Maturidade DevSecOps (Níveis 1 a 5 do DSOMM)**: uso de imagens mínimas imutáveis (Distroless / Chainguard), triagem e gating de CVEs, Shift-Left IaC scanning (Checkov/Trivy), gestão segura de secrets e `tfstate`, Pod Security Standards (`restricted`), **Policy-as-Code na admissão (OPA Gatekeeper / Kyverno)**, **GitOps com detecção de Drift** e **micro-segmentação de rede com mTLS**.

Ao final da auditoria, você deve listar os achados no chat/terminal, apresentar o **Scorecard de Maturidade DSOMM** e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura completa de diretórios e identifique os provedores de nuvem (AWS, GCP, Azure) e as tecnologias de infraestrutura utilizadas.
2. Leia todos os arquivos de documentação de infraestrutura, arquitetura e topologia (`README.md`, `/docs`, diagramas de rede, manuais de deploy).
3. Identifique e analise TODOS os arquivos de infraestrutura:
   - **IaC:** Arquivos `.tf`, `.tfvars`, templates CloudFormation (`.yaml`/`.json`), playbooks Ansible.
   - **Containers:** `Dockerfile`, `Containerfile`, `docker-compose.yml`.
   - **Kubernetes:** Manifestos `.yaml` de Deployments, StatefulSets, DaemonSets, Services, Ingress, NetworkPolicies, RBAC (`Role`, `RoleBinding`), PodSecurityStandards, políticas OPA/Kyverno e `values.yaml` de Helm Charts.
4. Você DEVE ler e analisar cada arquivo identificado linha por linha. Não faça suposições sem validar o código-fonte correspondente.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (DEVSECOPS: IaC, CONTAINERS, K8S & DSOMM)

### 1. Infraestrutura como Código (IaC - Cloud, State & Network Security - DSOMM Level 2-4)
- [ ] **Princípio do Menor Privilégio (IAM Least Privilege):** Identifique políticas IAM excessivamente permissivas (ex: uso de `Action: "*"` ou `Resource: "*"`), roles sem restrições de escopo e credenciais/chaves estáticas em código.
- [ ] **Exposição Pública de Armazenamento e Bancos:** Identifique buckets (AWS S3, GCS, Azure Blob) ou instâncias de banco (RDS) sem bloqueio explícito de acesso público (`block_public_acls = false`, `publicly_accessible = true`).
- [ ] **Grupos de Segurança e Firewalls Permissivos:** Localize Security Groups ou Firewall Rules com portas administrativas (SSH `22`, RDP `3389`, DBs `3306`/`5432`/`6379`) abertas para a internet global (`0.0.0.0/0` ou `::/0`).
- [ ] **Criptografia em Repouso e em Trânsito:** Verifique se volumes de disco (EBS, Persistent Volumes), bancos de dados e buckets possuem criptografia habilitada por padrão (ex: `encrypted = true`, KMS CMK) e se conexões exigem HTTPS/TLS.
- [ ] **Proteção do Estado de IaC (`tfstate`) e Segredos (DSOMM Level 3):** Verifique se o estado do Terraform/OpenTofu é armazenado em backend remoto seguro, com criptografia habilitada (KMS), controle de concorrência/lock (DynamoDB) e sem credenciais confidenciais expostas em texto puro.
- [ ] **Shift-Left IaC Static Analysis (DSOMM Level 3):** Verifique a existência de análise estática automatizada de IaC (ex: Checkov, tfsec, Trivy, KICS) integrada a hooks pré-commit ou workflows de PR para bloquear misconfigurations antes do provisionamento.

### 2. Segurança de Containers (Dockerfiles, Imagens & Vulnerabilidades - DSOMM Level 2-4)
- [ ] **Execução com Usuário Root:** Identifique Dockerfiles que não declaram um usuário não-privilegiado (ausência da diretiva `USER <non-root-uid>`).
- [ ] **Imagens Base e Dependências:** Verifique o uso de tags mutáveis (ex: `:latest`) em vez de tags imutáveis ou SHA256 digests (`image@sha256:...`).
- [ ] **Imagens Mínimas Distroless / Chainguard (DSOMM Level 3-4):** Verifique se a imagem final de produção utiliza bases mínimas (Distroless, Chainguard, Alpine stripped), eliminando package managers (apt, apk, yum), curl, wget e shells interativos (`/bin/sh`, `/bin/bash`), reduzindo drasticamente a superfície de ataque para execuções remotas de código.
- [ ] **Vazamento de Segredos e Build Cache:** Identifique credenciais, tokens ou chaves privadas copiadas para o container via `COPY`/`ADD` ou passadas via `ARG` sem o uso de `RUN --mount=type=secret`.
- [ ] **Práticas de Build Multistage:** Verifique se ferramentas de build (compiladores, SDKs, código-fonte bruto) permanecem na imagem final de produção em vez de usar *multi-stage builds*.
- [ ] **Gating de Vulnerabilidades em Containers (DSOMM Level 3-4):** Verifique se imagens geradas passam por scanners de vulnerabilidades (Trivy, Grype) com critérios de bloqueio para CVEs com exploit ativo conhecido (CISA KEV) ou alta probabilidade de exploração (EPSS).

### 3. Segurança e Resiliência em Kubernetes (K8s Manifests, Helm & Governance - DSOMM Level 3-5)
- [ ] **Security Contexts Restritivos:** Identifique Pods/Containers sem `securityContext` seguro: falta de `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true` e ausência de descarte de capacidades Linux (`drop: ["ALL"]`).
- [ ] **Containers Privilegiados:** Verifique a presença de flags perigosas ativas como `privileged: true`, `hostPID: true`, `hostNetwork: true` ou `hostIPC: true`.
- [ ] **Limites de Recursos (Prevenção de DoS no Cluster):** Localize containers sem definições explícitas de `resources.limits` e `resources.requests` para CPU e Memória.
- [ ] **Probes de Saúde e Ciclo de Vida:** Identifique a ausência de `livenessProbe`, `readinessProbe` e `startupProbe` configurados adequadamente para garantir alta disponibilidade.
- [ ] **Network Policies e Isolamento de Namespace:** Verifique se os namespaces operam em modo aberto (sem `NetworkPolicy`), permitindo comunicação irrestrita entre pods de diferentes domínios.
- [ ] **RBAC e Service Accounts:** Verifique se Pods utilizam `default` ServiceAccount com `automountServiceAccountToken: true` desnecessariamente, ou se há ClusterRoles com privilégios excessivos vinculadas a aplicações comuns.
- [ ] **Policy-as-Code & Admission Control (DSOMM Level 4):** Verifique se o cluster ou repositório possui políticas declarativas de admissão (ex: **Kyverno** ou **OPA Gatekeeper**) que bloqueiam ativamente a submissão de manifests fora de conformidade com Pod Security Standards (*Restricted profile*).
- [ ] **GitOps e Detecção de Drift em Tempo Real (DSOMM Level 4-5):** Verifique se o gerenciamento do cluster segue modelo GitOps (ex: ArgoCD, Flux) com reconciliação contínua e proteção contra alterações manuais pontuais (*out-of-band drift*).
- [ ] **Micro-segmentação Zero Trust e mTLS (DSOMM Level 5):** Verifique a presença de criptografia transparente em trânsito pod-a-pod (via mTLS de Service Mesh ou CNI Cilium com WireGuard/IPsec) e autenticação de identidade de workloads baseada em SPIFFE/SPIRE.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a auditoria estruturada:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados encontrados, ordenados obrigatoriamente do maior risco/facilidade para o menor:

| ID | Arquivo / Ponto | Categoria | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `terraform/iam.tf:18` | IAM (Least Privilege) | CRÍTICA | Baixo (15 min) | **SIM** |
| #2 | `k8s/deployment.yaml:45` | K8s (SecurityContext) | ALTA | Baixo (20 min) | **SIM** |
| #3 | `Dockerfile:1` | Containers (Root User) | ALTA | Baixo (10 min) | **SIM** |

*(Quick Win: Problema de Severidade ALTA ou MÉDIA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome do Problema]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Categoria:** [IaC - IAM & Cloud / IaC - State & Scans / Containers - Docker / Containers - Distroless & CVEs / K8s - Pod Security / K8s - Admission & GitOps]
- **Mapeamento DSOMM:** [Dimensão / Subdimensão / Nível atingido vs Nível esperado]
- **Problema:** Explicação direta do risco de segurança (ex: comprometimento de cluster, vazamento de bucket, container breakout, DoS).
- **Evidência:** Trecho do código-fonte atual identificado no repositório.
- **Correção Recomendada:** Código devidamente corrigido e refatorado aplicando as melhores práticas de DevSecOps.

### PARTE 3: SCORECARD DE MATURIDADE DSOMM (INFRASTRUCTURE & CONTAINERS)
Apresente uma tabela de avaliação da maturidade DevSecOps do repositório:

| Subdimensão DSOMM | Nível Atual (1-5) | Status | Requisito para Próximo Nível |
|---|:---:|---|---|
| **Infrastructure Hardening (IaC)** | Nível [X] | [Em progresso/Adequado] | [Ação necessária] |
| **Container Security & Minimal Images** | Nível [X] | [Crítico/Em progresso] | [Ação necessária] |
| **Kubernetes & Pod Security Standards** | Nível [X] | [Em progresso/Adequado] | [Ação necessária] |
| **Policy Enforcement & GitOps (Admissão)** | Nível [X] | [Crítico/Adequado] | [Ação necessária] |

**Nível Geral de Maturidade em Infraestrutura:** `Nível X / 5`
**Roadmap de Evolução:** Resumo em 3 passos para atingir o nível superior na escala DSOMM.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/devsecops-audit/relatorio-auditoria-devsecops.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria DevSecOps: IaC, Containers e Kubernetes (CIS & OWASP DSOMM) — <nome do projeto>", data, escopo auditado e nota metodológica (mapeamento para benchmarks CIS, NSA/CISA K8s Hardening e níveis 1 a 5 do DSOMM).
b) **Resumo Executivo:** Total de achados por severidade, gráfico de rosca por severidade e gráfico de barras por categoria.
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Scorecard e Radar de Maturidade DSOMM:** Gráfico de radar ou tabela comparativa com os níveis 1 a 5 nas subdimensões de infraestrutura.
d) **Pontos Fortes** (o que já está em conformidade e seguro na infraestrutura, com evidência) e **Pontos Fracos** (os riscos centrais de comprometimento).
e) **Tabela de Achados Detalhados por Categoria:** Severidade | Arquivo:linha | Descrição | Nível DSOMM, com indicação de Quick Win.
f) **Recomendações Priorizadas e Roadmap de Maturidade** (P1, P2, P3...).
g) **Seção Final "ISSUES PARA O GITHUB":** Para cada achado acionável, o texto COMPLETO de uma issue em Markdown, pronto para copiar e colar, dentro de um bloco delimitado (ex: entre `--- ISSUE n ---` e `--- FIM ISSUE n ---`). Cada issue deve conter:
   - Título no formato `[DevSecOps/Infra] <descrição curta da falha>`
   - Labels sugeridas: `devsecops`, `infrastructure` ou `kubernetes` + severidade
   - Descrição técnica do problema e por que viola os padrões de segurança
   - Evidência: `arquivo:linha` com trecho de código
   - Impacto (ex: risco de container breakout, ataque de negação de serviço, vazamento de dados)
   - Sugestão de correção (manifesto/código corrigido)
   - Critérios de aceite (checklist verificável de validação)

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Não instale pacotes globalmente no sistema. Use um ambiente isolado (ex: `venv` Python com `reportlab` + `matplotlib`, ou ferramentas equivalentes locais como `puppeteer`/HTML-to-PDF).
- Deixe o script gerador salvo no diretório `docs/devsecops-audit/` para que o relatório possa ser regerado futuramente.
- Verifique o PDF gerado: garanta o número correto de páginas, a renderização adequada dos gráficos e a legibilidade das tabelas.
- Formatação das páginas: tamanho A4, margens de aproximadamente 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS

Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2) e o Scorecard DSOMM (Parte 3).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/devsecops-audit/relatorio-auditoria-devsecops.pdf`, `docs/devsecops-audit/generate_report.py`).