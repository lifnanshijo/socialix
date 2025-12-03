import React, { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import ProfileCustomization from '../components/ProfileCustomization'
import '../styles/profile.css'

function Profile() {
  const { user, updateProfile } = useAuth()
  const [isEditing, setIsEditing] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [profileData, setProfileData] = useState({
    username: '',
    bio: '',
    avatar: '',
    coverImage: ''
  })

  useEffect(() => {
    if (user) {
      setProfileData({
        username: user.username || '',
        bio: user.bio || '',
        avatar: user.avatar || '',
        coverImage: user.coverImage || ''
      })
    }
  }, [user])

  const handleChange = (e) => {
    setProfileData({
      ...profileData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const result = await updateProfile({
        username: profileData.username,
        bio: profileData.bio
      })
      if (result) {
        setProfileData(prev => ({
          ...prev,
          username: result.username || prev.username,
          bio: result.bio || prev.bio
        }))
        setIsEditing(false)
        alert('Profile updated successfully!')
      }
    } catch (err) {
      console.error('Profile update failed:', err)
      setError(err.message || 'Failed to update profile')
      alert('Error: ' + (err.message || 'Failed to update profile'))
    } finally {
      setLoading(false)
    }
  }

  const handleImageUpload = (updatedUser) => {
    // Update local state with new image URLs
    setProfileData({
      ...profileData,
      avatar: updatedUser.avatar || profileData.avatar,
      coverImage: updatedUser.coverImage || profileData.coverImage
    })
  }

  return (
    <div className="profile-container">
      <div className="profile-header">
        <div className="cover-image" style={{ 
          backgroundImage: `url(${profileData.coverImage || 'https://via.placeholder.com/1200x300'})` 
        }}>
        </div>
        <div className="profile-info">
          <div className="avatar" style={{ 
            backgroundImage: `url(${profileData.avatar || 'https://via.placeholder.com/150'})` 
          }}>
          </div>
          <div className="user-details">
            <h1>{profileData.username}</h1>
            <p className="bio">{profileData.bio || 'No bio yet'}</p>
          </div>
          <button 
            className="btn btn-primary edit-btn"
            onClick={() => setIsEditing(!isEditing)}
            disabled={loading}
          >
            {isEditing ? 'Cancel' : 'Edit Profile'}
          </button>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      {isEditing && (
        <ProfileCustomization
          profileData={profileData}
          handleChange={handleChange}
          handleSubmit={handleSubmit}
          onImageUpload={handleImageUpload}
        />
      )}

      <div className="profile-content card">
        <h2>About</h2>
        <div className="about-section">
          <p><strong>Username:</strong> {profileData.username}</p>
          <p><strong>Email:</strong> {user?.email}</p>
          <p><strong>Member since:</strong> {new Date(user?.createdAt).toLocaleDateString()}</p>
        </div>
      </div>
    </div>
  )
}

export default Profile
