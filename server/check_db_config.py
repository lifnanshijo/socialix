from config.database import get_db_connection
import os
from dotenv import load_dotenv

load_dotenv()

print(f"DB_NAME from .env: {os.getenv('DB_NAME')}")
print(f"Attempting to connect...")

conn = get_db_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE()")
    current_db = cursor.fetchone()
    print(f"Connected to database: {current_db[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()
    print(f"Number of users: {user_count[0]}")
    
    cursor.close()
    conn.close()
else:
    print("Failed to connect to database")
