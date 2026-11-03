<div align="center">

<img width="112" height="112" alt="image" src="https://github.com/user-attachments/assets/b51bf775-abfe-44ab-afb8-def90211b3c3" />

# ABAP Skills

**Agent Skills for ABAP**

Clean ABAP · CDS Views · BTP Diagram Generator

[![skills.sh](https://skills.sh/b/likweitan/abap-skills)](https://skills.sh/likweitan/abap-skills)

</div>

A collection of AI agent skills for SAP ABAP development — RAP, CDS, OData, ABAP Cloud, testing, authorization, eventing, migration, and more. Small, composable, and model-agnostic: adapt them freely.

## Installation

**Skills CLI (recommended)** — works with GitHub Copilot, Claude Code, Cursor, Codex, OpenCode, and other compatible agents:

```bash
npx skills add likweitan/abap-skills                # choose skills interactively
npx skills add likweitan/abap-skills --skill abap   # install a single skill
npx skills add likweitan/abap-skills --global       # make skills available across projects
npx skills add likweitan/abap-skills --list         # preview without installing
```

<details>
<summary><strong>Manual / other agents</strong></summary>

**Claude Code** — copy skills into your skills directory, then restart Claude Code:

```bash
git clone https://github.com/likweitan/abap-skills.git
cp -r abap-skills/skills/* ~/.claude/skills/   # or a single folder, e.g. skills/abap
```

**OpenCode** — tell OpenCode: `Fetch and follow instructions from https://raw.githubusercontent.com/likweitan/abap-skills/refs/heads/main/.opencode/INSTALL.md` ([docs](docs/README.opencode.md))

**GitHub Copilot in VS Code** — see [docs/README.github-copilot-vscode.md](docs/README.github-copilot-vscode.md)

</details>

## Skills

| Skill                                                      | Covers                                                                                                                      | Example prompt                                                 |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| [abap](skills/abap/)                                       | abaplint static analysis + Clean ABAP review (15 categories, prioritized findings)                                          | "Check this ABAP code for Clean ABAP compliance"               |
| [abap-unit-testing](skills/abap-unit-testing/)             | Test classes, assertions, test doubles, CDS/OSQL test environments, RAP BO doubles                                          | "Test a CDS view entity using the CDS test environment"        |
| [abap-cloud](skills/abap-cloud/)                           | Clean core levels A–D, ABAP Cloud restrictions, wrapper patterns, released API discovery                                    | "What replaces AUTHORITY-CHECK in ABAP Cloud?"                 |
| [abap-cloud-migration](skills/abap-cloud-migration/)       | ATC Cloud Readiness, unreleased → released API replacements, migration checklist                                            | "Released replacement for GUID_CREATE and NUMBER_GET_NEXT?"    |
| [atc-cloudification](skills/atc-cloudification/)           | ATC Cloud Readiness / Clean Core checks via the [SAP Cloudification Repository](https://github.com/SAP/abap-atc-cr-cv-s4hc) | "Which JSON file for Cloud ERP Private 2025 FPS00?"            |
| [released-abap-classes](skills/released-abap-classes/)     | 50+ released classes (UUID, time, email, JSON, HTTP, RAP, …) with examples                                                  | "What is the released class for sending email?"                |
| [cds-view-entities](skills/cds-view-entities/)             | Root/child/projection views, associations, annotations, access controls, metadata extensions                                | "Add UI annotations for a Fiori list report"                   |
| [abap-sql-amdp](skills/abap-sql-amdp/)                     | Modern ABAP SQL, window functions, CTEs, AMDP procedures and table functions                                                | "Rank results with window functions in ABAP SQL"               |
| [rap](skills/rap/)                                         | BDL, EML, managed/unmanaged BOs, draft, actions, validations, determinations                                                | "Create a managed RAP BO with draft handling"                  |
| [rap-business-events](skills/rap-business-events/)         | Event definitions, `RAISE ENTITY EVENT`, event bindings, SAP Event Mesh                                                     | "Bind a RAP event to SAP Event Mesh"                           |
| [odata](skills/odata/)                                     | RAP-based V4/V2 and SEGW V2 services, bindings, annotations, external consumption                                           | "Expose my RAP BO as an OData V4 service"                      |
| [authorization-iam](skills/authorization-iam/)             | Auth checks, CDS DCL, IAM apps/catalogs/roles, RAP instance/global authorization                                            | "Implement instance authorization in my RAP BO"                |
| [badi-enhancement](skills/badi-enhancement/)               | New/classic BAdIs, filters, fallback classes, enhancement spots, key user extensibility                                     | "Create a custom BAdI with filter-based implementations"       |
| [abapgit](skills/abapgit/)                                 | Repo setup, `.abapgit.xml`, branching, transport vs. git, abaplint CI                                                       | "Set up abapGit and clone a repository"                        |
| [btp-abap-environment](skills/btp-abap-environment/)       | Steampunk provisioning, ADT connectivity, communication arrangements, IAM                                                   | "Configure a communication arrangement for outbound HTTP"      |
| [btp-diagram-generator](skills/btp-diagram-generator/)     | SAP BTP solution diagrams as draw.io files per the [official guidelines](https://sap.github.io/btp-solution-diagrams/)      | "Draw an L2 BTP architecture with CAP, HANA Cloud and S/4HANA" |
| [sap-fiori-url-generator](skills/sap-fiori-url-generator/) | Fiori Launchpad URLs from app names via fuzzy lookup in `AppList.json`                                                      | "Generate a URL for the Create Maintenance Request app"        |

Each skill lives in `skills/<name>/` with a `SKILL.md` and optional `references/` and `scripts/`. See [SKILLS_INDEX.md](SKILLS_INDEX.md) for a categorized index.

## Prerequisites

- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** — validation and BTP diagram generator scripts
- **Node.js** (v16+) — Fiori URL generator and [abaplint](https://github.com/abaplint/abaplint) (`npm install @abaplint/cli -g`)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Before submitting a skill change, run:

```bash
uv run python scripts/validate_skills.py
```

## License

MIT
