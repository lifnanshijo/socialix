import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

cursor = conn.cursor(dictionary=True)
cursor.execute('''
    SELECT p.id, u.username, p.content, p.image_url, p.video_url, p.created_at 
    FROM posts p 
    LEFT JOIN users u ON p.user_id = u.id 
    ORDER BY p.id DESC 
    LIMIT 1
''')

post = cursor.fetchone()
if post:
    print(f"Post ID: {post['id']}")
    print(f"Username: {post['username']}")
    print(f"Content: {post['content']}")
    print(f"Image URL: {post['image_url']}")
    print(f"Video URL: {post['video_url']}")
    print(f"Created: {post['created_at']}")
else:
    print("No posts found")

cursor.close()
conn.close()
