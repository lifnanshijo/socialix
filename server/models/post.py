from config.database import execute_query
from config.supabase_storage import upload_file_to_supabase, delete_file_from_supabase
from datetime import datetime
import base64

class Post:
    @staticmethod
    def create(user_id, content, image_data=None, image_type=None, video_data=None, video_type=None, media_type='text'):
        """Create a new post - Upload media to Supabase or fallback to base64"""
        image_url = None
        video_url = None
        
        # Upload image to Supabase if provided
        if image_data:
            print(f"Uploading image to Supabase (type: {image_type}, size: {len(image_data)} bytes)")
            image_url = upload_file_to_supabase(image_data, image_type, 'posts')
            if not image_url:
                raise Exception("Failed to upload image to Supabase storage")
        
        # Upload video to Supabase if provided
        if video_data:
            print(f"Uploading video to Supabase (type: {video_type}, size: {len(video_data)} bytes)")
            video_url = upload_file_to_supabase(video_data, video_type, 'posts')
            if not video_url:
                raise Exception("Failed to upload video to Supabase storage")
        
        print(f"Creating post in database: image_url={image_url[:50] if image_url else None}, video_url={video_url[:50] if video_url else None}")
        
        query = """
            INSERT INTO posts (user_id, content, image_url, video_url, media_type)
            VALUES (%s, %s, %s, %s, %s)
        """
        post_id = execute_query(query, (user_id, content, image_url, video_url, media_type))
        return Post.find_by_id(post_id)

    @staticmethod
    def find_by_id(post_id):
        """Find post by ID"""
        query = "SELECT * FROM posts WHERE id = %s"
        result = execute_query(query, (post_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def find_by_user(user_id, limit=20, offset=0):
        """Find posts by user ID"""
        query = """
            SELECT * FROM posts 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """
        result = execute_query(query, (user_id, limit, offset), fetch=True)
        return result if result else []
    
    @staticmethod
    def get_user_posts(user_id, limit=20, offset=0):
        """Get posts by specific user"""
        query = """
            SELECT * FROM posts 
            WHERE user_id = %s
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """
        result = execute_query(query, (user_id, limit, offset), fetch=True)
        return result if result else []

    @staticmethod
    def get_feed(limit=20, offset=0):
        """Get all posts for feed"""
        query = """
            SELECT * FROM posts 
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """
        result = execute_query(query, (limit, offset), fetch=True)
        return result if result else []

    @staticmethod
    def update(post_id, content=None, image_data=None, image_type=None, video_data=None, video_type=None):
        """Update a post - Upload new media to Supabase if provided"""
        updates = []
        params = []
        
        # Get current post to delete old files if needed
        current_post = Post.find_by_id(post_id)
        
        if content is not None:
            updates.append("content = %s")
            params.append(content)
            
        # Handle image upload
        if image_data is not None:
            # Delete old image from Supabase if exists
            if current_post and current_post.get('image_url') and current_post.get('image_url').startswith('http'):
                delete_file_from_supabase(current_post.get('image_url'))
            
            # Upload new image
            image_url = upload_file_to_supabase(image_data, image_type, 'posts')
            if image_url:
                updates.append("image_url = %s")
                params.append(image_url)
                
        # Handle video upload
        if video_data is not None:
            # Delete old video from Supabase if exists
            if current_post and current_post.get('video_url') and current_post.get('video_url').startswith('http'):
                delete_file_from_supabase(current_post.get('video_url'))
            
            # Upload new video
            video_url = upload_file_to_supabase(video_data, video_type, 'posts')
            if video_url:
                updates.append("video_url = %s")
                params.append(video_url)
        
        if not updates:
            return Post.find_by_id(post_id)
        
        params.append(post_id)
        query = f"UPDATE posts SET {', '.join(updates)} WHERE id = %s"
        execute_query(query, params)
        return Post.find_by_id(post_id)

    @staticmethod
    def delete(post_id):
        """Delete a post and its media from Supabase"""
        # Get post to delete media files
        post = Post.find_by_id(post_id)
        if post:
            # Delete image from Supabase
            if post.get('image_url') and post.get('image_url').startswith('http'):
                delete_file_from_supabase(post.get('image_url'))
            # Delete video from Supabase
            if post.get('video_url') and post.get('video_url').startswith('http'):
                delete_file_from_supabase(post.get('video_url'))
        
        query = "DELETE FROM posts WHERE id = %s"
        execute_query(query, (post_id,))
        return True

    @staticmethod
    def to_dict(post):
        """Convert post object to dictionary - URLs are already stored"""
        if not post:
            return None
        
        try:
            # Handle both dict and object access patterns
            def safe_get(obj, key, default=None):
                if isinstance(obj, dict):
                    return obj.get(key, default)
                return getattr(obj, key, default)
            
            # Helper function to convert bytes to string if needed
            def safe_decode(value):
                if value is None:
                    return None
                if isinstance(value, bytes):
                    try:
                        # Try to decode as UTF-8 text (for URLs or text data)
                        return value.decode('utf-8')
                    except UnicodeDecodeError:
                        # If it fails, it's binary data - convert to base64 data URI
                        import base64
                        # Detect media type from magic bytes
                        if value.startswith(b'\x89PNG'):
                            mime_type = 'image/png'
                        elif value.startswith(b'\xff\xd8\xff'):
                            mime_type = 'image/jpeg'
                        elif value.startswith(b'GIF'):
                            mime_type = 'image/gif'
                        elif value.startswith(b'RIFF') and b'WEBP' in value[:12]:
                            mime_type = 'image/webp'
                        else:
                            mime_type = 'application/octet-stream'
                        
                        base64_data = base64.b64encode(value).decode('utf-8')
                        return f"data:{mime_type};base64,{base64_data}"
                return value
            
            # Image and video are now URLs from Supabase
            image_url = safe_decode(safe_get(post, 'image_url'))
            video_url = safe_decode(safe_get(post, 'video_url'))
            content = safe_decode(safe_get(post, 'content'))
            
            created_at = safe_get(post, 'created_at')
            updated_at = safe_get(post, 'updated_at')
            
            if isinstance(created_at, datetime):
                created_at = created_at.isoformat()
            elif created_at:
                created_at = str(created_at)
                
            if isinstance(updated_at, datetime):
                updated_at = updated_at.isoformat()
            elif updated_at:
                updated_at = str(updated_at)
            
            return {
                'id': safe_get(post, 'id'),
                'userId': safe_get(post, 'user_id'),
                'content': content,
                'imageUrl': image_url,
                'videoUrl': video_url,
                'mediaType': safe_get(post, 'media_type', 'text'),
                'createdAt': created_at,
                'updatedAt': updated_at
            }
        except Exception as e:
            print(f"Error converting post to dict: {e}")
            raise
