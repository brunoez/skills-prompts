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

TARGET_DIR="${1:-.}"
INSTALL_MODE="${2:-claude}" # opcoes: claude (padrao), vscode, cursor, windsurf, all, submodule
COMPONENT="${3:-all}"       # opcoes: all (padrao: prompts + skills), prompts, skills

echo -e "${C_BLUE}ℹ️  Diretório alvo: ${C_BOLD}${TARGET_DIR}${C_RESET}"
echo -e "${C_BLUE}ℹ️  Modo de instalação: ${C_BOLD}${INSTALL_MODE}${C_RESET} (Componentes: ${COMPONENT})"

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

if [ -n "$SCRIPT_DIR" ] && [ -d "${SCRIPT_DIR}/prompts" ] && [ -d "${SCRIPT_DIR}/skills" ]; then
  LOCAL_PROMPTS_DIR="${SCRIPT_DIR}/prompts"
  LOCAL_SKILLS_DIR="${SCRIPT_DIR}/skills"
elif [ -n "$SCRIPT_DIR" ] && [ -d "${SCRIPT_DIR}/../prompts" ] && [ -d "${SCRIPT_DIR}/../skills" ]; then
  LOCAL_PROMPTS_DIR="${SCRIPT_DIR}/../prompts"
  LOCAL_SKILLS_DIR="${SCRIPT_DIR}/../skills"
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
  if [ -z "$LOCAL_PROMPTS_DIR" ] || [ -z "$LOCAL_SKILLS_DIR" ]; then
    echo -e "${C_YELLOW}📥 Baixando pacote do repositório (prompts + skills)...${C_RESET}"
    TMP_DOWNLOAD_DIR=$(mktemp -d)
    if curl -sSL "$ARCHIVE_URL" | tar -xz -C "$TMP_DOWNLOAD_DIR" --strip-components=1 2>/dev/null; then
      LOCAL_PROMPTS_DIR="${TMP_DOWNLOAD_DIR}/prompts"
      LOCAL_SKILLS_DIR="${TMP_DOWNLOAD_DIR}/skills"
    else
      echo -e "${C_YELLOW}⚠️  Falha ao baixar tarball. Clonando repositório...${C_RESET}"
      git clone --depth 1 "$REPO_URL" "$TMP_DOWNLOAD_DIR" 2>/dev/null || {
        echo -e "${C_RED}❌ Erro ao baixar arquivos do GitHub. Verifique sua conexão.${C_RESET}"
        exit 1
      }
      LOCAL_PROMPTS_DIR="${TMP_DOWNLOAD_DIR}/prompts"
      LOCAL_SKILLS_DIR="${TMP_DOWNLOAD_DIR}/skills"
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

# Aliases de compatibilidade
install_files() {
  install_prompts "$1"
}

# Dispatcher principal de instalação
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
  windsurf)
    do_install "${TARGET_DIR}/.windsurf/rules" "${TARGET_DIR}/.windsurf/skills"
    if [ "$COMPONENT" = "all" ] || [ "$COMPONENT" = "skills" ]; then
      install_skills "${TARGET_DIR}/.agent/skills"
    fi
    ;;
  all)
    if [ "$COMPONENT" = "all" ] || [ "$COMPONENT" = "prompts" ]; then
      install_prompts "${TARGET_DIR}/.claude/prompts"
      install_prompts "${TARGET_DIR}/.agent/prompts"
      install_prompts "${TARGET_DIR}/.cursor/rules"
      install_prompts "${TARGET_DIR}/.windsurf/rules"
    fi
    if [ "$COMPONENT" = "all" ] || [ "$COMPONENT" = "skills" ]; then
      install_skills "${TARGET_DIR}/.claude/skills"
      install_skills "${TARGET_DIR}/.agent/skills"
      install_skills "${TARGET_DIR}/.cursor/skills"
      install_skills "${TARGET_DIR}/.windsurf/skills"
    fi
    ;;
  agent|*)
    do_install "${TARGET_DIR}/.agent/prompts" "${TARGET_DIR}/.agent/skills"
    ;;
esac

echo ""
echo -e "${C_GREEN}${C_BOLD}🎉 Instalação concluída com sucesso!${C_RESET}"
echo -e "${C_CYAN}👉 Como usar no seu ambiente:${C_RESET}"
echo -e "   1. No Claude Code:"
echo -e "      - Prompts: use no terminal ou chat (ex: @[.claude/prompts/security/api.md])"
echo -e "      - Skills: carregadas nativamente pelo Claude Code em .claude/skills/"
echo -e "   2. No VSCode / Copilot Chat:"
echo -e "      - Prompts: @workspace @[.agent/prompts/driven-development/sdd_spec_driven.md]"
echo -e "      - Skills: agentes integrados em .agent/skills/"
echo -e "   3. No Cursor & Windsurf:"
echo -e "      - Prompts/Regras: @[.cursor/rules/...] ou @[.windsurf/rules/...]"
echo -e "      - Skills: em .cursor/skills/ e .windsurf/skills/"
echo -e "   4. Documentação completa em: ${C_BOLD}https://github.com/brunoez/skills-prompts${C_RESET}"
echo ""
