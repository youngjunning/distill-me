#!/usr/bin/env python3
"""Validate the standalone Distill Me skill contract."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


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
