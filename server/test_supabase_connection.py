from config.supabase_storage import supabase, SUPABASE_BUCKET, SUPABASE_URL, SUPABASE_KEY
import os

print("=" * 60)
print("SUPABASE CONNECTION TEST")
print("=" * 60)

print(f"\nSupabase URL: {SUPABASE_URL}")
print(f"Bucket Name: {SUPABASE_BUCKET}")
print(f"API Key (first 50 chars): {SUPABASE_KEY[:50] if SUPABASE_KEY else 'NOT SET'}...")
print(f"Supabase client initialized: {supabase is not None}")

if not supabase:
    print("\n❌ ERROR: Supabase client not initialized!")
    exit(1)

print("\n" + "=" * 60)
print("TESTING STORAGE ACCESS")
print("=" * 60)

try:
    # Test 1: List buckets
    print("\n1. Listing all storage buckets...")
    buckets = supabase.storage.list_buckets()
    print(f"   ✅ Found {len(buckets)} buckets:")
    for bucket in buckets:
        print(f"      - {bucket.name} (Public: {bucket.public})")
    
    # Test 2: Check if socialx bucket exists
    print(f"\n2. Checking if '{SUPABASE_BUCKET}' bucket exists...")
    bucket_exists = any(b.name == SUPABASE_BUCKET for b in buckets)
    if bucket_exists:
        print(f"   ✅ Bucket '{SUPABASE_BUCKET}' exists")
    else:
        print(f"   ❌ Bucket '{SUPABASE_BUCKET}' NOT found!")
        print(f"   Creating bucket '{SUPABASE_BUCKET}'...")
        try:
            supabase.storage.create_bucket(SUPABASE_BUCKET, {"public": True})
            print(f"   ✅ Bucket '{SUPABASE_BUCKET}' created successfully")
        except Exception as e:
            print(f"   ❌ Failed to create bucket: {e}")
    
    # Test 3: List files in bucket
    print(f"\n3. Listing files in '{SUPABASE_BUCKET}' bucket...")
    try:
        files = supabase.storage.from_(SUPABASE_BUCKET).list()
        print(f"   ✅ Found {len(files)} folders/files in bucket")
        for item in files[:5]:  # Show first 5
            print(f"      - {item.get('name', 'unnamed')}")
    except Exception as e:
        print(f"   ❌ Error listing files: {e}")
    
    # Test 4: Upload test file
    print(f"\n4. Testing file upload...")
    test_data = b"Hello from Social Connect!"
    test_path = "test/connection_test.txt"
    try:
        result = supabase.storage.from_(SUPABASE_BUCKET).upload(
            test_path,
            test_data,
            {"content-type": "text/plain"}
        )
        print(f"   ✅ Test file uploaded successfully")
        
        # Get public URL
        public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(test_path)
        print(f"   📁 Public URL: {public_url}")
        
        # Clean up test file
        print(f"\n5. Cleaning up test file...")
        supabase.storage.from_(SUPABASE_BUCKET).remove([test_path])
        print(f"   ✅ Test file deleted")
        
    except Exception as e:
        print(f"   ❌ Upload failed: {e}")
        print(f"   Error type: {type(e).__name__}")

except Exception as e:
    print(f"\n❌ CRITICAL ERROR: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
