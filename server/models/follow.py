from config.database import execute_query

class Follow:
    @staticmethod
    def follow_user(follower_id, following_id):
        """Follow a user"""
        if follower_id == following_id:
            return None  # Can't follow yourself
        
        query = """
            INSERT INTO followers (follower_id, following_id) 
            VALUES (%s, %s)
        """
        try:
            result = execute_query(query, (follower_id, following_id))
            return result
        except Exception as e:
            # Already following or error
            print(f"Follow error: {e}")
            return None
    
    @staticmethod
    def unfollow_user(follower_id, following_id):
        """Unfollow a user"""
        query = """
            DELETE FROM followers 
            WHERE follower_id = %s AND following_id = %s
        """
        return execute_query(query, (follower_id, following_id))
    
    @staticmethod
    def is_following(follower_id, following_id):
        """Check if user is following another user"""
        query = """
            SELECT id FROM followers 
            WHERE follower_id = %s AND following_id = %s
        """
        result = execute_query(query, (follower_id, following_id), fetch=True)
        return len(result) > 0 if result else False
    
    @staticmethod
    def get_followers_count(user_id):
        """Get number of followers for a user"""
        query = """
            SELECT COUNT(*) as count FROM followers 
            WHERE following_id = %s
        """
        result = execute_query(query, (user_id,), fetch=True)
        return result[0]['count'] if result else 0
    
    @staticmethod
    def get_following_count(user_id):
        """Get number of users a user is following"""
        query = """
            SELECT COUNT(*) as count FROM followers 
            WHERE follower_id = %s
        """
        result = execute_query(query, (user_id,), fetch=True)
        return result[0]['count'] if result else 0
    
    @staticmethod
    def get_followers(user_id):
        """Get list of followers for a user"""
        query = """
            SELECT u.id, u.username, u.email, u.bio
            FROM followers f
            JOIN users u ON f.follower_id = u.id
            WHERE f.following_id = %s
            ORDER BY f.created_at DESC
        """
        return execute_query(query, (user_id,), fetch=True)
    
    @staticmethod
    def get_following(user_id):
        """Get list of users a user is following"""
        query = """
            SELECT u.id, u.username, u.email, u.bio
            FROM followers f
            JOIN users u ON f.following_id = u.id
            WHERE f.follower_id = %s
            ORDER BY f.created_at DESC
        """
        return execute_query(query, (user_id,), fetch=True)
