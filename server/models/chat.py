from config.database import execute_query
from datetime import datetime

class Chat:
    @staticmethod
    def create_conversation(user1_id, user2_id):
        """Create or get existing conversation between two users"""
        # Check if conversation already exists
        query = """
            SELECT id FROM conversations 
            WHERE (user1_id = %s AND user2_id = %s) 
            OR (user1_id = %s AND user2_id = %s)
        """
        existing = execute_query(query, (user1_id, user2_id, user2_id, user1_id), fetch=True)
        
        if existing:
            return existing[0]['id']
        
        # Create new conversation
        query = """
            INSERT INTO conversations (user1_id, user2_id) 
            VALUES (%s, %s)
        """
        result = execute_query(query, (user1_id, user2_id), commit=True)
        return result
    
    @staticmethod
    def get_user_conversations(user_id):
        """Get all conversations for a user with latest message"""
        query = """
            SELECT 
                c.id,
                c.user1_id,
                c.user2_id,
                CASE 
                    WHEN c.user1_id = %s THEN u2.username
                    ELSE u1.username
                END as other_username,
                CASE 
                    WHEN c.user1_id = %s THEN c.user2_id
                    ELSE c.user1_id
                END as other_user_id,
                m.content as last_message,
                m.created_at as last_message_time,
                c.updated_at
            FROM conversations c
            LEFT JOIN users u1 ON c.user1_id = u1.id
            LEFT JOIN users u2 ON c.user2_id = u2.id
            LEFT JOIN (
                SELECT conversation_id, content, created_at
                FROM messages
                WHERE id IN (
                    SELECT MAX(id) FROM messages GROUP BY conversation_id
                )
            ) m ON c.id = m.conversation_id
            WHERE c.user1_id = %s OR c.user2_id = %s
            ORDER BY c.updated_at DESC
        """
        return execute_query(query, (user_id, user_id, user_id, user_id), fetch=True)
    
    @staticmethod
    def get_conversation_messages(conversation_id, limit=50):
        """Get messages in a conversation"""
        query = """
            SELECT 
                m.id,
                m.conversation_id,
                m.sender_id,
                m.content,
                m.created_at,
                u.username as sender_username
            FROM messages m
            JOIN users u ON m.sender_id = u.id
            WHERE m.conversation_id = %s
            ORDER BY m.created_at ASC
            LIMIT %s
        """
        return execute_query(query, (conversation_id, limit), fetch=True)
    
    @staticmethod
    def send_message(conversation_id, sender_id, content):
        """Send a message in a conversation"""
        query = """
            INSERT INTO messages (conversation_id, sender_id, content) 
            VALUES (%s, %s, %s)
        """
        result = execute_query(query, (conversation_id, sender_id, content), commit=True)
        
        # Update conversation timestamp
        update_query = "UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        execute_query(update_query, (conversation_id,), commit=True)
        
        return result
    
    @staticmethod
    def get_conversation_by_id(conversation_id):
        """Get conversation details by ID"""
        query = """
            SELECT id, user1_id, user2_id, created_at, updated_at
            FROM conversations
            WHERE id = %s
        """
        result = execute_query(query, (conversation_id,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def search_users(search_term, current_user_id):
        """Search for users to start a conversation with"""
        query = """
            SELECT id, username, email 
            FROM users 
            WHERE (username LIKE %s OR email LIKE %s) 
            AND id != %s
            LIMIT 10
        """
        search_pattern = f"%{search_term}%"
        return execute_query(query, (search_pattern, search_pattern, current_user_id), fetch=True)
