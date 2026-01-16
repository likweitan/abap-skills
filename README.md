# ABAP Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A collection of Claude Code skills for SAP ABAP development, including Fiori URL generation and Clean ABAP code analysis.

## Skills

### SAP Fiori Apps Reference Library

Generate SAP Fiori Launchpad (FLP) URLs by looking up app information and constructing the correct parameters.

**Features:**
- Smart Lookup: Finds apps by name (fuzzy search) in `AppList.json`
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

### Clean ABAP

Check ABAP code for compliance with Clean ABAP principles, based on Robert C. Martin's Clean Code adapted for ABAP.

**Features:**
- Comprehensive code analysis across 15 categories (Names, Language, Constants, Variables, Tables, Strings, Booleans, Conditions, Ifs, Classes, Methods, Error Handling, Comments, Formatting, Testing)
- Priority-based issue reporting (Critical, Major, Minor)
- Actionable recommendations with code examples
- Reference to complete Clean ABAP style guide

**Example Prompts:**
> "Check this ABAP code for clean code compliance"

> "Review my ABAP method for best practices"

> "Is this clean ABAP?"

**Check Categories:**
- **Names**: Descriptive naming, no Hungarian notation, snake_case
- **Language**: Modern syntax, functional constructs, no obsolete elements
- **Methods**: Small methods, few parameters, RETURNING over EXPORTING
- **Error Handling**: Exceptions over return codes, proper exception classes
- **And more...**

## Repository Structure

```
skills/
├── sap-fiori-apps-reference/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── fiori-url-generator.js
│   │   ├── fiori-url-generator.py
│   │   └── test.py
│   └── references/
│       └── AppList.json
└── clean-abap/
    ├── SKILL.md
    └── references/
        ├── CleanABAP.md
        ├── checklist.md
        └── quick-reference.md
```

## Prerequisites

- **Node.js** or **Python** for the Fiori URL generator scripts
- The `AppList.json` file for Fiori app lookups

## License

MIT
