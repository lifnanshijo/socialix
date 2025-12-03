import React, { useState } from 'react'
import axios from 'axios'

function ProfileCustomization({ profileData, handleChange, handleSubmit, onImageUpload = null }) {
  const [avatarPreview, setAvatarPreview] = useState(profileData.avatar || '')
  const [coverPreview, setCoverPreview] = useState(profileData.coverImage || '')
  const [uploading, setUploading] = useState(false)
  const [uploadError, setUploadError] = useState('')

  const uploadImage = async (file, type) => {
    if (!file) return

    setUploading(true)
    setUploadError('')
    
    try {
      const formData = new FormData()
      formData.append('file', file)

      const endpoint = type === 'avatar' 
        ? '/api/users/profile/upload-avatar' 
        : '/api/users/profile/upload-cover'

      const token = localStorage.getItem('token')
      console.log('Token:', token ? 'Present' : 'Missing')
      console.log('Uploading to:', endpoint)
      
      const config = {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }

      const response = await axios.post(endpoint, formData, config)

      console.log('Upload response:', response.data)

      if (response.data.user) {
        if (type === 'avatar') {
          setAvatarPreview(response.data.user.avatar)
        } else {
          setCoverPreview(response.data.user.coverImage)
        }
        
        if (onImageUpload) {
          onImageUpload(response.data.user)
        }
        
        alert(`${type === 'avatar' ? 'Profile picture' : 'Cover image'} uploaded successfully!`)
      }
    } catch (err) {
      console.error('Upload error:', err)
      const errorMsg = err.response?.data?.message || err.message || 'Upload failed'
      setUploadError(errorMsg)
      alert(`Error: ${errorMsg}`)
    } finally {
      setUploading(false)
    }
  }

  const handleAvatarChange = (e) => {
    const file = e.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (event) => {
        setAvatarPreview(event.target.result)
      }
      reader.readAsDataURL(file)
      uploadImage(file, 'avatar')
    }
  }

  const handleCoverChange = (e) => {
    const file = e.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (event) => {
        setCoverPreview(event.target.result)
      }
      reader.readAsDataURL(file)
      uploadImage(file, 'cover')
    }
  }

  return (
    <div className="profile-edit card">
      <h2>Edit Profile</h2>
      
      {uploadError && <div style={{color: 'red', marginBottom: '10px'}}>{uploadError}</div>}

      {/* Avatar Upload */}
      <div className="form-group">
        <label>Profile Picture</label>
        <div className="image-upload-zone">
          {avatarPreview ? (
            <div className="image-preview avatar-preview">
              <img src={avatarPreview} alt="Avatar preview" />
              <div className="overlay">
                <label htmlFor="avatar-input" className="change-btn">
                  Change
                </label>
              </div>
            </div>
          ) : (
            <label htmlFor="avatar-input" className="upload-placeholder">
              <svg className="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="17 8 12 3 7 8" />
                <line x1="12" y1="3" x2="12" y2="15" />
              </svg>
              <span>Click to upload profile picture</span>
            </label>
          )}
          <input
            id="avatar-input"
            type="file"
            accept="image/*"
            onChange={handleAvatarChange}
            disabled={uploading}
            style={{ display: 'none' }}
          />
        </div>
      </div>

      {/* Cover Image Upload */}
      <div className="form-group">
        <label>Cover Image</label>
        <div className="image-upload-zone cover-zone">
          {coverPreview ? (
            <div className="image-preview cover-preview">
              <img src={coverPreview} alt="Cover preview" />
              <div className="overlay">
                <label htmlFor="cover-input" className="change-btn">
                  Change
                </label>
              </div>
            </div>
          ) : (
            <label htmlFor="cover-input" className="upload-placeholder">
              <svg className="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="17 8 12 3 7 8" />
                <line x1="12" y1="3" x2="12" y2="15" />
              </svg>
              <span>Click to upload cover image</span>
            </label>
          )}
          <input
            id="cover-input"
            type="file"
            accept="image/*"
            onChange={handleCoverChange}
            disabled={uploading}
            style={{ display: 'none' }}
          />
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Username</label>
          <input
            type="text"
            name="username"
            value={profileData.username}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Bio</label>
          <textarea
            name="bio"
            value={profileData.bio}
            onChange={handleChange}
            rows="4"
            placeholder="Tell us about yourself..."
          />
        </div>

        <button type="submit" className="btn btn-primary" disabled={uploading}>
          {uploading ? 'Uploading...' : 'Save Changes'}
        </button>
      </form>
    </div>
  )
}

export default ProfileCustomization
