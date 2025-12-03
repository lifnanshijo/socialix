# Profile & Media Images - Database BLOB Storage

## Overview
Images are now stored directly in the database as BLOB (Binary Large Object) data instead of being saved as files on disk. This provides better data integrity, easier backup/restore, and centralized storage.

## What Changed

### 1. Database Schema Updates

#### Users Table
**Before:**
```sql
avatar VARCHAR(255)           -- Stored file path
cover_image VARCHAR(255)      -- Stored file path
```

**After:**
```sql
avatar LONGBLOB               -- Binary image data
avatar_type VARCHAR(50)       -- MIME type (image/jpeg, image/png, etc.)
cover_image LONGBLOB          -- Binary image data
cover_image_type VARCHAR(50)  -- MIME type
```

#### Posts Table
**Before:**
```sql
image_url VARCHAR(255)        -- File path
```

**After:**
```sql
image_data LONGBLOB           -- Binary image data
image_type VARCHAR(50)        -- MIME type
video_data LONGBLOB           -- Binary video data
video_type VARCHAR(50)        -- MIME type
media_type ENUM('text', 'image', 'video')
```

### 2. Backend Changes

**User Routes (`server/routes/user_routes.py`)**
- No more file system operations
- Images are read as bytes and stored directly in database
- MIME type is automatically detected and stored
- File size validation before storing (5MB max for profile images)

**User Model (`server/models/user.py`)**
- `update_profile()` now accepts binary image data
- `to_dict()` converts BLOB data to Base64 Data URLs for JSON response
- Returns images in format: `data:image/jpeg;base64,{base64_encoded_image}`

**Post Routes (`server/routes/post_routes.py`)** - NEW
- Handles both image and video uploads as BLOB data
- Image limit: 5MB
- Video limit: 50MB
- Stores MIME type for each media file

**Post Model (`server/models/post.py`)** - NEW
- Complete CRUD operations for posts
- Handles BLOB media storage
- Converts BLOB to Base64 Data URLs for response

### 3. Frontend Changes

The frontend remains mostly the same, as it already uses:
- FileReader API to read files as Base64
- Form submission with file objects
- Image display using Data URLs

When images come back from the API, they're already Base64-encoded Data URLs, so no changes needed in the UI layer.

## How It Works

### Profile Image Upload Flow

```
1. User selects image file
   ↓
2. Frontend sends as FormData with Authorization
   ↓
3. Backend receives file (multipart/form-data)
   ↓
4. Backend reads file as bytes:
   - Validates file type (PNG, JPG, GIF, WebP)
   - Validates file size (< 5MB)
   ↓
5. Backend stores in database:
   - Image bytes in `avatar` BLOB column
   - MIME type in `avatar_type` column
   ↓
6. Backend returns user object with:
   - avatar: "data:image/jpeg;base64,{base64_data}"
   - avatarType: "image/jpeg"
   ↓
7. Frontend displays image using Data URL
```

### Database Storage Example

```
User Record:
│
├─ id: 1
├─ username: "john_doe"
├─ email: "john@example.com"
├─ avatar: [LONGBLOB - 234,567 bytes of image data]
├─ avatar_type: "image/jpeg"
├─ cover_image: [LONGBLOB - 567,890 bytes of image data]
├─ cover_image_type: "image/png"
└─ bio: "Software developer"
```

When retrieved and sent to client:
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "avatar": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDA...",
  "coverImage": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB...",
  "bio": "Software developer"
}
```

## Implementation Details

### MIME Type Detection

```python
def get_mime_type(filename, file_type='image'):
    """Get MIME type of file"""
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or 'image/jpeg'  # Default fallback
```

Common MIME types:
- `image/jpeg` - JPG/JPEG files
- `image/png` - PNG files
- `image/gif` - GIF files
- `image/webp` - WebP files
- `video/mp4` - MP4 videos
- `video/quicktime` - MOV videos

### Base64 Encoding

```python
import base64

# Store in database (receives bytes)
avatar_bytes = file.read()
# Stored directly in BLOB column

# Retrieve from database and convert to Data URL
avatar_bytes = user.get('avatar')
if isinstance(avatar_bytes, bytes):
    avatar_b64 = base64.b64encode(avatar_bytes).decode('utf-8')
    avatar_data = f"data:{avatar_type};base64,{avatar_b64}"
```

### Supported File Types

**Images:**
- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- WebP (.webp)

**Videos:**
- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)
- WebM (.webm)

### File Size Limits

- Profile images: 5MB
- Post images: 5MB
- Post videos: 50MB
- Max request size: 50MB

## Database Migration

If upgrading from file-based storage:

### Option 1: Fresh Database
```bash
# Run the updated schema
python create_db.py
```

### Option 2: Update Existing Database
```sql
-- Backup existing data
ALTER TABLE users 
ADD COLUMN avatar_new LONGBLOB DEFAULT NULL,
ADD COLUMN avatar_type VARCHAR(50) DEFAULT NULL,
ADD COLUMN cover_image_new LONGBLOB DEFAULT NULL,
ADD COLUMN cover_image_type VARCHAR(50) DEFAULT NULL;

-- Drop old columns after migration
ALTER TABLE users DROP COLUMN avatar, DROP COLUMN cover_image;

-- Rename new columns
ALTER TABLE users 
CHANGE COLUMN avatar_new avatar LONGBLOB,
CHANGE COLUMN cover_image_new cover_image LONGBLOB;
```

## API Changes

### Profile Update Endpoint

**Request:**
```
PUT /api/users/profile
Content-Type: multipart/form-data
Authorization: Bearer {token}

Form Data:
- username: "john_doe"
- bio: "My bio"
- avatar: [File object]        # Optional
- cover_image: [File object]   # Optional
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "bio": "My bio",
  "avatar": "data:image/jpeg;base64,/9j/4AAQSkZJRgABA...",
  "coverImage": "data:image/png;base64,iVBORw0KGgo...",
  "createdAt": "2025-12-03T10:30:00"
}
```

### Create Post Endpoint

**Request:**
```
POST /api/posts/create
Content-Type: multipart/form-data
Authorization: Bearer {token}

Form Data:
- content: "Check out this photo!"
- image: [File object]    # Optional
- video: [File object]    # Optional
```

**Response:**
```json
{
  "id": 5,
  "userId": 1,
  "content": "Check out this photo!",
  "mediaType": "image",
  "imageUrl": "data:image/jpeg;base64,/9j/4AAQSkZJRgABA...",
  "createdAt": "2025-12-03T13:45:30"
}
```

## Advantages

✅ **Centralized Storage** - All data in one place
✅ **Better Backup** - Database backups include all user images
✅ **No File System Issues** - No permission/path problems
✅ **Easier Deployment** - No need to manage upload folders
✅ **ACID Compliance** - Transactional consistency
✅ **Simplified Data Portability** - Export/import entire database
✅ **Better Security** - Images not exposed via HTTP paths
✅ **Automatic Cleanup** - Delete user → all images deleted automatically

## Disadvantages & Mitigations

❌ **Larger Database Size**
- ✅ Mitigation: Use image compression before upload
- ✅ Mitigation: Set storage quotas per user
- ✅ Mitigation: Archive old posts to separate storage

❌ **Slower Queries** (if loading many images)
- ✅ Mitigation: Implement pagination in frontend
- ✅ Mitigation: Cache Base64 URLs in frontend
- ✅ Mitigation: Use CDN for frequently accessed images

❌ **Network Bandwidth**
- ✅ Mitigation: Load images on-demand, not in lists
- ✅ Mitigation: Implement progressive image loading
- ✅ Mitigation: Compress images before upload

## Performance Tips

1. **Image Compression**
   ```javascript
   // Compress image before upload
   canvas.toBlob(blob => {
     // Upload compressed blob
   }, 'image/jpeg', 0.8);  // 80% quality
   ```

2. **Lazy Loading**
   ```javascript
   // Don't load all user images at once
   // Fetch image only when user scrolls to it
   ```

3. **Pagination**
   ```
   GET /api/posts/user/1?page=1  // Load 20 posts
   GET /api/posts/user/1?page=2  // Load next 20
   ```

## Troubleshooting

### Images appear corrupted
- Check MIME type is correct
- Ensure binary data wasn't corrupted during transfer
- Verify Base64 encoding is valid

### Slow image loading
- Consider implementing caching
- Use image compression
- Load images in background

### Database getting too large
- Implement image compression
- Archive old posts
- Consider hybrid approach (old in DB, new on CDN)

### Migration issues
- Backup original database first
- Test migration on copy first
- Use transaction for atomicity

## Future Enhancements

1. **Image Resizing** - Generate thumbnails
2. **CDN Integration** - Serve images from CDN
3. **Cloud Storage** - Move to AWS S3, Google Cloud
4. **Image Compression** - Compress on upload
5. **Watermarking** - Add watermarks to images
6. **EXIF Removal** - Strip metadata for privacy
7. **Image Optimization** - Serve multiple formats (WebP, etc.)

## References

- MySQL BLOB: https://dev.mysql.com/doc/refman/8.0/en/blob.html
- Base64 Encoding: https://developer.mozilla.org/en-US/docs/Web/API/FileReader
- MIME Types: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
- Data URLs: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs
