from config.database import execute_query
from config.supabase_storage import upload_file_to_supabase, delete_file_from_supabase
import bcrypt
from datetime import datetime
import base64

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
    def update_profile(user_id, username=None, bio=None, avatar=None, avatar_type=None, cover_image=None, cover_image_type=None):
        """Update user profile - Upload images to Supabase or fallback to base64"""
        updates = []
        params = []
        
        # Get current user to delete old files if needed
        current_user = User.find_by_id(user_id)
        
        if username is not None and username != '':
            updates.append("username = %s")
            params.append(username)
        if bio is not None:
            updates.append("bio = %s")
            params.append(bio)
            
        # Handle avatar upload to Supabase
        if avatar is not None:
            # Delete old avatar from Supabase if exists
            if current_user and current_user.get('avatar') and current_user.get('avatar').startswith('http'):
                delete_file_from_supabase(current_user.get('avatar'))
            
            # Upload new avatar to Supabase
            avatar_url = upload_file_to_supabase(avatar, avatar_type, 'avatars')
            if avatar_url:
                updates.append("avatar = %s")
                params.append(avatar_url)
        
        # Handle cover image upload to Supabase
        if cover_image is not None:
            # Delete old cover image from Supabase if exists
            if current_user and current_user.get('cover_image') and current_user.get('cover_image').startswith('http'):
                delete_file_from_supabase(current_user.get('cover_image'))
            
            # Upload new cover image to Supabase
            cover_url = upload_file_to_supabase(cover_image, cover_image_type, 'covers')
            if cover_url:
                updates.append("cover_image = %s")
                params.append(cover_url)
        
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
        
        # Avatar and cover_image are now URLs from Supabase
        avatar_data = user.get('avatar') if user.get('avatar') else None
        cover_image_data = user.get('cover_image') if user.get('cover_image') else None
        
        return {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'bio': user.get('bio'),
            'avatar': avatar_data,
            'cover_image': cover_image_data,
            'created_at': user['created_at'].isoformat() if isinstance(user['created_at'], datetime) else user['created_at'],
            'updated_at': user.get('updated_at').isoformat() if isinstance(user.get('updated_at'), datetime) else user.get('updated_at')
        }
