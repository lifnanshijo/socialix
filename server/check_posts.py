"""
Check posts in database
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def check_posts():
    """Check posts in the database"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'socialmedia')
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Count total posts
        cursor.execute("SELECT COUNT(*) as count FROM posts")
        count = cursor.fetchone()['count']
        print(f"Total posts in database: {count}")
        
        if count > 0:
            print("\nRecent posts:")
            cursor.execute("""
                SELECT p.id, p.user_id, p.content, p.image_url, p.video_url, 
                       p.media_type, p.created_at, u.username
                FROM posts p
                LEFT JOIN users u ON p.user_id = u.id
                ORDER BY p.created_at DESC
                LIMIT 5
            """)
            
            posts = cursor.fetchall()
            for post in posts:
                print(f"\n  Post ID: {post['id']}")
                print(f"  User: {post['username']} (ID: {post['user_id']})")
                print(f"  Content: {post['content'][:50] if post['content'] else 'None'}...")
                print(f"  Image URL: {post['image_url'][:50] if post['image_url'] else 'None'}...")
                print(f"  Video URL: {post['video_url'][:50] if post['video_url'] else 'None'}...")
                print(f"  Media Type: {post['media_type']}")
                print(f"  Created: {post['created_at']}")
        else:
            print("\n❌ No posts found in database!")
            print("Try creating a post through the UI.")
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    check_posts()
