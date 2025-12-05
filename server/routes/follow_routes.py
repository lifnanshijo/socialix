from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from middleware.auth import token_required
from models.follow import Follow
from models.user import User

follow_bp = Blueprint('follow', __name__)

@follow_bp.route('/<int:user_id>/follow', methods=['POST'])
@token_required
def follow_user(user_id):
    """Follow a user"""
    try:
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        
        if current_user_id == user_id:
            return jsonify({'error': 'Cannot follow yourself'}), 400
        
        result = Follow.follow_user(current_user_id, user_id)
        if result is None:
            return jsonify({'error': 'Already following or invalid user'}), 400
        
        return jsonify({'success': True, 'message': 'User followed'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@follow_bp.route('/<int:user_id>/unfollow', methods=['POST'])
@token_required
def unfollow_user(user_id):
    """Unfollow a user"""
    try:
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        
        Follow.unfollow_user(current_user_id, user_id)
        return jsonify({'success': True, 'message': 'User unfollowed'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@follow_bp.route('/<int:user_id>/followers', methods=['GET'])
@token_required
def get_followers(user_id):
    """Get followers of a user"""
    try:
        followers = Follow.get_followers(user_id)
        return jsonify({'followers': followers}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@follow_bp.route('/<int:user_id>/following', methods=['GET'])
@token_required
def get_following(user_id):
    """Get users that a user is following"""
    try:
        following = Follow.get_following(user_id)
        return jsonify({'following': following}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@follow_bp.route('/<int:user_id>/stats', methods=['GET'])
@token_required
def get_follow_stats(user_id):
    """Get follow statistics for a user"""
    try:
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        
        followers_count = Follow.get_followers_count(user_id)
        following_count = Follow.get_following_count(user_id)
        is_following = Follow.is_following(current_user_id, user_id)
        
        return jsonify({
            'followers_count': followers_count,
            'following_count': following_count,
            'is_following': is_following
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500