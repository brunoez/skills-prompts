#!/usr/bin/env python3
"""
Script de Verificação de Integridade, Qualidade e Testes da Suíte de Prompts
Executado em CI/CD e localmente para garantir zero drift nos prompts e scripts.
"""

import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT_DIR / "prompts"

EXPECTED_PROMPTS = [
    "driven-development/sdd_spec_driven.md",
    "driven-development/secdd_abuse_cases.md",
    "driven-development/bdd_behavior_driven.md",
    "driven-development/tdd_test_driven.md",
    "driven-development/cdd_contract_driven.md",
    "driven-development/test_suite_generator.md",
    "driven-development/technical_documentation.md",
    "driven-development/project_context.md",
    "driven-development/full_app_validator.md",
    "driven-development/ddd_domain_driven.md",
    "driven-development/typedd_type_driven.md",
    "driven-development/datadd_data_driven.md",
    "security/api.md",

    "security/business.md",
    "security/db.md",
    "security/frontend.md",
    "security/secrets.md",
    "security/supply_chain.md",
    "security/threat_modeling.md",
    "security/ai_appsec.md",
    "security/authn_identity.md",
    "security/access_control.md",
    "security/ssrf.md",
    "security/secure_config.md",
    "security/input_validation.md",
    "security/adversarial_patching.md",
    "security/exploit_chaining.md",
    "security/vcs_security_history.md",
    "security/sec_advisor.md",
    "security/appsec_auditor.md",
    "devops/cicd_pipeline.md",
    "devops/iac_docker_k8s.md",
    "devops/resilience_observability.md",
    "jev/system_one_architecture.md",
    "jev/agent_guardrails_safety.md",
    "jev/intent_routing_dispatch.md",
    "jev/rag_verification_guardrails.md",
    "jev/secret_detection_triage.md",
    "jev/mcp_agent_security_scan.md",
    "jev/pii_sanitization_guardrail.md",
    "jev/vulnerability_triage_cvss.md",
]

SECURITY_PROMPTS = [
    "security/api.md",
    "security/business.md",
    "security/db.md",
    "security/frontend.md",
    "security/secrets.md",
    "security/supply_chain.md",
    "security/threat_modeling.md",
    "security/ai_appsec.md",
    "security/authn_identity.md",
    "security/access_control.md",
    "security/ssrf.md",
    "security/secure_config.md",
    "security/input_validation.md",
    "security/adversarial_patching.md",
    "security/exploit_chaining.md",
    "security/vcs_security_history.md",
    "security/sec_advisor.md",
    "security/appsec_auditor.md",
    "driven-development/secdd_abuse_cases.md",
]

EXPECTED_SKILLS = [
    "appsec-auditor",
    "driven-development",
    "full-app-validator",
    "jev-system-one",
]


REQUIRED_SECTIONS = [
    "## OBJETIVO",
    "## ESCOPO",
    "## SAÍDA",
    "## ENTREGÁVEIS",
]


def test_prompts_exist():
    print(f"🔍 [1/6] Verificando existência física de todos os {len(EXPECTED_PROMPTS)} prompts...")
    missing = []
    for rel_path in EXPECTED_PROMPTS:
        full_path = PROMPTS_DIR / rel_path
        if not full_path.is_file():
            missing.append(rel_path)
    if missing:
        print(f"❌ ERRO: Prompts ausentes no disco: {missing}")
        return False
    print(f"✅ Todos os {len(EXPECTED_PROMPTS)} prompts existem fisicamente.")
    return True


def test_prompt_structure():
    print("🔍 [2/6] Validando contrato de estrutura padrão dos prompts...")
    errors = []
    for rel_path in EXPECTED_PROMPTS:
        full_path = PROMPTS_DIR / rel_path
        content = full_path.read_text(encoding="utf-8")
        
        for section in REQUIRED_SECTIONS:
            if section not in content:
                errors.append(f"Prompt {rel_path} não contém a seção obrigatória '{section}'")
        
        if "## CHECKLIST" not in content and "### 1." not in content:
            errors.append(f"Prompt {rel_path} não contém seção de CHECKLIST de auditoria")

    if errors:
        for err in errors:
            print(f"❌ {err}")
        return False
    print("✅ Todos os prompts atendem ao contrato estrutural padrão.")
    return True


def test_install_script_sync():
    print("🔍 [3/6] Validando sincronia do instalador install.sh...")
    install_sh = ROOT_DIR / "install.sh"
    if not install_sh.is_file():
        print("❌ ERRO: install.sh não encontrado.")
        return False
    
    content = install_sh.read_text(encoding="utf-8")
    missing_in_installer = []
    for rel_path in EXPECTED_PROMPTS:
        if f'"{rel_path}"' not in content:
            missing_in_installer.append(rel_path)
            
    if missing_in_installer:
        print(f"❌ ERRO: install.sh não inclui os prompts: {missing_in_installer}")
        return False

    missing_skills_in_installer = []
    for skill in EXPECTED_SKILLS:
        if f'"{skill}"' not in content:
            missing_skills_in_installer.append(skill)

    if missing_skills_in_installer:
        print(f"❌ ERRO: install.sh não inclui as skills: {missing_skills_in_installer}")
        return False

    print("✅ install.sh está 100% sincronizado com os catálogos de prompts e skills.")
    return True


def test_readme_links():
    print("🔍 [4/6] Validando links de prompts no README.md...")
    readme = ROOT_DIR / "README.md"
    content = readme.read_text(encoding="utf-8")
    missing_in_readme = []
    for rel_path in EXPECTED_PROMPTS:
        if rel_path not in content:
            missing_in_readme.append(rel_path)
            
    if missing_in_readme:
        print(f"❌ ERRO: README.md não faz referência aos prompts: {missing_in_readme}")
        return False
    print("✅ README.md faz referência a todos os prompts.")
    return True


def test_installer_execution():
    print("🔍 [5/6] Testando execução funcional do instalador install.sh...")
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = ["bash", str(ROOT_DIR / "install.sh"), tmpdir, "all"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"❌ ERRO na execução do install.sh: {res.stderr}")
            return False
        
        for folder in [".claude/prompts", ".agent/prompts", ".cursor/rules"]:
            target_path = Path(tmpdir) / folder
            for prompt in EXPECTED_PROMPTS:
                if not (target_path / prompt).is_file():
                    print(f"❌ ERRO: Arquivo {prompt} não foi instalado em {folder}")
                    return False

        for folder in [".claude/skills", ".agent/skills", ".cursor/skills"]:
            target_path = Path(tmpdir) / folder
            for skill in EXPECTED_SKILLS:
                skill_md = target_path / skill / "SKILL.md"
                if not skill_md.is_file():
                    print(f"❌ ERRO: Skill {skill}/SKILL.md não foi instalada em {folder}")
                    return False
    print("✅ install.sh executado e testado com sucesso em todos os modos (prompts + skills).")
    return True


def test_global_installer_execution():
    print("🔍 [5.1/8] Testando execução funcional do instalador install.sh em modo --global...")
    with tempfile.TemporaryDirectory() as tmpdir:
        env = os.environ.copy()
        env["HOME"] = tmpdir
        cmd = ["bash", str(ROOT_DIR / "install.sh"), "--global", "all"]
        res = subprocess.run(cmd, capture_output=True, text=True, env=env)
        if res.returncode != 0:
            print(f"❌ ERRO na execução do install.sh --global: {res.stderr}")
            return False

        # Verifica commands do Claude Code
        claude_commands = Path(tmpdir) / ".claude" / "commands"
        if not claude_commands.is_dir():
            print("❌ ERRO: Diretório .claude/commands não foi criado no modo global.")
            return False

        for cmd_name in ["appsec-auditor.md", "full-app-validator.md", "tdd.md", "bdd.md", "sdd.md"]:
            if not (claude_commands / cmd_name).is_file():
                print(f"❌ ERRO: Slash command {cmd_name} não encontrado em .claude/commands")
                return False

        # Verifica skills do Claude Code e Antigravity
        for folder in [".claude/skills", ".gemini/skills"]:
            target_path = Path(tmpdir) / folder
            for skill in EXPECTED_SKILLS:
                skill_md = target_path / skill / "SKILL.md"
                if not skill_md.is_file():
                    print(f"❌ ERRO: Skill {skill}/SKILL.md não foi instalada em {folder}")
                    return False

        # Verifica suíte ChatGPT instalada em ~/.chatgpt
        chatgpt_sys = Path(tmpdir) / ".chatgpt" / "SYSTEM_INSTRUCTIONS.md"
        if not chatgpt_sys.is_file():
            print("❌ ERRO: Arquivo .chatgpt/SYSTEM_INSTRUCTIONS.md não foi instalado no modo global.")
            return False
    print("✅ install.sh --global executado e testado com sucesso (Claude commands/skills + Antigravity skills + ChatGPT suite).")
    return True


def test_chatgpt_suite_integrity():
    print("🔍 [8.1/8] Validando integridade da Suíte Universal ChatGPT / Web Chats...")
    chatgpt_dir = ROOT_DIR / "chatgpt"
    if not chatgpt_dir.is_dir():
        print("❌ ERRO: Diretório 'chatgpt' não encontrado.")
        return False

    required_files = [
        "README.md",
        "SYSTEM_INSTRUCTIONS.md",
        "custom-gpts/1-appsec-auditor.md",
        "custom-gpts/2-driven-development.md",
        "custom-gpts/3-full-app-validator.md",
        "prompts-condensed/appsec_auditor.md",
        "prompts-condensed/api_security.md",
        "prompts-condensed/tdd_workflow.md",
        "prompts-condensed/full_app_validator.md",
        "prompts-condensed/threat_modeling.md",
    ]

    for req_file in required_files:
        p = chatgpt_dir / req_file
        if not p.is_file():
            print(f"❌ ERRO: Arquivo obrigatório da suíte ChatGPT não encontrado: {req_file}")
            return False
        if len(p.read_text(encoding="utf-8").strip()) < 50:
            print(f"❌ ERRO: Arquivo {req_file} parece vazio ou incompleto.")
            return False

    print("✅ Suíte universal ChatGPT / Web Chats validada com sucesso.")
    return True



def test_sync_scripts_unit():
    print("🔍 [6/6] Executando suíte de testes unitários dos sincronizadores CI/CD...")
    test_file = ROOT_DIR / "tests" / "test_sync_scripts.py"
    res = subprocess.run([sys.executable, "-m", "unittest", str(test_file)], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ ERRO nos testes unitários dos scripts de sync:\n{res.stderr}")
        return False
    print("✅ 12/12 testes unitários dos scripts de sincronização passaram com sucesso.")
    return True


def test_skills_integrity():
    print("🔍 [8/8] Validando integridade das Agent Skills (YAML frontmatter e testes unitários)...")
    skills_dir = ROOT_DIR / "skills"
    if not skills_dir.is_dir():
        print("❌ ERRO: Diretório 'skills' não encontrado.")
        return False

    skill_folders = [d for d in skills_dir.iterdir() if d.is_dir()]
    if not skill_folders:
        print("❌ ERRO: Nenhuma skill encontrada em skills/")
        return False

    for folder in skill_folders:
        skill_md = folder / "SKILL.md"
        if not skill_md.is_file():
            print(f"❌ ERRO: Skill {folder.name} não possui SKILL.md")
            return False

        content = skill_md.read_text(encoding="utf-8")
        if not content.startswith("---"):
            print(f"❌ ERRO: Skill {folder.name}/SKILL.md não possui YAML frontmatter")
            return False

        if "name:" not in content or "description:" not in content:
            print(f"❌ ERRO: Skill {folder.name}/SKILL.md não possui campos obrigatórios 'name' ou 'description'")
            return False

    # Executa testes unitários dos scripts das skills
    for test_file_name in ["test_appsec_auditor.py", "test_driven_development.py", "test_full_app_validator.py"]:
        test_file = ROOT_DIR / "tests" / test_file_name

        if test_file.is_file():
            res = subprocess.run([sys.executable, "-m", "unittest", str(test_file)], capture_output=True, text=True)
            if res.returncode != 0:
                print(f"❌ ERRO no teste unitário {test_file_name}:\n{res.stderr}")
                return False

    print(f"✅ Todas as {len(skill_folders)} skills possuem SKILL.md válido e testes unitários verdes.")
    return True


def test_security_standards_coexistence():
    print(f"🔍 [7/7] Validando coexistência de padrões (OWASP ASVS & OWASP Risk Rating) nos {len(SECURITY_PROMPTS)} prompts de segurança...")
    errors = []
    for rel_path in SECURITY_PROMPTS:
        full_path = PROMPTS_DIR / rel_path
        content = full_path.read_text(encoding="utf-8")
        
        if "OWASP ASVS" not in content and "ASVS" not in content:
            errors.append(f"Prompt {rel_path} não referencia 'OWASP ASVS'")
        
        if "OWASP Risk Rating" not in content and "Risk Rating" not in content:
            errors.append(f"Prompt {rel_path} não referencia 'OWASP Risk Rating Methodology'")

    if errors:
        for err in errors:
            print(f"❌ {err}")
        return False
    print(f"✅ Todos os {len(SECURITY_PROMPTS)} prompts de segurança possuem referências completas a ASVS e Risk Rating.")
    return True


def main():
    print("=================================================================")
    print("  🛡️  Bateria de Testes de Integridade & Qualidade da Suíte")
    print("=================================================================")
    tests = [
        test_prompts_exist,
        test_prompt_structure,
        test_install_script_sync,
        test_readme_links,
        test_installer_execution,
        test_global_installer_execution,
        test_sync_scripts_unit,
        test_security_standards_coexistence,
        test_skills_integrity,
        test_chatgpt_suite_integrity,
    ]
    
    failed = False
    for t in tests:
        if not t():
            failed = True
            break
            
    if failed:
        print("\n❌ FALHA: A suíte de testes encontrou erros.")
        sys.exit(1)
    else:
        print("\n🎉 SUCESSO: Todos os testes de integridade, qualidade e unitários passaram!")
        sys.exit(0)


if __name__ == "__main__":
    main()
