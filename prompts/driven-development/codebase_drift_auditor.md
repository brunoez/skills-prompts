# PROMPT DE AUDITORIA: DETECÇÃO DE DRIFT ENTRE ESPECIFICAÇÃO, DOCUMENTAÇÃO E CÓDIGO (CODEBASE DRIFT)

## OBJETIVO
Atuar como Engenheiro Principal de QA de Arquitetura e Especialista em Governança de Software. Sua missão é realizar a detecção sistemática de divergência (*Drift Detection*) entre as especificações documentadas (READMEs, RFCs, SDDs em `docs/designs/`, ADRs, contratos OpenAPI) e a implementação real no código-fonte da aplicação.

Inspirado no protocolo de *Living Specifications* do **Elephant-Goldfish Model (EGM)**, este prompt visa identificar quando a documentação apodreceu em relação ao código, ou quando o código divergiu do design aprovado, gerando atalhos de implementação (*logic shortcuts*), modelos incompletos ou funcionalidades fantasmas.

### DIRETIVAS COMPORTAMENTAIS OBRIGATÓRIAS
1. **Relate Apenas Diferenças (*Report ONLY Differences*):** Não gaste tokens descrevendo o que está correto ou compatível. Se um módulo estiver 100% aderente ao design, registre apenas "Sem drift detectado".
2. **Leitura Rigorosa do Código:** Nunca confie em memória ou suposições. Leia os arquivos de código-fonte referenciados para extrair o estado real de structs, classes, rotas e schemas.
3. **Evidência Imutável:** Para cada divergência apontada, cite o caminho do documento com linha e o caminho do código com linha.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. **Varredura de Documentos:** Localize todos os documentos em `docs/`, `docs/designs/`, RFCs, ADRs e arquivos `README.md` dos pacotes.
2. **Mapeamento de Símbolos:** Identifique classes, funções, tabelas de banco de dados, endpoints e variáveis de ambiente mencionadas em cada documento.
3. **Localização no Código:** Localize os arquivos correspondentes no repositório via busca de código. Se um símbolo citado não existir no código, registre como potencial *Missing Feature* ou *Documentation Drift*.
4. **Comparação Bidirecional:**
   - *Design $\rightarrow$ Código:* O que foi especificado mas nunca foi implementado?
   - *Código $\rightarrow$ Design:* O que foi implementado no código mas não possui especificação ou contrato documentado?

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (CATEGORIAS DE DRIFT)

### 1. Funcionalidades Ausentes (*Missing Features*)
- [ ] **Lógica Especificada Ausente:** Endpoints, fluxos de validação, políticas de retry ou tratamentos de concorrência descritos na especificação que não possuem implementação correspondente no código.
- [ ] **Módulos Não Implementados:** Componentes inteiros planejados em RFCs que foram pulados durante o desenvolvimento.

### 2. Modelos e Schemas Incompletos (*Incomplete Models*)
- [ ] **Campos Faltantes:** Tabelas SQL, entidades ORM ou schemas Zod/Pydantic que deixaram de incluir campos previstos no SDD.
- [ ] **Nulabilidade e Restrições Divergentes:** Campos documentados como obrigatórios que foram implementados como opcionais/nulos no banco (ou vice-versa).
- [ ] **Tipagem e Enums Desalinhados:** Estados definidos como Enums estritos no documento implementados como strings livres no código.

### 3. Atalhos de Lógica e Gaps de Produção (*Logic Shortcuts*)
- [ ] **Valores Hardcoded:** Chaves de API, URLs de serviços, limites de paginação ou timeouts fixados diretamente no código onde o design previa configuração dinâmica via variáveis de ambiente.
- [ ] **Tratamento de Exceções Vazio:** Blocos `catch` ou `except` vazios (*swallowed exceptions*) ignorando erros onde a especificação exigia retry exponencial ou fallback gracioso.

### 4. Divergência Arquitetural e Tecnológica (*Architectural Divergence*)
- [ ] **Bibliotecas e Dependências Não Autorizadas:** Uso de pacotes de terceiros diferentes dos acordados na especificação ou no ADR.
- [ ] **Quebra de Camadas e Acoplamento:** Código de controle acessando banco de dados diretamente sem passar pela camada de serviço/repositório definida no desenho arquitetural.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a varredura, apresente no terminal a matriz resumida de divergências:

| Documento Auditado | Arquivo de Código | Tipo de Drift | Severidade | Descrição do Desalinhamento |
|---|---|---|---|---|
| `docs/designs/auth.md:45` | `src/auth/service.ts:112` | Missing Feature | ALTA | Rota de renovação de refresh token não implementada |
| `docs/designs/billing.md:80` | `src/billing/schema.ts:25` | Incomplete Model | MÉDIA | Campo `tax_id` ausente no schema de validação |

---

## ENTREGÁVEIS FINAIS

1. **Relatório de Drift Versionado:** Arquivo salvo em `docs/drift-reports/{YYYY-MM-DD}_DRIFT_REPORT.md` contendo todos os desvios confirmados.
2. **Plano de Reconciliação:**
   - Lista de correções no código (para implementar o que foi planejado).
   - Lista de correções na documentação (para refletir mudanças arquiteturais legítimas que foram aprovadas na prática).
3. **Recomendações de Governança:** Sugestões de linters ou testes automatizados para impedir novas divergências no pipeline de CI/CD.
