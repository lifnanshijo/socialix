import os
from dotenv import load_dotenv

# Test 1: Load from current directory
env_path1 = os.path.join(os.path.dirname(__file__), '.env')
print(f"Test 1 - Looking for .env at: {env_path1}")
print(f"File exists: {os.path.exists(env_path1)}")

load_dotenv(env_path1)
key1 = os.getenv('SUPABASE_KEY')
print(f"Key loaded: {key1[:50] if key1 else 'None'}...")
print(f"Key length: {len(key1) if key1 else 0}")
print()

# Test 2: Load from parent directory (like the code does)
env_path2 = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
print(f"Test 2 - Looking for .env at: {env_path2}")
print(f"File exists: {os.path.exists(env_path2)}")
