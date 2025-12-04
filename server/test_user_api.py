import requests

# Test getting user profile
BASE_URL = "http://localhost:5000/api"

# First, login to get a token
login_data = {
    "email": "lifnanshijo@gmail.com",
    "password": "testpassword"
}

print("=== Testing Login ===")
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
if response.status_code == 200:
    token = response.json().get('token')
    print(f"✓ Login successful, token received")
    
    # Test getting user 1
    print("\n=== Testing Get User 1 ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/1", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"User data: {response.json()}")
    else:
        print(f"Error: {response.json()}")
    
    # Test getting user 2
    print("\n=== Testing Get User 2 ===")
    response = requests.get(f"{BASE_URL}/users/2", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"User data: {response.json()}")
    else:
        print(f"Error: {response.json()}")
    
    # Test getting posts
    print("\n=== Testing Get Posts ===")
    response = requests.get(f"{BASE_URL}/posts/feed", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        posts = response.json().get('posts', [])
        print(f"Found {len(posts)} posts")
        for post in posts[:2]:  # Show first 2 posts
            print(f"  Post ID: {post.get('id')}, User ID: {post.get('userId')}, User: {post.get('user', {}).get('username')}")
    else:
        print(f"Error: {response.json()}")
else:
    print(f"Login failed: {response.json()}")
