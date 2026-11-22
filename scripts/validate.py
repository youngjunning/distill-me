#!/usr/bin/env python3
"""Validate the standalone Distill Me skill contract."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def section(text: str, start: str, end: str) -> str:
    if start not in text or end not in text:
        return ""
    return text.split(start, 1)[1].split(end, 1)[0]


def main() -> None:
    errors: list[str] = []
    required = [
        "SKILL.md",
        "README.md",
        "LICENSE",
        "references/automatic-distillation.md",
        "references/automatic-gate.md",
        "references/host-integration.md",
        "workbench/package.json",
    ]
    for relative in required:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    integration = (ROOT / "references/host-integration.md").read_text(encoding="utf-8")
    workbench_ignore = (ROOT / "workbench/.gitignore").read_text(encoding="utf-8").splitlines()

    for pattern, label in [
        (r"^name: distill-me$", "skill name"),
        (r"^description: .+$", "skill description"),
        (r"^  author: 杨俊宁$", "author metadata"),
        (r"^  email: luozhu2021@gmail\.com$", "email metadata"),
    ]:
        if not re.search(pattern, skill, re.MULTILINE):
            errors.append(f"missing or invalid {label}")

    old_source = "github.com/youngjunning/joyally-skills/tree/main/skills/productivity/distill-me"
    if old_source in readme:
        errors.append("README still points to the former monorepo path")
    if "https://github.com/youngjunning/distill-me" not in readme:
        errors.append("README is missing the standalone repository URL")

    for expected in (
        "### 第一步 A：Codex 安装",
        "### 第一步 B：千问办公安装",
        "~/.codex/AGENTS.md",
        "~/.qwenworkcn/awareness/main/AGENTS.md",
    ):
        if expected not in readme:
            errors.append(f"README is missing host-specific install contract: {expected}")

    codex_install = section(readme, "### 第一步 A：Codex 安装", "### 第一步 B：千问办公安装")
    qwen_install = section(readme, "### 第一步 B：千问办公安装", "### 第二步：初始化本地工作台")
    codex_update = section(readme, "### 在 Codex 更新 Skill", "### 在千问办公更新 Skill")
    qwen_update = section(readme, "### 在千问办公更新 Skill", "## 本地与隐私")

    for label, content in (("Codex install", codex_install), ("Codex update", codex_update)):
        if "~/.codex/AGENTS.md" not in content:
            errors.append(f"{label} is missing the Codex AGENTS.md path")
        if "~/.qwenworkcn/" in content:
            errors.append(f"{label} contains QwenWork-specific paths")

    for label, content in (("QwenWork install", qwen_install), ("QwenWork update", qwen_update)):
        for expected in (
            "~/.qwenworkcn/awareness/main/AGENTS.md",
            "~/.qwenworkcn/skills",
            "~/.agents/skills",
        ):
            if expected not in content:
                errors.append(f"{label} is missing QwenWork contract: {expected}")
        if "~/.codex/AGENTS.md" in content:
            errors.append(f"{label} contains the Codex AGENTS.md path")

    for expected in ("~/.codex/AGENTS.md", "~/.qwenworkcn/awareness/main/AGENTS.md"):
        if expected not in skill or expected not in integration:
            errors.append(f"skill contract is missing host instruction path: {expected}")

    for marker in ("<!-- BEGIN distill-me -->", "<!-- END distill-me -->"):
        if integration.count(marker) != 1:
            errors.append(f"host integration marker must appear once: {marker}")

    for ignored in (".next/", "node_modules/", "tsconfig.tsbuildinfo", "data/twin.json"):
        if ignored not in workbench_ignore:
            errors.append(f"workbench must ignore local artifact: {ignored}")

    if errors:
        raise SystemExit("\n".join(errors))
    print("Validated standalone Distill Me skill contract.")


if __name__ == "__main__":
    main()
