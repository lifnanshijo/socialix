#!/usr/bin/env python3
"""
Migration script to add missing columns to posts table
Run this if you get: "Unknown column 'image_data' in 'field list'"
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def migrate_posts_table():
    """Add missing columns to posts table if they don't exist"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'socialmedia')
        )
        
        cursor = connection.cursor()
        
        # Check current columns in posts table
        cursor.execute("SHOW COLUMNS FROM posts")
        existing_columns = {row[0] for row in cursor.fetchall()}
        
        print("Current columns in 'posts' table:")
        for col in existing_columns:
            print(f"  - {col}")
        print()
        
        # Add missing columns
        columns_to_add = [
            ('image_data', 'ALTER TABLE posts ADD COLUMN image_data LONGBLOB'),
            ('image_type', 'ALTER TABLE posts ADD COLUMN image_type VARCHAR(50)'),
            ('video_data', 'ALTER TABLE posts ADD COLUMN video_data LONGBLOB'),
            ('video_type', 'ALTER TABLE posts ADD COLUMN video_type VARCHAR(50)'),
            ('media_type', 'ALTER TABLE posts ADD COLUMN media_type ENUM(\'text\', \'image\', \'video\') DEFAULT \'text\''),
        ]
        
        added_count = 0
        for col_name, sql in columns_to_add:
            if col_name not in existing_columns:
                print(f"Adding column: {col_name}...")
                try:
                    cursor.execute(sql)
                    connection.commit()
                    print(f"  ✓ {col_name} added successfully")
                    added_count += 1
                except Error as e:
                    print(f"  ✗ Error adding {col_name}: {e}")
            else:
                print(f"  ✓ {col_name} already exists (skipped)")
        
        print()
        print("="*60)
        if added_count > 0:
            print(f"✓ Migration completed! Added {added_count} new columns")
        else:
            print("✓ All columns already exist. No migration needed.")
        print("="*60)
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"✗ Database error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("\n" + "="*60)
    print("POSTS TABLE MIGRATION")
    print("="*60 + "\n")
    
    if migrate_posts_table():
        print("\n✓ You can now create posts with images!")
    else:
        print("\n✗ Migration failed. Check your database connection.")
