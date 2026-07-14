#!/usr/bin/env python3
"""Validate skill discovery metadata and local manifest links."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
FRONTMATTER_PATTERN = re.compile(r"\A---\n(.*?)\n---(?:\n|\Z)", re.DOTALL)
MARKDOWN_LINK_PATTERN = re.compile(r"(?<!!)\[[^]]*]\(([^)]+)\)")


def frontmatter_value(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", frontmatter, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().strip("\"'")


def validate_skill(skill_file: Path) -> list[str]:
    errors: list[str] = []
    relative_path = skill_file.relative_to(ROOT)
    text = skill_file.read_text(encoding="utf-8")
    frontmatter_match = FRONTMATTER_PATTERN.match(text)

    if not frontmatter_match:
        return [f"{relative_path}: missing YAML frontmatter"]

    frontmatter = frontmatter_match.group(1)
    name = frontmatter_value(frontmatter, "name")
    description = frontmatter_value(frontmatter, "description")

    if not name:
        errors.append(f"{relative_path}: missing frontmatter name")
    elif name != skill_file.parent.name:
        errors.append(
            f"{relative_path}: name {name!r} must match folder "
            f"{skill_file.parent.name!r}"
        )

    if not description:
        errors.append(f"{relative_path}: missing frontmatter description")

    if "@skills/" in text:
        errors.append(
            f"{relative_path}: use paths relative to SKILL.md instead of @skills/"
        )

    for raw_target in MARKDOWN_LINK_PATTERN.findall(text):
        target = unquote(raw_target.split("#", 1)[0].strip())
        if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
            continue
        if not (skill_file.parent / target).resolve().exists():
            errors.append(f"{relative_path}: broken local link {raw_target!r}")

    return errors


def main() -> int:
    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        print("No skill manifests found.", file=sys.stderr)
        return 1

    errors = [
        error for skill_file in skill_files for error in validate_skill(skill_file)
    ]
    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(skill_files)} skill manifests.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())