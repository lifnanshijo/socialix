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
            database=os.getenv('DB_NAME', 'social_connect')
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

    connection.commit()
    cursor.close()
    connection.close()
    print("Database initialized successfully")

def execute_query(query, params=None, fetch=False):
    """Execute a query and return results if fetch=True"""
    connection = get_db_connection()
    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            connection.commit()
            return cursor.lastrowid
    except Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()
