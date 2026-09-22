#!/usr/bin/env python3
"""
Universal Test Runner & Stack Detector for Driven Development Skill.
Detects project test frameworks (pytest, vitest, jest, go, cargo) and provides structured execution results.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def detect_test_framework(root_dir: Path) -> Tuple[str, List[str]]:
    """Inspects root_dir and determines the most appropriate test command."""
    # 1. Node.js Ecosystem
    pkg_json = root_dir / "package.json"
    if pkg_json.is_file():
        try:
            data = json.loads(pkg_json.read_text(encoding="utf-8"))
            scripts = data.get("scripts", {})
            pkg_mgr = "npm"
            if (root_dir / "pnpm-lock.yaml").is_file() and shutil.which("pnpm"):
                pkg_mgr = "pnpm"
            elif (root_dir / "yarn.lock").is_file() and shutil.which("yarn"):
                pkg_mgr = "yarn"
            elif (root_dir / "bun.lockb").is_file() and shutil.which("bun"):
                pkg_mgr = "bun"

            if "test" in scripts:
                return (f"node ({pkg_mgr})", [pkg_mgr, "test"])
        except Exception:
            pass

    # 2. Python Ecosystem
    if (root_dir / "pytest.ini").is_file() or (root_dir / "pyproject.toml").is_file() or (root_dir / "tests").is_dir():
        if shutil.which("pytest"):
            return ("python (pytest)", ["pytest", "tests"])
        return ("python (unittest)", [sys.executable, "-m", "unittest", "discover", "-s", "tests"])

    # 3. Go Ecosystem
    if (root_dir / "go.mod").is_file() and shutil.which("go"):
        return ("go", ["go", "test", "./..."])

    # 4. Rust Ecosystem
    if (root_dir / "Cargo.toml").is_file() and shutil.which("cargo"):
        return ("rust", ["cargo", "test"])

    # Default fallback
    return ("python (unittest)", [sys.executable, "-m", "unittest"])


def parse_test_summary(stdout: str, stderr: str, framework: str) -> Dict[str, Any]:
    """Extracts high-level test counts from stdout/stderr."""
    summary: Dict[str, Any] = {"passed": 0, "failed": 0, "total": 0, "status": "unknown"}
    combined = stdout + "\n" + stderr

    # Pytest pattern: "5 passed, 1 failed in 0.12s"
    pytest_match = re.search(r"(\d+)\s+passed", combined)
    pytest_fail = re.search(r"(\d+)\s+failed", combined)
    if pytest_match or pytest_fail:
        passed = int(pytest_match.group(1)) if pytest_match else 0
        failed = int(pytest_fail.group(1)) if pytest_fail else 0
        summary["passed"] = passed
        summary["failed"] = failed
        summary["total"] = passed + failed
        summary["status"] = "PASSED" if failed == 0 else "FAILED"
        return summary

    # Unittest pattern: "Ran 12 tests in 0.005s\n\nOK" or "FAILED (failures=1)"
    unittest_ran = re.search(r"Ran (\d+) tests?", combined)
    if unittest_ran:
        total = int(unittest_ran.group(1))
        failed = 0
        fail_match = re.search(r"failures=(\d+)", combined)
        err_match = re.search(r"errors=(\d+)", combined)
        if fail_match:
            failed += int(fail_match.group(1))
        if err_match:
            failed += int(err_match.group(1))
        summary["total"] = total
        summary["failed"] = failed
        summary["passed"] = total - failed
        summary["status"] = "PASSED" if failed == 0 and "OK" in combined else "FAILED"
        return summary

    # Jest/Vitest pattern: "Tests:       1 failed, 4 passed, 5 total"
    vitest_match = re.search(r"Tests:\s+(?:(\d+)\s+failed,\s+)?(?:(\d+)\s+passed,\s+)?(\d+)\s+total", combined)
    if vitest_match:
        failed = int(vitest_match.group(1) or 0)
        passed = int(vitest_match.group(2) or 0)
        total = int(vitest_match.group(3) or 0)
        summary["passed"] = passed
        summary["failed"] = failed
        summary["total"] = total
        summary["status"] = "PASSED" if failed == 0 else "FAILED"
        return summary

    return summary


def run_tests(
    cmd: List[str],
    root_dir: Path,
    framework: str,
    timeout_sec: int = 180,
) -> Dict[str, Any]:
    """Executes the test command and captures output."""
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(root_dir),
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
        stdout = proc.stdout
        stderr = proc.stderr
        exit_code = proc.returncode
    except subprocess.TimeoutExpired:
        return {
            "framework": framework,
            "command": " ".join(cmd),
            "exit_code": 124,
            "status": "TIMEOUT",
            "error": f"Test execution timed out after {timeout_sec} seconds.",
            "stdout": "",
            "stderr": "",
            "summary": {"passed": 0, "failed": 1, "total": 1, "status": "FAILED"},
        }
    except FileNotFoundError as e:
        return {
            "framework": framework,
            "command": " ".join(cmd),
            "exit_code": 127,
            "status": "NOT_FOUND",
            "error": f"Command not found: {e}",
            "stdout": "",
            "stderr": "",
            "summary": {"passed": 0, "failed": 1, "total": 1, "status": "FAILED"},
        }

    summary = parse_test_summary(stdout, stderr, framework)
    if summary["status"] == "unknown":
        summary["status"] = "PASSED" if exit_code == 0 else "FAILED"

    return {
        "framework": framework,
        "command": " ".join(cmd),
        "exit_code": exit_code,
        "status": "PASSED" if exit_code == 0 else "FAILED",
        "stdout": stdout,
        "stderr": stderr,
        "summary": summary,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Universal Test Runner for Driven Development")
    parser.add_argument("--dir", default=".", help="Root directory of the project (default: .)")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--timeout", type=int, default=180, help="Execution timeout in seconds")

    args = parser.parse_args()
    root_dir = Path(args.dir).resolve()

    framework, cmd = detect_test_framework(root_dir)
    result = run_tests(cmd, root_dir, framework, timeout_sec=args.timeout)

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        status_emoji = "✅" if result["status"] == "PASSED" else "❌"
        print(f"=================================================================")
        print(f"  🧪 Driven Development Test Runner — {framework}")
        print(f"=================================================================")
        print(f"Command : {result['command']}")
        print(f"Status  : {status_emoji} {result['status']} (Exit code: {result['exit_code']})")
        summary = result.get("summary", {})
        if summary.get("total", 0) > 0:
            print(f"Metrics : {summary.get('passed', 0)} passed, {summary.get('failed', 0)} failed, {summary.get('total', 0)} total")
        print(f"-----------------------------------------------------------------")
        if result["stdout"]:
            print(result["stdout"].rstrip())
        if result["stderr"]:
            print(result["stderr"].rstrip())

    return 0 if result["status"] == "PASSED" else 1


if __name__ == "__main__":
    sys.exit(main())
