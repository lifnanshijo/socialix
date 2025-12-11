from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from middleware.auth import token_required
from models.chat import Chat
from models.notification import Notification
from models.user import User
from config.supabase_storage import upload_file_to_supabase
import base64

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
    """Send a message in a conversation (text, image, or voice)"""
    try:
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        
        # Check if it's JSON or form data (for file uploads)
        if request.is_json:
            data = request.get_json()
            content = data.get('content')
            message_type = data.get('message_type', 'text')
            media_url = None
            
            # Handle base64 encoded media (voice/image)
            if message_type in ['voice', 'image'] and data.get('media_data'):
                media_data = data.get('media_data')
                file_type = data.get('file_type', 'audio/webm' if message_type == 'voice' else 'image/jpeg')
                
                # Decode base64 data
                if ',' in media_data:
                    media_data = media_data.split(',')[1]
                
                file_binary = base64.b64decode(media_data)
                
                # Upload to Supabase
                folder = 'messages/voice' if message_type == 'voice' else 'messages/images'
                media_url = upload_file_to_supabase(file_binary, file_type, folder)
                
                if not media_url:
                    return jsonify({'error': 'Failed to upload media to storage'}), 500
        else:
            # Handle multipart form data
            content = request.form.get('content')
            message_type = request.form.get('message_type', 'text')
            media_url = None
            
            # Handle file upload
            if 'file' in request.files:
                file = request.files['file']
                if file and file.filename:
                    file_data = file.read()
                    file_type = file.content_type
                    
                    # Determine folder based on message type
                    if message_type == 'voice':
                        folder = 'messages/voice'
                    elif message_type == 'image':
                        folder = 'messages/images'
                    else:
                        folder = 'messages'
                    
                    media_url = upload_file_to_supabase(file_data, file_type, folder)
                    
                    if not media_url:
                        return jsonify({'error': 'Failed to upload media to storage'}), 500
        
        # Validate message has content or media
        if not content and not media_url:
            return jsonify({'error': 'Message must have content or media'}), 400
        
        message_id = Chat.send_message(conversation_id, current_user_id, content, message_type, media_url)
        
        # Get the other user in the conversation and create notification
        conversation = Chat.get_conversation_by_id(conversation_id)
        if conversation:
            other_user_id = conversation['user2_id'] if conversation['user1_id'] == current_user_id else conversation['user1_id']
            current_user = User.find_by_id(current_user_id)
            if current_user and other_user_id:
                # Customize notification based on message type
                if message_type == 'voice':
                    notification_content = f"{current_user['username']} sent you a voice message"
                elif message_type == 'image':
                    notification_content = f"{current_user['username']} sent you an image"
                else:
                    notification_content = f"{current_user['username']} sent you a message"
                
                Notification.create_notification(
                    user_id=other_user_id,
                    sender_id=current_user_id,
                    notification_type='message',
                    content=notification_content,
                    reference_id=conversation_id
                )
        
        return jsonify({'message_id': message_id, 'success': True}), 201
    except Exception as e:
        print(f"Error in send_message: {str(e)}")
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