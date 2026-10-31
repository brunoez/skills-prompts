# PROMPT DE ENGENHARIA: GERAÇÃO E AUDITORIA DE AGENTS.md (README PARA AGENTES DE IA)

## OBJETIVO
Atuar como Engenheiro Principal de Contexto de IA e Arquiteto de Software. Sua missão é realizar uma varredura completa na base de código para estruturar, auditar ou gerar o arquivo **`AGENTS.md`** na raiz do projeto (e arquivos aninhados em monorepos), aderindo à especificação aberta mantida pela **Linux Foundation** ([agents.md](https://agents.md/)).

O `AGENTS.md` funciona como um **"README para Agentes de Código"**: um local dedicado, previsível e padronizado para fornecer aos assistentes de IA (Claude Code, Google Antigravity, OpenAI Codex, Cursor, RooCode, Aider, GitHub Copilot) todo o contexto operacional necessário (comandos de desenvolvimento sem travar HMR, instruções de teste focalizadas, regras de código, invariantes de segurança e diretrizes de PR), mantendo o `README.md` principal conciso e focado em humanos.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. **Manifestos e Scripts de Execução:** Leia os arquivos de configuração do ecossistema (`package.json`, `pnpm-workspace.yaml`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, `docker-compose.yml`) para identificar os comandos reais de build, dev, lint e teste.
2. **Workflows de CI/CD:** Leia os arquivos em `.github/workflows/` ou `.gitlab-ci.yml` para extrair os comandos de teste exatos e variáveis de ambiente necessárias.
3. **Padrões e Convenções de Código:** Inspecione configs de linters e formatadores (`.eslintrc`, `biome.json`, `tsconfig.json`, `ruff.toml`) e convenções de nomenclatura de pastas e commits.
4. **Fronteiras de Segurança & Restrições Inegociáveis:** Mapeie regras de isolamento de banco de dados, sanitização de dados sensíveis e restrições de deploy/build.
5. **Arquitetura de Repositório (Monorepo vs. Polirepo):** Se o repositório for um monorepo (Turborepo, Nx, Cargo workspaces, pnpm workspaces), identifique a necessidade de arquivos `AGENTS.md` aninhados nos pacotes internos.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (CONTRATO AGENTS.md)

### 1. Instruções do Ambiente de Desenvolvimento (Dev Environment Tips)
- [ ] **Comando do Servidor de Desenvolvimento:** O arquivo especifica claramente o comando para iniciar o servidor local com hot-reload ativo (ex: `npm run dev`, `pnpm dev`, `cargo run`).
- [ ] **Prevenção de Build de Produção em Sessão Interativa:** Inclui aviso explícito para **não** rodar comandos de build de produção (ex: `npm run build`) durante sessões de codificação do agente, evitando que arquivos de cache desativem o hot-reload ou gerem inconsistências de assets.
- [ ] **Comandos de Navegação e Filtros em Monorepos:** Fornece comandos diretos para executar tarefas filtradas por pacote (ex: `pnpm --filter <pkg> test`) em vez de forçar o agente a varrer diretórios via `ls`.

### 2. Instruções de Teste & Verificação (Testing Instructions)
- [ ] **Comando Rápido da Suíte Completa:** Declara o comando exato para rodar todos os testes da aplicação (ex: `pytest`, `pnpm test`, `go test ./...`).
- [ ] **Comando para Execução de Teste Isolado:** Ensina o agente a rodar apenas um teste ou arquivo específico com flags de filtro (ex: `pnpm vitest run -t "<nome>"`, `pytest -k "<nome>"`), economizando tempo e contexto.
- [ ] **Critério de Aceite Estrito (*Proof of Done*):** Instrução clara de que todas as alterações devem vir acompanhadas de testes e que a suíte deve ficar 100% verde antes de submeter a tarefa.
- [ ] **Proibição de Alteração Oportunista de Testes:** Proíbe o agente de enfraquecer asserts ou desabilitar testes existentes para contornar falhas.

### 3. Convenções de Código & Arquitetura (Coding Conventions)
- [ ] **Linguagem & Tipagem Estrita:** Padrões de TypeScript/Python/Go (ex: modo estrito, inferência via Zod/Pydantic, proibição de tipos `any`).
- [ ] **Localização de Arquivos e Componentes:** Regras de co-localização de estilos, testes e utilitários próximos ao componente.
- [ ] **Tratamento de Erros e Exceções:** Padrão arquitetural de erros de domínio e proibição de strings puras em exceções.

### 4. Diretrizes de Pull Request e Commits (PR & Git Instructions)
- [ ] **Formato de Mensagens de Commit:** Padrão de versionamento e commits convencionais (ex: `feat(scope): ...`, `fix(scope): ...`).
- [ ] **Formato de Título de PR:** Template padronizado de abertura de pull requests.
- [ ] **Pré-Requisitos Antes do Commit:** Checklist mandatória de rodar linter, formatador e testes antes de submeter alterações.

### 5. Considerações de Segurança & Hardening (Security Invariants)
- [ ] **Segredos e Credenciais:** Proibição estrita de commitar chaves de API, senhas ou tokens mockados em texto aberto.
- [ ] **Permissões Mínimas:** Instruções para rodar comandos sem privilégios desnecessários de root/sudo.

### 6. Economia de Tokens & Invariantes de Scaffolding (Google Research Harness²)
- [ ] **Princípio de Economia de Contexto (*Token Economics*):** O `AGENTS.md` deve ser mantido enxuto e operacional (< 250 linhas). Procedimentos complexos, migrações de dados e auditorias profundas não devem inchar o contexto contínuo; delegue-os para **Skills sob demanda** (`skills/<nome>/SKILL.md`) ou **Scripts determinísticos** (`scripts/<nome>.py`), pois *"always-on prose is the expensive option"*.
- [ ] **Invariante de Existência de Scripts (*Script Existence Invariant*):** Todo comando, script Python (`.py`) ou shell script (`.sh`) referenciado no `AGENTS.md` DEVE existir fisicamente no repositório e ter permissões de execução válidas.
- [ ] **Invariante de Linha de Gatilho (*Trigger Line Invariant*):** Se o repositório contiver Agent Skills locais, o `AGENTS.md` deve apresentar uma linha concisa de ativação (1 frase de gatilho) por skill, permitindo que os agentes as descubram e carreguem apenas quando necessário.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise ou geração, apresente no chat:
1. Resumo dos comandos e convenções identificados no repositório.
2. Tabela de diagnóstico do `AGENTS.md`:

| Seção | Status | Conteúdo Mapeado | Ação Realizada |
|---|---|---|---|
| Dev Environment | 🟢 OK | `pnpm dev` com aviso anti-build | Gerado / Validado |
| Testing | 🟢 OK | `pytest tests/` + filtro por arquivo | Gerado / Validado |
| Coding Conventions | 🟢 OK | TypeScript strict + Zod | Gerado / Validado |
| Git & PR | 🟢 OK | Conventional Commits | Gerado / Validado |

---

## ENTREGÁVEIS FINAIS

1. **Arquivo `AGENTS.md` Gerado/Atualizado:** Salvo na raiz do repositório (`./AGENTS.md`) e, se aplicável, nos subdiretórios de pacotes do monorepo.
2. **Confirmação dos Comandos:** Validação em tempo de execução dos comandos documentados (testes e lint) para certificar que as instruções fornecidas aos agentes funcionam sem erros.
