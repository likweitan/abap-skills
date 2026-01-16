const fs = require('fs');
const path = require('path');

/**
 * SAP Fiori URL Generator
 * Generates FLP URLs based on app names from AppList.json
 */
class FioriUrlGenerator {
  constructor(appListPath) {
    try {
      let content = fs.readFileSync(appListPath, 'utf8');
      // Replace NaN with null to make it valid JSON
      content = content.replace(/:\s*NaN\s*,/g, ': null,').replace(/:\s*NaN\s*}/g, ': null}');
      this.apps = JSON.parse(content);
      console.log(`Loaded ${this.apps.length} apps from AppList.json`);
    } catch (error) {
      throw new Error(`Failed to load AppList.json: ${error.message}`);
    }
  }

  /**
   * Find an app by name (case-insensitive partial match)
   */
  findApp(appName) {
    const normalized = appName.toLowerCase().trim();
    return this.apps.find(app => 
      app['App Name'] && 
      app['App Name'].toLowerCase().includes(normalized)
    );
  }

  /**
   * Find all apps matching a search term
   */
  findAllApps(searchTerm, limit = 10) {
    const normalized = searchTerm.toLowerCase().trim();
    return this.apps
      .filter(app => 
        app['App Name'] && 
        app['App Name'].toLowerCase().includes(normalized)
      )
      .slice(0, limit)
      .map(app => ({
        name: app['App Name'],
        id: app['App ID'],
        semanticAction: app['Semantic Object - Action'],
        description: app['App Description']
      }));
  }

  /**
   * Generate a Fiori Launchpad URL
   * @param {string} baseUrl - SAP base URL (REQUIRED - must be provided by user)
   * @param {string} client - SAP client number (REQUIRED - must be provided by user)
   * @param {string} appName - Name of the app to search for
   * @param {object} options - Optional parameters
   * @param {string} options.language - Language code (default: 'EN')
   */
  generateUrl(baseUrl, client, appName, options = {}) {
    const { language = 'EN' } = options;
    
    // Validate required parameters
    if (!baseUrl) {
      throw new Error('Base URL is required and must be provided by user');
    }
    if (!client) {
      throw new Error('SAP Client is required and must be provided by user');
    }
    
    // Find the app
    const app = this.findApp(appName);
    if (!app) {
      throw new Error(`App "${appName}" not found in AppList.json`);
    }

    // Extract semantic action
    const semanticAction = app['Semantic Object - Action'];
    if (!semanticAction || semanticAction === 'NaN' || semanticAction === null) {
      throw new Error(
        `App "${app['App Name']}" (ID: ${app['App ID']}) does not have a Semantic Object-Action defined`
      );
    }

    // Clean base URL (remove trailing slash)
    const cleanBaseUrl = baseUrl.replace(/\/$/, '');

    // Construct URL
    const url = `${cleanBaseUrl}/sap/bc/ui2/flp?sap-client=${client}&sap-language=${language}#${semanticAction}`;

    return {
      url,
      appDetails: {
        name: app['App Name'],
        id: app['App ID'],
        description: app['App Description'],
        semanticAction: semanticAction,
        component: app['Application Component'],
        technicalCatalog: app['Technical Catalog'],
        transactionCode: app['Transaction Codes']
      }
    };
  }

  /**
   * Get detailed information about an app
   */
  getAppDetails(appName) {
    const app = this.findApp(appName);
    if (!app) {
      throw new Error(`App "${appName}" not found`);
    }

    return {
      name: app['App Name'],
      id: app['App ID'],
      description: app['App Description'],
      semanticAction: app['Semantic Object - Action'],
      uiTechnology: app['UI Technology'],
      component: app['Application Component'],
      technicalCatalog: app['Technical Catalog'],
      transactionCode: app['Transaction Codes'],
      odataService: app['OData Service'],
      odataV4ServiceGroup: app['OData V4 Service Group']
    };
  }
}

// CLI Usage
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log('Usage: node fiori-url-generator.js <base-url> <client> <app-name> [language]');
    console.log('Example: node fiori-url-generator.js https://myserver.com:44300 100 "Create Maintenance Request" EN');
    console.log('\nOr for search:');
    console.log('Usage: node fiori-url-generator.js search <search-term>');
    console.log('Example: node fiori-url-generator.js search workflow');
    console.log('\nNote: Base URL and SAP Client are REQUIRED parameters that must be provided by the user.');
    process.exit(1);
  }

  // Try to find AppList.json in current directory or parent directories
  let appListPath = path.join(__dirname, 'AppList.json');
  if (!fs.existsSync(appListPath)) {
    appListPath = path.join(__dirname, '..', '..', 'AppList.json');
  }
  if (!fs.existsSync(appListPath)) {
    appListPath = path.join(process.cwd(), 'AppList.json');
  }
  if (!fs.existsSync(appListPath)) {
    console.error('Error: AppList.json not found');
    console.error('Tried locations:');
    console.error('  - ' + path.join(__dirname, 'AppList.json'));
    console.error('  - ' + path.join(__dirname, '..', '..', 'AppList.json'));
    console.error('  - ' + path.join(process.cwd(), 'AppList.json'));
    process.exit(1);
  }
  
  const generator = new FioriUrlGenerator(appListPath);

  try {
    if (args[0] === 'search') {
      // Search mode
      const searchTerm = args[1];
      console.log(`\nSearching for apps matching "${searchTerm}"...\n`);
      
      const results = generator.findAllApps(searchTerm);
      
      if (results.length === 0) {
        console.log('No apps found matching your search.');
      } else {
        console.log(`Found ${results.length} app(s):\n`);
        results.forEach((app, index) => {
          console.log(`${index + 1}. ${app.name}`);
          console.log(`   App ID: ${app.id}`);
          console.log(`   Semantic Action: ${app.semanticAction || 'Not available'}`);
          if (app.description) {
            console.log(`   Description: ${app.description.substring(0, 100)}...`);
          }
          console.log('');
        });
      }
    } else {
      // URL generation mode
      if (args.length < 3) {
        console.error('Error: Missing required parameters for URL generation');
        console.log('\nUsage: node fiori-url-generator.js <base-url> <client> <app-name> [language]');
        console.log('Example: node fiori-url-generator.js https://myserver.com:44300 100 "Create Maintenance Request" EN');
        process.exit(1);
      }
      
      const baseUrl = args[0];
      const client = args[1];
      const appName = args[2];
      const language = args[3] || 'EN';

      console.log(`\nGenerating URL for: ${appName}`);
      console.log(`Base URL: ${baseUrl}`);
      console.log(`Client: ${client}`);
      console.log(`Language: ${language}\n`);

      const result = generator.generateUrl(baseUrl, client, appName, { language });

      console.log('App Details:');
      console.log(`  Name: ${result.appDetails.name}`);
      console.log(`  App ID: ${result.appDetails.id}`);
      console.log(`  Semantic Action: ${result.appDetails.semanticAction}`);
      console.log(`  Component: ${result.appDetails.component}`);
      console.log('');
      console.log('Generated URL:');
      console.log(result.url);
      console.log('');
    }
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

module.exports = FioriUrlGenerator;
