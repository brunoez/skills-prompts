# 🌐 Suíte Universal para ChatGPT, Web Chats e Assistentes de IA

Este diretório fornece **instruções de sistema, templates para assistentes personalizados (Custom GPTs / Gems / Projects) e prompts autocontidos** prontos para uso em interfaces de chat na web, desktop e APIs.

O objetivo desta suíte é ser **100% agnóstica de provedor e modelo**: ela pode ser utilizada com **qualquer modelo** da sua preferência — seja OpenAI (famílias GPT e série o), Anthropic (Claude), Google (Gemini), DeepSeek, ou modelos abertos (*open-weight*) executados localmente (via Ollama, LM Studio ou Open WebUI).

---

## 🧭 Quando Usar esta Suíte

| Ambiente | Melhor Opção | Como Usar |
| :--- | :--- | :--- |
| **Terminal / CLI do Agente** | Claude Code ou Antigravity CLI | Instalação global via `./install.sh --global` |
| **IDEs & Editores com IA** | Claude Code, Antigravity IDE, VS Code | Instalação via `./install.sh` |
| **Interfaces Web / Desktop** | ChatGPT, Claude.ai, Gemini, Open WebUI | Instruções deste diretório (`chatgpt/`) |
| **Projetos de Equipe na Nuvem** | ChatGPT Projects, Custom GPTs, Gemini Gems | Copiar templates de `chatgpt/custom-gpts/` |

---

## 📁 Estrutura de Arquivos

```plaintext
chatgpt/
├── README.md                      # Este guia de uso agnóstico
├── SYSTEM_INSTRUCTIONS.md         # Instrução Mestra Universal (Custom Instructions / System Prompt)
├── custom-gpts/                   # Templates para criação de assistentes personalizados
│   ├── 1-appsec-auditor.md        # Auditoria 360° AppSec, OWASP ASTF, ASVS L2 e SARIF
│   ├── 2-driven-development.md    # Engenharia de Software (DDD, SDD, TypeDD, TDD, BDD)
│   └── 3-full-app-validator.md    # Diagnóstico Holístico 360° & Health Card Executivo
└── prompts-condensed/             # Prompts autocontidos para copiar e colar no chat com código
    ├── appsec_auditor.md          # Auditoria de segurança profunda
    ├── api_security.md            # Auditoria de APIs (OWASP API Top 10)
    ├── tdd_workflow.md            # Ciclo Red-Green-Refactor estrito
    ├── full_app_validator.md      # Validação holística de 5 fronteiras
    └── threat_modeling.md         # Modelagem de ameaças STRIDE
```

---

## 🛠️ Como Usar

### 1. Configurar Instruções Personalizadas Globais (Custom Instructions)
Se você quer que seu assistente de chat sempre atue com mentalidade de **Principal Engineer & AppSec Yellow Team**:
1. Abra as configurações do seu chat (ex: *Custom Instructions* no ChatGPT, *User Preferences* no Open WebUI, ou *Instructions* no seu cliente favorito).
2. Copie o conteúdo de [`SYSTEM_INSTRUCTIONS.md`](SYSTEM_INSTRUCTIONS.md).
3. Cole na seção *"Como você gostaria que o modelo respondesse?"* (*How would you like the model to respond?*).

### 2. Criar Assistentes Especializados (Custom GPTs, Gemini Gems, Claude Projects)
Se você utiliza contas com suporte a assistentes personalizados:
1. Crie um novo assistente (no ChatGPT GPT Builder, Gemini Gems ou Claude Projects).
2. Abra um dos arquivos em [`custom-gpts/`](custom-gpts/):
   * [`1-appsec-auditor.md`](custom-gpts/1-appsec-auditor.md) para segurança defensiva e triagem de vulnerabilidades.
   * [`2-driven-development.md`](custom-gpts/2-driven-development.md) para arquitetura de software e testes orientados por metodologias.
   * [`3-full-app-validator.md`](custom-gpts/3-full-app-validator.md) para auditoria completa e geração de Health Cards.
3. Copie os campos: **Nome**, **Descrição**, **Instruções** e **Gatilhos de Início de Conversa** (*Conversation Starters*).

### 3. Copiar e Colar Prompts Autocontidos no Chat
Quando estiver analisando um arquivo ou módulo específico e não quiser configurar um assistente permanente:
1. Abra a pasta [`prompts-condensed/`](prompts-condensed/).
2. Escolha o prompt desejado.
3. Cole no seu chat junto com o código-fonte que deseja analisar.
   *Exemplo:*
   ```text
   [Cole o conteúdo de chatgpt/prompts-condensed/appsec_auditor.md]

   --- CÓDIGO DA MINHA APLICAÇÃO ---
   [Cole o seu arquivo de código aqui]
   ```

---

## 🎯 Guia de Escolha de Modelos (Universal & Agnóstico)

Não importa qual provedor ou infraestrutura você utiliza, recomendamos selecionar o tipo de modelo ideal para a complexidade da tarefa:

| Perfil de Modelo | Características | Ideal Para | Exemplos de Modelos |
| :--- | :--- | :--- | :--- |
| **Modelos de Fronteira (Flagship)** | Máxima inteligência, raciocínio amplo, suporte a contextos extensos | Auditorias de segurança 360°, geração de SARIF, diagnósticos arquiteturais complexos | Modelos topo de linha (ex: GPT-6 Astra, Claude 3.7 Sonnet, Gemini 2.5 Pro) |
| **Modelos de Raciocínio Profundo (Reasoning / CoT)** | Deliberação passo a passo, rigor lógico-matemático | Validação de criptografia, mitigação de race conditions, kill chains e algoritmos concorrentes | Modelos com Chain-of-Thought deliberado (ex: OpenAI série o [o3, o4-mini], DeepSeek-R1) |
| **Modelos de Produção / Balanceados** | Alta velocidade, resposta rápida e baixo custo de inferência | Ciclo diário de TDD (Red-Green-Refactor), geração de testes unitários, escrita de schemas Zod | Modelos balanceados (ex: GPT-6.1 Sol, Claude 3.5 Haiku, Gemini 2.5 Flash) |
| **Modelos Locais (Open-Weight)** | Privacidade total, execução 100% offline via Ollama/vLLM | Análise de código proprietário em ambientes corporativos com restrições rígidas de envio de dados | Modelos abertos (ex: gpt-oss, Llama 3.3, Qwen 2.5 Coder, DeepSeek) |
