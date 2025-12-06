# 🚀 Clips Feature - Setup & Integration Guide

## Quick Start (5 Minutes)

### Step 1: Create Database Table (1 minute)
```bash
# Connect to MySQL
mysql -u root -p

# Select your database
USE socialix;

# Paste schema from server/config/clips_schema.py
# Or run this:
CREATE TABLE IF NOT EXISTS clips (
    clip_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    caption VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    CONSTRAINT fk_clips_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_expires_at (expires_at),
    INDEX idx_created_at (created_at),
    INDEX idx_active_clips (expires_at, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Step 2: Install Dependencies (1 minute)
```bash
# Terminal in server folder
pip install APScheduler

# Already installed (no action needed):
# - flask
# - mysql.connector
# - flask-jwt-extended
# - werkzeug
```

### Step 3: Update Flask App (1 minute)
Edit `server/app.py`:

```python
# Add these imports at the top
from routes.clip_routes import clips_bp
from utils.clips_scheduler import ClipsScheduler

# In your Flask app initialization section, add:
# Register clips blueprint
app.register_blueprint(clips_bp, url_prefix='/api/clips')

# Initialize scheduler (runs cleanup every hour)
if __name__ == '__main__':
    scheduler = ClipsScheduler()
    scheduler.init_scheduler(app)
    app.run(debug=True)
```

### Step 4: Create Upload Directory (1 minute)
```bash
# In server folder
mkdir -p uploads/clips
```

### Step 5: Test It Works (1 minute)
```bash
# Start your server
python app.py

# In another terminal, test upload:
curl -X POST http://localhost:5000/api/clips/upload \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "clip=@test_video.mp4" \
  -F "caption=Test clip"
```

---

## 📂 Files Added

All files are **already created** and ready to use. No coding needed!

| File | Purpose | Status |
|------|---------|--------|
| `server/models/clip.py` | Database operations | ✅ Complete |
| `server/routes/clip_routes.py` | API endpoints | ✅ Complete |
| `server/config/clips_schema.py` | Database schema | ✅ Complete |
| `server/utils/clips_scheduler.py` | Auto-cleanup tasks | ✅ Complete |
| `server/utils/clips_validation.py` | Input validation | ✅ Complete |
| `server/clips_config.py` | Module config | ✅ Complete |

---

## 🔧 Integration Checklist

- [ ] Created MySQL table (`CREATE TABLE clips...`)
- [ ] Installed APScheduler (`pip install APScheduler`)
- [ ] Added imports to `app.py`
- [ ] Added blueprint registration to `app.py`
- [ ] Added scheduler initialization to `app.py`
- [ ] Created `uploads/clips/` directory
- [ ] Restarted Flask server
- [ ] Tested with curl/Postman

---

## 🧪 Testing the API

### 1. Upload a Clip
```bash
# Using curl
curl -X POST http://localhost:5000/api/clips/upload \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "clip=@video.mp4" \
  -F "caption=My awesome story!"

# Response:
# {
#   "message": "Clip uploaded successfully",
#   "clip": {...}
# }
```

### 2. Get Your Clips
```bash
# Replace USER_ID with actual user ID
curl -X GET http://localhost:5000/api/clips/user/5 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Response shows all active clips for that user
```

### 3. Get Followed Users' Clips
```bash
curl -X GET http://localhost:5000/api/clips/all \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Response shows clips from users you follow
```

### 4. Delete a Clip
```bash
# Replace CLIP_ID with actual clip ID
curl -X DELETE http://localhost:5000/api/clips/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Response: { "message": "Clip deleted successfully" }
```

---

## ⚙️ Configuration Options

### Scheduler Options

#### Option 1: APScheduler (Recommended)
```python
# In app.py
from utils.clips_scheduler import ClipsScheduler

scheduler = ClipsScheduler()
scheduler.init_scheduler(app)
```
- ✅ Recommended for production
- ✅ Runs in background
- ✅ No external service needed
- ✅ Automatic hourly cleanup

#### Option 2: Simple Threading
```python
# In app.py
from utils.clips_scheduler import SimpleClipsScheduler

scheduler = SimpleClipsScheduler()
scheduler.start()
```
- ✅ Light-weight
- ✅ Good for development
- ✅ Stops when app stops

#### Option 3: Celery + Redis (Advanced)
For distributed systems or high-scale apps. See `utils/clips_scheduler.py` for setup instructions.

---

## 📋 Environment Variables (Optional)

Create `.env` file in server folder:
```env
# Clips configuration
CLIPS_UPLOAD_FOLDER=uploads/clips
CLIPS_MAX_FILE_SIZE=104857600  # 100MB in bytes
CLIPS_EXPIRATION_HOURS=24
CLIPS_CAPTION_MAX_LENGTH=500

# Scheduler configuration
SCHEDULER_ENABLED=True
SCHEDULER_INTERVAL_HOURS=1
```

Load in app.py:
```python
from dotenv import load_dotenv
load_dotenv()

CLIPS_MAX_FILE_SIZE = int(os.getenv('CLIPS_MAX_FILE_SIZE', 104857600))
```

---

## 🗄️ Database Verification

After setup, verify table was created:
```sql
-- Check table exists
SHOW TABLES LIKE 'clips';

-- Check table structure
DESCRIBE clips;

-- Should show columns:
-- - clip_id (int, primary key)
-- - user_id (int, foreign key)
-- - file_url (varchar)
-- - caption (varchar)
-- - created_at (timestamp)
-- - expires_at (timestamp)

-- Check indexes
SHOW INDEXES FROM clips;
```

---

## 🎨 Client Integration (React)

### Create Upload Component
File: `client/src/components/ClipUpload.jsx`

```jsx
import React, { useState } from 'react';

export function ClipUpload() {
  const [file, setFile] = useState(null);
  const [caption, setCaption] = useState('');
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('clip', file);
    formData.append('caption', caption);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/api/clips/upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      if (response.ok) {
        alert('Clip uploaded!');
        setFile(null);
        setCaption('');
      }
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleUpload}>
      <input
        type="file"
        accept="video/*,image/*"
        onChange={(e) => setFile(e.target.files[0])}
        required
      />
      <textarea
        placeholder="Add caption (optional)"
        value={caption}
        onChange={(e) => setCaption(e.target.value)}
        maxLength={500}
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Uploading...' : 'Upload Clip'}
      </button>
    </form>
  );
}
```

### Display Clips Component
```jsx
import React, { useEffect, useState } from 'react';

export function ClipsView() {
  const [clips, setClips] = useState([]);

  useEffect(() => {
    const fetchClips = async () => {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/api/clips/all', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      setClips(data.clips);
    };

    fetchClips();
  }, []);

  return (
    <div className="clips-container">
      {clips.map(clip => (
        <div key={clip.clip_id} className="clip">
          <video src={clip.file_url} controls />
          <p>{clip.caption}</p>
          <small>by {clip.uploaded_by}</small>
        </div>
      ))}
    </div>
  );
}
```

---

## 🔍 Troubleshooting

### Issue: 404 on API endpoints
**Solution**: Make sure you added the blueprint registration to `app.py`
```python
app.register_blueprint(clips_bp, url_prefix='/api/clips')
```

### Issue: 413 File Too Large
**Solution**: File exceeds 100MB. Reduce file size or update limit in `routes/clip_routes.py`

### Issue: Clips expire too quickly
**Check**: Verify `expires_at` is calculated correctly in `models/clip.py`
```python
expires_at = datetime.utcnow() + timedelta(hours=24)
```

### Issue: Authorization errors
**Solution**: Ensure JWT token is valid and not expired
```bash
# Debug with:
curl -X GET http://localhost:5000/api/clips/all \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Issue: Cleanup not working
**Solution**: Verify scheduler is initialized:
```bash
# Check logs for: "ClipsScheduler initialized"
# Or manually trigger cleanup:
curl -X POST http://localhost:5000/api/clips/cleanup/expired
```

---

## 📊 Monitoring & Maintenance

### Check Active Clips
```sql
SELECT COUNT(*) FROM clips WHERE expires_at > NOW();
```

### Check Expired Clips
```sql
SELECT COUNT(*) FROM clips WHERE expires_at <= NOW();
```

### Monitor Disk Usage
```bash
# Check uploads folder size
du -sh uploads/clips/

# Or check specific user's clips
du -sh uploads/clips/5_*
```

### View Upload Logs
```bash
# If using standard output logging:
tail -f server_output.log | grep "clip"
```

---

## 🚀 Scaling Considerations

### For small apps (< 1000 users)
- ✅ Current setup is perfect
- ✅ APScheduler runs fine
- ✅ Single MySQL server sufficient

### For medium apps (1000-100k users)
- Consider: Add database indexes (already done!)
- Consider: Move uploads to S3/Azure Blob
- Consider: CDN for serving clips
- Keep: Current scheduler

### For large apps (> 100k users)
- Required: CDN for clips storage
- Required: Celery + Redis for scheduling
- Recommended: Database replication
- Required: Upload queue system

---

## 📝 Database Backups

```bash
# Backup clips table
mysqldump -u root -p socialix clips > clips_backup.sql

# Backup all uploads
tar -czf clips_uploads_backup.tar.gz uploads/clips/

# Restore clips table
mysql -u root -p socialix < clips_backup.sql

# Restore uploads
tar -xzf clips_uploads_backup.tar.gz
```

---

## ✅ Final Checklist Before Going Live

- [ ] Database table created with indexes
- [ ] APScheduler installed and configured
- [ ] Flask app updated with blueprint + scheduler
- [ ] Upload directory created with proper permissions
- [ ] JWT authentication verified
- [ ] File validation tested (size, format, caption)
- [ ] All 5 endpoints tested and working
- [ ] Scheduler cleanup verified (check logs)
- [ ] Error handling tested
- [ ] CORS enabled if needed (for cross-domain requests)
- [ ] Logs configured and monitored
- [ ] Backups scheduled

---

## 🎓 Learning Resources

### API Concepts
- RESTful API design: https://restfulapi.net/
- JWT authentication: https://jwt.io/
- File uploads: https://developer.mozilla.org/en-US/docs/Web/API/FormData

### Technologies Used
- Flask: https://flask.palletsprojects.com/
- MySQL: https://dev.mysql.com/doc/
- APScheduler: https://apscheduler.readthedocs.io/

### Next Steps
1. Build React UI component for upload
2. Add view count tracking
3. Implement emoji reactions
4. Add clip comments
5. Set up analytics dashboard

---

**Status**: Ready to Deploy ✅
**Setup Time**: ~5 minutes
**Support**: Check CLIPS_DOCUMENTATION.md for full reference

