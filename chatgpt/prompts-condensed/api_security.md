# 🛡️ Prompt Autocontido: Auditoria de APIs (OWASP API Top 10)

> **Como usar:** Copie todo o conteúdo abaixo e cole no seu chat seguido da especificação OpenAPI, rotas ou controllers da sua API.

---

```markdown
Atue como um Especialista em Segurança de APIs. Analise as rotas, controllers, middlewares e contratos de API fornecidos abaixo com base no OWASP API Security Top 10 (ASTF).

CHECKLIST OBRIGATÓRIO DE VERIFICAÇÃO:
- API1: BOLA / IDOR (Validação de permissão e propriedade do objeto no backend em cada rota com IDs).
- API2: Quebra de Autenticação (JWT sem assinatura adequada, tempos de expiração longos, falta de revogação).
- API3: Atribuição em Massa / Mass Assignment (Injeção de campos protegidos como 'isAdmin', 'role', 'balance').
- API4: Consumo Excessivo de Recursos (Falta de Rate Limiting, paginação sem limites de página, payloads gigantes).
- API5: BFLA (Quebra de Autorização em Nível de Função de Negócio ou rotas administrativas expostas).
- API6: Acesso Indevido a Fluxos de Negócio (Automação de ações restritas, burla de funil, idempotência ausente).
- API7: Server-Side Request Forgery (SSRF em webhooks, URLs externas de download ou integrações de terceiros).
- API8: Configuração Insegura (CORS excessivamente permissivo com Access-Control-Allow-Origin: *, headers de segurança ausentes).
- API9: Gerenciamento Inadequado de Inventário (Rotas legadas sem auth, endpoints /v1 não depreciados).
- API10: Consumo Inseguro de APIs de Terceiros (Falta de validação e sanitização de dados vindos de APIs parceiras).

ENTREGA:
1. Matriz de conformidade das 10 categorias OWASP API.
2. Patches cirúrgicos para cada falha encontrada.
3. Exemplo de teste de integração HTTP (Supertest / pytest) validando a rota corrigida.

--- ROTAS / CONTROLLERS / ESPECIFICAÇÃO DE API ---
[COLE SUAS ROTAS OU CÓDIGO AQUI]
```
