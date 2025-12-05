#!/usr/bin/env python3
"""Test script to debug post creation"""

import requests
import json
from io import BytesIO
from PIL import Image

# Test configuration
BASE_URL = "http://localhost:5000"
TEST_EMAIL = "testuser@example.com"
TEST_PASSWORD = "testpass123"

def create_test_image():
    """Create a simple test image"""
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

def test_post_creation():
    """Test the full post creation flow"""
    
    # First, let's register and login
    print("1. Registering user...")
    reg_data = {
        "username": "testuser",
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    reg_response = requests.post(f"{BASE_URL}/api/auth/register", json=reg_data)
    print(f"Registration response: {reg_response.status_code}")
    print(f"Response: {reg_response.json()}")
    
    # Login
    print("\n2. Logging in...")
    login_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    login_response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print(f"Login response: {login_response.status_code}")
    login_json = login_response.json()
    print(f"Response: {login_json}")
    
    if login_response.status_code != 200:
        print("Login failed!")
        return
    
    token = login_json.get('access_token')
    print(f"Got token: {token[:20]}...")
    
    # Test 1: Create post with just text
    print("\n3. Creating post with just text...")
    headers = {"Authorization": f"Bearer {token}"}
    post_data = {"content": "Hello, this is a test post!"}
    
    text_response = requests.post(
        f"{BASE_URL}/api/posts/create",
        data=post_data,
        headers=headers
    )
    print(f"Text post response: {text_response.status_code}")
    print(f"Response: {text_response.json()}")
    
    # Test 2: Create post with image
    print("\n4. Creating post with image...")
    
    files = {
        'image': ('test.png', create_test_image(), 'image/png')
    }
    form_data = {
        'content': 'Test post with image'
    }
    
    image_response = requests.post(
        f"{BASE_URL}/api/posts/create",
        data=form_data,
        files=files,
        headers=headers
    )
    print(f"Image post response: {image_response.status_code}")
    try:
        print(f"Response: {image_response.json()}")
    except:
        print(f"Response text: {image_response.text}")
    
    # Test 3: Fetch posts
    print("\n5. Fetching posts...")
    fetch_response = requests.get(
        f"{BASE_URL}/api/posts/feed",
        headers=headers
    )
    print(f"Fetch posts response: {fetch_response.status_code}")
    print(f"Response: {fetch_response.json()}")

if __name__ == "__main__":
    test_post_creation()
