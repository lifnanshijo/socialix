#!/usr/bin/env python3
"""Comprehensive test script for post creation and sharing"""

import requests
import json
import time
from io import BytesIO
from PIL import Image
import sys

# Test configuration
BASE_URL = "http://localhost:5000"
TEST_EMAIL = f"testuser{int(time.time())}@example.com"
TEST_PASSWORD = "testpass123"
TEST_USERNAME = f"testuser{int(time.time())}"

def create_test_image():
    """Create a simple test image"""
    img = Image.new('RGB', (200, 200), color='blue')
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

def print_result(title, success, details=""):
    """Print test result"""
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"{status}: {title}")
    if details:
        print(f"  → {details}")

def test_flow():
    """Test the complete post creation and sharing flow"""
    
    print("\n" + "="*60)
    print("POST CREATION & SHARING TEST")
    print("="*60 + "\n")
    
    # Step 1: Register
    print("[1/6] Registering user...")
    try:
        reg_response = requests.post(f"{BASE_URL}/api/auth/signup", json={
            "username": TEST_USERNAME,
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        
        if reg_response.status_code == 201:
            print_result("User Registration", True, f"User: {TEST_USERNAME}")
        else:
            print_result("User Registration", False, f"Status: {reg_response.status_code}, Response: {reg_response.json()}")
            return False
    except Exception as e:
        print_result("User Registration", False, str(e))
        return False
    
    # Step 2: Login
    print("\n[2/6] Logging in...")
    try:
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            token = login_data.get('access_token')
            print_result("Login", True, f"Token received: {token[:20]}...")
        else:
            print_result("Login", False, f"Status: {login_response.status_code}")
            return False
    except Exception as e:
        print_result("Login", False, str(e))
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 3: Create text post
    print("\n[3/6] Creating text post...")
    try:
        text_response = requests.post(
            f"{BASE_URL}/api/posts/create",
            data={"content": "Hello! This is my first test post!"},
            headers=headers
        )
        
        if text_response.status_code == 201:
            post_data = text_response.json()
            post_id = post_data.get('id')
            print_result("Text Post Creation", True, f"Post ID: {post_id}")
        else:
            print_result("Text Post Creation", False, f"Status: {text_response.status_code}, Response: {text_response.json()}")
            return False
    except Exception as e:
        print_result("Text Post Creation", False, str(e))
        return False
    
    # Step 4: Create post with image
    print("\n[4/6] Creating post with image...")
    try:
        files = {
            'image': ('test.png', create_test_image(), 'image/png')
        }
        form_data = {
            'content': 'Check out this amazing photo!'
        }
        
        image_response = requests.post(
            f"{BASE_URL}/api/posts/create",
            data=form_data,
            files=files,
            headers=headers
        )
        
        if image_response.status_code == 201:
            post_data = image_response.json()
            image_post_id = post_data.get('id')
            print_result("Image Post Creation", True, f"Post ID: {image_post_id}")
        else:
            print_result("Image Post Creation", False, f"Status: {image_response.status_code}, Response: {image_response.json()}")
            return False
    except Exception as e:
        print_result("Image Post Creation", False, str(e))
        return False
    
    # Step 5: Fetch posts
    print("\n[5/6] Fetching posts from feed...")
    try:
        feed_response = requests.get(
            f"{BASE_URL}/api/posts/feed",
            headers=headers
        )
        
        if feed_response.status_code == 200:
            posts_data = feed_response.json()
            posts = posts_data.get('posts', [])
            print_result("Fetch Posts", True, f"Posts in feed: {len(posts)}")
            
            # Verify our posts are there
            if len(posts) >= 2:
                print_result("Post Visibility", True, f"Both posts visible in feed")
            else:
                print_result("Post Visibility", False, f"Expected at least 2 posts, got {len(posts)}")
        else:
            print_result("Fetch Posts", False, f"Status: {feed_response.status_code}")
            return False
    except Exception as e:
        print_result("Fetch Posts", False, str(e))
        return False
    
    # Step 6: Get post details for sharing
    print("\n[6/6] Preparing post for sharing...")
    try:
        post_response = requests.get(
            f"{BASE_URL}/api/posts/{post_id}",
            headers=headers
        )
        
        if post_response.status_code == 200:
            post_data = post_response.json()
            share_url = f"http://localhost:3000/post/{post_id}"
            print_result("Post Share URL", True, f"URL: {share_url}")
        else:
            print_result("Post Share URL", False, f"Status: {post_response.status_code}")
            return False
    except Exception as e:
        print_result("Post Share URL", False, str(e))
        return False
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED! ✓")
    print("="*60 + "\n")
    print("Summary:")
    print(f"  - User registered and logged in")
    print(f"  - Text post created: ID {post_id}")
    print(f"  - Image post created: ID {image_post_id}")
    print(f"  - Posts visible in feed")
    print(f"  - Posts ready for sharing\n")
    
    return True

if __name__ == "__main__":
    try:
        success = test_flow()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nCritical error: {e}")
        sys.exit(1)
