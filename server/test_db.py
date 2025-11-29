#!/usr/bin/env python
"""Test database connection"""
from config.database import get_db_connection, init_db

print("Testing database connection...")
print("-" * 50)

connection = get_db_connection()

if connection:
    print("✓ Database connection successful!")
    print(f"  Host: {connection.server_host}")
    print(f"  Database: {connection.database}")
    print(f"  User: {connection.user}")
    
    # Test query
    cursor = connection.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"  MySQL Version: {version[0]}")
    
    cursor.close()
    connection.close()
    
    print("\nInitializing database tables...")
    init_db()
    print("✓ Database tables created successfully!")
    
else:
    print("✗ Database connection failed!")
    print("\nPlease check:")
    print("  1. MySQL server is running")
    print("  2. Database 'socialmedia' exists")
    print("  3. Credentials in .env are correct")
