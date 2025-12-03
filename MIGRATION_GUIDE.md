# Database BLOB Storage - Migration Guide

## Summary of Changes

✅ Profile images (avatar, cover) now stored as BLOB in database
✅ Post images and videos now stored as BLOB in database
✅ MIME types stored alongside images for proper display
✅ Base64-encoded Data URLs returned in API responses
✅ No more file system management needed

## Step-by-Step Migration

### Step 1: Backup Current Database
```bash
# MySQL backup
mysqldump -u root -p social_connect > backup_social_connect.sql

# Keep backup safe!
```

### Step 2: Update Database Schema

**Option A: Fresh Database (Recommended for testing)**
```bash
cd server
python create_db.py  # Runs updated schema.sql
```

**Option B: Migrate Existing Database**
```sql
-- Run these SQL commands

-- Add new BLOB columns
ALTER TABLE users 
ADD COLUMN avatar_new LONGBLOB DEFAULT NULL,
ADD COLUMN avatar_type VARCHAR(50) DEFAULT NULL,
ADD COLUMN cover_image_new LONGBLOB DEFAULT NULL,
ADD COLUMN cover_image_type VARCHAR(50) DEFAULT NULL;

-- Rename columns (old data becomes NULL, that's okay)
ALTER TABLE users 
DROP COLUMN avatar,
DROP COLUMN cover_image,
CHANGE COLUMN avatar_new avatar LONGBLOB,
CHANGE COLUMN cover_image_new cover_image LONGBLOB;

-- Update posts table
ALTER TABLE posts
ADD COLUMN image_data LONGBLOB DEFAULT NULL,
ADD COLUMN image_type VARCHAR(50) DEFAULT NULL,
ADD COLUMN video_data LONGBLOB DEFAULT NULL,
ADD COLUMN video_type VARCHAR(50) DEFAULT NULL;

-- Modify existing column
ALTER TABLE posts
MODIFY media_type ENUM('text', 'image', 'video') DEFAULT 'text';

-- Drop old URL column if exists
ALTER TABLE posts DROP COLUMN image_url;
```

### Step 3: Verify Schema

```sql
-- Check users table structure
DESCRIBE users;

-- Output should show:
-- avatar              | LONGBLOB
-- avatar_type        | VARCHAR(50)
-- cover_image        | LONGBLOB
-- cover_image_type   | VARCHAR(50)

-- Check posts table structure
DESCRIBE posts;

-- Output should show:
-- image_data         | LONGBLOB
-- image_type        | VARCHAR(50)
-- video_data        | LONGBLOB
-- video_type        | VARCHAR(50)
-- media_type        | ENUM('text','image','video')
```

### Step 4: Update Backend Code

The following files have been updated:
- ✅ `server/models/user.py` - Handles BLOB image data
- ✅ `server/models/post.py` - NEW: Handles post media
- ✅ `server/routes/user_routes.py` - Updated for BLOB storage
- ✅ `server/routes/post_routes.py` - NEW: Post creation with BLOB
- ✅ `server/app.py` - Registered post routes

### Step 5: Restart Backend Server

```bash
# Stop current server (Ctrl+C in terminal)

# Restart with new code
cd server
python app.py

# Should see: "Database initialized successfully"
# And: "Running on http://127.0.0.1:5000"
```

### Step 6: Test Profile Image Upload

1. **Login to frontend** (http://localhost:5173)
2. **Go to Profile page**
3. **Click "Edit Profile"**
4. **Upload a profile picture**
5. **Click "Save Changes"**

**Expected:**
- Image uploads successfully (no file system folders needed)
- Image displays as Base64 Data URL
- Image persists after page refresh

**Server logs should show:**
```
127.0.0.1 - - [03/Dec/2025 14:30:00] "PUT /api/users/profile HTTP/1.1" 200 -
```

### Step 7: Test Post Creation with Images

1. **In Profile page**
2. **Find post creator box**
3. **Upload a photo**
4. **Add caption**
5. **Click "Post"**

**Expected:**
- Post appears in feed
- Image displays properly
- Image is Base64 Data URL in JSON response

## File System Cleanup (Optional)

If you had old upload folders, you can now delete them:

```bash
# On server machine
rm -rf server/uploads/        # No longer needed
rm -rf server/uploads/media/  # No longer needed
rm -rf server/uploads/profiles/  # No longer needed
```

Note: Files are now in database only!

## Frontend Changes

**No changes needed!** The frontend already:
- ✅ Sends images as FormData
- ✅ Uses Base64 Data URLs for display
- ✅ Handles API responses correctly

The ProfileCustomization and PostCreator components work as-is.

## Verification Checklist

- [ ] Database schema updated
- [ ] New BLOB columns exist
- [ ] Backend server restarted
- [ ] Profile image upload works
- [ ] Post image upload works
- [ ] Images persist after refresh
- [ ] No file system folders created
- [ ] Server logs show 200 OK responses
- [ ] Images display correctly in UI

## Rollback Plan (If Needed)

If something goes wrong:

```bash
# 1. Stop backend server
# Ctrl+C in terminal

# 2. Restore database from backup
mysql -u root -p social_connect < backup_social_connect.sql

# 3. Revert code to previous version
git checkout HEAD~1  # Or restore from backup

# 4. Restart server
python app.py
```

## Database Size Monitoring

```sql
-- Check database size
SELECT 
  table_schema,
  ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS size_mb
FROM information_schema.tables
WHERE table_schema = 'social_connect'
GROUP BY table_schema;

-- Check users table size
SELECT 
  ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
FROM information_schema.tables
WHERE table_schema = 'social_connect' AND table_name = 'users';

-- Check posts table size
SELECT 
  ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
FROM information_schema.tables
WHERE table_schema = 'social_connect' AND table_name = 'posts';
```

## Optimization Tips

If database grows large:

```sql
-- Optimize tables
OPTIMIZE TABLE users;
OPTIMIZE TABLE posts;

-- Check table status
CHECK TABLE users;
CHECK TABLE posts;

-- Repair if needed
REPAIR TABLE users;
REPAIR TABLE posts;
```

## Troubleshooting

### Issue: "Column 'avatar' doesn't have a default value"
**Solution:**
```sql
ALTER TABLE users MODIFY avatar LONGBLOB DEFAULT NULL;
```

### Issue: Images not displaying
**Solution:**
1. Check API response contains `data:image/...;base64,...`
2. Verify MIME type is correct
3. Check frontend console for errors

### Issue: Database connection error
**Solution:**
1. Verify credentials in `server/config/database.py`
2. Ensure MySQL server is running
3. Check database name is correct

### Issue: File size limit error
**Solution:**
1. Compress image before upload
2. Increase MySQL max_allowed_packet:
   ```sql
   SET GLOBAL max_allowed_packet = 67108864;  -- 64MB
   ```

## Performance Considerations

### Query Optimization
```sql
-- If searching for posts with images only
SELECT * FROM posts WHERE media_type = 'image' LIMIT 20;

-- Use LONGBLOB only when needed (not in searches)
SELECT id, user_id, content, media_type FROM posts;  -- Faster

-- If you need the image:
SELECT * FROM posts WHERE id = 5;
```

### Indexing
```sql
-- Add indexes for better performance
ALTER TABLE posts ADD INDEX idx_media_type (media_type);
ALTER TABLE posts ADD INDEX idx_user_media (user_id, media_type);
```

## Success Indicators

✅ Profile images upload and display
✅ Post images/videos upload and display
✅ Images persist after page refresh
✅ Server logs show successful uploads
✅ No file system folders created
✅ Database contains BLOB data
✅ API returns Base64 Data URLs

## Next Steps

1. Monitor database size
2. Implement image compression if needed
3. Add thumbnails for posts list
4. Consider CDN for high-traffic scenarios
5. Implement image caching in frontend

## Support

If issues arise:
1. Check DATABASE_BLOB_STORAGE.md for detailed info
2. Review server logs for error messages
3. Verify database schema matches expected columns
4. Test with simple image file first

Congratulations! Your images are now securely stored in the database! 🎉
