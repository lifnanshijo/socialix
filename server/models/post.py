from config.database import execute_query
from datetime import datetime
import base64

class Post:
    @staticmethod
    def create(user_id, content, image_data=None, image_type=None, video_data=None, video_type=None, media_type='text'):
        """Create a new post with BLOB media"""
        query = """
            INSERT INTO posts (user_id, content, image_data, image_type, video_data, video_type, media_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        post_id = execute_query(query, (user_id, content, image_data, image_type, video_data, video_type, media_type))
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
        """Update a post"""
        updates = []
        params = []
        
        if content is not None:
            updates.append("content = %s")
            params.append(content)
        if image_data is not None:
            updates.append("image_data = %s")
            params.append(image_data)
        if image_type is not None:
            updates.append("image_type = %s")
            params.append(image_type)
        if video_data is not None:
            updates.append("video_data = %s")
            params.append(video_data)
        if video_type is not None:
            updates.append("video_type = %s")
            params.append(video_type)
        
        if not updates:
            return Post.find_by_id(post_id)
        
        params.append(post_id)
        query = f"UPDATE posts SET {', '.join(updates)} WHERE id = %s"
        execute_query(query, params)
        return Post.find_by_id(post_id)

    @staticmethod
    def delete(post_id):
        """Delete a post"""
        query = "DELETE FROM posts WHERE id = %s"
        execute_query(query, (post_id,))
        return True

    @staticmethod
    def to_dict(post):
        """Convert post object to dictionary with base64 encoded media"""
        if not post:
            return None
        
        try:
            # Handle both dict and object access patterns
            def safe_get(obj, key, default=None):
                if isinstance(obj, dict):
                    return obj.get(key, default)
                return getattr(obj, key, default)
            
            # Convert BLOB media to base64
            image_url = None
            image_data = safe_get(post, 'image_data')
            if image_data:
                image_type = safe_get(post, 'image_type', 'image/jpeg')
                if isinstance(image_data, bytes):
                    image_b64 = base64.b64encode(image_data).decode('utf-8')
                    image_url = f"data:{image_type};base64,{image_b64}"
                else:
                    image_url = image_data
            
            video_url = None
            video_data = safe_get(post, 'video_data')
            if video_data:
                video_type = safe_get(post, 'video_type', 'video/mp4')
                if isinstance(video_data, bytes):
                    video_b64 = base64.b64encode(video_data).decode('utf-8')
                    video_url = f"data:{video_type};base64,{video_b64}"
                else:
                    video_url = video_data
            
            created_at = safe_get(post, 'created_at')
            updated_at = safe_get(post, 'updated_at')
            
            if isinstance(created_at, datetime):
                created_at = created_at.isoformat()
            if isinstance(updated_at, datetime):
                updated_at = updated_at.isoformat()
            
            return {
                'id': safe_get(post, 'id'),
                'userId': safe_get(post, 'user_id'),
                'content': safe_get(post, 'content'),
                'imageUrl': image_url,
                'videoUrl': video_url,
                'mediaType': safe_get(post, 'media_type', 'text'),
                'createdAt': created_at,
                'updatedAt': updated_at
            }
        except Exception as e:
            print(f"Error converting post to dict: {e}")
            raise
