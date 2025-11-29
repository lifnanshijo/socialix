from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Token is invalid or expired'}), 401
    return decorated

def get_current_user():
    """Get current user from JWT token"""
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        return User.to_dict(user)
    except:
        return None
