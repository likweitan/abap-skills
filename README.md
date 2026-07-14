# ABAP Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A collection of Claude Code skills for SAP ABAP development — covering RAP, CDS, OData, ABAP Cloud, testing, authorization, eventing, migration, and more.

## Table of Contents

- [Installation](#installation)
- [Skills](#skills)
  - [SAP Fiori Apps Reference Library](#sap-fiori-apps-reference-library)
  - [Released ABAP Classes](#released-abap-classes)
  - [ATC Cloudification Repository](#atc-cloudification-repository)
  - [ABAP](#abap)
  - [Clean ABAP](#clean-abap)
  - [RAP (RESTful ABAP Programming Model)](#rap-restful-abap-programming-model)
  - [CDS View Entities](#cds-view-entities)
  - [ABAP Unit Testing](#abap-unit-testing)
  - [ABAP Cloud / Clean Core](#abap-cloud--clean-core)
  - [abapGit Workflows](#abapgit-workflows)
  - [OData Service Development](#odata-service-development)
  - [ABAP SQL & AMDP](#abap-sql--amdp)
  - [BAdI & Enhancement Framework](#badi--enhancement-framework)
  - [SAP BTP ABAP Environment](#sap-btp-abap-environment)
  - [Authorization & IAM](#authorization--iam)
  - [RAP Business Events & Enterprise Eventing](#rap-business-events--enterprise-eventing)
  - [ABAP Cloud Migration Patterns](#abap-cloud-migration-patterns)
  - [BTP Diagram Generator](#btp-diagram-generator)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [License](#license)

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

### GitHub Copilot in VS Code

Install GitHub Copilot in VS Code, clone this repository locally, and create a reusable prompt file that points Copilot Chat to the ABAP skill references.

**Detailed docs:** [docs/README.github-copilot-vscode.md](docs/README.github-copilot-vscode.md)

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

### Clean ABAP

Review ABAP code for compliance with Clean ABAP principles, based on the Clean ABAP style guide adapted from Robert C. Martin's Clean Code.

**Features:**

- Categorizes issues across 15 Clean ABAP sections (Names, Language, Constants, Variables, Tables, Strings, Booleans, Conditions, Ifs, Classes, Methods, Error Handling, Comments, Formatting, Testing)
- Prioritizes findings by severity (Critical, Major, Minor)
- Actionable recommendations with anti-pattern and clean code examples
- References the official Clean ABAP style guide
- Includes review checklist and quick-reference patterns

**Example Prompts:**

> "Check this ABAP code for Clean ABAP compliance"

> "Review my ABAP for clean code best practices"

> "Is this ABAP method following Clean ABAP guidelines?"

### RAP (RESTful ABAP Programming Model)

Build transactional applications using RAP in ABAP Cloud — behavior definitions (BDL), EML statements, managed/unmanaged BOs, draft handling, actions, validations, determinations, side effects, and business events.

**Features:**

- Full BDL syntax reference for behavior definitions (managed, unmanaged, projection)
- EML quick reference for CRUD, actions, deep create, and draft operations
- Handler and saver class implementation patterns
- Draft handling with `with draft` and collaborative draft support
- RAP save sequence and derived type components (`%tky`, `%cid`, `%control`, etc.)

**Example Prompts:**

> "Create a managed RAP business object with draft handling"

> "Write EML to execute an action on a RAP BO"

> "Add a validation and determination to my behavior definition"

### CDS View Entities

Build semantic data models using ABAP CDS view entities — data modeling, annotations, associations, compositions, access controls, expressions, input parameters, and metadata extensions.

**Features:**

- Complete CDS syntax for root, child, and projection view entities
- Associations, compositions, and join patterns with ABAP SQL path expressions
- Built-in functions (string, date/time, aggregate), CASE expressions, and input parameters
- UI, semantics, and access control annotations including metadata extensions
- Data model patterns for RAP composition trees and admin fields

**Example Prompts:**

> "Create a CDS root view entity with a composition to a child entity"

> "Add UI annotations and a metadata extension for a Fiori list report"

> "Define a CDS access control with PFCG authorization checks"

### ABAP Unit Testing

Write effective ABAP Unit tests — test class setup, assertions, test doubles, mocking frameworks, and specialized test environments for CDS views, SQL-dependent code, and RAP business objects.

**Features:**

- Complete `CL_ABAP_UNIT_ASSERT` assertion method reference
- Dependency injection and manual mock (test double) patterns
- CDS test environment (`cl_cds_test_environment`) for testing CDS views with stubbed data
- OSQL test environment (`cl_osql_test_environment`) for SQL-dependent code
- RAP BO test doubles (transactional buffer doubles and mock EML APIs)

**Example Prompts:**

> "Write a unit test class with a mock dependency for my ABAP class"

> "Test a CDS view entity using the CDS test environment"

> "Create RAP BO test doubles for testing EML operations"

### ABAP Cloud / Clean Core

Develop with the ABAP Cloud programming model — 3-tier extensibility model, ABAP for Cloud Development restrictions, wrapper patterns for unreleased APIs, released API discovery, and clean core principles.

**Features:**

- 3-tier extensibility model (Key User, Developer, Classic) with tier selection guidance
- ABAP for Cloud Development restrictions and prohibited language constructs
- Wrapper pattern for exposing unreleased APIs via released interfaces
- Common unreleased-to-released API replacement table
- Released API discovery methods (ADT search, Cloudification Viewer, ATC checks)

**Example Prompts:**

> "What is the released API replacement for AUTHORITY-CHECK in ABAP Cloud?"

> "Create a wrapper class for an unreleased function module"

> "Explain the 3-tier extensibility model and when to use each tier"

### abapGit Workflows

Manage ABAP development objects in Git repositories using abapGit — repository setup, cloning, branching strategies, `.abapgit.xml` configuration, transport-vs-git workflows, and CI/CD integration with abaplint.

**Features:**

- Setup instructions for abapGit standalone (on-premise) and ADT (BTP)
- Core operations: clone, push, pull with step-by-step guidance
- `.abapgit.xml` configuration reference (folder logic, ignore patterns, requirements)
- Branching strategy (trunk-based) and hybrid transport+git workflows
- CI/CD integration with abaplint GitHub Actions

**Example Prompts:**

> "Set up abapGit and clone a repository into my SAP system"

> "What branching strategy should I use for ABAP development with abapGit?"

> "Configure abaplint CI for my ABAP Git repository"

### OData Service Development

Create and consume OData services in ABAP — RAP-based (V4/V2) and SEGW-based (V2) approaches, service definitions and bindings, OData annotations for Fiori, external OData consumption, and troubleshooting.

**Features:**

- RAP-based OData service architecture (CDS → BDEF → Service Definition → Service Binding)
- OData V4 vs V2 comparison and service binding types
- SEGW-based classic OData V2 service development
- External OData consumption using HTTP client and OData client proxy
- OData/Fiori annotation patterns and error troubleshooting

**Example Prompts:**

> "Expose my RAP business object as an OData V4 service"

> "Consume an external OData service from ABAP Cloud"

> "What's the difference between OData V4 and V2 service bindings?"

### ABAP SQL & AMDP

Write modern ABAP SQL and ABAP Managed Database Procedures — inline declarations, window functions, CTEs, aggregate expressions, set operations, PRIVILEGED ACCESS, and AMDP table functions.

**Features:**

- Modern ABAP SQL syntax: inline declarations, expressions, CASE, CAST
- Window functions (ROW_NUMBER, RANK, LAG/LEAD, running totals)
- Common Table Expressions (CTE) with `WITH` clause
- AMDP class structure, procedures, and CDS table functions via SQLScript
- Built-in SQL functions reference (string, numeric, date/time, conversion, aggregate)

**Example Prompts:**

> "Write an ABAP SQL query using window functions to rank results"

> "Create an AMDP table function for a CDS view"

> "How do I use a Common Table Expression (CTE) in ABAP SQL?"

### BAdI & Enhancement Framework

Extend SAP standard functionality using BAdIs and the enhancement framework — new and classic BAdI frameworks, filter-based BAdIs, fallback classes, enhancement spots, and key user extensibility.

**Features:**

- New vs. classic BAdI framework comparison with ABAP Cloud compatibility
- Step-by-step BAdI creation (enhancement spot, interface, definition, fallback class)
- BAdI implementation and discovery techniques (ADT search, breakpoint on GET BADI)
- Enhancement spots and sections (explicit points, replaceable code sections)
- Key user extensibility (custom fields, custom logic, no-code extensions)

**Example Prompts:**

> "Create a custom BAdI with filter-based implementations"

> "How do I find and implement an existing SAP BAdI?"

> "What's the difference between new and classic BAdI frameworks?"

### SAP BTP ABAP Environment

Set up and develop in the SAP BTP ABAP Environment (Steampunk) — service instance creation, ADT connectivity, communication arrangements, software components, IAM setup, and project scaffolding.

**Features:**

- Service instance provisioning with JSON parameter configuration
- ADT connectivity setup (ABAP Cloud Project, service key authentication)
- Communication management (scenarios, systems, arrangements) for inbound/outbound integration
- Software component and package structure management
- IAM setup (IAM apps, business catalogs, business roles) and useful Fiori apps reference

**Example Prompts:**

> "Set up a new BTP ABAP Environment instance and connect ADT"

> "Configure a communication arrangement for outbound HTTP calls"

> "Create the package structure for my first RAP project on BTP"

### Authorization & IAM

Implement authorization checks and identity/access management — authorization objects, CDS access controls (DCL), IAM apps, business catalogs, business roles, PFCG roles, and RAP instance/global authorization.

**Features:**

- ABAP Cloud authorization via `CL_ABAP_AUTHORIZATION` and on-premise `AUTHORITY-CHECK`
- CDS access control (DCL) with `pfcg_auth`, inheritance, and user-based restrictions
- IAM model for ABAP Cloud (IAM App → Business Catalog → Business Role)
- RAP instance and global authorization handler implementations
- PFCG role management, composite roles, and restriction types

**Example Prompts:**

> "Implement instance authorization in my RAP business object"

> "Create a CDS access control with PFCG authorization checks"

> "Set up IAM apps and business catalogs for my OData service on BTP"

### RAP Business Events & Enterprise Eventing

Implement event-driven patterns using RAP business events and SAP Event Mesh — event definitions in BDEFs, raising events from handler/saver methods, event bindings, and event consumption patterns.

**Features:**

- Event definition in behavior definitions with CDS abstract entity parameters
- Raising events from handler and saver methods via `RAISE ENTITY EVENT`
- Enterprise event enablement with event bindings and SAP Event Mesh integration
- Local and external event consumption patterns
- Event-driven architecture patterns (fire-and-forget, event-carried state transfer)

**Example Prompts:**

> "Define and raise a business event in my RAP behavior definition"

> "How do I bind a RAP event to SAP Event Mesh for cross-system delivery?"

> "Create an event consumer that reacts to travel creation events"

### ABAP Cloud Migration Patterns

Systematically migrate classic ABAP custom code to ABAP Cloud (Tier 1) compliance — ATC Cloud Readiness checks, unreleased API replacements, wrapper class generation, and step-by-step migration workflows.

**Features:**

- ATC Cloud Readiness check execution and finding categorization
- Comprehensive unreleased-to-released API replacement tables (database access, FMs, language constructs)
- Wrapper pattern with step-by-step creation and C1 release process
- Migration strategies by object type (reports, dynpro transactions, BAPIs, RFC FMs)
- Step-by-step migration checklist from assessment to validation

**Example Prompts:**

> "Run a cloud readiness assessment on my ABAP package and suggest replacements"

> "What's the released API replacement for GUID_CREATE and NUMBER_GET_NEXT?"

> "Create a wrapper class to make READ_TEXT available in ABAP Cloud"

### BTP Diagram Generator

Generate SAP BTP solution architecture diagrams as native draw.io (`.drawio`) files following the official [SAP BTP Solution Diagram guidelines](https://sap.github.io/btp-solution-diagrams/) (Fiori Horizon design system) and open them via a configured [draw.io MCP server](https://www.drawio.com/doc/faq/ai-drawio-generation).

**Features:**

- Python `btp_builder` package with fluent API — a typical L1 diagram is ~20 lines of code
- Bundled SAP BTP icon library (~100 icons) with fuzzy-name lookup and the official SAP Fiori Horizon palette
- Audience-level presets (L0 business / L1 technical / L2 detailed) with correct icon sizes, fonts, and connector semantics
- Auto port-pinning, A4 landscape sizing, SVG icon upscaling, and built-in diagram validation
- 11 official editable example diagrams (Task Center, Build Work Zone, Cloud Identity Services, Private Link, etc.) as style donors

**Example Prompts:**

> "Draw a BTP architecture for a Task Center scenario with Cloud Identity Services"

> "Generate an L2 BTP solution diagram showing CAP + HANA Cloud + Build Work Zone + S/4HANA integration"

> "Create a draw.io diagram of our SAP BTP integration landscape using Integration Suite"

## Repository Structure

```
skills/
├── abap/
│   ├── SKILL.md
│   └── references/
│       ├── abaplint.md
│       ├── CleanABAP.md
│       ├── checklist.md
│       └── quick-reference.md
├── abap-cloud/
│   └── SKILL.md
├── abap-cloud-migration/
│   └── SKILL.md
├── abap-sql-amdp/
│   └── SKILL.md
├── abap-unit-testing/
│   └── SKILL.md
├── abapgit/
│   └── SKILL.md
├── atc-cloudification/
│   ├── SKILL.md
│   └── references/
│       └── quick-reference.md
├── authorization-iam/
│   └── SKILL.md
├── badi-enhancement/
│   └── SKILL.md
├── btp-abap-environment/
│   └── SKILL.md
├── cds-view-entities/
│   └── SKILL.md
├── clean-abap/
│   ├── SKILL.md
│   └── references/
│       ├── CleanABAP.md
│       ├── checklist.md
│       └── quick-reference.md
├── odata/
│   └── SKILL.md
├── rap/
│   └── SKILL.md
├── rap-business-events/
│   └── SKILL.md
├── released-abap-classes/
│   ├── SKILL.md
│   └── references/
│       └── Released_ABAP_Classes.md
└── sap-fiori-apps-reference/
    ├── SKILL.md
    ├── scripts/
    │   ├── fiori-url-generator.js
    │   ├── fiori-url-generator.py
    │   └── test.py
    └── references/
        └── AppList.json
```

## Prerequisites

- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** for contributor validation and the BTP diagram generator scripts
- **Node.js** (v16+) for the Fiori URL generator scripts and [abaplint](https://github.com/abaplint/abaplint) (`npm install @abaplint/cli -g`)
- The `AppList.json` file for Fiori app lookups

## Contributing

Before submitting a skill change, validate discovery metadata and local manifest links:

```bash
uv run python scripts/validate_skills.py
```

The same check runs in GitHub Actions for changes under `skills/`.

## License

MIT
