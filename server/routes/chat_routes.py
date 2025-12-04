from flask import Blueprint, request, jsonify
from middleware.auth import token_required
from models.chat import Chat

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/conversations', methods=['GET'])
@token_required
def get_conversations(current_user):
    """Get all conversations for current user"""
    try:
        conversations = Chat.get_user_conversations(current_user['id'])
        return jsonify({'conversations': conversations}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/conversations/<int:user_id>', methods=['POST'])
@token_required
def create_conversation(current_user, user_id):
    """Create or get conversation with another user"""
    try:
        conversation_id = Chat.create_conversation(current_user['id'], user_id)
        return jsonify({'conversation_id': conversation_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/conversations/<int:conversation_id>/messages', methods=['GET'])
@token_required
def get_messages(current_user, conversation_id):
    """Get messages in a conversation"""
    try:
        messages = Chat.get_conversation_messages(conversation_id)
        return jsonify({'messages': messages}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/conversations/<int:conversation_id>/messages', methods=['POST'])
@token_required
def send_message(current_user, conversation_id):
    """Send a message in a conversation"""
    try:
        data = request.get_json()
        content = data.get('content')
        
        if not content:
            return jsonify({'error': 'Message content is required'}), 400
        
        message_id = Chat.send_message(conversation_id, current_user['id'], content)
        return jsonify({'message_id': message_id, 'success': True}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/users/search', methods=['GET'])
@token_required
def search_users(current_user):
    """Search for users to chat with"""
    try:
        search_term = request.args.get('q', '')
        if not search_term:
            return jsonify({'users': []}), 200
        
        users = Chat.search_users(search_term, current_user['id'])
        return jsonify({'users': users}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
