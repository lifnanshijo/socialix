import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv('SUPABASE_KEY')
url = os.getenv('SUPABASE_URL')

print("Checking Supabase configuration...")
print(f"URL: {url}")
print(f"Key length: {len(key) if key else 0}")
print(f"Key starts with: {key[:20] if key else 'EMPTY'}...")
print(f"Key ends with: ...{key[-20:] if key else 'EMPTY'}")

# Check for whitespace
if key:
    if key != key.strip():
        print("⚠️ WARNING: Key has leading/trailing whitespace!")
    if '\n' in key or '\r' in key:
        print("⚠️ WARNING: Key contains newline characters!")
    
    # Try to decode the JWT to see the payload
    try:
        import base64
        import json
        
        parts = key.split('.')
        if len(parts) == 3:
            # Decode the payload (second part)
            payload = parts[1]
            # Add padding if needed
            padding = 4 - len(payload) % 4
            if padding != 4:
                payload += '=' * padding
            
            decoded = base64.urlsafe_b64decode(payload)
            payload_json = json.loads(decoded)
            
            print("\n✅ JWT Payload decoded successfully:")
            print(json.dumps(payload_json, indent=2))
        else:
            print(f"⚠️ JWT has {len(parts)} parts (expected 3)")
    except Exception as e:
        print(f"❌ Error decoding JWT: {e}")
