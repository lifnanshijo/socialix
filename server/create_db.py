#!/usr/bin/env python
"""Create the database"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

print("Creating database...")
print("-" * 50)

try:
    # Connect without specifying database
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', '')
    )
    
    if connection.is_connected():
        cursor = connection.cursor()
        db_name = os.getenv('DB_NAME', 'socialmedia')
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"✓ Database '{db_name}' created successfully!")
        
        # Show databases
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        print("\nAvailable databases:")
        for db in databases:
            print(f"  - {db[0]}")
        
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 50)
        print("Now initializing tables...")
        print("=" * 50)
        
        # Initialize tables
        from config.database import init_db
        init_db()
        
except Error as e:
    print(f"✗ Error: {e}")
    print("\nPlease check:")
    print("  1. MySQL server is running")
    print("  2. Credentials are correct")
    print("  3. User has permission to create databases")
