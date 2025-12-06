import React, { useState } from 'react'
import '../styles/clips.css'

export function ClipCard({ clip, isOwner, onDelete }) {
  const [showOptions, setShowOptions] = useState(false)

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this clip?')) {
      onDelete(clip.clip_id)
    }
  }

  const getFileType = (url) => {
    const ext = url.split('.').pop().toLowerCase()
    if (['mp4', 'avi', 'mov', 'mkv', 'webm', 'flv', 'wmv'].includes(ext)) {
      return 'video'
    }
    return 'image'
  }

  const fileType = getFileType(clip.file_url)

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
  )
}
