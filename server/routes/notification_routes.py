from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from middleware.auth import token_required
from models.notification import Notification

notification_bp = Blueprint('notifications', __name__)

@notification_bp.route('/', methods=['GET'])
@token_required
def get_notifications():
    """Get all notifications for current user"""
    try:
        user_id = get_jwt_identity()
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        limit = request.args.get('limit', 50, type=int)
        
        print(f"Fetching notifications for user_id: {user_id}")
        notifications = Notification.get_user_notifications(user_id, limit)
        print(f"Found {len(notifications)} notifications")
        
        return jsonify({'notifications': notifications}), 200
    except Exception as e:
        print(f"Error in get_notifications: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/unread-count', methods=['GET'])
@token_required
def get_unread_count():
    """Get count of unread notifications"""
    try:
        user_id = get_jwt_identity()
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        count = Notification.get_unread_count(user_id)
        print(f"Unread count for user {user_id}: {count}")
        return jsonify({'count': count}), 200
    except Exception as e:
        print(f"Error in get_unread_count: {str(e)}")
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/<int:notification_id>/read', methods=['PUT'])
@token_required
def mark_notification_read(notification_id):
    """Mark a notification as read"""
    try:
        user_id = get_jwt_identity()
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        success = Notification.mark_as_read(notification_id, user_id)
        
        if not success:
            return jsonify({'error': 'Failed to mark notification as read'}), 400
        
        return jsonify({'message': 'Notification marked as read'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/mark-all-read', methods=['PUT'])
@token_required
def mark_all_notifications_read():
    """Mark all notifications as read"""
    try:
        user_id = get_jwt_identity()
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        success = Notification.mark_all_as_read(user_id)
        
        if not success:
            return jsonify({'error': 'Failed to mark notifications as read'}), 400
        
        return jsonify({'message': 'All notifications marked as read'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/<int:notification_id>', methods=['DELETE'])
@token_required
def delete_notification(notification_id):
    """Delete a notification"""
    try:
        user_id = get_jwt_identity()
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        success = Notification.delete_notification(notification_id, user_id)
        
        if not success:
            return jsonify({'error': 'Failed to delete notification'}), 400
        
        return jsonify({'message': 'Notification deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
