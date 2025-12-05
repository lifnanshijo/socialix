import React, { useState } from 'react'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'

const API_URL = 'http://localhost:5000'

function ProfileCustomization({ profileData, handleChange, handleSubmit, onImageUpload = null }) {
  const { updateProfile: contextUpdateProfile } = useAuth()
  const [avatarPreview, setAvatarPreview] = useState(profileData.avatar || '')
  const [coverPreview, setCoverPreview] = useState(profileData.cover_image || '')
  const [avatarFile, setAvatarFile] = useState(null)
  const [coverFile, setCoverFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [uploadError, setUploadError] = useState('')

  const handleAvatarChange = (e) => {
    const file = e.target.files?.[0]
    if (file) {
      setAvatarFile(file)
      const reader = new FileReader()
      reader.onload = (event) => {
        setAvatarPreview(event.target.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleCoverChange = (e) => {
    const file = e.target.files?.[0]
    if (file) {
      setCoverFile(file)
      const reader = new FileReader()
      reader.onload = (event) => {
        setCoverPreview(event.target.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleSaveChanges = async (e) => {
    e.preventDefault()
    setUploading(true)
    setUploadError('')

    try {
      const files = {}
      if (avatarFile) files.avatarFile = avatarFile
      if (coverFile) files.coverFile = coverFile

      const updateData = {
        username: profileData.username,
        bio: profileData.bio
      }

      console.log('Updating profile with:', { updateData, files })

      // Use context method to update profile - this updates global user state
      const response = await contextUpdateProfile(updateData, files)

      console.log('Profile update response:', response)

      if (response) {
        // Update previews and clear file inputs
        if (response.avatar) {
          setAvatarPreview(response.avatar)
        }
        if (response.cover_image) {
          setCoverPreview(response.cover_image)
        }
        setAvatarFile(null)
        setCoverFile(null)

        if (onImageUpload) {
          onImageUpload(response)
        }

        alert('Profile updated successfully!')
      }
    } catch (err) {
      console.error('Profile update error:', err)
      const errorMsg = err.message || 'Profile update failed'
      setUploadError(errorMsg)
      alert(`Error: ${errorMsg}`)
    } finally {
      setUploading(false)
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

      <form onSubmit={handleSaveChanges}>
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
