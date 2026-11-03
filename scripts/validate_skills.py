#!/usr/bin/env python3
"""Validate skill discovery metadata and local manifest links."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
FRONTMATTER_PATTERN = re.compile(r"\A---\n(.*?)\n---(?:\n|\Z)", re.DOTALL)
MARKDOWN_LINK_PATTERN = re.compile(r"(?<!!)\[[^]]*]\(([^)]+)\)")
EVALS_FILE = Path("evals/evals.json")


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


def validate_evals(evals_file: Path) -> tuple[list[str], int]:
    relative_path = evals_file.relative_to(ROOT)
    try:
        data = json.loads(evals_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"{relative_path}: unable to read valid JSON ({error})"], 0

    errors: list[str] = []
    if not isinstance(data, dict):
        return [f"{relative_path}: top-level value must be an object"], 0
    if data.get("skill_name") != evals_file.parents[1].name:
        errors.append(
            f"{relative_path}: skill_name must match "
            f"{evals_file.parents[1].name!r}"
        )

    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        return errors + [f"{relative_path}: evals must be a non-empty array"], 0

    seen_ids: set[int] = set()
    required_strings = ("name", "prompt", "expected_output")
    for index, case in enumerate(evals):
        location = f"{relative_path}: evals[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{location} must be an object")
            continue

        case_id = case.get("id")
        if type(case_id) is not int or case_id < 1:
            errors.append(f"{location}.id must be a positive integer")
        elif case_id in seen_ids:
            errors.append(f"{location}.id {case_id} is duplicated")
        else:
            seen_ids.add(case_id)

        for key in required_strings:
            if not isinstance(case.get(key), str) or not case[key].strip():
                errors.append(f"{location}.{key} must be a non-empty string")

        files = case.get("files", [])
        if not isinstance(files, list) or any(
            not isinstance(file_path, str) for file_path in files
        ):
            errors.append(f"{location}.files must be an array of strings")

    return errors, len(evals)


def main() -> int:
    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        print("No skill manifests found.", file=sys.stderr)
        return 1

    errors = [
        error for skill_file in skill_files for error in validate_skill(skill_file)
    ]
    evals_files = sorted(SKILLS_DIR.glob(f"*/{EVALS_FILE.as_posix()}"))
    eval_count = 0
    for evals_file in evals_files:
        eval_errors, count = validate_evals(evals_file)
        errors.extend(eval_errors)
        eval_count += count

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"Validated {len(skill_files)} skill manifests "
        f"and {eval_count} regression prompts."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())