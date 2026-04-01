# Test script for Module B6 Dashboard Stats API Endpoint
import json

import requests

BASE_URL = "http://127.0.0.1:8000/api"
AUTH_URL = "http://127.0.0.1:8000/api/auth"


def login_demo_user():
    """Login with demo user to get access token"""
    print("\n=== Logging in with demo user ===")
    data = {"email": "demo@demo.com", "password": "demo1234"}
    response = requests.post(f"{AUTH_URL}/login/", json=data)
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Login successful")
        return result["access"]
    else:
        print(f"✗ Login failed: {response.status_code}")
        print(f"Response: {response.text}")
        return None


def test_dashboard_stats(token):
    """Test dashboard stats endpoint"""
    print("\n=== Testing Dashboard Stats Endpoint ===")
    print(f"GET {BASE_URL}/dashboard/stats/")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/dashboard/stats/", headers=headers)

    print(f"\nStatus: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"\n{'=' * 60}")
        print("DASHBOARD STATISTICS")
        print("=" * 60)

        # Display KPI metrics
        print(f"\n📊 ORDER METRICS:")
        print(f"  • Orders Today:        {result['orders_today']}")
        print(f"  • Pending Orders:      {result['pending_orders']}")
        print(f"  • Completed Today:     {result['completed_orders']}")
        print(f"  • Revenue Today:       ${result['revenue_today']}")

        print(f"\n📦 INVENTORY METRICS:")
        print(f"  • Low Stock Count:     {result['low_stock_count']}")
        print(f"  • Total Products:      {len(result['product_summary'])}")

        # Display product summary
        print(f"\n📋 PRODUCT SUMMARY:")
        if result["product_summary"]:
            # Count by status
            status_counts = {"ok": 0, "low_stock": 0, "out_of_stock": 0}

            for product in result["product_summary"]:
                status_counts[product["status"]] = (
                    status_counts.get(product["status"], 0) + 1
                )

            print(f"  • OK Stock:            {status_counts['ok']}")
            print(f"  • Low Stock:           {status_counts['low_stock']}")
            print(f"  • Out of Stock:        {status_counts['out_of_stock']}")

            print(f"\n  Product Details:")
            for product in result["product_summary"][:10]:  # Show first 10
                status_icon = {"ok": "✓", "low_stock": "⚠", "out_of_stock": "✗"}.get(
                    product["status"], "?"
                )

                print(
                    f"    {status_icon} {product['name'][:40]:<40} | Stock: {product['stock_quantity']:<5} | Status: {product['status']}"
                )

            if len(result["product_summary"]) > 10:
                print(
                    f"    ... and {len(result['product_summary']) - 10} more products"
                )
        else:
            print("  No products found")

        print(f"\n{'=' * 60}")
        print("\n✓ Dashboard stats retrieved successfully!")

        # Also print raw JSON for reference
        print(f"\nRaw JSON Response:")
        print(json.dumps(result, indent=2))

        return result
    else:
        print(f"\n✗ Request failed")
        print(f"Response: {response.text}")
        return None


def test_without_auth():
    """Test dashboard stats endpoint without authentication"""
    print("\n=== Testing Dashboard Stats Without Authentication ===")
    print(f"GET {BASE_URL}/dashboard/stats/")

    response = requests.get(f"{BASE_URL}/dashboard/stats/")
    print(f"Status: {response.status_code}")

    if response.status_code == 401:
        print("✓ Correctly rejected unauthorized request")
    else:
        print(f"Response: {response.text}")


if __name__ == "__main__":
    print("=" * 60)
    print("Module B6 - Dashboard Stats API Test Suite")
    print("=" * 60)

    try:
        # Test without authentication first
        test_without_auth()

        # Login to get access token
        access_token = login_demo_user()

        if access_token:
            # Test dashboard stats endpoint
            test_dashboard_stats(access_token)

            print("\n" + "=" * 60)
            print("✓ All tests completed successfully!")
            print("=" * 60)
        else:
            print("\n✗ Could not obtain access token. Tests aborted.")
            print("Make sure the server is running and demo user exists.")

    except requests.exceptions.RequestException as e:
        print(f"\n✗ Error: {e}")
        print("Make sure the development server is running:")
        print("  python manage.py runserver")
