#!/usr/bin/env python3
"""
Test script for clips upload functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'server'))

from datetime import datetime, timedelta
from config.database import get_db_connection
from models.clip import Clip
import jwt
import json

# Create a test JWT token
SECRET_KEY = 'your_secret_key_here'  # This should match your Flask app config

# First, let's verify the database setup
def test_database():
    print("=" * 60)
    print("TEST 1: Database Setup")
    print("=" * 60)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if clips table exists
    cursor.execute("SHOW TABLES LIKE 'clips'")
    if cursor.fetchone():
        print("[PASS] Clips table exists")
        
        # Check table structure
        cursor.execute("DESCRIBE clips")
        columns = cursor.fetchall()
        print(f"[INFO] Table has {len(columns)} columns:")
        for col in columns:
            print(f"       - {col[0]}: {col[1]}")
    else:
        print("[FAIL] Clips table does not exist")
    
    # Check if users exist for testing
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"[INFO] Database has {user_count} users")
    
    cursor.close()
    conn.close()

def test_clip_creation():
    print("\n" + "=" * 60)
    print("TEST 2: Clip Creation (Model)")
    print("=" * 60)
    
    # Get first user
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users LIMIT 1")
    user_row = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not user_row:
        print("[SKIP] No users in database to test with")
        return
    
    user_id = user_row[0]
    print(f"[INFO] Testing with user_id: {user_id}")
    
    # Test clip creation
    test_file_data = b"test image data"
    test_file_name = "test_clip.jpg"
    test_file_type = "image/jpeg"
    test_caption = "Test upload caption"
    
    result = Clip.create_clip(
        user_id,
        test_file_data,
        test_file_name,
        test_file_type,
        len(test_file_data),
        test_caption
    )
    
    if result:
        print(f"[PASS] Clip created successfully")
        print(f"       Clip ID: {result['clip_id']}")
        print(f"       Created at: {result['created_at']}")
        print(f"       Expires at: {result['expires_at']}")
    else:
        print("[FAIL] Failed to create clip")

def test_get_clips():
    print("\n" + "=" * 60)
    print("TEST 3: Retrieve Clips")
    print("=" * 60)
    
    # Get first user
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users LIMIT 1")
    user_row = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not user_row:
        print("[SKIP] No users in database to test with")
        return
    
    user_id = user_row[0]
    
    clips = Clip.get_active_clips_by_user(user_id)
    
    if clips is not None:
        print(f"[PASS] Retrieved clips for user {user_id}")
        print(f"       Total clips: {len(clips)}")
        for clip in clips[:3]:  # Show first 3
            print(f"       - Clip {clip['clip_id']}: {clip['file_name']}")
    else:
        print("[FAIL] Failed to retrieve clips")

if __name__ == '__main__':
    test_database()
    test_clip_creation()
    test_get_clips()
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)
