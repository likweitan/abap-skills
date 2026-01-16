# SAP Fiori URL Generator - Quick Reference

## Required User Inputs

When generating a Fiori URL, the user **MUST** provide:

1. **Base URL** - The SAP system URL
   - Example: `https://myserver.com:44300`
   - No default value
   - Must be provided every time

2. **SAP Client** - The client number
   - Example: `100`
   - No default value
   - Must be provided every time

3. **App Name** - The Fiori app to launch
   - Example: `Create Maintenance Request`
   - Can be partial match (case-insensitive)
   - Will be searched in AppList.json

4. **Language** (Optional) - The UI language
   - Example: `EN`, `DE`, `FR`, etc.
   - Defaults to `EN` if not provided
   - Can be customized per request

## URL Format

```
{BASE_URL}/sap/bc/ui2/flp?sap-client={CLIENT}&sap-language={LANGUAGE}#{SEMANTIC_OBJECT}-{ACTION}
```

**Where:**
- `{BASE_URL}` = User-provided base URL
- `{CLIENT}` = User-provided SAP client
- `{LANGUAGE}` = User-provided language (or default EN)
- `{SEMANTIC_OBJECT}-{ACTION}` = Auto-extracted from AppList.json

## Usage Examples

### Complete Request
```
Generate a Fiori URL for "Create Maintenance Request"
Base URL: https://myserver.com:44300
Client: 100
Language: EN
```

### Result
```
https://myserver.com:44300/sap/bc/ui2/flp?sap-client=100&sap-language=EN#MaintenanceWorkRequest-create
```

## Command Line Usage

### Python
```bash
python fiori-url-generator.py <BASE_URL> <CLIENT> <APP_NAME> [LANGUAGE]
python fiori-url-generator.py https://myserver.com:44300 100 "Create Maintenance Request" EN
```

### Node.js
```bash
node fiori-url-generator.js <BASE_URL> <CLIENT> <APP_NAME> [LANGUAGE]
node fiori-url-generator.js https://myserver.com:44300 100 "Create Maintenance Request" EN
```

### Search Apps
```bash
python fiori-url-generator.py search "maintenance"
node fiori-url-generator.js search "workflow"
```

## Validation

The skill will validate:
- ✅ Base URL is provided (required)
- ✅ SAP Client is provided (required)
- ✅ App exists in AppList.json
- ✅ App has a valid Semantic Object-Action
- ✅ Language defaults to EN if not specified

## Error Messages

### Missing Base URL or Client
```
Error: Base URL is required and must be provided by user
Error: SAP Client is required and must be provided by user
```

### App Not Found
```
Error: App "Invalid Name" not found in AppList.json
```

### Missing Semantic Action
```
Error: App "Workflow Component" (F2506) does not have a Semantic Object-Action defined
```

## Best Practices

1. **Always ask for all required parameters** - Don't assume defaults for base URL or client
2. **Validate before generating** - Check that app exists first
3. **Show app details** - Confirm the correct app was found
4. **Support search** - Let users search for apps by partial name
5. **Multiple languages** - Support all SAP language codes

## Parameter Matrix

| Parameter | Required | Default | Example |
|-----------|----------|---------|---------|
| Base URL | ✅ YES | None | https://myserver.com:44300 |
| SAP Client | ✅ YES | None | 100 |
| App Name | ✅ YES | None | Create Maintenance Request |
| Language | ❌ No | EN | DE, FR, ES, etc. |

## Common Language Codes

- `EN` - English (Default)
- `DE` - German (Deutsch)
- `ES` - Spanish (Español)
- `FR` - French (Français)
- `IT` - Italian (Italiano)
- `PT` - Portuguese (Português)
- `ZH` - Chinese (中文)
- `JA` - Japanese (日本語)
- `KO` - Korean (한국어)

## Integration with OpenCode

When a user asks to generate a Fiori URL:

1. **Check for required parameters** in the request
2. **If missing**, prompt the user:
   ```
   To generate a Fiori URL, I need:
   - Base URL (e.g., https://myserver.com:44300)
   - SAP Client (e.g., 100)
   - App Name (you provided: Create Maintenance Request)
   - Language (optional, defaults to EN)
   ```

3. **Once all parameters are provided**, generate the URL
4. **Show confirmation** with app details before final URL

## Summary

✅ Base URL - MUST be provided by user
✅ SAP Client - MUST be provided by user
✅ App Name - MUST be provided by user
⚪ Language - Optional (defaults to EN)

**Never assume or hardcode base URL or client values!**
