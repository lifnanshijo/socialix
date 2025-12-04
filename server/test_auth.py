import requests
import json

BASE_URL = "http://localhost:5000/api/auth"

def test_signup():
    """Test signup"""
    url = f"{BASE_URL}/signup"
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    print("=== Testing Signup ===")
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 201

def test_login():
    """Test login with lifnanshijo@gmail.com"""
    url = f"{BASE_URL}/login"
    payload = {
        "email": "lifnanshijo@gmail.com",
        "password": "testpassword"
    }
    
    print("\n=== Testing Login (lifnanshijo@gmail.com) ===")
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_login_testuser():
    """Test login with test user"""
    url = f"{BASE_URL}/login"
    payload = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    print("\n=== Testing Login (test@example.com) ===")
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

if __name__ == '__main__':
    test_signup()
    test_login_testuser()
    test_login()
