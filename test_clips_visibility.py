#!/usr/bin/env python3
"""
Test script to verify clips are working end-to-end
"""

import sys
sys.path.insert(0, 'server')

from models.clip import Clip
from config.database import get_db_connection

def test_clips_visibility():
    """Test that clips can be retrieved and displayed"""
    print("\n" + "=" * 70)
    print("CLIPS VISIBILITY TEST")
    print("=" * 70)
    
    # Get all users
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if not users:
        print("[FAIL] No users found")
        return False
    
    print(f"\n[INFO] Found {len(users)} users:")
    for user in users:
        print(f"       ID: {user[0]}, Username: {user[1]}")
    
    # Check clips for each user
    all_clips_visible = True
    for user_id, username in users:
        clips = Clip.get_active_clips_by_user(user_id)
        if clips:
            print(f"\n[PASS] User '{username}' (ID:{user_id}) has {len(clips)} clips:")
            for clip in clips:
                print(f"       - Clip {clip['clip_id']}: {clip['file_name']}")
                print(f"         Caption: {clip.get('caption', 'No caption')}")
                print(f"         URL: {clip['file_url']}")
        else:
            print(f"\n[INFO] User '{username}' (ID:{user_id}) has no clips")
    
    # Check followers relationship
    print(f"\n[INFO] Checking followers relationships:")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.follower_id, u1.username, f.following_id, u2.username 
        FROM followers f
        JOIN users u1 ON f.follower_id = u1.id
        JOIN users u2 ON f.following_id = u2.id
    """)
    follows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if follows:
        print(f"       Found {len(follows)} follow relationships:")
        for follower_id, follower_name, following_id, following_name in follows:
            print(f"       - {follower_name} (ID:{follower_id}) follows {following_name} (ID:{following_id})")
    else:
        print(f"       No follow relationships found")
    
    print("\n" + "=" * 70)
    print("RECOMMENDATION:")
    print("=" * 70)
    print("\nTo see clips in the app:")
    print("1. Go to 'My Stories' tab to see YOUR uploaded clips")
    print("2. Go to 'Feed' tab to see clips from users you follow")
    print("3. If 'Feed' is empty, follow other users first!")
    print("\nAlternatively, directly view from backend:")
    print(f"- Each clip should be accessible at: /api/clips/{{clip_id}}/download")
    print("\n" + "=" * 70)
    
    return True

if __name__ == '__main__':
    test_clips_visibility()
