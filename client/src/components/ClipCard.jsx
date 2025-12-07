import React, { useState } from 'react'
import '../styles/clips.css'

export function ClipCard({ clip, isOwner, onDelete }) {
  const [showOptions, setShowOptions] = useState(false)
  const [imageError, setImageError] = useState(false)

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this clip?')) {
      onDelete(clip.clip_id)
    }
  }

  const getFileType = (mimeType) => {
    if (!mimeType) return 'image'
    
    if (mimeType.startsWith('video/')) {
      return 'video'
    }
    return 'image'
  }

  const fileType = getFileType(clip.file_type)
  const fileUrl = clip.file_url || `/api/clips/${clip.clip_id}/download`

  return (
    <div className="clip-card">
      <div className="clip-media">
        {fileType === 'video' ? (
          <video controls style={{ width: '100%', height: '100%', objectFit: 'cover' }}>
            <source src={fileUrl} type={clip.file_type} />
            Your browser does not support the video tag.
          </video>
        ) : (
          <img 
            src={fileUrl} 
            alt={clip.caption || 'Clip'}
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
            onError={(e) => {
              setImageError(true)
              e.target.style.display = 'none'
            }}
          />
        )}
        {imageError && (
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            width: '100%',
            height: '100%',
            backgroundColor: '#f0f0f0'
          }}>
            <p>Image failed to load</p>
          </div>
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
  )
}
