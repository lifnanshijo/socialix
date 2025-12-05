from config.database import execute_query
from datetime import datetime
import base64

class Like:
    @staticmethod
    def add_like(user_id, post_id):
        """Add a like to a post"""
        query = """
            INSERT INTO likes (user_id, post_id)
            VALUES (%s, %s)
        """
        try:
            execute_query(query, (user_id, post_id))
            return True
        except:
            return False

    @staticmethod
    def remove_like(user_id, post_id):
        """Remove a like from a post"""
        query = "DELETE FROM likes WHERE user_id = %s AND post_id = %s"
        execute_query(query, (user_id, post_id))
        return True

    @staticmethod
    def get_like_count(post_id):
        """Get the number of likes for a post"""
        query = "SELECT COUNT(*) as count FROM likes WHERE post_id = %s"
        result = execute_query(query, (post_id,), fetch=True)
        return result[0]['count'] if result else 0

    @staticmethod
    def is_liked_by_user(user_id, post_id):
        """Check if a user has liked a post"""
        query = "SELECT * FROM likes WHERE user_id = %s AND post_id = %s"
        result = execute_query(query, (user_id, post_id), fetch=True)
        return len(result) > 0 if result else False

    @staticmethod
    def get_post_likes(post_id):
        """Get all users who liked a post"""
        query = """
            SELECT l.*, u.username
            FROM likes l
            JOIN users u ON l.user_id = u.id
            WHERE l.post_id = %s
            ORDER BY l.created_at DESC
        """
        return execute_query(query, (post_id,), fetch=True)


class Comment:
    @staticmethod
    def create(user_id, post_id, content):
        """Create a new comment"""
        query = """
            INSERT INTO comments (user_id, post_id, content)
            VALUES (%s, %s, %s)
        """
        comment_id = execute_query(query, (user_id, post_id, content))
        return Comment.find_by_id(comment_id)

    @staticmethod
    def find_by_id(comment_id):
        """Find comment by ID"""
        query = """
            SELECT c.*, u.username, u.avatar, u.avatar_type
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.id = %s
        """
        result = execute_query(query, (comment_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def find_by_post(post_id):
        """Get all comments for a post"""
        query = """
            SELECT c.*, u.username, u.avatar, u.avatar_type
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.post_id = %s
            ORDER BY c.created_at ASC
        """
        return execute_query(query, (post_id,), fetch=True)

    @staticmethod
    def get_comment_count(post_id):
        """Get the number of comments for a post"""
        query = "SELECT COUNT(*) as count FROM comments WHERE post_id = %s"
        result = execute_query(query, (post_id,), fetch=True)
        return result[0]['count'] if result else 0

    @staticmethod
    def delete(comment_id, user_id):
        """Delete a comment (only by owner)"""
        query = "DELETE FROM comments WHERE id = %s AND user_id = %s"
        execute_query(query, (comment_id, user_id))
        return True

    @staticmethod
    def to_dict(comment):
        """Convert comment to dictionary"""
        if not comment:
            return None
        
        # Get avatar URL
        avatar_url = 'https://via.placeholder.com/40'
        avatar = comment.get('avatar') if isinstance(comment, dict) else getattr(comment, 'avatar', None)
        if avatar:
            avatar_type = comment.get('avatar_type', 'image/jpeg') if isinstance(comment, dict) else getattr(comment, 'avatar_type', 'image/jpeg')
            if isinstance(avatar, bytes):
                avatar_b64 = base64.b64encode(avatar).decode('utf-8')
                avatar_url = f"data:{avatar_type};base64,{avatar_b64}"
            else:
                avatar_url = avatar
        
        created_at = comment['created_at'] if isinstance(comment, dict) else getattr(comment, 'created_at')
        if isinstance(created_at, datetime):
            created_at = created_at.isoformat()
        
        return {
            'id': comment['id'] if isinstance(comment, dict) else comment.id,
            'userId': comment['user_id'] if isinstance(comment, dict) else comment.user_id,
            'postId': comment['post_id'] if isinstance(comment, dict) else comment.post_id,
            'username': comment['username'] if isinstance(comment, dict) else comment.username,
            'avatar': avatar_url,
            'content': comment['content'] if isinstance(comment, dict) else comment.content,
            'createdAt': created_at
        }
