import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Test image data (1x1 red PNG)
image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf\xc0\x00\x00\x00\x03\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'

# First, login to get token
login_response = requests.post(
    'http://localhost:5000/api/auth/login',
    json={'email': 'lifnanshijo@gmail.com', 'password': 'lifnan123'}
)

if login_response.status_code != 200:
    print("Login failed:", login_response.json())
    exit(1)

token = login_response.json()['access_token']
print(f"✅ Logged in successfully")

# Create post with image
files = {
    'image': ('test.png', image_data, 'image/png')
}
data = {
    'content': 'Test post with image using base64 fallback'
}

headers = {
    'Authorization': f'Bearer {token}'
}

response = requests.post(
    'http://localhost:5000/api/posts/create',
    files=files,
    data=data,
    headers=headers
)

print(f"\nResponse status: {response.status_code}")
print(f"Response: {response.json()}")

if response.status_code == 201:
    post_id = response.json()['post']['id']
    print(f"\n✅ Post created successfully with ID: {post_id}")
    
    # Check the post in database
    import mysql.connector
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, content, LEFT(image_url, 50) as image_preview FROM posts WHERE id = %s', (post_id,))
    post = cursor.fetchone()
    print(f"\nDatabase check:")
    print(f"  ID: {post['id']}")
    print(f"  Content: {post['content']}")
    print(f"  Image preview: {post['image_preview']}...")
    cursor.close()
    conn.close()
