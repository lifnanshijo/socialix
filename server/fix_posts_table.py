#!/usr/bin/env python
"""Fix the posts table to allow NULL content"""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

print("Fixing posts table...")
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
        
        # Alter the posts table to allow NULL content
        cursor.execute("""
            ALTER TABLE posts 
            MODIFY COLUMN content TEXT NULL
        """)
        
        connection.commit()
        print("✓ Posts table updated successfully!")
        print("  Content field now allows NULL values")
        
        cursor.close()
        connection.close()
        
except Exception as e:
    print(f"✗ Error: {e}")
    print("\nMake sure:")
    print("  1. MySQL server is running")
    print("  2. Database exists")
    print("  3. You have ALTER permissions")
