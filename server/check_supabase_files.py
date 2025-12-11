from config.supabase_storage import supabase

try:
    # List all files in the socialx bucket
    response = supabase.storage.from_('socialx').list('posts')
    
    print("Files in Supabase 'socialx/posts' bucket:")
    print("=" * 60)
    
    if response:
        for file in response:
            print(f"Name: {file['name']}")
            print(f"Size: {file.get('metadata', {}).get('size', 'Unknown')} bytes")
            print(f"Created: {file.get('created_at', 'Unknown')}")
            print("-" * 60)
        print(f"\nTotal files: {len(response)}")
    else:
        print("No files found in the bucket")
        
except Exception as e:
    print(f"Error accessing Supabase storage: {e}")
