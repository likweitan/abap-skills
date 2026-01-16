# SAP Fiori URL Generator Skill

A skill for OpenCode that generates SAP Fiori Launchpad (FLP) URLs from app names using AppList.json.

## Overview

This skill enables you to:
- Search for SAP Fiori apps by name
- Generate complete FLP URLs with proper parameters
- Look up app details and metadata
- Support multiple languages and customization

## Quick Start

### Using the Skill in OpenCode

Simply ask OpenCode to generate a Fiori URL:

```
Generate a Fiori URL for "Create Maintenance Request" 
using base URL https://myserver.com:44300 
and client 100
```

**Note:** Both base URL and SAP client are REQUIRED parameters that must be provided by the user.

### Using the Command-Line Tools

#### JavaScript/Node.js

```bash
# Generate URL
node fiori-url-generator.js https://myserver.com:44300 100 "Create Maintenance Request" EN

# Search for apps
node fiori-url-generator.js search workflow
```

#### Python

```bash
# Generate URL
python fiori-url-generator.py https://myserver.com:44300 100 "Create Maintenance Request" EN

# Search for apps
python fiori-url-generator.py search workflow
```

## URL Format

Generated URLs follow the SAP Fiori Launchpad standard:

```
{BASE_URL}/sap/bc/ui2/flp?sap-client={CLIENT}&sap-language={LANGUAGE}#{SEMANTIC_OBJECT}-{ACTION}
```

### Example

**Input (ALL REQUIRED - must be provided by user):**
- Base URL: `https://myserver.com:44300`
- SAP Client: `100`
- App Name: `Create Maintenance Request`
- Language: `EN` (optional - defaults to EN if not specified)

**Output:**
```
https://myserver.com:44300/sap/bc/ui2/flp?sap-client=100&sap-language=EN#MaintenanceWorkRequest-create
```

## Features

### 1. App Search
Find apps by partial name match (case-insensitive):
```
Search for apps matching "maintenance"
```

### 2. URL Generation
Generate complete FLP URLs with all required parameters:
```
Generate URL for "Manage Workflows" with language DE
```

### 3. App Details
Get detailed information about any app:
```
Show me details for "Create Maintenance Request"
```

### 4. Language Support
Support for all SAP language codes:
- EN (English) - Default
- DE (German)
- ES (Spanish)
- FR (French)
- IT (Italian)
- PT (Portuguese)
- ZH (Chinese)
- JA (Japanese)
- KO (Korean)

## AppList.json Structure

The skill reads from AppList.json, which contains SAP Fiori app metadata:

```json
{
  "App Name": "Create Maintenance Request",
  "App ID": "F1511A",
  "Semantic Object - Action": "MaintenanceWorkRequest-create",
  "UI Technology": "SAP Fiori (SAPUI5)",
  "Application Component": "PM-FIO-WOC-MN",
  "App Description": "With this app, you can create maintenance requests...",
  "Technical Catalog": "SAP_TC_EAM_COMMON",
  "Transaction Codes": "IW21",
  "OData Service": "UI_MAINTWORKREQUESTOVW_V2 - 0001"
}
```

## Requirements

### For OpenCode
- AppList.json file in the project directory

### For Command-Line Tools
- Node.js 14+ (for JavaScript version)
- Python 3.7+ (for Python version)
- AppList.json file in the same directory or parent directory

## Installation

1. Place the skill folder in your OpenCode skills directory:
   ```
   .opencode/skills/sap-fiori-url-generator/
   ```

2. Ensure AppList.json is accessible in your project

3. Use the skill naturally in your conversations with OpenCode

## Error Handling

The skill handles common scenarios:

### App Not Found
```
Error: App "Invalid Name" not found in AppList.json
Suggestion: Check spelling or try searching with partial name
```

### Missing Semantic Object-Action
```
Error: App "Workflow Component" (ID: F2506) does not have a Semantic Object-Action defined
Note: This app may not be launchable via FLP URL
```

### Multiple Matches
```
Found multiple apps matching "workflow":
1. Manage Workflows (F2190)
2. Workflow Component (F2506)
3. Manage Workflow Templates (F2787)
Please specify which app you want
```

## Examples

### Example 1: Basic URL Generation
```
Q: Generate URL for Create Maintenance Request
A: https://myserver.com:44300/sap/bc/ui2/flp?sap-client=100&sap-language=EN#MaintenanceWorkRequest-create
```

### Example 2: Custom Language
```
Q: Generate URL for Create Maintenance Request in German
A: https://myserver.com:44300/sap/bc/ui2/flp?sap-client=100&sap-language=DE#MaintenanceWorkRequest-create
```

### Example 3: Search Apps
```
Q: Find apps related to "Business Partners"
A: Found 3 apps:
   1. Application Log for Business Partners (F5247A)
   2. Application Log Messages for Business Partners (F5250A)
   3. Scheduling Block Business Partners (F2047A)
```

## API Reference

### FioriUrlGenerator Class

#### Constructor
```javascript
new FioriUrlGenerator(appListPath)
```

#### Methods
- `findApp(appName)` - Find single app by name
- `findAllApps(searchTerm, limit)` - Find multiple apps
- `generateUrl(baseUrl, appName, options)` - Generate FLP URL
- `getAppDetails(appName)` - Get detailed app information

## License

MIT License - See LICENSE.txt for details

## Contributing

This skill is designed to work with SAP Fiori app metadata. To extend:

1. Update AppList.json with new apps
2. Modify search logic in the generator classes
3. Add custom URL parameter handling
4. Extend app details extraction

## Support

For issues or questions:
- Check SKILL.md for detailed documentation
- Verify AppList.json is properly formatted
- Ensure app names match entries in AppList.json

## Version History

- 1.0.0 - Initial release
  - Basic URL generation
  - App search functionality
  - Multi-language support
  - JavaScript and Python implementations
