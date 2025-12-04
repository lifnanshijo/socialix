from config.database import execute_query
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
        """Update user profile with BLOB images"""
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
        if avatar_type is not None:
            updates.append("avatar_type = %s")
            params.append(avatar_type)
        if cover_image is not None:
            updates.append("cover_image = %s")
            params.append(cover_image)
        if cover_image_type is not None:
            updates.append("cover_image_type = %s")
            params.append(cover_image_type)
        
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
        
        # Convert BLOB images to base64 for JSON serialization
        avatar_data = None
        if user.get('avatar'):
            avatar_type = user.get('avatar_type') or 'image/jpeg'
            avatar_bytes = user.get('avatar')
            if avatar_bytes:
                try:
                    if isinstance(avatar_bytes, bytes):
                        avatar_b64 = base64.b64encode(avatar_bytes).decode('utf-8')
                        avatar_data = f"data:{avatar_type};base64,{avatar_b64}"
                    elif isinstance(avatar_bytes, str) and avatar_bytes.startswith('data:'):
                        avatar_data = avatar_bytes
                    else:
                        avatar_data = None
                except Exception as e:
                    print(f"Error encoding avatar: {e}")
                    avatar_data = None
        
        cover_image_data = None
        if user.get('cover_image'):
            cover_type = user.get('cover_image_type') or 'image/jpeg'
            cover_bytes = user.get('cover_image')
            if cover_bytes:
                try:
                    if isinstance(cover_bytes, bytes):
                        cover_b64 = base64.b64encode(cover_bytes).decode('utf-8')
                        cover_image_data = f"data:{cover_type};base64,{cover_b64}"
                    elif isinstance(cover_bytes, str) and cover_bytes.startswith('data:'):
                        cover_image_data = cover_bytes
                    else:
                        cover_image_data = None
                except Exception as e:
                    print(f"Error encoding cover_image: {e}")
                    cover_image_data = None
        
        return {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'bio': user.get('bio'),
            'avatar': avatar_data,
            'cover_image': cover_image_data,
            'avatar_type': user.get('avatar_type'),
            'cover_image_type': user.get('cover_image_type'),
            'created_at': user['created_at'].isoformat() if isinstance(user['created_at'], datetime) else user['created_at'],
            'updated_at': user.get('updated_at').isoformat() if isinstance(user.get('updated_at'), datetime) else user.get('updated_at')
        }
