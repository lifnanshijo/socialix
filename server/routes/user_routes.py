from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from models.user import User
from middleware.auth import token_required
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import mimetypes

user_bp = Blueprint('users', __name__)

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_upload_file(file, subfolder):
    """Save uploaded file and return the path"""
    if not file or file.filename == '':
        return None
    
    if not allowed_file(file.filename):
        raise ValueError('File type not allowed. Use: PNG, JPG, JPEG, GIF, WebP')
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise ValueError('File size exceeds 5MB limit')
    
    # Create folder if it doesn't exist
    folder_path = os.path.join(UPLOAD_FOLDER, subfolder)
    os.makedirs(folder_path, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
    filename = secure_filename(file.filename)
    filename = timestamp + filename
    
    # Save file
    filepath = os.path.join(folder_path, filename)
    file.save(filepath)
    
    # Return relative path for storage in database
    return f'/uploads/{subfolder}/{filename}'

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
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        data = request.get_json()
        
        username = data.get('username')
        bio = data.get('bio')
        avatar = data.get('avatar')
        cover_image = data.get('coverImage')
        
        # Check if username is already taken by another user
        if username:
            existing_user = User.find_by_username(username)
            if existing_user and existing_user['id'] != user_id:
                return jsonify({'message': 'Username already taken'}), 400
        
        # Update profile
        user = User.update_profile(user_id, username, bio, avatar, cover_image)
        
        if not user:
            return jsonify({'message': 'Failed to update profile'}), 500
        
        return jsonify(User.to_dict(user)), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    try:
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        return jsonify(User.to_dict(user)), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@user_bp.route('/profile/upload-avatar', methods=['POST'])
@token_required
def upload_avatar():
    """Upload user avatar image"""
    try:
        user_id = get_jwt_identity()
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        if 'file' not in request.files:
            return jsonify({'message': 'No file provided'}), 400
        
        file = request.files['file']
        avatar_path = save_upload_file(file, 'avatars')
        
        # Update user profile with new avatar
        user = User.update_profile(user_id, avatar=avatar_path)
        
        if not user:
            return jsonify({'message': 'Failed to update avatar'}), 500
        
        return jsonify({
            'message': 'Avatar uploaded successfully',
            'user': User.to_dict(user)
        }), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@user_bp.route('/profile/upload-cover', methods=['POST'])
@token_required
def upload_cover():
    """Upload user cover image"""
    try:
        user_id = get_jwt_identity()
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        if 'file' not in request.files:
            return jsonify({'message': 'No file provided'}), 400
        
        file = request.files['file']
        cover_path = save_upload_file(file, 'covers')
        
        # Update user profile with new cover image
        user = User.update_profile(user_id, cover_image=cover_path)
        
        if not user:
            return jsonify({'message': 'Failed to update cover image'}), 500
        
        return jsonify({
            'message': 'Cover image uploaded successfully',
            'user': User.to_dict(user)
        }), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@user_bp.route('/search', methods=['GET'])
def search_users():
    """Search users by username"""
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({'message': 'Search query is required'}), 400
        
        # Simple search implementation (can be enhanced)
        from config.database import execute_query
        
        search_query = """
            SELECT * FROM users 
            WHERE username LIKE %s 
            LIMIT 20
        """
        users = execute_query(search_query, (f'%{query}%',), fetch=True)
        
        return jsonify([User.to_dict(user) for user in users]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
