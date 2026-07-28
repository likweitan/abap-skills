# Contributing to ABAP Skills

Thank you for helping improve the ABAP skills collection. Contributions can add a new skill, improve an existing skill or reference, fix documentation, or strengthen repository tooling.

## Before You Start

- Search existing issues and pull requests to avoid duplicate work.
- Open an issue before making a large or cross-cutting change so the approach can be discussed.
- Keep each pull request focused on one topic.
- Do not include confidential, customer-specific, or proprietary SAP system information.

## Development Setup

1. Fork and clone the repository.
2. Create a branch from `main`.
3. Install [uv](https://docs.astral.sh/uv/getting-started/installation/).
4. Make and validate your changes.

The repository validator has no project dependencies and can be run directly with uv:

```bash
uv run python scripts/validate_skills.py
```

## Adding a Skill

Create a lowercase, hyphen-separated directory under `skills/` with a `SKILL.md` manifest:

```text
skills/
└── example-skill/
    ├── SKILL.md
    └── references/
        └── quick-reference.md
```

Every `SKILL.md` must begin with YAML frontmatter:

```yaml
---
name: example-skill
description: Explain what the skill does and the user requests that should trigger it.
---
```

Follow these requirements:

- Make `name` exactly match the skill directory name.
- Write a specific `description` that states the capability, intended use, and useful trigger phrases.
- Give the skill clear, actionable instructions rather than general background alone.
- Put substantial supporting material in a `references/` directory when it helps keep the manifest focused.
- Link local files relative to `SKILL.md`, for example `[Quick reference](references/quick-reference.md)`.
- Do not use repository-root aliases such as `@skills/` in manifests.
- Add the skill to the catalog in [README.md](README.md), keeping the directory slug and description consistent with its frontmatter.

Use an existing neighboring skill as a structural example, but tailor the workflow and guidance to the new topic.

## Updating Existing Content

- Preserve the skill's scope unless the pull request intentionally changes it.
- Keep commands and ABAP examples executable and internally consistent.
- Prefer authoritative SAP documentation and primary sources for technical claims.
- Update nearby references and README catalog text when behavior or scope changes.
- Avoid unrelated formatting or wording changes in the same pull request.

## Validation

Run the validator before submitting a pull request:

```bash
uv run python scripts/validate_skills.py
```

It checks that each skill has valid frontmatter, that its name matches its directory, and that local Markdown links resolve. GitHub Actions runs the same command for changes under `skills/` and to the validation tooling.

Also review rendered Markdown and run any tests supplied by scripts or tooling you changed.

## Pull Requests

In the pull request description:

- Explain the problem and the proposed change.
- Identify the skills and references affected.
- Include the validation commands you ran and their results.
- Link related issues when applicable.
- Call out new external sources, generated assets, or large data files.

By contributing, you agree that your changes are licensed under the repository's [MIT License](LICENSE).
