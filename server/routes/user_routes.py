from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from models.user import User
from middleware.auth import token_required

user_bp = Blueprint('users', __name__)

@user_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """Get user profile"""
    try:
        user_id = get_jwt_identity()
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
