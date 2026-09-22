# PROMPT DE AUDITORIA E VERIFICAÇÃO DE RAG, CITAÇÕES E GUARDRAILS DE SAÍDA COM JEV (TYPESAFE AI) & OWASP LLM09

## OBJETIVO
Atuar como Especialista em Arquitetura de Busca Semântica (RAG - Retrieval-Augmented Generation) e Engenheiro de Segurança de IA. Sua missão é auditar e implementar uma camada ultra-rápida de **Verificação de Fidedignidade de Citações, Re-ranking de Passagens e Guardrail de Saída** utilizando o **Jev (TypeSafe AI)** para combater **Alucinações e Dependência Excessiva (OWASP LLM09: Overreliance)** e **Vazamento de Informações Sensíveis (OWASP LLM02)** em sistemas de RAG e agentes de busca.

Você deve estruturar a verificação em duas pontas (*Ingest/Retrieval Filter* e *Post-Generation Citation Check*), utilizando as primitivas `Score`, `Choice` e `Noul` com probabilidades calibradas para certificar que o contexto recuperado realmente responde à consulta do usuário e que o texto gerado pelo LLM está rigorosamente fundamentado nas fontes, descartando passagens irrelevantes e barrando afirmações alucinadas antes que cheguem ao usuário final.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie os fluxos de RAG: consultas ao banco vetorial, nós de recuperação (*retrievers*), montagem do prompt de contexto e respostas do gerador.
2. Identifique onde passagens ruidosas recuperadas por busca por similaridade de cosseno (top-k vetorial) degradam o contexto do LLM gerador (*Context Bloat / Lost in the Middle*).
3. Verifique se o sistema entrega respostas ao usuário contendo citações ou referências sem validar programaticamente se a citação confere com o texto do documento original.
4. Avalie se o sistema gasta recursos chamando um segundo LLM generativo completo apenas para atuar como "juiz" (*LLM-as-a-Judge*), gerando latência insustentável.
5. Você DEVE ler e analisar os pipelines de RAG, prompts de geração e middlewares de resposta linha por linha.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (VERIFICAÇÃO DE RAG & OWASP LLM09)

### 1. Filtragem e Re-ranking de Passagens Recuperadas (Retrieval Quality)
- [ ] **Filtragem de Ruído Pré-Geração:** Antes de injetar os top-k documentos no prompt do LLM gerador, execute uma pergunta `Score` ou `Choice` no Jev avaliando a relevância direta de cada trecho recuperado contra a pergunta do usuário.
- [ ] **Eliminação de Alucinação Induzida por Ruído:** Descarte deterministicamente no código qualquer passagem cuja pontuação de relevância fique abaixo do threshold calibrado, reduzindo o tamanho do prompt final e o custo de tokens do LLM generativo.
- [ ] **Validação de Suficiência da Base:** Adicione uma pergunta `Noul` (`"O documento recuperado contém informações suficientes para responder à pergunta com precisão factual?"`). Se `noul < 0.30`, aborte a geração e informe diretamente ao usuário que a informação não consta na base de conhecimento (*evita alucinações de preenchimento*).

### 2. Verificação de Citações e Fidedignidade Pós-Geração (Citation Checking)
- [ ] **Checagem Atômica de Afirmações:** Para cada alegação factual ou citação gerada pelo modelo principal, envie como `state` o par `{"source_excerpt": "...", "generated_claim": "..."}` ao Jev.
- [ ] **Avaliação de Suporte com `Choice`:**
  `type: "choice", instructions: "O trecho original dá suporte à afirmação gerada?", criteria: {"supported": "A afirmação é diretamente derivada e confirmada pelo texto", "contradicted": "A afirmação entra em conflito com o texto", "unsupported": "O texto não menciona ou extrapola a informação"}`.
- [ ] **Ação Determinística sobre Fuga de Fatos:** Se `choice != "supported"` ou `confidence < 0.80`, sinalize a citação como não verificada ou acione o fallback do sistema.

### 3. Guardrail de Saída para Vazamento de Dados Sensíveis (OWASP LLM02)
- [ ] **Inspeção de Saída em Paralelo:** Em conjunto com a verificação de citação, envie em paralelo via Speculative Fan-out perguntas `Noul` verificando:
  - `"A resposta contém chaves de API, senhas, tokens ou dados pessoais (PII) sensíveis?"`
  - `"A resposta quebrou as diretrizes éticas ou regras de negócio estabelecidas?"`
- [ ] **Latência Praticamente Nula:** A validação completa do Jev (fidedignidade + segurança) deve ocorrer em <120ms, permitindo streaming responsivo ou bloqueio imperceptível.

### 4. Telemetria e Indicadores de Confiabilidade
- [ ] **Score de Fidedignidade (*Faithfulness Score*):** Exiba na interface ou armazene em metadados uma nota auditável de conformidade da resposta com base nas probabilidades do Jev.
- [ ] **Auditoria de Drift de Recuperação:** Monitore flutuações nas médias de `confidence` das passagens recuperadas para identificar quando documentos desatualizados ou incompletos estão degradando a base vetorial.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica do pipeline de RAG, exiba no chat:

### PARTE 1: DIAGNÓSTICO DE RISCO DE ALUCINAÇÃO & CONFIABILIDADE DO RAG
Apresente a tabela mapeando as etapas do pipeline de RAG e suas vulnerabilidades:

| Etapa do Pipeline | Mecanismo Atual | Risco OWASP LLM | Severidade (RRM) | Mitigação com Jev System One |
|---|---|---|---|---|
| Recuperação Vetorial | Top-5 Cosine Similarity | Context Bloat / Falsos Positivos | MÉDIA | Re-ranking via `Score` + Descarte de ruído |
| Geração da Resposta | Prompt direto sem validação | LLM09: Alucinação de Citação | ALTA | Citation Checker via `Choice` (`supported`) |
| Entrega ao Usuário | Resposta direta no frontend | LLM02: Vazamento de PII | ALTA | Pre-flight `Noul` de segurança em paralelo |

### PARTE 2: IMPLEMENTAÇÃO DO VERIFICADOR EM CÓDIGO
Apresente o código de produção do componente verificador (TypeScript ou Python):
1. Função de pré-filtragem de passagens (Re-ranking leve com Jev).
2. Função de validação de citações pós-geração com parsing tipado de `choice` e `confidence`.
3. Tratamento de exceções e regras de substituição automática para citações não suportadas.

---

## ENTREGÁVEIS FINAIS
1. **Pipeline de RAG Blindado:** Código completo do interceptador de RAG com verificação de passagens e citações.
2. **Dataset de Validação de Alucinações:** Conjunto de testes contendo casos verdadeiros, citações extrapoladas e contradições flagrantes para verificar a sensibilidade do guardrail.
3. **Métricas de Qualidade:** Dashboard de observabilidade medindo taxa de alucinações barradas e tempo de resposta da verificação.
