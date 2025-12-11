"""
Check users table structure
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def check_users_table():
    """Check the structure of the users table"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'socialmedia')
        )
        
        cursor = connection.cursor()
        
        # Check users table structure
        print("Users table structure:")
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        
        for col in columns:
            print(f"  {col[0]}: {col[1]} (Null: {col[2]}, Key: {col[3]}, Default: {col[4]})")
        
        print("\n" + "="*50)
        
        # Check if old columns exist
        column_names = [col[0] for col in columns]
        
        if 'avatar_type' in column_names or 'cover_image_type' in column_names:
            print("\n⚠️  WARNING: Old type columns still exist!")
            print("The migration may not have completed properly.")
        else:
            print("\n✅ Users table structure is correct (no type columns)")
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    check_users_table()
