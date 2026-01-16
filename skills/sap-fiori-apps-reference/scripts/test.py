#!/usr/bin/env python3
"""
Test script for SAP Fiori URL Generator
"""

import sys
from pathlib import Path

# Import the generator module (use hyphenated filename with importlib)
import importlib.util

spec = importlib.util.spec_from_file_location(
    "fiori_url_generator", Path(__file__).parent / "fiori-url-generator.py"
)
fiori_url_generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fiori_url_generator)
FioriUrlGenerator = fiori_url_generator.FioriUrlGenerator


def test_basic_url_generation():
    """Test basic URL generation"""
    print("=" * 60)
    print("Test 1: Basic URL Generation")
    print("=" * 60)

    app_list_path = Path(__file__).parent.parent / "AppList.json"
    generator = FioriUrlGenerator(str(app_list_path))

    result = generator.generate_url(
        "https://myserver.com:44300", "100", "Create Maintenance Request"
    )

    print(f"App Name: {result['appDetails']['name']}")
    print(f"App ID: {result['appDetails']['id']}")
    print(f"Semantic Action: {result['appDetails']['semanticAction']}")
    print(f"\nGenerated URL:\n{result['url']}")

    expected_url = "https://myserver.com:44300/sap/bc/ui2/flp?sap-client=100&sap-language=EN#MaintenanceWorkRequest-create"
    assert result["url"] == expected_url, (
        f"URL mismatch! Expected:\n{expected_url}\nGot:\n{result['url']}"
    )
    print("\n[PASS] Test passed!")
    print()


def test_custom_language():
    """Test URL generation with custom language"""
    print("=" * 60)
    print("Test 2: Custom Language")
    print("=" * 60)

    app_list_path = Path(__file__).parent.parent / "AppList.json"
    generator = FioriUrlGenerator(str(app_list_path))

    result = generator.generate_url(
        "https://myserver.com:44300", "100", "Create Maintenance Request", language="DE"
    )

    print(f"Language: DE (German)")
    print(f"\nGenerated URL:\n{result['url']}")

    assert "sap-language=DE" in result["url"], "Language parameter not set correctly"
    print("\n[PASS] Test passed!")
    print()


def test_app_search():
    """Test app search functionality"""
    print("=" * 60)
    print("Test 3: App Search")
    print("=" * 60)

    app_list_path = Path(__file__).parent.parent / "AppList.json"
    generator = FioriUrlGenerator(str(app_list_path))

    results = generator.find_all_apps("workflow", limit=5)

    print(f"Search term: 'workflow'")
    print(f"Found {len(results)} apps:\n")

    for i, app in enumerate(results, 1):
        print(f"{i}. {app['name']}")
        print(f"   App ID: {app['id']}")
        print(f"   Semantic Action: {app['semanticAction']}")
        print()

    assert len(results) > 0, "No apps found for search term 'workflow'"
    print("[PASS] Test passed!")
    print()


def test_app_not_found():
    """Test error handling for non-existent app"""
    print("=" * 60)
    print("Test 4: App Not Found Error Handling")
    print("=" * 60)

    app_list_path = Path(__file__).parent.parent / "AppList.json"
    generator = FioriUrlGenerator(str(app_list_path))

    try:
        generator.generate_url(
            "https://myserver.com:44300", "100", "Nonexistent App That Does Not Exist"
        )
        print("[FAIL] Test failed - should have raised an error")
    except ValueError as e:
        print(f"Expected error caught: {str(e)}")
        print("\n[PASS] Test passed!")
        print()


def test_get_app_details():
    """Test getting app details"""
    print("=" * 60)
    print("Test 5: Get App Details")
    print("=" * 60)

    app_list_path = Path(__file__).parent.parent / "AppList.json"
    generator = FioriUrlGenerator(str(app_list_path))

    details = generator.get_app_details("Create Maintenance Request")

    print(f"Name: {details['name']}")
    print(f"App ID: {details['id']}")
    print(f"Semantic Action: {details['semanticAction']}")
    print(f"UI Technology: {details['uiTechnology']}")
    print(f"Component: {details['component']}")
    print(f"Transaction Code: {details['transactionCode']}")

    assert details["name"] == "Create Maintenance Request", "App name mismatch"
    assert details["id"] == "F1511A", "App ID mismatch"
    print("\n[PASS] Test passed!")
    print()


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("SAP Fiori URL Generator - Test Suite")
    print("=" * 60)
    print()

    try:
        test_basic_url_generation()
        test_custom_language()
        test_app_search()
        test_app_not_found()
        test_get_app_details()

        print("=" * 60)
        print("All tests passed!")
        print("=" * 60)
        print()

    except Exception as e:
        print(f"\n[FAIL] Test suite failed with error: {str(e)}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
