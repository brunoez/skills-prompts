# PROMPT DE ROTEAMENTO DE INTENÇÃO E DESPACHO DINÂMICO COM JEV (TYPESAFE AI): SYSTEM ONE DISPATCHER

## OBJETIVO
Atuar como Engenheiro Principal de Sistemas Distribuídos e Arquiteto de IA. Sua missão é auditar e implementar uma camada de **Roteamento de Intenção e Despacho Dinâmico (Intent Routing & Dynamic Dispatch)** de ultra-baixa latência (<100ms) utilizando o **Jev (TypeSafe AI)** para triagem inteligente de eventos de entrada (tickets de suporte, e-mails, webhooks, mensagens de chat e comandos de usuários).

Você deve substituir roteadores baseados em LLMs convencionais ou cadeias frágeis de regex pelo padrão **Speculative Fan-out** do Jev, direcionando cada requisição ao manipulador ótimo: lógica determinística de código, modelo pequeno/econômico (ex: gpt-mini / flash), modelo de raciocínio profundo (System 2) ou operadores humanos, calibrando o despacho pela métrica de confiança (*confidence*).

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie todas as portas de entrada de tráfego que requerem classificação semântica para decisão de roteamento (ex: filas de atendimento ao cliente, triagem de leads, classificação de e-mails, processamento de webhooks e multiplexadores de agentes).
2. Avalie onde modelos generativos (como GPT-4 ou Claude) estão sendo usados unicamente para responder "para onde devo enviar esta mensagem?", gerando custos excessivos e latências de segundos.
3. Identifique onde árvores de regex e regras estáticas falham em lidar com a ambiguidade da linguagem natural, gerando roteamentos errôneos e fricção no produto.
4. Você DEVE ler e analisar cada ponto de entrada de requisições, controllers e filas de eventos linha por linha.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (DISPATCH SYSTEM ONE & SPECULATIVE FAN-OUT)

### 1. Definição do Grafo de Despacho (Dispatch Graph)
- [ ] **Mapeamento de Destinos de Roteamento:** Identifique com precisão os destinos possíveis da requisição:
  - Rota 1: Lógica puramente determinística (APIs de consulta, automações via script).
  - Rota 2: Modelo leve/econômico (tarefas de extração direta, preenchimento de campos).
  - Rota 3: Modelo frontier / raciocínio deliberado (planejamento complexo, redação criativa).
  - Rota 4: Fila de atendimento ou revisão humana (solicitações sensíveis, transações de alto valor).
- [ ] **Critérios Mutuamente Exclusivos e Exaustivos:** Formule as descrições de cada opção no `criteria` da pergunta `Choice` de forma clara, sem sobreposição ambígua entre categorias.

### 2. Modelagem com Speculative Fan-out em Chamada Única
- [ ] **Empacotamento de Múltiplas Decisões:** Aproveite a amostragem paralela do Jev para enviar em uma única requisição HTTP:
  - Pergunta 1 (`Choice`): Categoria / Destino do chamado (`destination`).
  - Pergunta 2 (`Score`): Nível de urgência e impacto (`urgency_level`: `["Normal", "Urgente", "Emergência de Produção"]`).
  - Pergunta 3 (`Noul`): Detecção de fraude ou solicitação suspeita (`is_suspicious_or_abusive`).
  - Pergunta 4 (`Noul`): Presença de solicitação explícita de cancelamento/reembolso (`has_churn_or_refund_intent`).
- [ ] **Garantia de Latência Constante:** Assegure que o payload de perguntas agregadas seja despachado de uma só vez, obtendo todas as respostas em ~100ms.

### 3. Mecanismo de Seleção de Modelo (Model Router Middleware)
- [ ] **Classificação da Complexidade da Tarefa:** No caso de agentes e assistentes, configure o Jev para escolher o modelo LLM menos custoso capaz de resolver o pedido (ex: tarefas pontuais de extração vão para modelos rápidos; decisões arquiteturais vão para modelos de raciocínio).
- [ ] **Controle Baseado em Confiança:**
  - Se a escolha do modelo retornar `confidence >= 0.85`, despache imediatamente para o modelo selecionado.
  - Se `confidence < 0.85`, adote a postura segura (*conservative fallback*): encaminhe para o modelo mais capaz ou solicite esclarecimento ao usuário.

### 4. Observabilidade e Telemetria
- [ ] **Registro de Calibração:** Implemente logs que gravem o ID da requisição, a opção escolhida, a probabilidade, o `confidence` e a ação final executada pelo software.
- [ ] **Métricas de Economia:** Monitore em dashboards (ex: OpenTelemetry / Prometheus) o percentual de tráfego resolvido sem chamar LLMs caros, calculando a economia de tokens de entrada/saída.

---

## SAÍDA NO CHAT / TERMINAL

Ao concluir o design do roteador, apresente no chat:

### PARTE 1: MATRIZ DE DECOMPOSIÇÃO DE ROTEAMENTO
Exiba a tabela detalhando a estratégia de despacho para os tipos de requisição:

| Canal / Entrada | Volume / s | Rota Determinística (%) | Rota LLM Rápido (%) | Rota Frontier LLM (%) | Rota Humana (%) | Redução Estimada de Custo |
|---|---|---|---|---|---|---|
| Suporte ao Cliente | 15 req/s | 45% (Auto-resolvido) | 35% (Respostas padrão) | 15% (Casos atípicos) | 5% (Baixa confiança) | ~80% |
| Webhooks de E-commerce | 50 req/s | 90% (Processamento direto) | 8% (Normalização) | 0% | 2% (Análise de fraude) | ~95% |

### PARTE 2: IMPLEMENTAÇÃO DO ROTEADOR EM CÓDIGO
Apresente a implementação completa do Dispatcher (TypeScript ou Python):
1. Tipagem Zod/TypeScript dos dados de estado (`state`) e do resultado retornado pelo Jev.
2. Chamada à API da TypeSafe AI estruturada com Speculative Fan-out.
3. Switch de decisão determinístico no código consumidor que avalia `answers[key].choice` e `answers[key].confidence`.
4. Roteamento transparente e assíncrono para as filas de processamento.

---

## ENTREGÁVEIS FINAIS
1. **Módulo Dispatcher:** Código de produção do despachador de alta performance com tipagem completa.
2. **Suíte de Testes de Carga e Acurácia:** Testes cobrindo requisições claras, casos de fronteira entre categorias e cenários de degradação com fallback.
3. **Guia de Manutenção de Critérios:** Instruções para a equipe de produto adicionar novas categorias no `criteria` do Jev sem quebrar o código existente.
