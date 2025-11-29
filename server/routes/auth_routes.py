from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from models.user import User
from middleware.auth import token_required, get_current_user
from google.oauth2 import id_token
from google.auth.transport import requests
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """Register a new user"""
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({'message': 'Missing required fields'}), 400

        # Check if user already exists
        if User.find_by_email(email):
            return jsonify({'message': 'Email already registered'}), 400
        
        if User.find_by_username(username):
            return jsonify({'message': 'Username already taken'}), 400

        # Create new user
        user = User.create(username, email, password)
        if not user:
            return jsonify({'message': 'Failed to create user'}), 500

        # Generate token
        access_token = create_access_token(identity=user['id'])

        return jsonify({
            'token': access_token,
            'user': User.to_dict(user)
        }), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'message': 'Missing email or password'}), 400

        # Find user
        user = User.find_by_email(email)
        if not user or not user.get('password'):
            return jsonify({'message': 'Invalid credentials'}), 401

        # Verify password
        if not User.verify_password(password, user['password']):
            return jsonify({'message': 'Invalid credentials'}), 401

        # Generate token
        access_token = create_access_token(identity=user['id'])

        return jsonify({
            'token': access_token,
            'user': User.to_dict(user)
        }), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@auth_bp.route('/google', methods=['POST'])
def google_auth():
    """Google OAuth login/signup"""
    try:
        data = request.get_json()
        credential = data.get('credential')

        if not credential:
            return jsonify({'message': 'Missing credential'}), 400

        # Verify Google token
        try:
            idinfo = id_token.verify_oauth2_token(
                credential, 
                requests.Request(), 
                os.getenv('GOOGLE_CLIENT_ID')
            )
            
            email = idinfo.get('email')
            name = idinfo.get('name')
            google_id = idinfo.get('sub')
            avatar = idinfo.get('picture')

            if not email:
                return jsonify({'message': 'Failed to get email from Google'}), 400

            # Check if user exists
            user = User.find_by_email(email)
            
            if not user:
                # Create new user with Google OAuth
                user = User.create(
                    username=name or email.split('@')[0],
                    email=email,
                    password=None,
                    oauth_provider='google',
                    oauth_id=google_id
                )
                
                # Update avatar if provided
                if avatar and user:
                    User.update_profile(user['id'], avatar=avatar)
                    user = User.find_by_id(user['id'])

            # Generate token
            access_token = create_access_token(identity=user['id'])

            return jsonify({
                'token': access_token,
                'user': User.to_dict(user)
            }), 200

        except ValueError:
            return jsonify({'message': 'Invalid Google token'}), 401

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_me():
    """Get current user"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        return jsonify(user), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
