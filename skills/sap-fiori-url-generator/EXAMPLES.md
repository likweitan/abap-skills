# SAP Fiori URL Generator - Examples

This document demonstrates various ways to use the SAP Fiori URL Generator skill.

## Example 1: Basic URL Generation

**Request:**
```
Generate a Fiori URL for "Create Maintenance Request" 
using base URL https://myserver.com:44300 
and client 100
```

**Result:**
```
App Found: Create Maintenance Request (F1511A)
Semantic Object-Action: MaintenanceWorkRequest-create

Generated URL:
https://myserver.com:44300/sap/bc/ui2/flp?sap-client=100&sap-language=EN#MaintenanceWorkRequest-create
```

## Example 2: URL with Custom Language

**Request:**
```
Generate a Fiori URL for "Create Maintenance Request" in German (DE)
with base URL https://myserver.com:44300 and client 100
```

**Result:**
```
Generated URL:
https://myserver.com:44300/sap/bc/ui2/flp?sap-client=100&sap-language=DE#MaintenanceWorkRequest-create
```

## Example 3: Search for Apps

**Request:**
```
Search for apps related to "workflow"
```

**Result:**
```
Found 10 apps matching "workflow":

1. Workflow System Jobs (F4919)
   Action: WorkflowMonitor-showApplicationLog

2. Manage Workflows (F2190)
   Action: Workflow-showList

3. Manage Workflow Templates (F2787)
   Action: WorkflowTemplate-showList

4. Manage Workflows - For Bank Accounts (F2796)
   Action: BankAccount-workflowShowList

...
```

## Example 4: Generate Multiple URLs

**Request:**
```
Generate Fiori URLs for these apps:
- Create Maintenance Request
- Manage Workflows
- Monitor Archiving Jobs
```

**Result:**
```
1. Create Maintenance Request:
   https://myserver.com:44300/sap/bc/ui2/flp?sap-client=100&sap-language=EN#MaintenanceWorkRequest-create

2. Manage Workflows:
   https://myserver.com:44300/sap/bc/ui2/flp?sap-client=100&sap-language=EN#Workflow-showList

3. Monitor Archiving Jobs:
   https://myserver.com:44300/sap/bc/ui2/flp?sap-client=100&sap-language=EN#Document-displayArchObjT
```

## Example 5: Get App Details

**Request:**
```
Show me details for "Create Maintenance Request"
```

**Result:**
```
App Details:
- Name: Create Maintenance Request
- App ID: F1511A
- Semantic Object-Action: MaintenanceWorkRequest-create
- UI Technology: SAP Fiori (SAPUI5)
- Application Component: PM-FIO-WOC-MN
- Technical Catalog: SAP_TC_EAM_COMMON
- Transaction Code: IW21
- OData Service: UI_MAINTWORKREQUESTOVW_V2 - 0001

Description:
With this app, you can create maintenance requests. While creating a maintenance request, 
you can provide relevant information that is required to identify and solve the problem.
```

## Example 6: Partial Name Search

**Request:**
```
Find the URL for "Maintenance Request" (partial name)
```

**Result:**
```
App Found: Create Maintenance Request (F1511A)

Generated URL:
https://myserver.com:44300/sap/bc/ui2/flp?sap-client=100&sap-language=EN#MaintenanceWorkRequest-create
```

## Example 7: Different Languages

**Request:**
```
Generate URLs for "Manage Workflows" in multiple languages:
- English
- German
- Spanish
```

**Result:**
```
English (EN):
https://myserver.com:44300/sap/bc/ui2/flp?sap-client=100&sap-language=EN#Workflow-showList

German (DE):
https://myserver.com:44300/sap/bc/ui2/flp?sap-client=100&sap-language=DE#Workflow-showList

Spanish (ES):
https://myserver.com:44300/sap/bc/ui2/flp?sap-client=100&sap-language=ES#Workflow-showList
```

## Command-Line Examples

### Using Python:

```bash
# Search for apps
python fiori-url-generator.py search "maintenance"

# Generate URL (requires base URL and client)
python fiori-url-generator.py https://myserver.com:44300 100 "Create Maintenance Request" EN

# Generate URL with German language
python fiori-url-generator.py https://myserver.com:44300 100 "Create Maintenance Request" DE
```

### Using Node.js:

```bash
# Search for apps
node fiori-url-generator.js search "workflow"

# Generate URL (requires base URL and client)
node fiori-url-generator.js https://myserver.com:44300 100 "Create Maintenance Request" EN

# Generate URL with French language
node fiori-url-generator.js https://myserver.com:44300 100 "Manage Workflows" FR
```

## Common Use Cases

### 1. Creating Bookmarks
Generate URLs to create browser bookmarks for frequently used apps:
```
Generate URLs for my most used apps:
- Create Maintenance Request
- Manage Business Partners
- Monitor Archiving Jobs
```

### 2. Documentation
Generate URLs for user documentation:
```
I'm writing documentation. Generate URLs for all workflow-related apps.
```

### 3. Testing
Generate URLs for different environments:
```
Generate the URL for "Create Maintenance Request" for:
- Development: https://dev-server.example.com:44301
- QA: https://qa-server.example.com:44301
- Production: https://prod-server.example.com:44301
```

### 4. Training Materials
Create URLs for training in different languages:
```
Generate training URLs for "Manage Workflows" in EN, DE, FR, and ES
```

## Supported Languages

- EN - English (Default)
- DE - German (Deutsch)
- ES - Spanish (Español)
- FR - French (Français)
- IT - Italian (Italiano)
- PT - Portuguese (Português)
- NL - Dutch (Nederlands)
- PL - Polish (Polski)
- RU - Russian (Русский)
- ZH - Chinese (中文)
- JA - Japanese (日本語)
- KO - Korean (한국어)
- TR - Turkish (Türkçe)
- AR - Arabic (العربية)

## Tips

1. **Partial Matches**: You don't need to type the complete app name - partial matches work
2. **Case Insensitive**: Search is case-insensitive ("maintenance" = "Maintenance" = "MAINTENANCE")
3. **Default Client**: Client is always set to 100 (mandatory for this system)
4. **Multiple Matches**: If your search returns multiple apps, be more specific
5. **App Not Found**: Try searching first to see available apps

## Error Examples

### App Not Found
```
Request: Generate URL for "Nonexistent App"
Result: Error: App "Nonexistent App" not found in AppList.json
Suggestion: Try searching with: search "Nonexistent"
```

### No Semantic Action
```
Request: Generate URL for "Workflow Component"
Result: Error: App "Workflow Component" (F2506) does not have a Semantic Object-Action defined
Note: This app may not be launchable via FLP URL
```
