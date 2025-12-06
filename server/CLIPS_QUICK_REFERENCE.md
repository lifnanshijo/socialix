# Clips Feature - Quick Reference Card

## 🚀 5-Minute Setup

```bash
# 1. Create table in MySQL
CREATE TABLE clips (
    clip_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    file_url VARCHAR(500),
    caption VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX (user_id), INDEX (expires_at), INDEX (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

# 2. Install APScheduler
pip install APScheduler

# 3. Update app.py (see below)

# 4. Create folder
mkdir -p uploads/clips

# 5. Run server
python app.py
```

---

## 📝 App.py Integration

```python
# Add to imports
from routes.clip_routes import clips_bp
from utils.clips_scheduler import ClipsScheduler

# Add to Flask app initialization
app.register_blueprint(clips_bp, url_prefix='/api/clips')

# In main block
if __name__ == '__main__':
    scheduler = ClipsScheduler()
    scheduler.init_scheduler(app)
    app.run(debug=True)
```

---

## 🔌 API Endpoints

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| POST | `/api/clips/upload` | Upload clip | ✅ |
| GET | `/api/clips/user/{id}` | Get user's clips | ✅ |
| GET | `/api/clips/all` | Get followed clips | ✅ |
| DELETE | `/api/clips/{id}` | Delete clip | ✅ |
| POST | `/api/clips/cleanup/expired` | Manual cleanup | ❌ |

---

## 📤 Upload Clip

**URL**: `POST /api/clips/upload`

**Headers**:
```
Authorization: Bearer {JWT_TOKEN}
Content-Type: multipart/form-data
```

**Form Data**:
```
clip: <file>           (required, video or image)
caption: <string>      (optional, max 500 chars)
```

**Success Response** (201):
```json
{
  "message": "Clip uploaded successfully",
  "clip": {
    "clip_id": 1,
    "user_id": 5,
    "file_url": "/uploads/clips/5_1701234567.mp4",
    "caption": "My first story!",
    "created_at": "2024-12-06T10:30:00",
    "expires_at": "2024-12-07T10:30:00"
  }
}
```

**Curl Example**:
```bash
curl -X POST http://localhost:5000/api/clips/upload \
  -H "Authorization: Bearer YOUR_JWT" \
  -F "clip=@video.mp4" \
  -F "caption=My awesome story!"
```

---

## 🎬 Get User's Clips

**URL**: `GET /api/clips/user/{user_id}`

**Headers**:
```
Authorization: Bearer {JWT_TOKEN}
```

**Success Response** (200):
```json
{
  "user_id": 5,
  "clips": [
    {
      "clip_id": 1,
      "user_id": 5,
      "file_url": "/uploads/clips/5_1701234567.mp4",
      "caption": "My first story!",
      "created_at": "2024-12-06T10:30:00",
      "expires_at": "2024-12-07T10:30:00"
    }
  ],
  "count": 1
}
```

**Curl Example**:
```bash
curl -X GET http://localhost:5000/api/clips/user/5 \
  -H "Authorization: Bearer YOUR_JWT"
```

---

## 📺 Get All Followed Clips

**URL**: `GET /api/clips/all`

**Headers**:
```
Authorization: Bearer {JWT_TOKEN}
```

**Success Response** (200):
```json
{
  "clips": [
    {
      "clip_id": 1,
      "user_id": 5,
      "file_url": "/uploads/clips/5_1701234567.mp4",
      "caption": "My first story!",
      "created_at": "2024-12-06T10:30:00",
      "expires_at": "2024-12-07T10:30:00",
      "uploaded_by": "john_doe"
    }
  ],
  "count": 5
}
```

**Curl Example**:
```bash
curl -X GET http://localhost:5000/api/clips/all \
  -H "Authorization: Bearer YOUR_JWT"
```

---

## 🗑️ Delete Clip

**URL**: `DELETE /api/clips/{clip_id}`

**Headers**:
```
Authorization: Bearer {JWT_TOKEN}
```

**Success Response** (200):
```json
{
  "message": "Clip deleted successfully"
}
```

**Curl Example**:
```bash
curl -X DELETE http://localhost:5000/api/clips/1 \
  -H "Authorization: Bearer YOUR_JWT"
```

---

## 🧹 Manual Cleanup

**URL**: `POST /api/clips/cleanup/expired`

**Success Response** (200):
```json
{
  "message": "Cleanup completed",
  "deleted_count": 10
}
```

**Curl Example**:
```bash
curl -X POST http://localhost:5000/api/clips/cleanup/expired
```

---

## 📏 File Validation

| Validation | Limit | Error |
|-----------|-------|-------|
| Video formats | mp4, avi, mov, mkv, webm, flv, wmv | 400 |
| Image formats | jpg, jpeg, png, gif, webp, bmp, svg | 400 |
| File size | 100 MB | 413 |
| Caption length | 500 characters | 400 |

---

## ⏱️ Expiration Rules

- **Expires after**: 24 hours from upload
- **Automatic cleanup**: Every hour (if scheduler enabled)
- **Calculation**: `expires_at = created_at + 24 hours`
- **Manual cleanup**: `POST /api/clips/cleanup/expired`

---

## 🔐 Security Features

✅ JWT authentication required  
✅ Ownership verification (can only delete own clips)  
✅ File extension whitelist  
✅ File size limit (100MB)  
✅ Filename secured (no path traversal)  
✅ Caption sanitized (no HTML/JS)  
✅ Foreign key constraints  
✅ Cascade delete on user deletion  

---

## 📊 Files Created

```
server/
├── models/clip.py                      # Database operations
├── routes/clip_routes.py               # 5 API endpoints
├── config/clips_schema.py              # MySQL schema
├── utils/clips_scheduler.py            # Auto-cleanup
├── utils/clips_validation.py           # File/caption validation
├── clips_config.py                     # Module config
├── CLIPS_DOCUMENTATION.md              # Full reference
└── CLIPS_SETUP_GUIDE.md                # Setup instructions
```

---

## 🆘 Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| 404 | Blueprint not registered | Add `app.register_blueprint()` |
| 401 | Missing/invalid JWT | Include valid token in header |
| 400 | Invalid file | Check format, size, caption |
| 413 | File too large | Max 100MB |
| 500 | Database error | Check MySQL connection |

---

## 📱 React Integration

### Upload Component
```jsx
const [file, setFile] = useState(null);
const [caption, setCaption] = useState('');

const upload = async () => {
  const form = new FormData();
  form.append('clip', file);
  form.append('caption', caption);
  
  await fetch('http://localhost:5000/api/clips/upload', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: form
  });
};
```

### View Clips
```jsx
const [clips, setClips] = useState([]);

useEffect(() => {
  fetch('http://localhost:5000/api/clips/all', {
    headers: { 'Authorization': `Bearer ${token}` }
  }).then(r => r.json()).then(d => setClips(d.clips));
}, []);
```

---

## 🗄️ Database Verification

```sql
-- Check table
SHOW TABLES LIKE 'clips';

-- Check structure
DESCRIBE clips;

-- Check data
SELECT * FROM clips WHERE expires_at > NOW() ORDER BY created_at DESC;

-- Check indexes
SHOW INDEXES FROM clips;
```

---

## 📈 Performance Tips

1. Use indexes (already created!)
2. Run cleanup regularly (scheduler enabled)
3. Move old clips to archive table
4. Use CDN for serving clips
5. Monitor disk space

---

## ✅ Deployment Checklist

- [ ] MySQL table created
- [ ] APScheduler installed
- [ ] app.py updated with blueprint + scheduler
- [ ] uploads/clips directory created
- [ ] All 5 endpoints tested
- [ ] JWT authentication working
- [ ] File validation working
- [ ] Scheduler cleanup running (check logs)
- [ ] CORS enabled (if cross-domain)
- [ ] Logs configured
- [ ] Backups scheduled

---

## 🚀 Production Deployment

```bash
# Set environment to production
export FLASK_ENV=production

# Use production WSGI server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Set up log rotation
# Set up database backups
# Enable HTTPS
# Configure CDN for uploads
# Enable rate limiting
```

---

**Version**: 1.0  
**Status**: Production-Ready ✅  
**Last Updated**: Dec 6, 2025

See `CLIPS_DOCUMENTATION.md` for complete reference.

