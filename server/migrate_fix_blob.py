import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def migrate_to_blob():
    """Migrate existing avatar and cover_image columns to LONGBLOB type"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'shailu@2903'),
            database=os.getenv('DB_NAME', 'social_connect')
        )
        
        cursor = connection.cursor()
        
        print("Converting columns to LONGBLOB type...")
        
        # Alter avatar column to LONGBLOB
        print("\nAltering users.avatar to LONGBLOB...")
        cursor.execute("ALTER TABLE users MODIFY avatar LONGBLOB;")
        print("✓ users.avatar converted to LONGBLOB")
        
        # Alter cover_image column to LONGBLOB
        print("\nAltering users.cover_image to LONGBLOB...")
        cursor.execute("ALTER TABLE users MODIFY cover_image LONGBLOB;")
        print("✓ users.cover_image converted to LONGBLOB")
        
        # Verify changes
        print("\n\nVerifying schema changes...")
        cursor.execute("DESCRIBE users;")
        columns = cursor.fetchall()
        
        print("\nUsers table columns:")
        for col in columns:
            col_name = col[0]
            col_type = col[1]
            if col_name in ['avatar', 'cover_image', 'avatar_type', 'cover_image_type']:
                print(f"  {col_name}: {col_type}")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("\n✓ Migration completed successfully!")
        
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    migrate_to_blob()
