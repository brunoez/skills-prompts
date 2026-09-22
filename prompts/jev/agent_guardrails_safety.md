# PROMPT DE AUDITORIA E IMPLEMENTAÇÃO DE GUARDRAILS PARA AGENTES DE IA COM JEV (TYPESAFE AI) & OWASP LLM TOP 10

## OBJETIVO
Atuar como Engenheiro Principal de Segurança em Inteligência Artificial (AI AppSec & Red Teaming). Sua missão é auditar e blindar loops de agentes autônomos contra **Agência Excessiva (OWASP LLM06: Excessive Agency)**, **Injeção Indireta de Prompt (OWASP LLM01)** e **Execução Insegura de Ferramentas (OWASP ASVS v4.0.3 Capítulo V1.14 e V5.3)** utilizando o **Jev (TypeSafe AI)** como uma camada ultra-rápida (<100ms) de interceptação e decisão antes da invocação de ferramentas (*Pre-Execution Tool Guardrail*).

Você deve implementar o padrão de **Auto Mode Seguro com Aprovação Baseada em Confiança (*Confidence-Gated Tool Approval*)**, permitindo que comandos seguros rodem automaticamente, bloqueando comandos destrutivos e direcionando chamadas de ferramentas ambíguas para supervisão humana (*Human-in-the-Loop*), medindo os riscos pelo **OWASP Risk Rating Methodology**.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie todas as definições de ferramentas (*Tools / Function Calling*) expostas aos agentes (ex: execução shell/bash, queries em banco de dados, manipulação de arquivos, chamadas de rede, disparo de e-mails, mutações financeiras).
2. Analise o loop de controle do agente (LangChain, LlamaIndex, LangGraph, CrewAI, AutoGen ou orquestrador próprio) e verifique se as ferramentas são executadas cegamente sem validação intermediária.
3. Identifique onde agentes recebem dados de fontes externas não confiáveis (web, e-mails, PDFs indexados em RAG) que possam conter instruções maliciosas induzindo chamadas de ferramentas perigosas.
4. Você DEVE ler e analisar cada manipulador de ferramenta e middleware de execução linha por linha.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (AGENT GUARDRAILS & OWASP ASVS v4.0.3)

### 1. Interceptação de Ferramentas Críticas (Excessive Agency & ASVS V1.14.3, V5.3)
- [ ] **Mapeamento de Tools de Alto Impacto:** Identifique todas as ferramentas com capacidade de mutação destrutiva (`rm`, `drop`, `truncate`, `delete_user`, `update_permissions`, `transfer_funds`, `send_email`).
- [ ] **Camada de Interceptação Pré-Execução:** Verifique se existe um hook/middleware que intercepta o payload da ferramenta (nome da função + argumentos serializados + contexto da tarefa) antes do disparo da chamada no sistema operacional ou banco de dados.

### 2. Modelagem de Julgamento com Primitivas Jev
- [ ] **Avaliação de Risco com Primitiva `Score`:** Configure uma pergunta `Score` avaliando o potencial de dano da ação:
  `criteria: ["Inofensivo (Leitura / Consulta)", "Baixo Risco (Modificação pontual reversível)", "Risco Crítico (Exclusão em massa, shell command, alteração de permissão)"]`.
- [ ] **Detecção de Desvio de Intenção com `Noul`:** Configure uma pergunta `Noul` checando se os argumentos da ferramenta foram manipulados por prompt injection ou divergem do objetivo aprovado pelo usuário (`"O comando proposto realiza exatamente o que o usuário solicitou sem efeitos colaterais ocultos?"`).
- [ ] **Classificação de Categoria de Ação com `Choice`:** Categorize a ação entre destinos de política: `["auto_allow", "require_confirmation", "block_destructive"]`.
- [ ] **Verificação de Contexto de Execução com `Choice` (Anti-Falsos Positivos):** Quando comandos potencialmente perigosos forem detectados em snippets ou prompts, avalie se o contexto é de execução ativa em produção (`active`), documentação/exemplo (`example`) ou teste mock (`test_fixture`), evitando bloquear referências acadêmicas ou documentais inofensivas.

### 3. Matriz de Confiança e Human-in-the-Loop
- [ ] **Garantia de Não-Bypass em Baixa Certeza:** Se o Jev retornar `confidence < 0.85` na avaliação de segurança, o sistema DEVE suspender a execução automática e solicitar confirmação explícita do operador humano (*Fail-Safe Defaults*).
- [ ] **Bloqueio Incondicional de Ações Críticas:** Comandos avaliados com nível de severidade máxima ou probabilidade de injeção > 0.80 devem ser abortados imediatamente no middleware, logando o incidente de segurança sem atingir a ferramenta real.

### 4. Resiliência Operacional e Proteção do Guardrail
- [ ] **Proteção Contra Denial of Wallet / Latência:** O guardrail com Jev deve executar com conexão HTTP persistente (keep-alive) para evitar a sobrecarga de ~1.2s de handshake TCP/TLS e manter a latência de round-trip em ~290ms (p50 de processamento do servidor Envoy em 75-90ms).
- [ ] **Controle de Concorrência e Tratamento de 529:** Em loops de múltiplos subagentes, limite a concorrência a no máximo 16 requisições simultâneas via semáforo para prevenir respostas `529 Overloaded`, aplicando retry com exponential backoff e jitter.
- [ ] **Isolamento de Credenciais:** Assegure que a chave de API do Jev permaneça no backend seguro e que logs de segurança registrem o payload anonimizado, sem expor tokens de acesso ou segredos de infraestrutura.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica e estruturação dos guardrails, apresente no chat:

### PARTE 1: MATRIZ DE RISCO DE FERRAMENTAS DO AGENTE (OWASP RISK RATING METHODOLOGY)
Apresente a tabela classificando as ferramentas expostas segundo o risco operacional:

$$\text{Risco (Severidade)} = \text{Probabilidade de Abuso} \times \text{Impacto da Ação}$$

| ID | Ferramenta / Tool | Argumentos Aceitos | Vetor de Risco (Injeção / Destruição) | Severidade (RRM) | Política de Guardrail Jev |
|---|---|---|---|---|---|
| #1 | `execute_bash` | `command: string` | RCE via injeção indireta / Deleção de arquivos | **CRÍTICA** | Score de Risco + Bloqueio ou HITL Obrigatório |
| #2 | `db_query` | `sql: string` | SQL Injection / Exfiltração de dados | **ALTA** | Noul (É apenas leitura?) + Bloqueio de DDL/DML |
| #3 | `search_knowledge_base`| `query: string` | Busca semântica somente leitura | **BAIXA** | Auto-Allow imediato |

### PARTE 2: IMPLEMENTAÇÃO DO MIDDLEWARE DE DEFESA
Apresente o código de produção do middleware de interceptação (ex: TypeScript ou Python / LangChain `AutoModeMiddleware`), demonstrando:
1. Interceptação do `tool_name` e `tool_input`.
2. Montagem do payload de `state` e disparo concorrente das perguntas `Choice`, `Score` e `Noul` ao Jev.
3. Decisão baseada na combinação de probabilidade e `confidence`.
4. Emissão de alerta de segurança e interrupção do loop do agente em caso de ataque detectado.

---

## ENTREGÁVEIS FINAIS
1. **Middleware de Guardrail do Agente:** Código pronto para produção interceptando as tools antes da execução.
2. **Suite de Testes de Evasão (Red Teaming):** Casos de teste automatizados simulando injeção direta, injeção indireta em documentos e comandos ofuscados (ex: base64, pipes no bash) para validar que o Jev barra as tentativas.
3. **Template de Auditoria de Agentes:** Documentação para a equipe de SRE e Segurança acompanhar os logs de intervenção do guardrail.
