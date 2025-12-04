import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_follow_system():
    """Test follow/unfollow functionality"""
    
    # First, let's login to get a token
    login_response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "lifnanshijo@gmail.com",
        "password": "testpassword"
    })
    
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return
    
    token = login_response.json()['token']
    current_user_id = login_response.json()['user']['id']
    print(f"✅ Logged in as user ID: {current_user_id}")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Let's assume we want to follow user with ID 2 (if it exists)
    # First check if there are other users
    
    # Try to get user stats for user 1 (assuming there's at least 1 user)
    test_user_id = 1 if current_user_id != 1 else 2
    
    print(f"\n--- Testing with user ID: {test_user_id} ---")
    
    # Get initial stats
    stats_response = requests.get(f"{BASE_URL}/users/{test_user_id}/stats", headers=headers)
    if stats_response.status_code == 200:
        initial_stats = stats_response.json()
        print(f"\n📊 Initial Stats:")
        print(f"  Followers: {initial_stats['followers_count']}")
        print(f"  Following: {initial_stats['following_count']}")
        print(f"  Is Following: {initial_stats['is_following']}")
    else:
        print(f"❌ Failed to get stats: {stats_response.status_code}")
        print(f"Response: {stats_response.text}")
        return
    
    # Follow user
    print(f"\n🔔 Attempting to follow user {test_user_id}...")
    follow_response = requests.post(f"{BASE_URL}/users/{test_user_id}/follow", headers=headers)
    print(f"Status: {follow_response.status_code}")
    print(f"Response: {follow_response.json()}")
    
    # Get updated stats
    stats_response = requests.get(f"{BASE_URL}/users/{test_user_id}/stats", headers=headers)
    if stats_response.status_code == 200:
        updated_stats = stats_response.json()
        print(f"\n📊 After Follow Stats:")
        print(f"  Followers: {updated_stats['followers_count']}")
        print(f"  Following: {updated_stats['following_count']}")
        print(f"  Is Following: {updated_stats['is_following']}")
    
    # Unfollow user
    print(f"\n🔕 Attempting to unfollow user {test_user_id}...")
    unfollow_response = requests.post(f"{BASE_URL}/users/{test_user_id}/unfollow", headers=headers)
    print(f"Status: {unfollow_response.status_code}")
    print(f"Response: {unfollow_response.json()}")
    
    # Get final stats
    stats_response = requests.get(f"{BASE_URL}/users/{test_user_id}/stats", headers=headers)
    if stats_response.status_code == 200:
        final_stats = stats_response.json()
        print(f"\n📊 After Unfollow Stats:")
        print(f"  Followers: {final_stats['followers_count']}")
        print(f"  Following: {final_stats['following_count']}")
        print(f"  Is Following: {final_stats['is_following']}")

if __name__ == '__main__':
    test_follow_system()
