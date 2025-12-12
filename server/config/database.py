import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'socialmedia')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_db():
    """Initialize the database and create tables if they don't exist"""
    connection = get_db_connection()
    if connection is None:
        print("Failed to connect to database")
        return

    cursor = connection.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255),
            bio TEXT,
            avatar LONGBLOB,
            avatar_type VARCHAR(50),
            cover_image LONGBLOB,
            cover_image_type VARCHAR(50),
            oauth_provider VARCHAR(20),
            oauth_id VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_email (email),
            INDEX idx_username (username)
        )
    """)
    
    # Add missing columns if they don't exist (for existing databases)
    try:
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS avatar_type VARCHAR(50) AFTER avatar
        """)
    except Error:
        pass  # Column already exists
    
    try:
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS cover_image_type VARCHAR(50) AFTER cover_image
        """)
    except Error:
        pass  # Column already exists

    # Create posts table (for future use)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            content TEXT,
            image_data LONGBLOB,
            image_type VARCHAR(50),
            video_data LONGBLOB,
            video_type VARCHAR(50),
            media_type ENUM('text', 'image', 'video') DEFAULT 'text',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_user_id (user_id)
        )
    """)

    # Create likes table (for future use)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS likes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            post_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
            UNIQUE KEY unique_like (user_id, post_id)
        )
    """)

    # Create comments table (for future use)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            post_id INT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
            INDEX idx_post_id (post_id)
        )
    """)

    # Create conversations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user1_id INT NOT NULL,
            user2_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user1_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (user2_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_user1 (user1_id),
            INDEX idx_user2 (user2_id)
        )
    """)

    # Create messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            conversation_id INT NOT NULL,
            sender_id INT NOT NULL,
            content TEXT,
            message_type ENUM('text', 'image', 'voice') DEFAULT 'text',
            media_url VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
            FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_conversation (conversation_id)
        )
    """)

    # Create followers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS followers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            follower_id INT NOT NULL,
            following_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE KEY unique_follow (follower_id, following_id),
            INDEX idx_follower (follower_id),
            INDEX idx_following (following_id)
        )
    """)

    # Create clips table (for stories feature)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clips (
            clip_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            file_data LONGBLOB NOT NULL,
            file_name VARCHAR(255) NOT NULL,
            file_type VARCHAR(100) NOT NULL,
            file_size INT NOT NULL,
            caption TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            is_deleted BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_user_id (user_id),
            INDEX idx_expires_at (expires_at)
        )
    """)

    # Create notifications table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            sender_id INT NOT NULL,
            type ENUM('message', 'follow', 'like', 'comment') NOT NULL,
            content TEXT,
            reference_id INT,
            is_read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_user_id (user_id),
            INDEX idx_is_read (is_read),
            INDEX idx_created_at (created_at)
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()
    print("Database initialized successfully")

def execute_query(query, params=None, fetch=False, commit=False):
    """Execute a query and return results if fetch=True"""
    connection = get_db_connection()
    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
            # Convert any bytes to strings in the result (only if valid UTF-8)
            if result:
                for row in result:
                    for key, value in row.items():
                        if isinstance(value, bytes):
                            try:
                                # Try to decode as UTF-8 text
                                row[key] = value.decode('utf-8')
                            except UnicodeDecodeError:
                                # If it fails, it's binary data (image, etc.) - leave as bytes
                                # This will be handled by the model's to_dict method
                                pass
            return result
        else:
            if commit or not fetch:
                connection.commit()
            return cursor.lastrowid
    except Error as e:
        print(f"Database error: {e}")
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()
