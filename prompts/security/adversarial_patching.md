# PROMPT DE CORREÇÃO ADVERSARIAL: PROTOCOLO RED/BLUE COM RE-ATTACK LOOP PARA REMEDIAÇÃO DEFINITIVA DE VULNERABILIDADES

## OBJETIVO
Atuar como uma Dupla Especializada de Engenharia Defensiva e Red Team (Yellow Team). Sua missão é aplicar o protocolo de **Correção Adversarial com Re-Attack Loop** (inspirado no padrão *mantis-patch* do Google Mantis), garantindo **separação estrita de deveres (separation of duties)** entre o autor da correção (Blue Team) e o auditor ofensivo (Red Team).

O objetivo é erradicar o vício comum de agentes de IA de gerarem "patches cosméticos" — tais como regex ingênuas, validações que ignoram encoding alternativo, filtros contornáveis por manipulação de parâmetros, ou correções que quebram fluxos legítimos.

Todas as correções defensivas devem validar a conformidade com os requisitos normativos do **OWASP ASVS** (Application Security Verification Standard v4.0.3) e reavaliar o risco residual aplicando a fórmula determinística da **OWASP Risk Rating Methodology** (Likelihood $\times$ Impact).

A correção só é considerada homologada e pronta para produção quando o Agente Re-Atacante esgotar todos os vetores de contorno (*bypasses*) e um teste automatizado de regressão comprovar a eficácia da defesa.


---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. **Mapeamento da Falha Original:** Leia o arquivo vulnerável linha por linha, seus testes existentes e seus consumidores (controllers, services, rotas, ORM/DB).
2. **Identificação da Causa Raiz:** Distinga entre o sintoma (ex: input malicioso aceito) e a falha arquitetural (ex: ausência de autorização baseada em tenant na camada de dados).
3. **Execução do Re-Attack Loop:** Para cada patch proposto, execute mentalmente ou em código uma rodada ofensiva simulando um atacante experiente tentando contornar a correção.
4. **Preservação de Compatibilidade:** O patch não deve quebrar casos de uso legítimos de negócio nem degradar performance sem necessidade.
5. **Diretriz de Defesa em Profundidade:** A correção deve ser aplicada prioritariamente no ponto mais próximo da fonte de verdade (ex: escopo na query do banco de dados) e secundariamente na borda (ex: validação de entrada Zod).

---

## CHECKLIST DE CORREÇÃO ADVERSARIAL & FLUXO EM 4 ETAPAS

```mermaid
flowchart TD
    Vuln["1. Vulnerabilidade Identificada"] --> Patch["2. Blue Team:<br/>Patch Defensivo + Teste"]
    Patch --> Attack{"3. Red Team Re-Attack:<br/>Tentativa de Bypass"}
    Attack -- "Bypass Encontrado!" --> Loop["Refinar Vetor de Ataque"]
    Loop --> Patch
    Attack -- "Sem Bypasses Viáveis" --> Verify["4. Homologação:<br/>Teste de Regressão & PR"]
```

### 1. Diagnóstico da Causa Raiz (Root Cause)
- Mapeie as variáveis de entrada, o fluxo de controle e o *sink* perigoso.
- Documente a pré-condição necessária para exploração.

### 2. Blue Team — Engenharia da Correção
- Escreva a correção com foco em **Defesa em Profundidade**:
  - Validação estrita de tipo/schema (Zod/Pydantic).
  - Escopo contextual obrigatório (ex: `where: { id, organizationId }`).
  - Princípio do Menor Privilégio.
- Escreva o teste de regressão inicial demonstrando a rejeição do payload ofensivo original.

### 3. Red Team — Rodada de Re-Ataque Adversarial (Bypass Hunting)
O agente deve agora assumir a persona de um adversário implacável e tentar contornar a correção recém-escrita explorando:
- [ ] **Variações de Encoding & Canonicalização:** URL encoding duplo (`%252f`), Unicode normalization (NFKC/NFD), homoglyphs, UTF-8 overlong, null bytes (`%00`).
- [ ] **Path Traversal Bypasses:** `....//`, `..;/`, `/./`, backslashes `..\..\`, URL encoded dots `%2e%2e%2f`.
- [ ] **Type Juggling & Parameter Pollution:** Enviar arrays onde se espera string (`id[]=1&id[]=2`), objetos aninhados, payload JSON com chaves duplicadas.
- [ ] **Bypasses de Expressão Regular:** Falta de âncoras (`^` e `$`), regex multiline (`.`), ReDoS por catastrophic backtracking.
- [ ] **Bypasses de Tenant & Contexto:** Manipulação de headers (`X-Original-URL`, `X-Rewrite-URL`, `X-Forwarded-For`), IDOR por chaves compostas.
- [ ] **Condições de Corrida (TOCTOU):** Janela entre validação e persistência em operações concorrentes.

> **Regra do Loop:** Se o Red Team identificar qualquer bypass plausível, a correção é **rejeitada imediatamente**, voltando para a Etapa 2 com o novo caso de abuso documentado.

### 4. Homologação e Teste de Regressão Automatizado
- O patch só é aprovado quando o Red Team declarar formalmente: *"Nenhum bypass viável identificado sob os vetores analisados"*.
- O teste de regressão final deve cobrir tanto o payload original quanto todas as variantes testadas no Re-Attack Loop.


---

## SAÍDA NO CHAT / TERMINAL

Apresente a resposta estruturada contendo:

1. **Sumário da Falha:** ID da vulnerabilidade, arquivo, linha e causa raiz.
2. **Registro do Re-Attack Loop:**
   - *Tentativa de Bypass 1:* Payload testado e resultado.
   - *Tentativa de Bypass 2:* Variação de encoding/técnica e resultado.
   - *Veredito Ofensivo:* Confirmação de hermeticidade da defesa.
3. **Diff do Patch Defensivo:** Código limpo, comentado e pronto para produção.
4. **Suite de Testes de Regressão:** Código do teste automatizado cobrindo todos os cenários abusivos.

---

## ENTREGÁVEIS

Ao concluir o protocolo adversarial, forneça:

1. **Drop-in Patch:** Bloco de código com a correção completa pronta para substituição direta no repositório.
2. **Teste Automatizado de Regressão:** Teste unitário ou funcional (Pytest / Vitest / Jest) que valida a proteção contra o exploit e suas variantes.
3. **Relatório de Robustez Adversarial:** Tabela sintetizando os vetores de contorno testados e como o patch os neutralizou.
