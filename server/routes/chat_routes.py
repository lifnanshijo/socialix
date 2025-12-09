from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from middleware.auth import token_required
from models.chat import Chat
from models.notification import Notification
from models.user import User

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/conversations', methods=['GET'])
@token_required
def get_conversations():
    """Get all conversations for current user"""
    try:
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        
        conversations = Chat.get_user_conversations(current_user_id)
        return jsonify({'conversations': conversations}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/conversations/<int:user_id>', methods=['POST'])
@token_required
def create_conversation(user_id):
    """Create or get conversation with another user"""
    try:
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        
        conversation_id = Chat.create_conversation(current_user_id, user_id)
        return jsonify({'conversation_id': conversation_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/conversations/<int:conversation_id>/messages', methods=['GET'])
@token_required
def get_messages(conversation_id):
    """Get messages in a conversation"""
    try:
        messages = Chat.get_conversation_messages(conversation_id)
        return jsonify({'messages': messages}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/conversations/<int:conversation_id>/messages', methods=['POST'])
@token_required
def send_message(conversation_id):
    """Send a message in a conversation"""
    try:
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        
        data = request.get_json()
        content = data.get('content')
        
        if not content:
            return jsonify({'error': 'Message content is required'}), 400
        
        message_id = Chat.send_message(conversation_id, current_user_id, content)
        
        # Get the other user in the conversation and create notification
        conversation = Chat.get_conversation_by_id(conversation_id)
        if conversation:
            other_user_id = conversation['user2_id'] if conversation['user1_id'] == current_user_id else conversation['user1_id']
            current_user = User.find_by_id(current_user_id)
            if current_user and other_user_id:
                Notification.create_notification(
                    user_id=other_user_id,
                    sender_id=current_user_id,
                    notification_type='message',
                    content=f"{current_user['username']} sent you a message",
                    reference_id=conversation_id
                )
        
        return jsonify({'message_id': message_id, 'success': True}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/users/search', methods=['GET'])
@token_required
def search_users():
    """Search for users to chat with"""
    try:
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        
        search_term = request.args.get('q', '')
        if not search_term:
            return jsonify({'users': []}), 200
        
        users = Chat.search_users(search_term, current_user_id)
        return jsonify({'users': users}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500