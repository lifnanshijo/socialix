from config.database import get_db_connection

def check_tables():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database")
        return
    
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    
    print("Tables in database:")
    for table in tables:
        print(f"  - {table}")
    
    if 'conversations' in tables:
        cursor.execute("DESCRIBE conversations")
        print("\nConversations table structure:")
        for row in cursor.fetchall():
            print(f"  {row}")
    
    if 'messages' in tables:
        cursor.execute("DESCRIBE messages")
        print("\nMessages table structure:")
        for row in cursor.fetchall():
            print(f"  {row}")
    
    cursor.close()
    conn.close()

if __name__ == '__main__':
    check_tables()
