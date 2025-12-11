import mysql.connector
from dotenv import load_dotenv
import os
import json

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

cursor = conn.cursor(dictionary=True)
cursor.execute('''
    SELECT p.id, u.username, p.content, 
           CASE 
               WHEN p.image_url IS NULL THEN 'NULL'
               WHEN p.image_url LIKE 'data:%' THEN CONCAT('base64 data URI (', LENGTH(p.image_url), ' chars)')
               ELSE p.image_url
           END as image_info,
           p.created_at 
    FROM posts p
    LEFT JOIN users u ON p.user_id = u.id
    ORDER BY p.created_at DESC 
    LIMIT 5
''')

posts = cursor.fetchall()
print(json.dumps(posts, indent=2, default=str))

cursor.close()
conn.close()
