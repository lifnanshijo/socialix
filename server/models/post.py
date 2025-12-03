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
        
        # Convert BLOB media to base64
        image_url = None
        if post.get('image_data'):
            image_type = post.get('image_type', 'image/jpeg')
            image_bytes = post.get('image_data')
            if isinstance(image_bytes, bytes):
                image_b64 = base64.b64encode(image_bytes).decode('utf-8')
                image_url = f"data:{image_type};base64,{image_b64}"
            else:
                image_url = image_bytes
        
        video_url = None
        if post.get('video_data'):
            video_type = post.get('video_type', 'video/mp4')
            video_bytes = post.get('video_data')
            if isinstance(video_bytes, bytes):
                video_b64 = base64.b64encode(video_bytes).decode('utf-8')
                video_url = f"data:{video_type};base64,{video_b64}"
            else:
                video_url = video_bytes
        
        return {
            'id': post['id'],
            'userId': post['user_id'],
            'content': post['content'],
            'imageUrl': image_url,
            'videoUrl': video_url,
            'mediaType': post.get('media_type', 'text'),
            'createdAt': post['created_at'].isoformat() if isinstance(post['created_at'], datetime) else post['created_at'],
            'updatedAt': post['updated_at'].isoformat() if isinstance(post['updated_at'], datetime) else post['updated_at']
        }
