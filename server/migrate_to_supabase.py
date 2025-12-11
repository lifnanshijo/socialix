"""
Migration script to convert BLOB columns to VARCHAR URL columns for Supabase storage
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def migrate_to_urls():
    """Migrate database columns from BLOB to VARCHAR for URLs"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'socialmedia')
        )
        
        cursor = connection.cursor()
        
        print("Starting migration to URL-based storage...")
        
        # Backup existing data first
        print("Creating backup tables...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users_backup AS SELECT * FROM users
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts_backup AS SELECT * FROM posts
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clips_backup AS SELECT * FROM clips
        """)
        
        # Modify users table
        print("Modifying users table...")
        
        # Check and drop avatar_type if exists
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'users' 
            AND COLUMN_NAME = 'avatar_type'
        """, (os.getenv('DB_NAME', 'socialmedia'),))
        
        if cursor.fetchone()[0] > 0:
            cursor.execute("ALTER TABLE users DROP COLUMN avatar_type")
            print("Dropped avatar_type column")
        
        # Check and drop cover_image_type if exists
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'users' 
            AND COLUMN_NAME = 'cover_image_type'
        """, (os.getenv('DB_NAME', 'socialmedia'),))
        
        if cursor.fetchone()[0] > 0:
            cursor.execute("ALTER TABLE users DROP COLUMN cover_image_type")
            print("Dropped cover_image_type column")
        
        # Modify columns to VARCHAR
        cursor.execute("""
            ALTER TABLE users
            MODIFY COLUMN avatar VARCHAR(500),
            MODIFY COLUMN cover_image VARCHAR(500)
        """)
        
        # Modify posts table
        print("Modifying posts table...")
        
        # First, check if video_url column exists, if not add it
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'posts' 
            AND COLUMN_NAME = 'video_url'
        """, (os.getenv('DB_NAME', 'socialmedia'),))
        
        result = cursor.fetchone()
        if result[0] == 0:
            print("Adding video_url column...")
            cursor.execute("""
                ALTER TABLE posts
                ADD COLUMN video_url VARCHAR(500) AFTER image_url
            """)
        
        # Now modify image_url if needed and drop old columns
        cursor.execute("""
            ALTER TABLE posts
            MODIFY COLUMN image_url VARCHAR(500),
            MODIFY COLUMN video_url VARCHAR(500)
        """)
        
        # Drop old BLOB columns one by one (safer for MySQL compatibility)
        print("Dropping old BLOB columns from posts table...")
        
        for col in ['image_data', 'image_type', 'video_data', 'video_type']:
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = 'posts' 
                AND COLUMN_NAME = %s
            """, (os.getenv('DB_NAME', 'socialmedia'), col))
            
            if cursor.fetchone()[0] > 0:
                cursor.execute(f"ALTER TABLE posts DROP COLUMN {col}")
                print(f"Dropped {col} column")
        
        # Modify clips table
        print("Modifying clips table...")
        
        # Check if video_url column exists in clips
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'clips' 
            AND COLUMN_NAME = 'video_url'
        """, (os.getenv('DB_NAME', 'socialmedia'),))
        
        result = cursor.fetchone()
        if result[0] == 0:
            print("Adding video_url column to clips...")
            cursor.execute("""
                ALTER TABLE clips
                ADD COLUMN video_url VARCHAR(500) AFTER user_id
            """)
        else:
            cursor.execute("""
                ALTER TABLE clips
                MODIFY COLUMN video_url VARCHAR(500)
            """)
        
        # Drop old BLOB column from clips
        print("Dropping old file_data column from clips table...")
        
        for col in ['file_data', 'video_type']:
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = 'clips' 
                AND COLUMN_NAME = %s
            """, (os.getenv('DB_NAME', 'socialmedia'), col))
            
            if cursor.fetchone()[0] > 0:
                cursor.execute(f"ALTER TABLE clips DROP COLUMN {col}")
                print(f"Dropped {col} column from clips")
        
        connection.commit()
        print("Migration completed successfully!")
        print("\nNote: Old BLOB data has been backed up in *_backup tables")
        print("You can drop these backup tables after verifying the migration")
        
    except Error as e:
        print(f"Error during migration: {e}")
        if connection:
            connection.rollback()
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    response = input("This will modify your database schema. Continue? (yes/no): ")
    if response.lower() == 'yes':
        migrate_to_urls()
    else:
        print("Migration cancelled.")
