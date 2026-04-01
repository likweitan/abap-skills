# ABAP Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A collection of Claude Code skills for SAP ABAP development, including Fiori URL generation and ABAP code analysis with [abaplint](https://github.com/abaplint/abaplint).

## Installation

Note: Installation differs by platform.

### Claude Code

Clone the repository and copy the skills to your Claude Code skills directory:

```bash
git clone https://github.com/likweitan/abap-skills.git
cp -r abap-skills/skills/* ~/.claude/skills/
```

Or install a single skill:

```bash
# Example: Install only the abap skill
cp -r abap-skills/skills/abap ~/.claude/skills/
```

After installation, restart Claude Code to load the new skills.

### OpenCode

Tell OpenCode:

```
Fetch and follow instructions from https://raw.githubusercontent.com/likweitan/abap-skills/refs/heads/main/.opencode/INSTALL.md
```

**Detailed docs:** [docs/README.opencode.md](docs/README.opencode.md)

## Skills

### SAP Fiori Apps Reference Library

Generate SAP Fiori Launchpad (FLP) URLs by looking up app information and constructing the correct parameters.

**Features:**

- Smart Lookup: Finds apps by name (fuzzy search) in `AppList.json`
  - _Source: [SAP Fiori Apps Library](https://pr.alm.me.sap.com/launchpad#FALApp-display&/apps)_
- Automatic Construction: Builds standard FLP URLs with `sap-client` and `sap-language`
- Language Support: Toggle between EN, DE, FR, etc.
- Intelligent Suggestions: Suggests similar apps if an exact match isn't found

**Example Prompts:**

> "Generate URL for Create Maintenance Request app with base URL https://myserver.com:44300 and client 100"

> "Find apps related to 'Workflow'"

**URL Format:**

```
{BASE_URL}/sap/bc/ui2/flp?sap-client={CLIENT}&sap-language={LANGUAGE}#{SEMANTIC_OBJECT}-{ACTION}
```

### Released ABAP Classes

Quick reference for finding released ABAP classes available in ABAP Cloud Development (SAP BTP ABAP Environment).

**Features:**

- Comprehensive catalog of 50+ released ABAP classes organized by category
- Ready-to-use code examples for common use cases
- Covers: Console, UUID, Time/Date, Email, JSON/XML, HTTP, RAP, String Processing, Random Numbers, Regex, Unit Testing, Parallel Processing, Application Logs, PDF Rendering, and more

**Example Prompts:**

> "What is the released class for sending email?"

> "Give me the class for getting time and date in UTC format"

> "How do I generate a UUID in ABAP Cloud?"

> "Show me classes for JSON processing"

**Common Categories:**

- **Console Output**: `IF_OO_ADT_CLASSRUN`, `CL_DEMO_CLASSRUN`
- **Email**: `CL_BCS_MAIL_MESSAGE`
- **UUID**: `CL_SYSTEM_UUID`, `XCO_CP_UUID`
- **Time & Date**: `CL_ABAP_CONTEXT_INFO`, `XCO_CP_TIME`, `CL_ABAP_UTCLONG`
- **JSON/XML**: `XCO_CP_JSON`, `/UI2/CL_JSON`, `CL_SXML_*`
- **HTTP**: `CL_WEB_HTTP_CLIENT_MANAGER`, `CL_HTTP_DESTINATION_PROVIDER`
- **RAP**: `CL_ABAP_BEHV_AUX`, `CL_ABAP_BEHAVIOR_HANDLER`

### ATC Cloudification Repository

Configure ATC Cloud Readiness and Clean Core checks using the [SAP Cloudification Repository](https://github.com/SAP/abap-atc-cr-cv-s4hc) for Released APIs.

**Features:**

- Configuration guidance for SAP Cloud ERP and SAP Cloud ERP Private
- JSON file URL reference for all available versions (Latest, PCE2022–PCE2025)
- Required SAP Notes checklist for Cloud Readiness and Clean Core setup
- Links to the Cloudification API Viewer for interactive browsing
- Support for new Clean Core checks (Usage of APIs, Allowed Enhancement Technologies)

**Example Prompts:**

> "Configure ATC cloud readiness check for SAP Cloud ERP"

> "Which JSON file do I use for Cloud ERP Private 2025 FPS00?"

> "Set up clean core ATC check variant"

> "Show me the URL for the cloudification repository"

### ABAP

Check and improve ABAP code quality using [abaplint](https://github.com/abaplint/abaplint) and Clean ABAP principles.

**Features:**

- Automated static analysis via [abaplint](https://github.com/abaplint/abaplint) CLI for syntax, type, and rule checking
- Starter configurations for On-Premise, Steampunk/BTP, and HANA compatibility
- Comprehensive Clean ABAP review across 15 categories (Names, Language, Constants, Variables, Tables, Strings, Booleans, Conditions, Ifs, Classes, Methods, Error Handling, Comments, Formatting, Testing)
- Priority-based issue reporting (Critical, Major, Minor)
- Actionable recommendations with code examples

**Example Prompts:**

> "Run abaplint on my ABAP project"

> "Configure abaplint for my on-premise system"

> "Check this ABAP code for clean code compliance"

> "Review my ABAP method for best practices"

**Check Categories:**

- **abaplint**: Syntax errors, type checking, parser errors, DDIC checks, and [configurable rules](https://rules.abaplint.org/)
- **Names**: Descriptive naming, no Hungarian notation, snake_case
- **Language**: Modern syntax, functional constructs, no obsolete elements
- **Methods**: Small methods, few parameters, RETURNING over EXPORTING
- **Error Handling**: Exceptions over return codes, proper exception classes
- **And more...**

## Repository Structure

```
skills/
├── atc-cloudification/
│   ├── SKILL.md
│   └── references/
│       └── quick-reference.md
├── sap-fiori-apps-reference/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── fiori-url-generator.js
│   │   ├── fiori-url-generator.py
│   │   └── test.py
│   └── references/
│       └── AppList.json
├── released-abap-classes/
│   ├── SKILL.md
│   └── references/
│       └── Released_ABAP_Classes.md
└── abap/
    ├── SKILL.md
    └── references/
        ├── abaplint.md
        ├── CleanABAP.md
        ├── checklist.md
        └── quick-reference.md
```

## Prerequisites

- **Node.js** (v16+) for the Fiori URL generator scripts and [abaplint](https://github.com/abaplint/abaplint) (`npm install @abaplint/cli -g`)
- The `AppList.json` file for Fiori app lookups

## License

MIT
