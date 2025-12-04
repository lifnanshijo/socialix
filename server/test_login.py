import requests
import json

url = "http://localhost:5000/api/auth/login"
payload = {
    "email": "lifnanshijo@gmail.com",
    "password": "testpassword"
}

print("Testing login...")
response = requests.post(url, json=payload)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
