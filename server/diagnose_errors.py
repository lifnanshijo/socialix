"""
Quick diagnostic test - Run this to identify which error is occurring
"""
import sys
sys.path.insert(0, 'C:\\Users\\lifni\\social connect\\server')

from models.user import User
from models.post import Post
from config.database import execute_query
import json

print("=" * 60)
print("DIAGNOSTIC TEST - Checking for errors")
print("=" * 60)

# Test 1: User serialization (bytes error)
print("\n1. Testing User.to_dict() for bytes error...")
try:
    user = User.find_by_id(1)
    if user:
        result = User.to_dict(user)
        json.dumps(result)  # Try to serialize
        print("   ✓ User serialization works!")
    else:
        print("   ⚠ No user found with ID 1")
except Exception as e:
    print(f"   ✗ ERROR: {e}")

# Test 2: Post table structure (video_url error)
print("\n2. Checking posts table for video_url column...")
try:
    columns = execute_query('DESCRIBE posts', fetch=True)
    col_names = [c['Field'] for c in columns]
    if 'video_url' in col_names:
        print("   ✓ video_url column exists")
    else:
        print("   ✗ MISSING: video_url column not found!")
        print(f"   Current columns: {col_names}")
except Exception as e:
    print(f"   ✗ ERROR: {e}")

# Test 3: Posts query
print("\n3. Testing Post.find_by_id() query...")
try:
    posts = execute_query('SELECT * FROM posts LIMIT 1', fetch=True)
    if posts:
        post_dict = Post.to_dict(posts[0])
        json.dumps(post_dict)
        print("   ✓ Post query and serialization works!")
    else:
        print("   ⚠ No posts in database")
except Exception as e:
    print(f"   ✗ ERROR: {e}")

# Test 4: Messages table structure
print("\n4. Checking messages table for media columns...")
try:
    columns = execute_query('DESCRIBE messages', fetch=True)
    col_names = [c['Field'] for c in columns]
    has_type = 'message_type' in col_names
    has_url = 'media_url' in col_names
    
    if has_type and has_url:
        print("   ✓ message_type and media_url columns exist")
    else:
        if not has_type:
            print("   ✗ MISSING: message_type column")
        if not has_url:
            print("   ✗ MISSING: media_url column")
except Exception as e:
    print(f"   ✗ ERROR: {e}")

# Test 5: Supabase configuration
print("\n5. Checking Supabase configuration...")
try:
    import os
    from dotenv import load_dotenv
    load_dotenv('C:\\Users\\lifni\\social connect\\server\\.env')
    
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    bucket = os.getenv('SUPABASE_BUCKET')
    
    if url and key and bucket:
        print(f"   ✓ Supabase configured")
        print(f"     URL: {url}")
        print(f"     Key length: {len(key)} chars")
        print(f"     Bucket: {bucket}")
    else:
        print("   ✗ Supabase configuration incomplete!")
        if not url:
            print("     MISSING: SUPABASE_URL")
        if not key:
            print("     MISSING: SUPABASE_KEY")
        if not bucket:
            print("     MISSING: SUPABASE_BUCKET")
except Exception as e:
    print(f"   ✗ ERROR: {e}")

print("\n" + "=" * 60)
print("DIAGNOSIS COMPLETE")
print("=" * 60)
