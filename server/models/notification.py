from config.database import execute_query
from datetime import datetime

class Notification:
    @staticmethod
    def create_notification(user_id, sender_id, notification_type, content=None, reference_id=None):
        """Create a new notification"""
        query = """
            INSERT INTO notifications (user_id, sender_id, type, content, reference_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            result = execute_query(query, (user_id, sender_id, notification_type, content, reference_id), commit=True)
            return result
        except Exception as e:
            print(f"Error creating notification: {e}")
            return None
    
    @staticmethod
    def get_user_notifications(user_id, limit=50):
        """Get all notifications for a user"""
        query = """
            SELECT 
                n.id,
                n.user_id,
                n.sender_id,
                n.type,
                n.content,
                n.reference_id,
                n.is_read,
                n.created_at,
                u.username as sender_username
            FROM notifications n
            JOIN users u ON n.sender_id = u.id
            WHERE n.user_id = %s
            ORDER BY n.created_at DESC
            LIMIT %s
        """
        try:
            result = execute_query(query, (user_id, limit), fetch=True)
            print(f"Notification query returned: {len(result) if result else 0} rows")
            return result or []
        except Exception as e:
            print(f"Error in get_user_notifications: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    @staticmethod
    def get_unread_count(user_id):
        """Get count of unread notifications"""
        query = """
            SELECT COUNT(*) as count
            FROM notifications
            WHERE user_id = %s AND is_read = FALSE
        """
        result = execute_query(query, (user_id,), fetch=True)
        return result[0]['count'] if result else 0
    
    @staticmethod
    def mark_as_read(notification_id, user_id):
        """Mark a notification as read"""
        query = """
            UPDATE notifications
            SET is_read = TRUE
            WHERE id = %s AND user_id = %s
        """
        try:
            execute_query(query, (notification_id, user_id), commit=True)
            return True
        except Exception as e:
            print(f"Error marking notification as read: {e}")
            return False
    
    @staticmethod
    def mark_all_as_read(user_id):
        """Mark all notifications as read for a user"""
        query = """
            UPDATE notifications
            SET is_read = TRUE
            WHERE user_id = %s AND is_read = FALSE
        """
        try:
            execute_query(query, (user_id,), commit=True)
            return True
        except Exception as e:
            print(f"Error marking all notifications as read: {e}")
            return False
    
    @staticmethod
    def delete_notification(notification_id, user_id):
        """Delete a notification"""
        query = """
            DELETE FROM notifications
            WHERE id = %s AND user_id = %s
        """
        try:
            execute_query(query, (notification_id, user_id), commit=True)
            return True
        except Exception as e:
            print(f"Error deleting notification: {e}")
            return False
