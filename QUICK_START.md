# 🚀 SOCIALIX BLOB STORAGE - QUICK START GUIDE

## What Changed?
Your images are now stored **directly in the database** instead of on the filesystem!

- **Before:** Images saved as files → `uploads/` folder
- **After:** Images saved as BLOB → MySQL database

## How to Run

### Terminal 1: Backend Server
```powershell
cd d:\aura-spark\socialix\server
python app.py
```
✅ Server will start on http://127.0.0.1:5000

### Terminal 2: Frontend Server
```powershell
cd d:\aura-spark\socialix\client
npm run dev
```
✅ Frontend will start on http://localhost:3001

### Terminal 3: Test BLOB Storage (Optional)
```powershell
cd d:\aura-spark\socialix
python -X utf8 TEST_BLOB_STORAGE.py
```
✅ Comprehensive test of upload and retrieval

## How It Works

### Upload Flow
```
1. User selects image in Profile → Edit Profile
2. Image shows as preview (Base64 preview only)
3. User clicks "Save Changes"
4. File sent to backend via FormData (actual file, not Base64)
5. Backend validates file (type + size)
6. Backend reads file as binary bytes
7. Binary stored in database LONGBLOB column
8. MIME type stored in VARCHAR column
9. Response includes Base64-encoded image
10. Frontend displays image from Data URL
```

### What You Can Upload
**Profile Images:** PNG, JPG, JPEG, GIF, WebP (5MB max)
**Post Images:** PNG, JPG, JPEG, GIF, WebP (5MB max)
**Post Videos:** MP4, AVI, MOV, MKV, WebM (50MB max)

## Database Schema

### Users Table
```sql
avatar LONGBLOB              -- Binary image data
avatar_type VARCHAR(50)      -- MIME type (e.g., 'image/jpeg')
cover_image LONGBLOB         -- Binary cover image
cover_image_type VARCHAR(50) -- MIME type
```

### Posts Table
```sql
image_data LONGBLOB          -- Binary image
image_type VARCHAR(50)       -- MIME type
video_data LONGBLOB          -- Binary video
video_type VARCHAR(50)       -- MIME type
media_type ENUM(...)         -- Type: text/image/video
```

## API Endpoints

### Profile Management
- `PUT /api/users/profile` - Update profile with images
- `GET /api/users/profile` - Get current user profile
- `GET /api/users/<id>` - Get specific user

### Posts
- `POST /api/posts/create` - Create post with image/video
- `GET /api/posts/<id>` - Get specific post
- `GET /api/posts/user/<id>` - Get user's posts
- `GET /api/posts/feed` - Get all posts (paginated)
- `PUT /api/posts/<id>` - Update post
- `DELETE /api/posts/<id>` - Delete post

## Frontend Usage

### Upload Profile Image
```jsx
// ProfileCustomization.jsx handles file selection
// Profile.jsx manages file state
// AuthContext.jsx sends FormData to backend

// User flow:
1. Profile page → "Edit Profile"
2. Click avatar → Select image file
3. See preview immediately
4. Click "Save Changes"
5. Image stored in database
6. Page refreshes → Image displays from BLOB
```

### Create Post with Image
```jsx
// PostCreator.jsx handles image upload
// AuthContext.jsx sends FormData
// PostFeed.jsx displays from Base64 Data URL

// User flow:
1. Home page → "Create Post"
2. Click "📷 Photo"
3. Select image file
4. See preview
5. Add caption
6. Click "Post"
7. Image stored in database
8. Post appears in feed with image
```

## Key Files

### Backend
- `server/config/database.py` - BLOB schema definition
- `server/models/user.py` - User model with BLOB handling
- `server/models/post.py` - Post model with media BLOB
- `server/routes/user_routes.py` - Profile BLOB upload
- `server/routes/post_routes.py` - Post BLOB upload
- `server/app.py` - Flask app configured for BLOB

### Frontend
- `client/src/context/AuthContext.jsx` - FormData + JWT
- `client/src/pages/Profile.jsx` - File state management
- `client/src/components/ProfileCustomization.jsx` - Upload UI
- `client/src/components/PostCreator.jsx` - Post media UI
- `client/src/components/PostFeed.jsx` - Display BLOB images

## API Response Format

### Profile with Avatar
```json
{
  "id": 2,
  "username": "john_doe",
  "avatar": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA...",
  "coverImage": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYA..."
}
```

### Post with Image
```json
{
  "id": 1,
  "user_id": 2,
  "content": "Beautiful sunset!",
  "image_data": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYA...",
  "image_type": "image/jpeg",
  "media_type": "image"
}
```

## Troubleshooting

### Images not uploading
- Check file format is supported
- Verify file size is under limit
- Check server logs for errors
- Verify JWT token is valid

### Images not displaying
- Check browser console for errors
- Verify Base64 Data URL format
- Check MIME type is correct
- Refresh page (F5)

### Database errors
- Verify MySQL is running
- Check credentials in `.env`
- Ensure database created: `python create_db.py`
- Check tables have LONGBLOB columns

## Performance Tips

1. **Pagination** - Posts list uses pagination
2. **Compression** - Consider image optimization
3. **Caching** - Browser caches Data URLs automatically
4. **Indexing** - Foreign keys indexed for fast queries

## Security Features

✅ File type whitelist (PNG, JPG, GIF, WebP, MP4, etc.)
✅ File size enforcement (5MB images, 50MB videos)
✅ JWT authentication required
✅ User can only upload to own profile
✅ User can only edit own posts
✅ Automatic cascade delete with user

## Testing

Run the comprehensive test suite:
```bash
cd d:\aura-spark\socialix
python -X utf8 TEST_BLOB_STORAGE.py
```

Tests verify:
- ✅ User registration/login
- ✅ Profile avatar upload to BLOB
- ✅ Image retrieval as Base64
- ✅ Post creation with image BLOB
- ✅ MIME type preservation
- ✅ Database integrity

## Architecture Diagram

```
┌─────────────────┐
│   Browser UI    │
│ (React 18)      │
└────────┬────────┘
         │ FormData + File
         ↓
┌─────────────────────────┐
│  Frontend (Vite)        │
│  AuthContext            │──→ JWT Bearer Token
│  FormData with Files    │
└────────┬────────────────┘
         │ multipart/form-data
         ↓
┌──────────────────────────┐
│  Flask Backend           │
│  - Validate file         │
│  - Read as binary        │
│  - Store in LONGBLOB     │──→ MySQL
│  - Detect MIME type      │
│  - Return Base64         │
└────────┬─────────────────┘
         │ Base64 Data URL
         ↓
┌─────────────────┐
│ Browser Display │
│ <img src="..."/> │
└─────────────────┘
```

## Database Storage Example

### User with Avatar
```sql
SELECT 
  id,                    -- 2
  username,              -- 'john_doe'
  avatar,                -- [binary: 5000 bytes]
  avatar_type,           -- 'image/jpeg'
  cover_image,           -- [binary: 15000 bytes]
  cover_image_type       -- 'image/png'
FROM users 
WHERE id = 2;
```

### Post with Image
```sql
SELECT 
  id,                    -- 1
  user_id,               -- 2
  content,               -- 'Beautiful sunset!'
  image_data,            -- [binary: 8000 bytes]
  image_type,            -- 'image/jpeg'
  media_type             -- 'image'
FROM posts 
WHERE id = 1;
```

## Storage Capacity

**Example Calculations:**
- 1000 users × 2 images × 5MB = 10GB
- 10,000 posts × 1 image × 5MB = 50GB
- Include videos: Add significantly more

**Recommendations:**
- Monitor database size regularly
- Implement cleanup policies if needed
- Consider archiving old content
- Scale to larger database if needed

## Rollback (If Needed)

If you need to go back to file storage:
1. Restore from database backup
2. Update schema back to VARCHAR
3. Update Python models to use file paths
4. Restart server
5. Old images will be in database as BLOB (migrate if needed)

## Support

For issues or questions:
1. Check documentation files:
   - `DATABASE_BLOB_STORAGE.md` - Implementation details
   - `MIGRATION_GUIDE.md` - Migration procedures
   - `BLOB_STORAGE_COMPLETE.md` - Feature summary
   - `BLOB_VERIFICATION_COMPLETE.md` - Test results

2. Review test output: `TEST_BLOB_STORAGE.py`

3. Check server logs for errors

## Summary

✅ Images stored securely in MySQL database
✅ MIME types automatically preserved
✅ Base64 encoding for JSON API transport
✅ Works with existing frontend (no changes!)
✅ Full file validation and security
✅ Scalable and maintainable architecture

🚀 Your Socialix app is ready to store images in the database!
