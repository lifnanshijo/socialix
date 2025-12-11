"""
Test Supabase connection
"""
import os
from dotenv import load_dotenv

# Load environment first with explicit path
env_file = os.path.join(os.path.dirname(__file__), '.env')
print(f"Loading .env from: {env_file}")
load_dotenv(dotenv_path=env_file, override=True)

print(f"Current directory: {os.getcwd()}")
print(f".env file exists: {os.path.exists('.env')}")
print(f"SUPABASE_URL from os.getenv: {repr(os.getenv('SUPABASE_URL'))}")
print(f"SUPABASE_KEY from os.getenv: {repr(os.getenv('SUPABASE_KEY')[:20] if os.getenv('SUPABASE_KEY') else None)}...")

# Also try reading the file directly
with open('.env', 'r') as f:
    lines = [line for line in f.readlines() if 'SUPABASE' in line]
    print(f"\nSUPABASE lines in .env file:")
    for line in lines:
        print(f"  {line.strip()}")

from config.supabase_storage import is_supabase_enabled, upload_file_to_supabase, SUPABASE_URL, SUPABASE_KEY, SUPABASE_BUCKET

def test_supabase():
    print("Testing Supabase Configuration...")
    print(f"SUPABASE_URL: {SUPABASE_URL}")
    print(f"SUPABASE_KEY: {'Set (' + str(len(SUPABASE_KEY)) + ' chars)' if SUPABASE_KEY else 'Not set'}")
    print(f"SUPABASE_BUCKET: {SUPABASE_BUCKET}")
    print(f"Supabase Enabled: {is_supabase_enabled()}")
    
    if not is_supabase_enabled():
        print("\n❌ Supabase is not properly configured!")
        print("Check your .env file for SUPABASE_URL and SUPABASE_KEY")
        return
    
    print("\n✅ Supabase is configured!")
    print("\nTesting file upload...")
    
    # Create a small test image (1x1 red pixel PNG)
    test_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf\xc0\x00\x00\x00\x03\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
    
    try:
        url = upload_file_to_supabase(test_image, 'image/png', 'test')
        if url:
            print(f"\n✅ Test upload successful!")
            print(f"URL: {url}")
            print("\nYour Supabase storage is working correctly! 🎉")
        else:
            print("\n❌ Upload failed - check the error messages above")
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_supabase()
