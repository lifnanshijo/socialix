# TEAM FIX: Bytes Encoding Errors (JSON serializable & UTF-8 decode)

## 🐛 Problems You May See

**Error 1:**
```
Object of type bytes is not JSON serializable
```

**Error 2:**
```
'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
```

These happen because:
1. MySQL returns TEXT/MEDIUMTEXT fields as bytes
2. Some users have binary image data (PNG/JPEG) stored in the database
3. Flask's `jsonify()` cannot serialize bytes, and you can't decode binary images as UTF-8 text

## ✅ Solution - Apply These 3 Changes

### **1. Fix: server/config/database.py**

Find the `execute_query` function (around line 202) and replace it with:

```python
def execute_query(query, params=None, fetch=False, commit=False):
    """Execute a query and return results if fetch=True"""
    connection = get_db_connection()
    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
            # Convert any bytes to strings in the result (only if valid UTF-8)
            if result:
                for row in result:
                    for key, value in row.items():
                        if isinstance(value, bytes):
                            try:
                                # Try to decode as UTF-8 text
                                row[key] = value.decode('utf-8')
                            except UnicodeDecodeError:
                                # If it fails, it's binary data (image, etc.) - leave as bytes
                                # This will be handled by the model's to_dict method
                                pass
            return result
        else:
            if commit or not fetch:
                connection.commit()
            return cursor.lastrowid
    except Error as e:
        print(f"Database error: {e}")
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()
```

**What changed:** Added smart bytes-to-string conversion that only decodes valid UTF-8 text, skips binary data.

---

### **2. Fix: server/models/user.py**

Find the `to_dict` method (around line 104) and replace it with:

```python
    @staticmethod
    def to_dict(user):
        """Convert user object to dictionary (excluding password)"""
        if not user:
            return None
        
        # Helper function to convert bytes to string if needed
        def safe_decode(value):
            if value is None:
                return None
            if isinstance(value, bytes):
                try:
                    # Try to decode as UTF-8 text (for URLs or text data)
                    return value.decode('utf-8')
                except UnicodeDecodeError:
                    # If it fails, it's binary image data - convert to base64 data URI
                    import base64
                    # Detect image type from magic bytes
                    if value.startswith(b'\x89PNG'):
                        mime_type = 'image/png'
                    elif value.startswith(b'\xff\xd8\xff'):
                        mime_type = 'image/jpeg'
                    elif value.startswith(b'GIF'):
                        mime_type = 'image/gif'
                    elif value.startswith(b'RIFF') and b'WEBP' in value[:12]:
                        mime_type = 'image/webp'
                    else:
                        mime_type = 'image/jpeg'  # default
                    
                    base64_data = base64.b64encode(value).decode('utf-8')
                    return f"data:{mime_type};base64,{base64_data}"
            return value
        
        # Avatar and cover_image are now URLs from Supabase (or base64 fallback)
        avatar_data = safe_decode(user.get('avatar'))
        cover_image_data = safe_decode(user.get('cover_image'))
        bio_data = safe_decode(user.get('bio'))
        
        return {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'bio': bio_data,
            'avatar': avatar_data,
            'cover_image': cover_image_data,
            'created_at': user['created_at'].isoformat() if isinstance(user['created_at'], datetime) else str(user['created_at']),
            'updated_at': user.get('updated_at').isoformat() if user.get('updated_at') and isinstance(user.get('updated_at'), datetime) else str(user.get('updated_at')) if user.get('updated_at') else None
        }
```

**What changed:** `safe_decode()` now handles binary images by converting them to base64 data URIs if UTF-8 decode fails.

---

### **3. Fix: server/models/post.py**

Find the `to_dict` method (around line 141) and replace the entire method with:

```python
    @staticmethod
    def to_dict(post):
        """Convert post object to dictionary - URLs are already stored"""
        if not post:
            return None
        
        try:
            # Handle both dict and object access patterns
            def safe_get(obj, key, default=None):
                if isinstance(obj, dict):
                    return obj.get(key, default)
                return getattr(obj, key, default)
            
            # Helper function to convert bytes to string if needed
            def safe_decode(value):
                if value is None:
                    return None
                if isinstance(value, bytes):
                    try:
                        # Try to decode as UTF-8 text (for URLs or text data)
                        return value.decode('utf-8')
                    except UnicodeDecodeError:
                        # If it fails, it's binary data - convert to base64 data URI
                        import base64
                        # Detect media type from magic bytes
                        if value.startswith(b'\x89PNG'):
                            mime_type = 'image/png'
                        elif value.startswith(b'\xff\xd8\xff'):
                            mime_type = 'image/jpeg'
                        elif value.startswith(b'GIF'):
                            mime_type = 'image/gif'
                        elif value.startswith(b'RIFF') and b'WEBP' in value[:12]:
                            mime_type = 'image/webp'
                        else:
                            mime_type = 'application/octet-stream'
                        
                        base64_data = base64.b64encode(value).decode('utf-8')
                        return f"data:{mime_type};base64,{base64_data}"
                return value
            
            # Image and video are now URLs from Supabase (or base64 fallback)
            image_url = safe_decode(safe_get(post, 'image_url'))
            video_url = safe_decode(safe_get(post, 'video_url'))
            content = safe_decode(safe_get(post, 'content'))
            
            created_at = safe_get(post, 'created_at')
            updated_at = safe_get(post, 'updated_at')
            
            if isinstance(created_at, datetime):
                created_at = created_at.isoformat()
            elif created_at:
                created_at = str(created_at)
                
            if isinstance(updated_at, datetime):
                updated_at = updated_at.isoformat()
            elif updated_at:
                updated_at = str(updated_at)
            
            return {
                'id': safe_get(post, 'id'),
                'userId': safe_get(post, 'user_id'),
                'content': content,
                'imageUrl': image_url,
                'videoUrl': video_url,
                'mediaType': safe_get(post, 'media_type', 'text'),
                'createdAt': created_at,
                'updatedAt': updated_at
            }
        except Exception as e:
            print(f"Error converting post to dict: {e}")
            raise
```

**What changed:** `safe_decode()` now handles binary media by converting to base64 data URIs if UTF-8 decode fails.

---

## 🧪 Test After Applying Fixes

Run this command to verify the fix works:

```bash
cd server
python -c "from models.user import User; user = User.find_by_email('lifnanshijo@gmail.com'); import json; print(json.dumps(User.to_dict(user), indent=2))"
```

You should see user data in JSON format without errors.

---

## 📝 Summary

**Root Causes:** 
1. MySQL connector returns TEXT fields as bytes
2. Some users have binary image data (PNG/JPEG) stored in database
3. You can't decode binary images as UTF-8 text

**Solution Approach:**
1. **Database layer**: Try to decode bytes as UTF-8, skip if it fails (leave as bytes)
2. **Model layer**: Try UTF-8 decode first, fallback to base64 data URI for binary images
3. This allows both URL strings AND legacy binary images to work

**What Gets Converted:**
- ✅ Supabase URLs (text) → Decoded as UTF-8 strings
- ✅ Legacy binary images → Converted to base64 data URIs
- ✅ Text content → Decoded as UTF-8 strings
- ✅ NULL values → Remain as None/null

**Files Modified:**
- `server/config/database.py` - 1 function (execute_query)
- `server/models/user.py` - 1 method (to_dict)
- `server/models/post.py` - 1 method (to_dict)

After applying these changes, **restart your Flask server** and both errors should be fixed! 🎉

