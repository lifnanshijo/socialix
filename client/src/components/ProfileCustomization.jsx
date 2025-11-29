import React from 'react'

function ProfileCustomization({ profileData, handleChange, handleSubmit }) {
  return (
    <div className="profile-edit card">
      <h2>Edit Profile</h2>
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

        <div className="form-group">
          <label>Avatar URL</label>
          <input
            type="url"
            name="avatar"
            value={profileData.avatar}
            onChange={handleChange}
            placeholder="https://example.com/avatar.jpg"
          />
        </div>

        <div className="form-group">
          <label>Cover Image URL</label>
          <input
            type="url"
            name="coverImage"
            value={profileData.coverImage}
            onChange={handleChange}
            placeholder="https://example.com/cover.jpg"
          />
        </div>

        <button type="submit" className="btn btn-primary">Save Changes</button>
      </form>
    </div>
  )
}

export default ProfileCustomization
