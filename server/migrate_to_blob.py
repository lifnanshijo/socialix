"""
Migration script to update users table to support BLOB image storage
"""

from config.database import get_db_connection

def migrate_to_blob():
    """Migrate users table to support BLOB images"""
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to database")
        return False

    cursor = conn.cursor()
    
    try:
        print("Starting database migration...")
        
        # Drop old columns if they exist
        try:
            cursor.execute("ALTER TABLE users DROP COLUMN avatar_type")
            print("Dropped existing avatar_type column")
        except:
            pass
        
        try:
            cursor.execute("ALTER TABLE users DROP COLUMN cover_image_type")
            print("Dropped existing cover_image_type column")
        except:
            pass
        
        # Drop old avatar and cover_image columns (they are VARCHAR)
        try:
            cursor.execute("ALTER TABLE users DROP COLUMN avatar")
            print("Dropped existing avatar column")
        except:
            pass
        
        try:
            cursor.execute("ALTER TABLE users DROP COLUMN cover_image")
            print("Dropped existing cover_image column")
        except:
            pass
        
        # Add new BLOB columns
        cursor.execute("ALTER TABLE users ADD COLUMN avatar LONGBLOB")
        print("Added avatar LONGBLOB column")
        
        cursor.execute("ALTER TABLE users ADD COLUMN avatar_type VARCHAR(50)")
        print("Added avatar_type column")
        
        cursor.execute("ALTER TABLE users ADD COLUMN cover_image LONGBLOB")
        print("Added cover_image LONGBLOB column")
        
        cursor.execute("ALTER TABLE users ADD COLUMN cover_image_type VARCHAR(50)")
        print("Added cover_image_type column")
        
        conn.commit()
        print("Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrate_to_blob()
