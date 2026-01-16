# SAP Fiori URL Generator

> **Note**: This repository contains the `sap-fiori-url-generator` skill for Claude Code.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A specialized Claude Code skill designed to generate SAP Fiori Launchpad (FLP) URLs by looking up app information and constructing the correct parameters.

## 🚀 Overview

This tool simplifies the process of creating direct links to SAP Fiori applications. It takes an app name and environment details, looks up the technical configuration (Semantic Object & Action), and outputs a ready-to-use URL.

**Key Features:**
- 🔍 **Smart Lookup**: Finds apps by name (fuzzy search support) in `AppList.json`
- 🔗 **Automatic Construction**: Builds standard FLP URLs with `sap-client` and `sap-language`
- 🌍 **Language Support**: easily toggle between EN, DE, FR, etc.
- 💡 **Intelligent Suggestions**: Suggests similar apps if an exact match isn't found

## 🛠 Prerequisites

To run this skill, you need **Node.js** or **Python** installed in your environment to execute the generation scripts.

The `AppList.json` file is located in the `skills/sap-fiori-url-generator/` directory.

**JSON Structure:**
```json
[
  {
    "App Name": "Create Maintenance Request",
    "App ID": "F1511A",
    "Semantic Object - Action": "MaintenanceWorkRequest-create",
    "App Description": "Create maintenance requests for assets..."
  }
]
```

## � Usage

Once installed as a Claude Code skill, you can ask for URLs naturally.

### Required Information
You must provide:
1.  **Base URL** (e.g., `https://myserver.com:44300`)
2.  **SAP Client** (e.g., `100`)
3.  **App Name** (e.g., "Create Maintenance Request")

### Example Prompts

**Basic Generation:**
> "Generate URL for Create Maintenance Request app with base URL https://myserver.com:44300 and client 100"

**Different Language:**
> "Link for 'Manage Workflows' in German (DE) for client 200 on https://myserver.com"

**Search:**
> "Find apps related to 'Workflow'"

## 🔧 URL Structure

The generator produces URLs in the standard SAP Fiori format:

```
{BASE_URL}/sap/bc/ui2/flp?sap-client={CLIENT}&sap-language={LANGUAGE}#{SEMANTIC_OBJECT}-{ACTION}
```

## 📂 Repository Structure

- `skills/sap-fiori-url-generator/`
    - `SKILL.md`: The core prompt engineering and logic definition for Claude.
    - `fiori-url-generator.js`: Reference JavaScript implementation.
    - `fiori-url-generator.py`: Reference Python implementation.
    - `AppList.json`: (Required at runtime) The data source for app lookups.

## 📄 License

MIT
