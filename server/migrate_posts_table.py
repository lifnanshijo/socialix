#!/usr/bin/env python
"""Migrate posts table to add image and video columns"""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

print("Migrating posts table...")
print("-" * 50)

try:
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'socialmedia')
    )
    
    if connection.is_connected():
        cursor = connection.cursor()
        
        # Check current table structure
        cursor.execute("DESCRIBE posts")
        columns = [row[0] for row in cursor.fetchall()]
        print(f"Current columns: {', '.join(columns)}")
        
        # Add missing columns if they don't exist
        if 'image_data' not in columns:
            print("\nAdding image_data column...")
            cursor.execute("ALTER TABLE posts ADD COLUMN image_data LONGBLOB")
            print("✓ image_data column added")
        
        if 'image_type' not in columns:
            print("Adding image_type column...")
            cursor.execute("ALTER TABLE posts ADD COLUMN image_type VARCHAR(50)")
            print("✓ image_type column added")
        
        if 'video_data' not in columns:
            print("Adding video_data column...")
            cursor.execute("ALTER TABLE posts ADD COLUMN video_data LONGBLOB")
            print("✓ video_data column added")
        
        if 'video_type' not in columns:
            print("Adding video_type column...")
            cursor.execute("ALTER TABLE posts ADD COLUMN video_type VARCHAR(50)")
            print("✓ video_type column added")
        
        if 'media_type' not in columns:
            print("Adding media_type column...")
            cursor.execute("ALTER TABLE posts ADD COLUMN media_type ENUM('text', 'image', 'video') DEFAULT 'text'")
            print("✓ media_type column added")
        
        # Make content nullable if it isn't already
        cursor.execute("ALTER TABLE posts MODIFY COLUMN content TEXT NULL")
        print("✓ content column set to allow NULL")
        
        connection.commit()
        
        # Show updated structure
        cursor.execute("DESCRIBE posts")
        print("\n" + "=" * 50)
        print("Updated table structure:")
        print("=" * 50)
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} {row[2]}")
        
        cursor.close()
        connection.close()
        
        print("\n✓ Migration completed successfully!")
        
except Exception as e:
    print(f"✗ Error: {e}")
    print("\nMake sure:")
    print("  1. MySQL server is running")
    print("  2. Database 'socialmedia' exists")
    print("  3. You have ALTER permissions")
