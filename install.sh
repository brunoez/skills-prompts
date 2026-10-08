#!/usr/bin/env bash
# ==============================================================================
# Script de Instalação Automática da Suíte de Prompts & Agent Skills
# Repositório: https://github.com/brunoez/skills-prompts
# ==============================================================================

set -e

REPO_URL="https://github.com/brunoez/skills-prompts.git"
RAW_BASE="https://raw.githubusercontent.com/brunoez/skills-prompts/main"
ARCHIVE_URL="https://github.com/brunoez/skills-prompts/archive/refs/heads/main.tar.gz"

# Cores para saída no terminal
C_RESET='\033[0m'
C_BOLD='\033[1m'
C_GREEN='\033[32m'
C_BLUE='\033[34m'
C_YELLOW='\033[33m'
C_CYAN='\033[36m'
C_RED='\033[31m'

echo -e "${C_CYAN}${C_BOLD}"
echo "================================================================="
echo "  🛡️  Instalador da Suíte de Prompts & Agent Skills"
echo "  📦 Repositório: https://github.com/brunoez/skills-prompts"
echo "================================================================="
echo -e "${C_RESET}"

IS_GLOBAL=false
if [ "$1" = "--global" ] || [ "$1" = "-g" ]; then
  IS_GLOBAL=true
  TARGET_DIR="${GLOBAL_TARGET_DIR:-${HOME:-~}}"
  INSTALL_MODE="${2:-all}" # opcoes globais: all (padrao: claude + antigravity), claude, antigravity
  COMPONENT="${3:-all}"    # opcoes: all (padrao: prompts + skills), prompts, skills
else
  TARGET_DIR="${1:-.}"
  INSTALL_MODE="${2:-claude}" # opcoes locais: claude (padrao), vscode, cursor, all, submodule
  COMPONENT="${3:-all}"       # opcoes: all (padrao: prompts + skills), prompts, skills
fi

if [ "$IS_GLOBAL" = true ]; then
  echo -e "${C_BLUE}ℹ️  Instalação GLOBAL para o usuário: ${C_BOLD}${TARGET_DIR}${C_RESET}"
  echo -e "${C_BLUE}ℹ️  Ambientes globais: ${C_BOLD}${INSTALL_MODE}${C_RESET} (Componentes: ${COMPONENT})"
else
  echo -e "${C_BLUE}ℹ️  Diretório alvo: ${C_BOLD}${TARGET_DIR}${C_RESET}"
  echo -e "${C_BLUE}ℹ️  Modo de instalação local: ${C_BOLD}${INSTALL_MODE}${C_RESET} (Componentes: ${COMPONENT})"
fi

# Lista de categorias e arquivos de prompts
PROMPT_FILES=(
  "driven-development/sdd_spec_driven.md"
  "driven-development/secdd_abuse_cases.md"
  "driven-development/bdd_behavior_driven.md"
  "driven-development/tdd_test_driven.md"
  "driven-development/cdd_contract_driven.md"
  "driven-development/test_suite_generator.md"
  "driven-development/technical_documentation.md"
  "driven-development/project_context.md"
  "driven-development/full_app_validator.md"
  "driven-development/ddd_domain_driven.md"
  "driven-development/typedd_type_driven.md"
  "driven-development/datadd_data_driven.md"

  "security/api.md"
  "security/business.md"
  "security/db.md"
  "security/frontend.md"
  "security/secrets.md"
  "security/supply_chain.md"
  "security/threat_modeling.md"
  "security/ai_appsec.md"
  "security/authn_identity.md"
  "security/access_control.md"
  "security/ssrf.md"
  "security/secure_config.md"
  "security/input_validation.md"
  "security/adversarial_patching.md"
  "security/exploit_chaining.md"
  "security/vcs_security_history.md"
  "security/sec_advisor.md"
  "security/appsec_auditor.md"

  "devops/cicd_pipeline.md"
  "devops/iac_docker_k8s.md"
  "devops/resilience_observability.md"
  "jev/system_one_architecture.md"
  "jev/agent_guardrails_safety.md"
  "jev/intent_routing_dispatch.md"
  "jev/rag_verification_guardrails.md"
  "jev/secret_detection_triage.md"
  "jev/mcp_agent_security_scan.md"
  "jev/pii_sanitization_guardrail.md"
  "jev/vulnerability_triage_cvss.md"
)

# Lista de Agent Skills
SKILL_NAMES=(
  "appsec-auditor"
  "driven-development"
  "full-app-validator"
  "jev-system-one"
)

# Identifica se está rodando localmente ou precisa baixar
SCRIPT_DIR=""
if [ -n "${BASH_SOURCE[0]}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

LOCAL_PROMPTS_DIR=""
LOCAL_SKILLS_DIR=""
LOCAL_CHATGPT_DIR=""

if [ -n "$SCRIPT_DIR" ] && [ -d "${SCRIPT_DIR}/prompts" ] && [ -d "${SCRIPT_DIR}/skills" ]; then
  LOCAL_PROMPTS_DIR="${SCRIPT_DIR}/prompts"
  LOCAL_SKILLS_DIR="${SCRIPT_DIR}/skills"
  LOCAL_CHATGPT_DIR="${SCRIPT_DIR}/chatgpt"
elif [ -n "$SCRIPT_DIR" ] && [ -d "${SCRIPT_DIR}/../prompts" ] && [ -d "${SCRIPT_DIR}/../skills" ]; then
  LOCAL_PROMPTS_DIR="${SCRIPT_DIR}/../prompts"
  LOCAL_SKILLS_DIR="${SCRIPT_DIR}/../skills"
  LOCAL_CHATGPT_DIR="${SCRIPT_DIR}/../chatgpt"
fi

TMP_DOWNLOAD_DIR=""
cleanup() {
  if [ -n "$TMP_DOWNLOAD_DIR" ] && [ -d "$TMP_DOWNLOAD_DIR" ]; then
    rm -rf "$TMP_DOWNLOAD_DIR"
  fi
}
trap cleanup EXIT INT TERM

# Se não estiver em clone local, faz download sob demanda
prepare_sources() {
  if [ -z "$LOCAL_PROMPTS_DIR" ] || [ -z "$LOCAL_SKILLS_DIR" ] || [ -z "$LOCAL_CHATGPT_DIR" ]; then
    echo -e "${C_YELLOW}📥 Baixando pacote do repositório (prompts + skills + chatgpt)...${C_RESET}"
    TMP_DOWNLOAD_DIR=$(mktemp -d)
    if curl -sSL "$ARCHIVE_URL" | tar -xz -C "$TMP_DOWNLOAD_DIR" --strip-components=1 2>/dev/null; then
      LOCAL_PROMPTS_DIR="${TMP_DOWNLOAD_DIR}/prompts"
      LOCAL_SKILLS_DIR="${TMP_DOWNLOAD_DIR}/skills"
      LOCAL_CHATGPT_DIR="${TMP_DOWNLOAD_DIR}/chatgpt"
    else
      echo -e "${C_YELLOW}⚠️  Falha ao baixar tarball. Clonando repositório...${C_RESET}"
      git clone --depth 1 "$REPO_URL" "$TMP_DOWNLOAD_DIR" 2>/dev/null || {
        echo -e "${C_RED}❌ Erro ao baixar arquivos do GitHub. Verifique sua conexão.${C_RESET}"
        exit 1
      }
      LOCAL_PROMPTS_DIR="${TMP_DOWNLOAD_DIR}/prompts"
      LOCAL_SKILLS_DIR="${TMP_DOWNLOAD_DIR}/skills"
      LOCAL_CHATGPT_DIR="${TMP_DOWNLOAD_DIR}/chatgpt"
    fi
  fi
}

install_submodule() {
  echo -e "${C_YELLOW}📦 Instalando como Git Submodule em ${TARGET_DIR}/.agent/prompts...${C_RESET}"
  cd "$TARGET_DIR"
  if [ -d ".git" ]; then
    git submodule add "$REPO_URL" .agent/prompts || git submodule update --init --recursive
    echo -e "${C_GREEN}✅ Submódulo configurado com sucesso!${C_RESET}"
  else
    echo -e "${C_RED}❌ O diretório alvo não é um repositório git. Inicialize com 'git init' primeiro.${C_RESET}"
    exit 1
  fi
}

install_prompts() {
  local DEST_BASE="$1"
  prepare_sources
  echo -e "${C_YELLOW}📥 Instalando prompts em ${DEST_BASE}...${C_RESET}"
  
  mkdir -p "${DEST_BASE}/driven-development" "${DEST_BASE}/security" "${DEST_BASE}/devops" "${DEST_BASE}/jev"
  
  for file in "${PROMPT_FILES[@]}"; do
    dest_path="${DEST_BASE}/${file}"
    if [ -n "$LOCAL_PROMPTS_DIR" ] && [ -f "${LOCAL_PROMPTS_DIR}/${file}" ]; then
      cp "${LOCAL_PROMPTS_DIR}/${file}" "$dest_path"
    else
      curl -sSL "${RAW_BASE}/prompts/${file}" -o "$dest_path"
    fi
  done
  
  echo -e "${C_GREEN}✅ Prompts instalados em: ${DEST_BASE} (${#PROMPT_FILES[@]} prompts)${C_RESET}"
}

install_skills() {
  local DEST_BASE="$1"
  prepare_sources
  echo -e "${C_YELLOW}📥 Instalando Agent Skills em ${DEST_BASE}...${C_RESET}"
  
  mkdir -p "${DEST_BASE}"
  local count=0
  for skill in "${SKILL_NAMES[@]}"; do
    local src_skill="${LOCAL_SKILLS_DIR}/${skill}"
    if [ -d "$src_skill" ]; then
      mkdir -p "${DEST_BASE}/${skill}"
      cp -R "${src_skill}/." "${DEST_BASE}/${skill}/"
      find "${DEST_BASE}/${skill}" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
      find "${DEST_BASE}/${skill}" -type f -name "*.pyc" -delete 2>/dev/null || true
      count=$((count + 1))
    fi
  done
  
  echo -e "${C_GREEN}✅ Agent Skills instaladas em: ${DEST_BASE} (${count} skills)${C_RESET}"
}

# Instalação de prompts como Slash Commands no Claude Code (~/.claude/commands/)
install_claude_commands() {
  local DEST_BASE="$1"
  prepare_sources
  echo -e "${C_YELLOW}📥 Instalando Slash Commands do Claude Code em ${DEST_BASE}...${C_RESET}"
  
  mkdir -p "${DEST_BASE}"
  local count=0
  for file in "${PROMPT_FILES[@]}"; do
    local src_file=""
    if [ -n "$LOCAL_PROMPTS_DIR" ] && [ -f "${LOCAL_PROMPTS_DIR}/${file}" ]; then
      src_file="${LOCAL_PROMPTS_DIR}/${file}"
    fi

    local base_name="$(basename "$file")"
    local clean_name="${base_name%.md}"
    local cmd_name="$clean_name"

    case "$file" in
      driven-development/sdd_*) cmd_name="sdd" ;;
      driven-development/secdd_*) cmd_name="secdd" ;;
      driven-development/bdd_*) cmd_name="bdd" ;;
      driven-development/tdd_*) cmd_name="tdd" ;;
      driven-development/cdd_*) cmd_name="cdd" ;;
      driven-development/ddd_*) cmd_name="ddd" ;;
      driven-development/typedd_*) cmd_name="typedd" ;;
      driven-development/datadd_*) cmd_name="datadd" ;;
      driven-development/full_app_validator.md) cmd_name="full-app-validator" ;;
      driven-development/test_suite_generator.md) cmd_name="test-suite-generator" ;;
      driven-development/technical_documentation.md) cmd_name="technical-documentation" ;;
      driven-development/project_context.md) cmd_name="project-context" ;;
      
      security/appsec_auditor.md) cmd_name="appsec-auditor" ;;
      security/sec_advisor.md) cmd_name="sec-advisor" ;;
      security/threat_modeling.md) cmd_name="threat-modeling" ;;
      security/*) cmd_name="sec-${clean_name//_/-}" ;;
      
      devops/*) cmd_name="devops-${clean_name//_/-}" ;;
      jev/*) cmd_name="jev-${clean_name//_/-}" ;;
    esac

    local target_cmd="${DEST_BASE}/${cmd_name}.md"
    if [ -n "$src_file" ]; then
      cp "$src_file" "$target_cmd"
    else
      curl -sSL "${RAW_BASE}/prompts/${file}" -o "$target_cmd"
    fi

    # Alias com o nome original do arquivo para compatibilidade direta
    local alias_cmd="${DEST_BASE}/${clean_name}.md"
    if [ "$alias_cmd" != "$target_cmd" ]; then
      cp "$target_cmd" "$alias_cmd"
    fi

    count=$((count + 1))
  done

  echo -e "${C_GREEN}✅ Slash Commands instalados em: ${DEST_BASE} (${count} comandos disponíveis com /)${C_RESET}"
}

install_chatgpt() {
  local DEST_BASE="$1"
  prepare_sources
  echo -e "${C_YELLOW}📥 Instalando suíte ChatGPT / OpenAI em ${DEST_BASE}...${C_RESET}"
  
  mkdir -p "${DEST_BASE}"
  if [ -n "$LOCAL_CHATGPT_DIR" ] && [ -d "$LOCAL_CHATGPT_DIR" ]; then
    cp -R "${LOCAL_CHATGPT_DIR}/." "${DEST_BASE}/"
    echo -e "${C_GREEN}✅ Suíte ChatGPT instalada em: ${DEST_BASE}${C_RESET}"
  else
    echo -e "${C_YELLOW}⚠️  Pasta chatgpt não encontrada para cópia.${C_RESET}"
  fi
}

# Aliases de compatibilidade
install_files() {
  install_prompts "$1"
}

# Dispatcher de instalação local por repositório
do_install() {
  local prompt_target="$1"
  local skill_target="$2"

  if [ "$COMPONENT" = "all" ] || [ "$COMPONENT" = "prompts" ]; then
    if [ -n "$prompt_target" ]; then
      install_prompts "$prompt_target"
    fi
  fi

  if [ "$COMPONENT" = "all" ] || [ "$COMPONENT" = "skills" ]; then
    if [ -n "$skill_target" ]; then
      install_skills "$skill_target"
    fi
  fi
}

# Dispatcher de instalação global no sistema do usuário
do_global_install() {
  local mode="$1"
  case "$mode" in
    claude|claude-code)
      if [ "$COMPONENT" = "all" ] || [ "$COMPONENT" = "prompts" ]; then
        install_claude_commands "${TARGET_DIR}/.claude/commands"
      fi
      if [ "$COMPONENT" = "all" ] || [ "$COMPONENT" = "skills" ]; then
        install_skills "${TARGET_DIR}/.claude/skills"
      fi
      ;;
    antigravity|gemini)
      if [ "$COMPONENT" = "all" ] || [ "$COMPONENT" = "skills" ]; then
        install_skills "${TARGET_DIR}/.gemini/skills"
        if [ -d "${TARGET_DIR}/.gemini/antigravity-cli" ]; then
          install_skills "${TARGET_DIR}/.gemini/antigravity-cli/skills"
        fi
      fi
      ;;
    chatgpt|openai)
      install_chatgpt "${TARGET_DIR}/.chatgpt"
      ;;
    all|*)
      if [ "$COMPONENT" = "all" ] || [ "$COMPONENT" = "prompts" ]; then
        install_claude_commands "${TARGET_DIR}/.claude/commands"
      fi
      if [ "$COMPONENT" = "all" ] || [ "$COMPONENT" = "skills" ]; then
        install_skills "${TARGET_DIR}/.claude/skills"
        install_skills "${TARGET_DIR}/.gemini/skills"
        if [ -d "${TARGET_DIR}/.gemini/antigravity-cli" ]; then
          install_skills "${TARGET_DIR}/.gemini/antigravity-cli/skills"
        fi
      fi
      install_chatgpt "${TARGET_DIR}/.chatgpt"
      ;;
  esac
}

# Execução do fluxo de instalação
if [ "$IS_GLOBAL" = true ]; then
  do_global_install "$INSTALL_MODE"
else
  case "$INSTALL_MODE" in
    submodule)
      install_submodule
      ;;
    claude|claude-code)
      do_install "${TARGET_DIR}/.claude/prompts" "${TARGET_DIR}/.claude/skills"
      ;;
    vscode)
      do_install "${TARGET_DIR}/.agent/prompts" "${TARGET_DIR}/.agent/skills"
      ;;
    cursor)
      do_install "${TARGET_DIR}/.cursor/rules" "${TARGET_DIR}/.cursor/skills"
      if [ "$COMPONENT" = "all" ] || [ "$COMPONENT" = "skills" ]; then
        install_skills "${TARGET_DIR}/.agent/skills"
      fi
      ;;
    all)
      if [ "$COMPONENT" = "all" ] || [ "$COMPONENT" = "prompts" ]; then
        install_prompts "${TARGET_DIR}/.claude/prompts"
        install_prompts "${TARGET_DIR}/.agent/prompts"
        install_prompts "${TARGET_DIR}/.cursor/rules"
      fi
      if [ "$COMPONENT" = "all" ] || [ "$COMPONENT" = "skills" ]; then
        install_skills "${TARGET_DIR}/.claude/skills"
        install_skills "${TARGET_DIR}/.agent/skills"
        install_skills "${TARGET_DIR}/.cursor/skills"
      fi
      ;;
    agent|*)
      do_install "${TARGET_DIR}/.agent/prompts" "${TARGET_DIR}/.agent/skills"
      ;;
  esac
fi

echo ""
echo -e "${C_GREEN}${C_BOLD}🎉 Instalação concluída com sucesso!${C_RESET}"
if [ "$IS_GLOBAL" = true ]; then
  echo -e "${C_CYAN}👉 Como usar globalmente no seu sistema:${C_RESET}"
  echo -e "   1. No Claude Code (em qualquer pasta/projeto):"
  echo -e "      - Slash Commands: digite /appsec-auditor, /full-app-validator, /tdd, /bdd, etc."
  echo -e "      - Agent Skills: ativadas automaticamente em ~/.claude/skills/"
  echo -e "   2. No Google Antigravity (em qualquer workspace):"
  echo -e "      - Agent Skills: ativadas automaticamente em ~/.gemini/skills/"
  echo -e "   3. No ChatGPT (OpenAI) e Web Chats:"
  echo -e "      - Instruções Mestras: copie ~/.chatgpt/SYSTEM_INSTRUCTIONS.md para as Custom Instructions"
  echo -e "      - Custom GPTs e Prompts Condensados prontos em: ~/.chatgpt/"
  echo -e "   4. Documentação completa em: ${C_BOLD}https://github.com/brunoez/skills-prompts${C_RESET}"
else
  echo -e "${C_CYAN}👉 Como usar no seu projeto:${C_RESET}"
  echo -e "   1. No Claude Code:"
  echo -e "      - Prompts locais: use no chat (ex: @[.claude/prompts/security/api.md])"
  echo -e "      - Skills locais: carregadas em .claude/skills/"
  echo -e "   2. No VSCode / Copilot Chat / Antigravity:"
  echo -e "      - Prompts: @workspace @[.agent/prompts/driven-development/sdd_spec_driven.md]"
  echo -e "      - Skills: agentes integrados em .agent/skills/"
  echo -e "   3. No Cursor:"
  echo -e "      - Prompts/Regras: @[.cursor/rules/...]"
  echo -e "      - Skills: em .cursor/skills/ e .agent/skills/"
  echo -e "   💡 Dica: Para usar em TODOS os projetos sem reinstalar, use: ./install.sh --global"
  echo -e "   4. Documentação completa em: ${C_BOLD}https://github.com/brunoez/skills-prompts${C_RESET}"
fi
echo ""
