"""
Check posts table structure
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def check_table_structure():
    """Check the structure of the posts table"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'socialmedia')
        )
        
        cursor = connection.cursor()
        
        # Check posts table structure
        print("Posts table structure:")
        cursor.execute("DESCRIBE posts")
        columns = cursor.fetchall()
        
        for col in columns:
            print(f"  {col[0]}: {col[1]} (Null: {col[2]}, Key: {col[3]}, Default: {col[4]})")
        
        print("\n" + "="*50)
        
        # Check if old columns exist
        column_names = [col[0] for col in columns]
        
        if 'image_data' in column_names or 'video_data' in column_names:
            print("\n⚠️  WARNING: Old BLOB columns still exist!")
            print("You need to run the migration script.")
        elif 'image_url' in column_names and 'video_url' in column_names:
            print("\n✅ Table structure is correct (using URL columns)")
        else:
            print("\n❌ ERROR: Table structure is incorrect")
            print("Missing required columns: image_url, video_url")
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    check_table_structure()
