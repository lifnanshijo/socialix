import os
from supabase import create_client, Client
from dotenv import load_dotenv
import uuid
from datetime import datetime

# Load .env from parent directory (server folder)
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(env_path)

# Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_BUCKET = os.getenv('SUPABASE_BUCKET', 'social-media-files')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

def upload_file_to_supabase(file_data, file_type, folder='uploads'):
    """
    Upload a file to Supabase Storage
    
    Args:
        file_data: File binary data
        file_type: MIME type of the file (e.g., 'image/jpeg', 'video/mp4')
        folder: Folder path in the bucket (e.g., 'avatars', 'posts', 'covers')
    
    Returns:
        Public URL of the uploaded file or None if upload fails
    """
    if not supabase:
        print("Supabase client not initialized. Check your environment variables.")
        print(f"SUPABASE_URL: {SUPABASE_URL}")
        print(f"SUPABASE_KEY: {'Set' if SUPABASE_KEY else 'Not set'}")
        return None
    
    try:
        # Generate unique filename
        extension = get_extension_from_mime(file_type)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{folder}/{timestamp}_{unique_id}{extension}"
        
        print(f"Uploading to Supabase: {filename} (type: {file_type}, size: {len(file_data)} bytes)")
        
        # Upload to Supabase Storage
        response = supabase.storage.from_(SUPABASE_BUCKET).upload(
            filename,
            file_data,
            file_options={"content-type": file_type}
        )
        
        print(f"Upload response: {response}")
        
        # Get public URL
        public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(filename)
        
        print(f"File uploaded successfully. URL: {public_url}")
        return public_url
    
    except Exception as e:
        print(f"Error uploading to Supabase: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None


def delete_file_from_supabase(file_url):
    """
    Delete a file from Supabase Storage
    
    Args:
        file_url: Public URL of the file to delete
    
    Returns:
        True if deletion successful, False otherwise
    """
    if not supabase or not file_url:
        return False
    
    try:
        # Extract filename from URL
        # URL format: https://[project-ref].supabase.co/storage/v1/object/public/[bucket]/[filename]
        parts = file_url.split(f'/{SUPABASE_BUCKET}/')
        if len(parts) < 2:
            return False
        
        filename = parts[1]
        
        # Delete from Supabase Storage
        supabase.storage.from_(SUPABASE_BUCKET).remove([filename])
        
        return True
    
    except Exception as e:
        print(f"Error deleting from Supabase: {e}")
        return False


def get_extension_from_mime(mime_type):
    """Get file extension from MIME type"""
    mime_map = {
        'image/jpeg': '.jpg',
        'image/jpg': '.jpg',
        'image/png': '.png',
        'image/gif': '.gif',
        'image/webp': '.webp',
        'video/mp4': '.mp4',
        'video/mpeg': '.mpeg',
        'video/webm': '.webm',
        'video/quicktime': '.mov',
    }
    return mime_map.get(mime_type, '.bin')


def is_supabase_enabled():
    """Check if Supabase is properly configured"""
    return supabase is not None and SUPABASE_URL and SUPABASE_KEY
