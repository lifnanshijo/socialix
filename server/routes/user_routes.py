from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from models.user import User
from middleware.auth import token_required
import mimetypes
import os

user_bp = Blueprint('users', __name__)

# Configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_mime_type(filename):
    """Get MIME type of file"""
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or 'image/jpeg'

def read_image_to_blob(file):
    """Read image file and return binary data"""
    if not file or file.filename == '':
        return None, None
    
    if not allowed_file(file.filename):
        raise ValueError('File type not allowed. Use: PNG, JPG, JPEG, GIF, WebP')
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise ValueError('File size exceeds 5MB limit')
    
    # Read file content as bytes
    image_data = file.read()
    mime_type = get_mime_type(file.filename)
    
    return image_data, mime_type

@user_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """Get user profile"""
    try:
        user_id = get_jwt_identity()
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        return jsonify(User.to_dict(user)), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@user_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    """Update user profile with image uploads stored as BLOB"""
    try:
        user_id = get_jwt_identity()
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        username = request.form.get('username')
        bio = request.form.get('bio')
        avatar_blob = None
        avatar_type = None
        cover_image_blob = None
        cover_image_type = None
        
        # Get current user to preserve existing images
        current_user = User.find_by_id(user_id)
        if current_user:
            avatar_blob = current_user.get('avatar')
            avatar_type = current_user.get('avatar_type')
            cover_image_blob = current_user.get('cover_image')
            cover_image_type = current_user.get('cover_image_type')
        
        # Handle avatar upload
        if 'avatar' in request.files:
            avatar_file = request.files['avatar']
            if avatar_file and avatar_file.filename:
                avatar_blob, avatar_type = read_image_to_blob(avatar_file)
        
        # Handle cover image upload
        if 'cover_image' in request.files:
            cover_file = request.files['cover_image']
            if cover_file and cover_file.filename:
                cover_image_blob, cover_image_type = read_image_to_blob(cover_file)
        
        # Check if username is already taken by another user
        if username:
            existing_user = User.find_by_username(username)
            if existing_user and existing_user['id'] != user_id:
                return jsonify({'message': 'Username already taken'}), 400
        
        # Update profile with BLOB data
        user = User.update_profile(
            user_id, 
            username=username, 
            bio=bio, 
            avatar=avatar_blob,
            avatar_type=avatar_type,
            cover_image=cover_image_blob,
            cover_image_type=cover_image_type
        )
        
        if not user:
            return jsonify({'message': 'Failed to update profile'}), 500
        
        return jsonify(User.to_dict(user)), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    """Get user by ID"""
    try:
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        return jsonify(User.to_dict(user)), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@user_bp.route('/search', methods=['GET'])
@token_required
def search_users():
    """Search users by username"""
    try:
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({'message': 'Search query is required'}), 400
        
        print(f"Searching for users with query: {query}")
        print(f"Current user ID: {current_user_id}")
        
        # Simple search implementation (can be enhanced)
        from config.database import execute_query
        
        search_query = """
            SELECT id, username, email, bio, avatar, cover_image, created_at, updated_at
            FROM users 
            WHERE username LIKE %s AND id != %s
            LIMIT 20
        """
        users = execute_query(search_query, (f'%{query}%', current_user_id), fetch=True)
        
        print(f"Found {len(users) if users else 0} users")
        
        if not users:
            return jsonify([]), 200
        
        result = [User.to_dict(user) for user in users]
        print(f"Returning {len(result)} user results")
        
        return jsonify(result), 200
    except Exception as e:
        print(f"Search error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': str(e)}), 500

