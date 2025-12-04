from config.database import get_db_connection

def check_user():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database")
        return
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, email, password FROM users WHERE email = %s", ('lifnanshijo@gmail.com',))
    user = cursor.fetchone()
    
    if user:
        print("User found:")
        print(f"  ID: {user['id']}")
        print(f"  Username: {user['username']}")
        print(f"  Email: {user['email']}")
        print(f"  Has password: {bool(user['password'])}")
        if user['password']:
            print(f"  Password hash starts with: {user['password'][:20]}...")
    else:
        print("User not found with email: lifnanshijo@gmail.com")
        print("\nAll users in database:")
        cursor.execute("SELECT id, username, email FROM users")
        users = cursor.fetchall()
        for u in users:
            print(f"  - {u['username']} ({u['email']})")
    
    cursor.close()
    conn.close()

if __name__ == '__main__':
    check_user()
