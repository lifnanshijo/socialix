from config.database import get_db_connection

# Check if followers table exists and is accessible
conn = get_db_connection()
if not conn:
    print("Failed to connect to database")
    exit(1)

cursor = conn.cursor(dictionary=True)

# Check table structure
print("=== Followers Table Structure ===")
cursor.execute("DESCRIBE followers")
for row in cursor.fetchall():
    print(f"  {row}")

# Check if there are any followers
print("\n=== Current Followers ===")
cursor.execute("SELECT * FROM followers")
followers = cursor.fetchall()
if followers:
    for f in followers:
        print(f"  User {f['follower_id']} follows User {f['following_id']}")
else:
    print("  No followers yet")

# Get all users
print("\n=== Available Users ===")
cursor.execute("SELECT id, username, email FROM users")
users = cursor.fetchall()
for u in users:
    print(f"  ID: {u['id']}, Username: {u['username']}, Email: {u['email']}")

cursor.close()
conn.close()
print("\n✓ Database check complete")
