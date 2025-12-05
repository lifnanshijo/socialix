#!/usr/bin/env python3
"""Test script to verify post creation works after auth fix"""

import requests
import json
import time
from io import BytesIO
from PIL import Image

BASE_URL = "http://localhost:5000"
TEST_EMAIL = f"fixtest{int(time.time())}@test.com"
TEST_PASSWORD = "testpass123"
TEST_USERNAME = f"fixtest{int(time.time())}"

def test_post_creation():
    print("\n" + "="*60)
    print("TESTING POST CREATION AFTER AUTH FIX")
    print("="*60 + "\n")
    
    # Step 1: Register
    print("[1/4] Registering user...")
    reg_data = {
        "username": TEST_USERNAME,
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    try:
        reg_response = requests.post(f"{BASE_URL}/api/auth/signup", json=reg_data)
        if reg_response.status_code != 201:
            print(f"✗ Registration failed: {reg_response.status_code}")
            print(f"Response: {reg_response.text}")
            return False
        print("✓ Registration successful")
    except Exception as e:
        print(f"✗ Registration error: {e}")
        return False
    
    # Step 2: Login
    print("\n[2/4] Logging in...")
    login_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if login_response.status_code != 200:
            print(f"✗ Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return False
        
        token = login_response.json().get('access_token')
        if not token:
            print("✗ No token in response")
            return False
        print(f"✓ Login successful (token: {token[:20]}...)")
    except Exception as e:
        print(f"✗ Login error: {e}")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 3: Create post with just text
    print("\n[3/4] Creating text post...")
    try:
        post_response = requests.post(
            f"{BASE_URL}/api/posts/create",
            data={"content": "This is a test post after auth fix!"},
            headers=headers
        )
        
        if post_response.status_code != 201:
            print(f"✗ Post creation failed: {post_response.status_code}")
            print(f"Response: {post_response.text}")
            return False
        
        post_data = post_response.json()
        post_id = post_data.get('id')
        print(f"✓ Text post created successfully (ID: {post_id})")
    except Exception as e:
        print(f"✗ Post creation error: {e}")
        return False
    
    # Step 4: Verify post appears in feed
    print("\n[4/4] Verifying post in feed...")
    try:
        feed_response = requests.get(
            f"{BASE_URL}/api/posts/feed",
            headers=headers
        )
        
        if feed_response.status_code != 200:
            print(f"✗ Feed fetch failed: {feed_response.status_code}")
            return False
        
        posts = feed_response.json().get('posts', [])
        if not any(p['id'] == post_id for p in posts):
            print(f"✗ Post {post_id} not found in feed")
            return False
        
        print(f"✓ Post verified in feed")
    except Exception as e:
        print(f"✗ Feed fetch error: {e}")
        return False
    
    print("\n" + "="*60)
    print("✓ ALL TESTS PASSED!")
    print("="*60 + "\n")
    print("Summary:")
    print(f"  ✓ User registration works")
    print(f"  ✓ User login works")
    print(f"  ✓ Post creation works (no 401 errors)")
    print(f"  ✓ Posts appear in feed")
    print("\n✓ Auth token handling is now fixed!\n")
    return True

if __name__ == "__main__":
    test_post_creation()
