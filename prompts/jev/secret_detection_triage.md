# PROMPT DE TRIAGEM E VALIDAÇÃO SEMÂNTICA DE SEGREDOS COM JEV (TYPESAFE AI) & OWASP ASVS

## OBJETIVO
Atuar como Engenheiro Principal de DevSecOps e Segurança de Aplicações (AppSec). Sua missão é conceber e implementar um pipeline híbrido de detecção e triagem de segredos e credenciais de altíssima precisão (*Secret Scanning & Triage Pipeline*), combinando varredura estática de alta velocidade (Regex e entropia de Shannon) com **validação semântica via Jev (TypeSafe AI)** para erradicar falsos positivos e capturar credenciais de baixa entropia em configurações (*config-shaped secrets*), em conformidade com **OWASP ASVS v4.0.3 Capítulo V14 (Configurações e Segredos)** e medindo a criticidade pelo **OWASP Risk Rating Methodology**.

O pipeline deve resolver o dilema clássico dos scanners tradicionais (Gitleaks, TruffleHog): eliminar o ruído de hashes aleatórios, UUIDs, bcrypt, blobs base64 e placeholders de documentação/testes (`EXAMPLE_API_KEY`, `hunter2`, `changeit`), enquanto detecta com precisão senhas reais escolhidas por operadores em arquivos de configuração (ex: Spring Boot, pgbouncer, LDAP `bindpw`, msmtp, Ansible `group_vars`).

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie os pontos de entrada do ciclo de desenvolvimento de software onde segredos são comumente expostos: commits git (hooks pré-commit), pipelines de CI/CD (pull requests), logs de execução e repositórios de documentação.
2. Analise os scanners estáticos existentes e mapeie as taxas de falsos positivos gerados por tokens de teste, mocks e valores de documentação pública.
3. Identifique formatos de arquivos de configuração (YAML, TOML, Properties, INI, Conf) onde senhas de baixa entropia sem prefixos conhecidos de fornecedores (*unprefixed generic secrets*) passam desapercebidas por regras puras de regex.
4. Você DEVE ler e analisar cada regra de extração estática e o fluxo de sanitização antes de enviar payloads ao Jev.

---

## CHECKLIST DE IMPLEMENTAÇÃO (OWASP ASVS v4.0.3 & RISK RATING)

### 1. Pré-Filtragem Estática e Associação de Contexto (ASVS V14.1, V14.2)
- [ ] **Filtro Rápido (Regex & Entropia):** Execute um pré-filtro local com padrões conhecidos de fornecedores (GitHub, Stripe, AWS, Slack) e buscas por chaves sensíveis (`password`, `secret`, `token`, `api_key`, `bindpw`).
- [ ] **Emparelhamento de Ativo (*Asset Pairing*):** Ao extrair um candidato a segredo, preserve no trecho (*snippet*) as linhas vizinhas contendo o ativo correspondente (ex: URL de banco de dados, hostname, porta ou bloco de configuração), garantindo contexto para decisão semântica.
- [ ] **Ofuscação Pré-Envio:** Não envie segredos corporativos conhecidos ou chaves mestras completas sem necessidade; certifique-se de que caminhos de arquivos relativos e snippets não incluam dados pessoais ou PII não relacionados à credencial.

### 2. Modelagem Semântica com Primitivas Jev
- [ ] **Validação Binária com Primitiva `Noul`:** Submeta o snippet a uma pergunta `Noul` especificamente calibrada:
  ```json
  {
    "type": "noul",
    "instructions": "O snippet contém uma credencial ou segredo real e utilizável que alguém lendo poderia utilizar para se autenticar?",
    "criteria": {
      "true": "Senhas em texto puro em configs, tokens de API de provedores reais, chaves privadas, strings de conexão ativas",
      "false": "Placeholders de exemplo (ex: EXAMPLE_KEY, dummy), hashes criptográficos (bcrypt, sha256), UUIDs de correlação, senhas padrão de teste documentadas (ex: changeit, hunter2)"
    }
  }
  ```
- [ ] **Classificação de Tipo com Primitiva `Choice`:** Categorize a credencial identificada para direcionar a equipe responsável:
  `criteria: {"vendor_token": "Chave de terceiro", "database_credential": "Senha de banco ou URI", "private_key": "Certificado/SSH/GCP SA", "generic_password": "Senha de serviço", "false_positive": "Placeholder ou hash"}`.

### 3. Bandas Calibradas de Decisão e Triagem
- [ ] **Banda Segura / Benigna (`noul < 0.30`):** Classifique como falso positivo confirmado. Permita a passagem no pipeline sem interromper o desenvolvedor.
- [ ] **Banda de Revisão (`0.30 <= noul <= 0.75`):** Indique ambiguidade (ex: hashes em `.htpasswd`, credenciais de teste comuns). Não falhe o build automaticamente; envie para quarentena ou solicite confirmação em PR.
- [ ] **Banda de Bloqueio Crítico (`noul > 0.75`):** Segredo real confirmado. Bloqueie o commit ou falhe o pipeline de CI/CD imediatamente, alertando a equipe de AppSec e disparando fluxo de revogação.

### 4. Engenharia de Produção e Resiliência
- [ ] **Controle de Concorrência (Máximo 16 Paralelos):** Limite o envio simultâneo de requisições à API do Jev a no máximo 16 chamadas concorrentes (via semáforo assíncrono), prevenindo erros `529 Overloaded`.
- [ ] **Keep-Alive e Connection Pooling:** Mantenha conexões HTTP persistentes reutilizando o socket TLS para evitar a sobrecarga de ~1.2s de inicialização de conexão em `us-west-2` e manter latência de resposta em ~290ms (com p50 de servidor Envoy em 75-90ms).
- [ ] **Retry com Exponential Backoff:** Trate retornos `429` e `529` com backoff exponencial e jitter.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica, apresente no chat:

### PARTE 1: MATRIZ DE RISCO DE VAZAMENTO DE CREDENCIAIS (OWASP RISK RATING METHODOLOGY)

$$\text{Risco (Severidade)} = \text{Probabilidade de Exposição} \times \text{Impacto do Comprometimento}$$

| ID | Categoria do Segredo | Exemplo Típico | Limitação do Scanner Regex Tradicional | Avaliação Semântica Jev (Noul) | Severidade (RRM) | Ação Recomendada |
|---|---|---|---|---|---|---|
| #1 | Config-Shaped Password | `password Mailer-Relay-7719` em `msmtp` | Falso Negativo (Baixa entropia, sem prefixo) | `noul = 0.88 - 0.95` | **CRÍTICA** | Bloquear Commit & Revogar |
| #2 | Hash / UUID de Teste | `apr1$digest` em `.htpasswd` ou UUID de trace | Falso Positivo (Alta entropia, parece chave) | `noul = 0.10 - 0.28` | **INFORMATIVA** | Permitir Commit (Auto-Allow) |
| #3 | Test Seed / Documentação | `changeit` / `EXAMPLE_API_KEY` | Falso Positivo (Detectado como senha ativa) | `noul = 0.40 - 0.55` | **MÉDIA** | Quarentena / Revisão Manual |
| #4 | Token de Provedor Ativo | `ghp_...` ou `sk_live_...` | Detectado por Regex | `noul = 0.98` | **CRÍTICA** | Bloquear & Alertar SOC |

### PARTE 2: IMPLEMENTAÇÃO DO SCRIPT DE TRIAGEM HÍBRIDA
Apresente o código de produção em Python ou TypeScript do script de triagem (`secret_scanner_triage.py`), demonstrando:
1. Regex local rápido para extração inicial de candidatos e janela de contexto circundante.
2. Cliente HTTP assíncrono com semáforo de 16 conexões e `httpx.AsyncClient` com connection pooling.
3. Avaliação semântica via Jev `Noul` + `Choice`.
4. Roteamento por bandas de decisão (`<0.30`, `0.30-0.75`, `>0.75`).
5. Geração de relatório de auditoria e código de saída (`exit code: 0` seguro, `1` violação de segurança detectada).

---

## ENTREGÁVEIS FINAIS
1. **Script de Triagem Híbrida de Segredos:** Script executável pronto para integração em pre-commit hooks (`.pre-commit-config.yaml`) e GitHub Actions / GitLab CI.
2. **Suite de Testes com Fixtures de Calibração:** Conjunto de testes contendo casos sintéticos de credenciais reais, segredos em configs de baixa entropia e falsos positivos notórios (UUIDs, bcrypt, `hunter2`, `EXAMPLE_API_KEY`).
3. **Guia Operacional de Resiliência:** Diretrizes para ajuste de limites de concorrência e monitoramento do header `x-envoy-upstream-service-time`.
