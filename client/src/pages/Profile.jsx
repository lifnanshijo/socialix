import React, { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import ProfileCustomization from '../components/ProfileCustomization'
import '../styles/profile.css'

function Profile() {
  const { user } = useAuth()
  const [isEditing, setIsEditing] = useState(false)
  const [profileData, setProfileData] = useState({
    username: '',
    bio: '',
    avatar: '',
    cover_image: ''
  })

  useEffect(() => {
    if (user) {
      setProfileData({
        username: user.username || '',
        bio: user.bio || '',
        avatar: user.avatar || '',
        cover_image: user.cover_image || ''
      })
    }
  }, [user])

  const handleChange = (e) => {
    setProfileData({
      ...profileData,
      [e.target.name]: e.target.value
    })
  }

  const handleImageUpload = (updatedUser) => {
    // Update local state with new image URLs from the updated user
    setProfileData({
      username: updatedUser.username || profileData.username,
      bio: updatedUser.bio || profileData.bio,
      avatar: updatedUser.avatar || profileData.avatar,
      cover_image: updatedUser.cover_image || profileData.cover_image
    })
    setIsEditing(false)
  }

  return (
    <div className="profile-container">
      <div className="profile-header">
        <div className="cover-image" style={{ 
          backgroundImage: `url(${profileData.cover_image || 'https://via.placeholder.com/1200x300'})` 
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
          >
            {isEditing ? 'Cancel' : 'Edit Profile'}
          </button>
        </div>
      </div>

      {isEditing && (
        <ProfileCustomization
          profileData={profileData}
          handleChange={handleChange}
          onImageUpload={handleImageUpload}
        />
      )}

      <div className="profile-content card">
        <h2>About</h2>
        <div className="about-section">
          <p><strong>Username:</strong> {profileData.username}</p>
          <p><strong>Email:</strong> {user?.email}</p>
          <p><strong>Member since:</strong> {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}</p>
        </div>
      </div>
    </div>
  )
}

export default Profile
