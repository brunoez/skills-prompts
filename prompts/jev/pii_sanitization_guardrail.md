# PROMPT DE AUDITORIA E SANITIZAÇÃO DE DADOS PESSOAIS (PII) COM JEV (TYPESAFE AI) & OWASP ASVS

## OBJETIVO
Atuar como Engenheiro Principal de Privacidade e Segurança em IA (AI Privacy & AppSec Engineer). Sua missão é auditar, projetar e implementar um guardrail híbrido de detecção, classificação de sensibilidade e anonimização/mascaramento de Dados Pessoais Identificáveis (*Personally Identifiable Information - PII*), em conformidade com **LGPD (Lei Geral de Proteção de Dados)**, **GDPR**, **OWASP ASVS v4.0.3 Capítulo V8 (Proteção de Dados)** e **OWASP Top 10 for LLM (LLM07: System Information Leakage)**.

O pipeline deve resolver as limitações de regras puramente sintéticas (regex) usando o **Jev (TypeSafe AI)** em uma arquitetura de três camadas para:
1. Detectar categorias de PII semânticas (nomes de pessoas, afiliações, diagnósticos) onde regex falha;
2. Desambiguar sequências numéricas (distinguir números de cartão de crédito e identificadores governamentais de números de pedidos, IDs de rastreio ou códigos seriais de produtos);
3. Avaliar o nível contextual de sensibilidade (*none*, *low*, *high*) de acordo com a taxonomia do IBM PII Corpus (ex: diferenciar o registro de um paciente em clínica de uma lista pública de participantes de conferência);
4. Aplicar mascaramento determinístico (*first2...last1*) antes de persistir dados em bancos ou enviar prompts para LLMs de terceiros, calculando a severidade pelo **OWASP Risk Rating Methodology**.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie todos os pontos de ingestão e saída de dados de IA: prompts de usuários, arquivos indexados em RAG, payloads de ferramentas chamadas por agentes e logs de auditoria.
2. Analise os fluxos onde dados sensíveis podem ser transmitidos para provedores externos de LLM sem consentimento ou anonimização prévia.
3. Inspecione os padrões regex existentes e identifique ambiguidades entre códigos de produtos e cartões de pagamento ou IDs governamentais.
4. Você DEVE ler e avaliar a política de retenção de dados da API do Jev antes de submeter payloads, assegurando conformidade com requisitos contratuais de privacidade.

---

## CHECKLIST DE IMPLEMENTAÇÃO (OWASP ASVS v4.0.3 V8 & RISK RATING)

### 1. Camada 1: Filtro Rápido e Limpeza Determinística Local (ASVS V8.1, V8.2)
- [ ] **Extração Sintética por Regex:** Extraia previamente padrões rígidos de alta certeza (e-mails, números de telefone com código de país/DDD, sequências de 10 a 16 dígitos com checagem de algoritmo de Luhn para cartões).
- [ ] **Filtro de Ruído Corporativo:** Descarte falsos positivos óbvios via lista de exceções locais (ex: e-mails de sistema como `noreply@`, `suporte@`, números 0800/0120 e endereços IP de servidores internos).
- [ ] **Chunking Adaptativo com Tolerância a Falhas:** Fragmente textos extensos em blocos de até 4.000 caracteres; implemente divisão ao meio (*half-split*) caso a API retorne `max_tokens_exceeded`.

### 2. Camada 2: Portão Multicategórico e Nível de Sensibilidade com Jev
- [ ] **Portão Multicategórico via `Noul` (13 Categorias de PII):** Submeta em uma única chamada paralela as perguntas binárias para:
  `nome_pessoa`, `email_ou_telefone`, `endereco_postal`, `data_nascimento`, `documento_governamental` (CPF, RG, Passaporte), `conta_financeira`, `dado_saude`, `dado_biometrico`, `endereco_ip_pessoal`, `handle_redes_sociais`, `dado_emprego`, `origem_racial_etnica`, `conviccao_religiosa`.
- [ ] **Avaliação de Nível de Sensibilidade com `Score`:** Classifique o contexto do documento em 3 níveis graduados:
  ```json
  {
    "type": "score",
    "instructions": "Avalie o nível contextual de sensibilidade e privacidade das informações identificáveis encontradas no documento segundo a taxonomia IBM PII.",
    "criteria": [
      "none - Nenhum dado pessoal identificável ou menções estritamente corporativas",
      "low - Dados de contato comercial, participantes públicos de eventos ou dados de baixa criticidade",
      "high - Diagnósticos clínicos, dados de menores, senhas, informações financeiras ou documentos governamentais"
    ]
  }
  ```

### 3. Camada 3: Desambiguação Semântica e Extração de Entidades
- [ ] **Desambiguação de Dígitos Numéricos com `Choice`:** Submeta sequências de 10 a 16 dígitos candidatas ao Jev para distinguir seu propósito:
  `criteria: {"cartao_credito": "Número de cartão de pagamento", "documento_identificacao": "ID governamental ou CPF", "numero_pedido": "Código de transação ou tracking de ecommerce", "serial_produto": "SKU ou serial de equipamento", "outro": "Sequência numérica aleatória"}`.
- [ ] **Extração e Segmentação de Nomes Próprios:** Em textos em linguagem natural, utilize segmentação léxica combinada com validação semântica no Jev para diferenciar nomes de pessoas reais de nomes de organizações ou personagens históricos de domínio público.

### 4. Mascaramento e Políticas de Interrupção (*Fail-Safe*)
- [ ] **Mascaramento Parcial Determinístico:** Mascare os valores sensíveis identificados mantendo apenas caracteres de contorno para rastreabilidade:
  - E-mails: `joao.silva@empresa.com` $\to$ `jo...m`
  - Telefones: `+55 11 98765-4321` $\to$ `+55...21`
  - CPF/IDs: `123.456.789-00` $\to$ `12...00`
- [ ] **Comporta de Bloqueio em CI/CD e Agentes:**
  - Se a sensibilidade atingir o nível `high` e o contexto for de saída para LLMs públicos, aborte o pipeline com código de saída `2` (`exit code: 2`).
  - Permita passagem sem interrupção para nível `none` ou dados mascarados (`exit code: 0`).

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica, apresente no chat:

### PARTE 1: MATRIZ DE RISCO DE VAZAMENTO DE PII (OWASP RISK RATING METHODOLOGY)

$$\text{Risco (Severidade)} = \text{Probabilidade de Exposição} \times \text{Impacto à Privacidade (LGPD/GDPR)}$$

| ID | Categoria de Dado | Amostra Típica | Vetor de Risco | Nível de Sensibilidade Jev | Severidade (RRM) | Ação de Mitigação |
|---|---|---|---|---|---|---|
| #1 | Dado Clínico / Saúde | "Paciente João diagnosticado com..." | Violação de sigilo médico / Multa regulatória | `high` (Score ~2.8) | **CRÍTICA** | Bloquear Saída & Mascarar |
| #2 | Cartão de Crédito | `4532 0123 4567 8910` | Fraude financeira / Não conformidade PCI-DSS | `high` (Score ~2.9) | **CRÍTICA** | Redigir Totalmente |
| #3 | Contato Comercial | "Ana Silva - Depto Comercial" | Exposição comercial de baixo impacto | `low` (Score ~1.1) | **BAIXA** | Mascaramento Parcial |
| #4 | Serial / Pedido | `#PED-982348234` | Falso positivo (confundido com cartão) | `none` (Score ~0.1) | **INFORMATIVA** | Permitir Sem Mascaramento |

### PARTE 2: IMPLEMENTAÇÃO DO GUARDRAIL DE PII
Apresente o código de produção em Python ou TypeScript (`pii_sanitizer_guardrail.py`), demonstrando:
1. Extração estática preliminar via regex com filtro de ruído corporativo.
2. Chamada única ao Jev com o portão de 13 perguntas `Noul` + `Score` de sensibilidade.
3. Desambiguação de sequências numéricas ambíguas com pergunta `Choice`.
4. Função determinística de mascaramento de strings.
5. Emissão de relatório JSON com contagem de PIIs e código de saída de segurança.

---

## ENTREGÁVEIS FINAIS
1. **Script de Guardrail de PII:** Módulo executável pronto para atuar como middleware pré-LLM ou filtro em pipelines de dados.
2. **Suite de Testes com Corpus Multilíngue:** Casos de teste sintéticos incluindo nomes de pessoas, sequências numéricas (cartão vs pedido) e contextos hospitalares vs comerciais.
3. **Guia de Conformidade LGPD/GDPR:** Diretrizes de descarte de dados e termos de retenção ao utilizar a API do Jev.
