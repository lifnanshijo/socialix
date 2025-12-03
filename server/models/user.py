from config.database import execute_query
import bcrypt
from datetime import datetime

class User:
    @staticmethod
    def create(username, email, password, oauth_provider=None, oauth_id=None):
        """Create a new user"""
        hashed_password = None
        if password:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        query = """
            INSERT INTO users (username, email, password, oauth_provider, oauth_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        user_id = execute_query(query, (username, email, hashed_password, oauth_provider, oauth_id))
        return User.find_by_id(user_id)

    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        query = "SELECT * FROM users WHERE email = %s"
        result = execute_query(query, (email,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def find_by_username(username):
        """Find user by username"""
        query = "SELECT * FROM users WHERE username = %s"
        result = execute_query(query, (username,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        query = "SELECT * FROM users WHERE id = %s"
        result = execute_query(query, (user_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def find_by_oauth(provider, oauth_id):
        """Find user by OAuth provider and ID"""
        query = "SELECT * FROM users WHERE oauth_provider = %s AND oauth_id = %s"
        result = execute_query(query, (provider, oauth_id), fetch=True)
        return result[0] if result else None

    @staticmethod
    def verify_password(password, hashed_password):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def update_profile(user_id, username=None, bio=None, avatar=None, cover_image=None):
        """Update user profile"""
        updates = []
        params = []
        
        if username is not None and username != '':
            updates.append("username = %s")
            params.append(username)
        if bio is not None:
            updates.append("bio = %s")
            params.append(bio)
        if avatar is not None:
            updates.append("avatar = %s")
            params.append(avatar)
        if cover_image is not None:
            updates.append("cover_image = %s")
            params.append(cover_image)
        
        if not updates:
            return User.find_by_id(user_id)
        
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
        execute_query(query, params)
        return User.find_by_id(user_id)

    @staticmethod
    def to_dict(user):
        """Convert user object to dictionary (excluding password)"""
        if not user:
            return None
        return {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'bio': user.get('bio'),
            'avatar': user.get('avatar'),
            'coverImage': user.get('cover_image'),
            'createdAt': user['created_at'].isoformat() if isinstance(user['created_at'], datetime) else user['created_at']
        }
