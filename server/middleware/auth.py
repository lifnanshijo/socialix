from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user_id = int(user_id) if isinstance(user_id, str) else user_id
            user = User.find_by_id(user_id)
            
            if not user:
                return jsonify({'message': 'User not found'}), 404
            
            # Just verify the token is valid, don't pass user as parameter
            return f(*args, **kwargs)
        except Exception as e:
            print(f"Auth Error: {str(e)}")
            return jsonify({'message': 'Token is invalid or expired'}), 401
    return decorated

def get_current_user():
    """Get current user from JWT token"""
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        user = User.find_by_id(user_id)
        return User.to_dict(user)
    except:
        return None
