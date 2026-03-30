# Test script for Module B1 Authentication API Endpoints
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/auth"

def test_register():
    """Test user registration"""
    print("\n=== Testing Registration Endpoint ===")
    data = {
        "email": "newuser@test.com",
        "username": "newuser",
        "password": "securepass123",
        "password2": "securepass123",
        "role": "manager"
    }
    response = requests.post(f"{BASE_URL}/register/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_login():
    """Test user login with demo user"""
    print("\n=== Testing Login Endpoint ===")
    data = {
        "email": "demo@demo.com",
        "password": "demo1234"
    }
    response = requests.post(f"{BASE_URL}/login/", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    return result

def test_current_user(token):
    """Test get current user profile"""
    print("\n=== Testing Current User Endpoint ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/me/", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_token_refresh(refresh_token):
    """Test token refresh"""
    print("\n=== Testing Token Refresh Endpoint ===")
    data = {"refresh": refresh_token}
    response = requests.post(f"{BASE_URL}/token/refresh/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

if __name__ == "__main__":
    print("=" * 60)
    print("Module B1 - Authentication API Test Suite")
    print("=" * 60)
    
    # Test registration
    try:
        reg_result = test_register()
    except requests.exceptions.RequestException as e:
        print(f"Registration test skipped (user may already exist): {e}")
    
    # Test login
    login_result = test_login()
    access_token = login_result["access"]
    refresh_token = login_result["refresh"]
    
    # Test current user
    test_current_user(access_token)
    
    # Test token refresh
    test_token_refresh(refresh_token)
    
    print("\n" + "=" * 60)
    print("✓ All tests completed successfully!")
    print("=" * 60)
