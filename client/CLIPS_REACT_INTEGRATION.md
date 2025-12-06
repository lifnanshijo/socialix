# 🎨 Clips Feature - React Integration Guide

## Overview

This guide shows how to integrate the Clips feature into your React frontend. Complete components with styling are provided.

---

## 📁 Files to Create

```
client/src/
├── components/
│   ├── ClipUpload.jsx          # Upload form component
│   ├── ClipsView.jsx            # Display clips feed
│   ├── ClipCard.jsx             # Individual clip card
│   └── clips.css                # Styling
├── hooks/
│   └── useClips.js              # Custom hook for API calls
└── pages/
    └── Clips.jsx                # Main clips page
```

---

## 🚀 Custom Hook (Data Fetching)

**File**: `client/src/hooks/useClips.js`

```javascript
import { useState, useEffect } from 'react';

const API_BASE = 'http://localhost:5000/api/clips';

export function useClips() {
  const [clips, setClips] = useState([]);
  const [userClips, setUserClips] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const token = localStorage.getItem('token');

  // Fetch clips from followed users
  const fetchFollowedClips = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE}/all`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setClips(data.clips || []);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching clips:', err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch user's own clips
  const fetchUserClips = async (userId) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE}/user/${userId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setUserClips(data.clips || []);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching user clips:', err);
    } finally {
      setLoading(false);
    }
  };

  // Upload new clip
  const uploadClip = async (file, caption) => {
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('clip', file);
      if (caption) {
        formData.append('caption', caption);
      }

      const response = await fetch(`${API_BASE}/upload`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Upload failed');
      }

      const data = await response.json();
      return data.clip;
    } catch (err) {
      setError(err.message);
      console.error('Error uploading clip:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Delete clip
  const deleteClip = async (clipId) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE}/${clipId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Delete failed');
      }

      // Remove from local state
      setClips(clips.filter(c => c.clip_id !== clipId));
      setUserClips(userClips.filter(c => c.clip_id !== clipId));
    } catch (err) {
      setError(err.message);
      console.error('Error deleting clip:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    clips,
    userClips,
    loading,
    error,
    fetchFollowedClips,
    fetchUserClips,
    uploadClip,
    deleteClip
  };
}
```

---

## 📤 Upload Component

**File**: `client/src/components/ClipUpload.jsx`

```jsx
import React, { useState } from 'react';
import { useClips } from '../hooks/useClips';
import './clips.css';

export function ClipUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [caption, setCaption] = useState('');
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const { uploadClip } = useClips();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      // Validate file type
      const validTypes = ['video/mp4', 'video/avi', 'image/jpeg', 'image/png', 'image/gif'];
      if (!validTypes.some(type => selectedFile.type.startsWith(type.split('/')[0]))) {
        setError('Invalid file format. Please upload a video or image.');
        return;
      }

      // Validate file size (100MB)
      if (selectedFile.size > 100 * 1024 * 1024) {
        setError('File size exceeds 100MB limit.');
        return;
      }

      setFile(selectedFile);
      setError(null);
    }
  };

  const handleCaptionChange = (e) => {
    const text = e.target.value;
    if (text.length <= 500) {
      setCaption(text);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setError('Please select a file.');
      return;
    }

    setUploading(true);
    setError(null);
    setSuccess(false);

    try {
      const uploadedClip = await uploadClip(file, caption);
      setSuccess(true);
      setFile(null);
      setCaption('');

      // Reset form
      e.target.reset();

      // Notify parent component
      if (onUploadSuccess) {
        onUploadSuccess(uploadedClip);
      }

      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      setError(err.message || 'Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="clip-upload-container">
      <h2>📹 Upload Your Story</h2>

      <form onSubmit={handleSubmit} className="clip-upload-form">
        <div className="upload-input-group">
          <label htmlFor="clip-file" className="file-input-label">
            <input
              id="clip-file"
              type="file"
              accept="video/*,image/*"
              onChange={handleFileChange}
              disabled={uploading}
            />
            <span className="file-label-text">
              {file ? `📄 ${file.name}` : '📁 Choose file'}
            </span>
          </label>
          <small>Supported: MP4, AVI, PNG, JPG, GIF (Max 100MB)</small>
        </div>

        <div className="caption-input-group">
          <textarea
            placeholder="Add caption (optional)"
            value={caption}
            onChange={handleCaptionChange}
            disabled={uploading}
            rows={3}
            maxLength={500}
          />
          <small>{caption.length}/500 characters</small>
        </div>

        {error && <div className="error-message">❌ {error}</div>}
        {success && <div className="success-message">✅ Clip uploaded successfully!</div>}

        <button
          type="submit"
          disabled={uploading || !file}
          className="submit-button"
        >
          {uploading ? 'Uploading...' : 'Upload Clip'}
        </button>
      </form>
    </div>
  );
}
```

---

## 🎬 Clip Card Component

**File**: `client/src/components/ClipCard.jsx`

```jsx
import React, { useState } from 'react';
import './clips.css';

export function ClipCard({ clip, isOwner, onDelete }) {
  const [showOptions, setShowOptions] = useState(false);

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this clip?')) {
      onDelete(clip.clip_id);
    }
  };

  const getFileType = (url) => {
    const ext = url.split('.').pop().toLowerCase();
    if (['mp4', 'avi', 'mov', 'mkv', 'webm', 'flv', 'wmv'].includes(ext)) {
      return 'video';
    }
    return 'image';
  };

  const fileType = getFileType(clip.file_url);

  return (
    <div className="clip-card">
      <div className="clip-media">
        {fileType === 'video' ? (
          <video controls>
            <source src={clip.file_url} />
            Your browser does not support the video tag.
          </video>
        ) : (
          <img src={clip.file_url} alt="Clip" />
        )}
      </div>

      <div className="clip-info">
        {clip.uploaded_by && (
          <div className="clip-user">
            <strong>@{clip.uploaded_by}</strong>
          </div>
        )}

        {clip.caption && (
          <p className="clip-caption">{clip.caption}</p>
        )}

        <div className="clip-meta">
          <small>
            {new Date(clip.created_at).toLocaleDateString()} 
            {' '}
            {new Date(clip.created_at).toLocaleTimeString()}
          </small>
          
          {clip.expires_at && (
            <small className="expires">
              Expires: {new Date(clip.expires_at).toLocaleDateString()}
            </small>
          )}
        </div>
      </div>

      {isOwner && (
        <div className="clip-actions">
          <button
            className="options-button"
            onClick={() => setShowOptions(!showOptions)}
          >
            ⋮
          </button>

          {showOptions && (
            <div className="clip-menu">
              <button onClick={handleDelete} className="delete-button">
                🗑️ Delete
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

---

## 📺 Clips View Component

**File**: `client/src/components/ClipsView.jsx`

```jsx
import React, { useEffect } from 'react';
import { useClips } from '../hooks/useClips';
import { ClipCard } from './ClipCard';
import './clips.css';

export function ClipsView({ showUserClips = false, userId }) {
  const {
    clips,
    userClips,
    loading,
    error,
    fetchFollowedClips,
    fetchUserClips,
    deleteClip
  } = useClips();

  useEffect(() => {
    if (showUserClips && userId) {
      fetchUserClips(userId);
    } else {
      fetchFollowedClips();
    }
  }, [showUserClips, userId]);

  const displayClips = showUserClips ? userClips : clips;

  if (loading) {
    return <div className="clips-loading">Loading clips...</div>;
  }

  if (error) {
    return <div className="clips-error">Error: {error}</div>;
  }

  if (displayClips.length === 0) {
    return (
      <div className="clips-empty">
        <p>📭 No clips available</p>
        <small>
          {showUserClips ? 'Upload your first story!' : 'Follow users to see their stories!'}
        </small>
      </div>
    );
  }

  return (
    <div className="clips-container">
      <div className="clips-grid">
        {displayClips.map(clip => (
          <ClipCard
            key={clip.clip_id}
            clip={clip}
            isOwner={clip.user_id === userId}
            onDelete={deleteClip}
          />
        ))}
      </div>
    </div>
  );
}
```

---

## 📄 Main Clips Page

**File**: `client/src/pages/Clips.jsx`

```jsx
import React, { useState } from 'react';
import { ClipUpload } from '../components/ClipUpload';
import { ClipsView } from '../components/ClipsView';
import { useAuth } from '../context/AuthContext';
import '../components/clips.css';

export function ClipsPage() {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('feed');
  const [refreshKey, setRefreshKey] = useState(0);

  const handleUploadSuccess = () => {
    // Force refresh of clips
    setRefreshKey(prev => prev + 1);
    setActiveTab('feed');
  };

  return (
    <div className="clips-page">
      <div className="clips-header">
        <h1>📸 Stories</h1>
      </div>

      <div className="clips-tabs">
        <button
          className={`tab ${activeTab === 'feed' ? 'active' : ''}`}
          onClick={() => setActiveTab('feed')}
        >
          📺 Feed
        </button>
        <button
          className={`tab ${activeTab === 'my-clips' ? 'active' : ''}`}
          onClick={() => setActiveTab('my-clips')}
        >
          ✏️ My Stories
        </button>
        <button
          className={`tab ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          📤 Upload
        </button>
      </div>

      <div className="clips-content">
        {activeTab === 'feed' && (
          <ClipsView key={refreshKey} showUserClips={false} />
        )}

        {activeTab === 'my-clips' && (
          <ClipsView key={refreshKey} showUserClips={true} userId={user?.id} />
        )}

        {activeTab === 'upload' && (
          <ClipUpload onUploadSuccess={handleUploadSuccess} />
        )}
      </div>
    </div>
  );
}
```

---

## 🎨 Styling

**File**: `client/src/components/clips.css`

```css
/* Clips Container */
.clips-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.clips-header {
  text-align: center;
  margin-bottom: 30px;
}

.clips-header h1 {
  font-size: 32px;
  color: var(--primary-color, #000);
  margin: 0;
}

/* Tabs */
.clips-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  border-bottom: 2px solid #e0e0e0;
}

.tab {
  padding: 12px 20px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #666;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
}

.tab:hover {
  color: #000;
}

.tab.active {
  color: var(--primary-color, #007bff);
  border-bottom-color: var(--primary-color, #007bff);
}

/* Upload Form */
.clip-upload-container {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 0 auto;
}

.clip-upload-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.upload-input-group,
.caption-input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.file-input-label {
  position: relative;
}

.file-input-label input[type="file"] {
  display: none;
}

.file-label-text {
  display: block;
  padding: 15px;
  border: 2px dashed #ddd;
  border-radius: 8px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.file-input-label:hover .file-label-text {
  border-color: var(--primary-color, #007bff);
  background: rgba(0, 123, 255, 0.05);
}

.file-input-label input:disabled ~ .file-label-text {
  opacity: 0.5;
  cursor: not-allowed;
}

textarea {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
}

textarea:focus {
  outline: none;
  border-color: var(--primary-color, #007bff);
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.submit-button {
  padding: 12px 24px;
  background: var(--primary-color, #007bff);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-button:hover:not(:disabled) {
  background: var(--primary-dark, #0056b3);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
}

.submit-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Messages */
.error-message,
.success-message {
  padding: 12px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
}

.error-message {
  background: #fee;
  color: #c00;
  border-left: 4px solid #c00;
}

.success-message {
  background: #efe;
  color: #060;
  border-left: 4px solid #060;
}

/* Clips Grid */
.clips-container {
  padding: 20px;
}

.clips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.clip-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.clip-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.clip-media {
  width: 100%;
  height: 300px;
  background: #f0f0f0;
  overflow: hidden;
}

.clip-media video,
.clip-media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.clip-info {
  padding: 15px;
}

.clip-user {
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--primary-color, #007bff);
}

.clip-caption {
  margin: 8px 0;
  color: #333;
  font-size: 14px;
  word-wrap: break-word;
}

.clip-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
  margin-top: 10px;
  flex-wrap: wrap;
  gap: 10px;
}

.clip-meta small.expires {
  color: #f00;
}

/* Actions */
.clip-actions {
  position: relative;
}

.options-button {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  padding: 8px 12px;
  float: right;
  margin: -8px -12px 0 0;
}

.clip-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 10;
}

.delete-button {
  display: block;
  width: 100%;
  padding: 12px 20px;
  border: none;
  background: none;
  cursor: pointer;
  text-align: left;
  font-size: 14px;
  color: #c00;
  transition: all 0.2s ease;
}

.delete-button:hover {
  background: #fee;
}

/* Loading & Empty States */
.clips-loading,
.clips-empty {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.clips-loading {
  font-size: 16px;
}

.clips-empty p {
  font-size: 18px;
  margin: 0;
}

.clips-empty small {
  display: block;
  margin-top: 10px;
  color: #999;
}

.clips-error {
  padding: 20px;
  background: #fee;
  color: #c00;
  border-radius: 8px;
  margin: 20px;
}

/* Responsive */
@media (max-width: 768px) {
  .clips-page {
    padding: 15px;
  }

  .clips-header h1 {
    font-size: 24px;
  }

  .clips-tabs {
    flex-wrap: wrap;
  }

  .clips-grid {
    grid-template-columns: 1fr;
  }

  .clip-upload-container {
    padding: 20px;
  }

  .clip-card {
    border-radius: 8px;
  }

  .clip-media {
    height: 250px;
  }
}

@media (max-width: 480px) {
  .clips-tabs {
    gap: 5px;
  }

  .tab {
    padding: 10px 15px;
    font-size: 12px;
  }

  .clip-media {
    height: 200px;
  }

  .clip-info {
    padding: 12px;
  }

  .clip-caption {
    font-size: 13px;
  }
}
```

---

## 🔗 Add Route to App.jsx

```jsx
import { ClipsPage } from './pages/Clips';

// Add to your routes
<Route path="/clips" element={<ClipsPage />} />

// Add to navigation (if you have a navigation menu)
<Link to="/clips">📸 Stories</Link>
```

---

## 🧪 Test Integration

```jsx
// In your browser console:

// Test upload
const form = new FormData();
form.append('clip', fileInput.files[0]);
form.append('caption', 'Test');
fetch('http://localhost:5000/api/clips/upload', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
  body: form
}).then(r => r.json()).then(console.log);

// Test get clips
fetch('http://localhost:5000/api/clips/all', {
  headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
}).then(r => r.json()).then(console.log);
```

---

## 📋 Integration Checklist

- [ ] Created `useClips` hook with API calls
- [ ] Created `ClipUpload` component
- [ ] Created `ClipCard` component
- [ ] Created `ClipsView` component
- [ ] Created `Clips` page
- [ ] Added `clips.css` stylesheet
- [ ] Added route to App.jsx
- [ ] Added navigation link
- [ ] Tested upload functionality
- [ ] Tested display functionality
- [ ] Tested delete functionality
- [ ] Styling looks good on mobile

---

## 🎯 Environment Variables (Optional)

`.env`:
```
REACT_APP_API_URL=http://localhost:5000
```

Usage:
```javascript
const API_BASE = `${process.env.REACT_APP_API_URL}/api/clips`;
```

---

**Status**: Production-Ready ✅  
**Last Updated**: Dec 6, 2025

