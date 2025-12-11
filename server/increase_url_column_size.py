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

cursor = conn.cursor()

print("Increasing image_url and video_url column sizes to handle base64 data URIs...")

# Increase column sizes to MEDIUMTEXT (can store up to 16MB)
# This will allow both Supabase URLs and base64 data URIs
try:
    cursor.execute("ALTER TABLE posts MODIFY COLUMN image_url MEDIUMTEXT")
    print("✅ Updated posts.image_url to MEDIUMTEXT")
except Exception as e:
    print(f"❌ Error updating posts.image_url: {e}")

try:
    cursor.execute("ALTER TABLE posts MODIFY COLUMN video_url MEDIUMTEXT")
    print("✅ Updated posts.video_url to MEDIUMTEXT")
except Exception as e:
    print(f"❌ Error updating posts.video_url: {e}")

try:
    cursor.execute("ALTER TABLE users MODIFY COLUMN avatar MEDIUMTEXT")
    print("✅ Updated users.avatar to MEDIUMTEXT")
except Exception as e:
    print(f"❌ Error updating users.avatar: {e}")

try:
    cursor.execute("ALTER TABLE users MODIFY COLUMN cover_image MEDIUMTEXT")
    print("✅ Updated users.cover_image to MEDIUMTEXT")
except Exception as e:
    print(f"❌ Error updating users.cover_image: {e}")

try:
    cursor.execute("ALTER TABLE clips MODIFY COLUMN video_url MEDIUMTEXT")
    print("✅ Updated clips.video_url to MEDIUMTEXT")
except Exception as e:
    print(f"❌ Error updating clips.video_url: {e}")

conn.commit()
cursor.close()
conn.close()

print("\n✅ Migration complete! Base64 data URIs can now be stored.")
