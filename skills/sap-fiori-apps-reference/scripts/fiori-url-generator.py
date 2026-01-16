#!/usr/bin/env python3
"""
SAP Fiori URL Generator
Generates FLP URLs based on app names from AppList.json
"""

import json
import sys
from typing import Optional, Dict, List
from pathlib import Path


class FioriUrlGenerator:
    """Generate SAP Fiori Launchpad URLs from app names"""

    def __init__(self, app_list_path: str):
        """Initialize with path to AppList.json"""
        try:
            with open(app_list_path, "r", encoding="utf-8") as f:
                self.apps = json.load(f)
            print(f"Loaded {len(self.apps)} apps from AppList.json")
        except Exception as e:
            raise Exception(f"Failed to load AppList.json: {str(e)}")

    def find_app(self, app_name: str) -> Optional[Dict]:
        """Find an app by name (case-insensitive partial match)"""
        normalized = app_name.lower().strip()
        for app in self.apps:
            if app.get("App Name") and normalized in app["App Name"].lower():
                return app
        return None

    def find_all_apps(self, search_term: str, limit: int = 10) -> List[Dict]:
        """Find all apps matching a search term"""
        normalized = search_term.lower().strip()
        results = []

        for app in self.apps:
            if app.get("App Name") and normalized in app["App Name"].lower():
                results.append(
                    {
                        "name": app.get("App Name"),
                        "id": app.get("App ID"),
                        "semanticAction": app.get("Semantic Object - Action"),
                        "description": app.get("App Description"),
                    }
                )
                if len(results) >= limit:
                    break

        return results

    def generate_url(
        self, base_url: str, client: str, app_name: str, language: str = "EN"
    ) -> Dict:
        """
        Generate a Fiori Launchpad URL

        Args:
            base_url: SAP base URL (REQUIRED - must be provided by user)
            client: SAP client number (REQUIRED - must be provided by user)
            app_name: Name of the app to search for
            language: Language code (default: 'EN')
        """

        # Validate required parameters
        if not base_url:
            raise ValueError("Base URL is required and must be provided by user")
        if not client:
            raise ValueError("SAP Client is required and must be provided by user")

        # Find the app
        app = self.find_app(app_name)
        if not app:
            raise ValueError(f'App "{app_name}" not found in AppList.json')

        # Extract semantic action
        semantic_action = app.get("Semantic Object - Action")
        if not semantic_action or str(semantic_action).lower() in ["nan", "none"]:
            raise ValueError(
                f'App "{app["App Name"]}" (ID: {app.get("App ID")}) '
                f"does not have a Semantic Object-Action defined"
            )

        # Clean base URL (remove trailing slash)
        clean_base_url = base_url.rstrip("/")

        # Construct URL
        url = (
            f"{clean_base_url}/sap/bc/ui2/flp?"
            f"sap-client={client}&sap-language={language}#{semantic_action}"
        )

        return {
            "url": url,
            "appDetails": {
                "name": app.get("App Name"),
                "id": app.get("App ID"),
                "description": app.get("App Description"),
                "semanticAction": semantic_action,
                "component": app.get("Application Component"),
                "technicalCatalog": app.get("Technical Catalog"),
                "transactionCode": app.get("Transaction Codes"),
            },
        }

    def get_app_details(self, app_name: str) -> Dict:
        """Get detailed information about an app"""
        app = self.find_app(app_name)
        if not app:
            raise ValueError(f'App "{app_name}" not found')

        return {
            "name": app.get("App Name"),
            "id": app.get("App ID"),
            "description": app.get("App Description"),
            "semanticAction": app.get("Semantic Object - Action"),
            "uiTechnology": app.get("UI Technology"),
            "component": app.get("Application Component"),
            "technicalCatalog": app.get("Technical Catalog"),
            "transactionCode": app.get("Transaction Codes"),
            "odataService": app.get("OData Service"),
            "odataV4ServiceGroup": app.get("OData V4 Service Group"),
        }


def main():
    """CLI interface"""
    if len(sys.argv) < 3:
        print(
            "Usage: python fiori-url-generator.py <base-url> <client> <app-name> [language]"
        )
        print(
            "Example: python fiori-url-generator.py "
            'https://myserver.com:44300 100 "Create Maintenance Request" EN'
        )
        print("\nOr for search:")
        print("Usage: python fiori-url-generator.py search <search-term>")
        print("Example: python fiori-url-generator.py search workflow")
        print(
            "\nNote: Base URL and SAP Client are REQUIRED parameters that must be provided by the user."
        )
        sys.exit(1)

    # Find AppList.json in parent directory or other locations
    app_list_path = Path(__file__).parent.parent / "AppList.json"
    if not app_list_path.exists():
        app_list_path = Path(__file__).parent.parent.parent / "AppList.json"
    if not app_list_path.exists():
        app_list_path = Path("AppList.json")

    if not app_list_path.exists():
        print("Error: AppList.json not found")
        sys.exit(1)

    generator = FioriUrlGenerator(str(app_list_path))

    try:
        if sys.argv[1] == "search":
            # Search mode
            search_term = sys.argv[2]
            print(f'\nSearching for apps matching "{search_term}"...\n')

            results = generator.find_all_apps(search_term)

            if not results:
                print("No apps found matching your search.")
            else:
                print(f"Found {len(results)} app(s):\n")
                for i, app in enumerate(results, 1):
                    print(f"{i}. {app['name']}")
                    print(f"   App ID: {app['id']}")
                    semantic = app["semanticAction"] or "Not available"
                    print(f"   Semantic Action: {semantic}")
                    if app["description"]:
                        desc = app["description"][:100] + "..."
                        print(f"   Description: {desc}")
                    print()
        else:
            # URL generation mode
            if len(sys.argv) < 4:
                print("Error: Missing required parameters for URL generation")
                print(
                    "\nUsage: python fiori-url-generator.py <base-url> <client> <app-name> [language]"
                )
                print(
                    "Example: python fiori-url-generator.py "
                    'https://myserver.com:44300 100 "Create Maintenance Request" EN'
                )
                sys.exit(1)

            base_url = sys.argv[1]
            client = sys.argv[2]
            app_name = sys.argv[3]
            language = sys.argv[4] if len(sys.argv) > 4 else "EN"

            print(f"\nGenerating URL for: {app_name}")
            print(f"Base URL: {base_url}")
            print(f"Client: {client}")
            print(f"Language: {language}\n")

            result = generator.generate_url(
                base_url, client, app_name, language=language
            )

            print("App Details:")
            print(f"  Name: {result['appDetails']['name']}")
            print(f"  App ID: {result['appDetails']['id']}")
            print(f"  Semantic Action: {result['appDetails']['semanticAction']}")
            print(f"  Component: {result['appDetails']['component']}")
            print()
            print("Generated URL:")
            print(result["url"])
            print()

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
