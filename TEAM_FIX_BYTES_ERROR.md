# TEAM FIX: "Object of type bytes is not JSON serializable" Error

## 🐛 Problem
When logging in or fetching user data, you may see this error:
```
Object of type bytes is not JSON serializable
```

This happens because MySQL returns TEXT/MEDIUMTEXT fields as bytes, and Flask's `jsonify()` cannot convert bytes to JSON.

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
            # Convert any bytes to strings in the result
            if result:
                for row in result:
                    for key, value in row.items():
                        if isinstance(value, bytes):
                            row[key] = value.decode('utf-8')
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

**What changed:** Added automatic bytes-to-string conversion in the result processing.

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
                return value.decode('utf-8')
            return value
        
        # Avatar and cover_image are now URLs from Supabase
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

**What changed:** Added `safe_decode()` helper to convert bytes to strings for avatar, cover_image, and bio fields.

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
                    return value.decode('utf-8')
                return value
            
            # Image and video are now URLs from Supabase
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

**What changed:** Added `safe_decode()` helper for content, image_url, and video_url fields.

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

**Root Cause:** MySQL connector returns TEXT fields as bytes in some configurations.

**Solution:** Convert bytes to strings at two levels:
1. Database layer (`execute_query`) - catches all text fields
2. Model layer (`to_dict` methods) - extra safety for serialization

**Files Modified:**
- `server/config/database.py` - 1 function
- `server/models/user.py` - 1 method
- `server/models/post.py` - 1 method

After applying these changes, restart your Flask server and login should work without errors! 🎉
