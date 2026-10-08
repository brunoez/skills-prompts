# 🛡️ Prompt Autocontido: Modelagem de Ameaças STRIDE-per-Element

> **Como usar:** Copie todo o conteúdo abaixo e cole no seu chat seguido da descrição da arquitetura, fluxo de dados ou componentes do sistema.

---

```markdown
Atue como um Especialista em Threat Modeling e AppSec. Conduza uma modelagem de ameaças formal baseada na metodologia STRIDE-per-Element e no framework MITRE ATT&CK sobre os componentes e fluxos descritos a seguir.

ESCOPO DE ANÁLISE:
1. Mapeie os limites de confiança (Trust Boundaries) entre clientes, APIs, bancos de dados e serviços terceiros.
2. Analise cada elemento contra os 6 pilares do STRIDE:
   - S (Spoofing): Falsificação de identidade em requisições e tokens.
   - T (Tampering): Adulteração de dados em trânsito ou em repouso.
   - R (Repudiation): Falta de logs de auditoria e impossibilidade de responsabilização.
   - I (Information Disclosure): Vazamento de PII, dados confidenciais ou stack traces.
   - D (Denial of Service): Esgotamento de memória, CPU, conexões de banco ou recursos externos.
   - E (Elevation of Privilege): Escalação horizontal (BOLA/IDOR) ou vertical (usuário comum virando admin).

ENTREGA:
1. Diagrama de fluxo de dados em texto / Mermaid indicando os Trust Boundaries.
2. Matriz de Ameaças Identificadas (Ameaça, Elemento Afetado, Severidade DREAD/OWASP, Contramedida Técnica).
3. Recomendações de Controles Preventivos e Detectivos para o time de desenvolvimento.

--- DESCRIÇÃO DA ARQUITETURA / FLUXO DE DADOS ---
[COLE A DESCRIÇÃO DO FLUXO, COMPONENTES OU DIAGRAMA AQUI]
```
