"""
Migration script to add missing columns to posts table
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def migrate_database():
    try:
        # Connect to MySQL with credentials from .env
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'social_connect')
        )
        
        cursor = connection.cursor()
        
        # First, migrate USERS table
        print("=" * 50)
        print("Migrating USERS table...")
        print("=" * 50)
        
        cursor.execute("SHOW COLUMNS FROM users;")
        existing_user_columns = [col[0] for col in cursor.fetchall()]
        print("Existing columns in users table:", existing_user_columns)
        
        user_migrations = []
        if 'avatar_type' not in existing_user_columns:
            user_migrations.append("ALTER TABLE users ADD COLUMN avatar_type VARCHAR(50);")
        if 'cover_image_type' not in existing_user_columns:
            user_migrations.append("ALTER TABLE users ADD COLUMN cover_image_type VARCHAR(50);")
        
        print("\nStarting users table migration...")
        for migration in user_migrations:
            try:
                cursor.execute(migration)
                print(f"✓ Executed: {migration}")
            except Error as err:
                print(f"✗ Error: {err}")
        
        # Second, migrate POSTS table
        print("\n" + "=" * 50)
        print("Migrating POSTS table...")
        print("=" * 50)
        
        cursor.execute("SHOW COLUMNS FROM posts;")
        existing_columns = [col[0] for col in cursor.fetchall()]
        
        print("Existing columns in posts table:", existing_columns)
        
        # List of ALTER TABLE statements - only add if column doesn't exist
        migrations = []
        
        if 'image_data' not in existing_columns:
            migrations.append("ALTER TABLE posts ADD COLUMN image_data LONGBLOB;")
        if 'image_type' not in existing_columns:
            migrations.append("ALTER TABLE posts ADD COLUMN image_type VARCHAR(50);")
        if 'video_data' not in existing_columns:
            migrations.append("ALTER TABLE posts ADD COLUMN video_data LONGBLOB;")
        if 'video_type' not in existing_columns:
            migrations.append("ALTER TABLE posts ADD COLUMN video_type VARCHAR(50);")
        if 'media_type' not in existing_columns:
            migrations.append("ALTER TABLE posts ADD COLUMN media_type ENUM('text', 'image', 'video') DEFAULT 'text';")
        
        print("\nStarting posts table migration...")
        for migration in migrations:
            try:
                cursor.execute(migration)
                print(f"✓ Executed: {migration}")
            except Error as err:
                print(f"✗ Error: {err}")
        
        connection.commit()
        print("\n" + "=" * 50)
        print("✓ Migration completed successfully!")
        print("=" * 50)
        
        # Verify users table columns
        print("\nCurrent USERS table columns:")
        cursor.execute("SHOW COLUMNS FROM users;")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[0]} ({col[1]})")
        
        # Verify posts table columns
        print("\nCurrent POSTS table columns:")
        cursor.execute("SHOW COLUMNS FROM posts;")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[0]} ({col[1]})")
        
        cursor.close()
        connection.close()
        
    except Error as err:
        print(f"Error connecting to database: {err}")
        print("\nTroubleshooting:")
        print("1. Make sure MySQL is running")
        print("2. Update the password in this script if you have one")
        print("3. Make sure the 'social_connect' database exists")

if __name__ == "__main__":
    migrate_database()
