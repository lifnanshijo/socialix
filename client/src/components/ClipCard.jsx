import React, { useState, useEffect } from 'react'
import '../styles/clips.css'

const API_BASE = 'http://localhost:5000/api'

export function ClipCard({ clip, isOwner, onDelete }) {
  const [showOptions, setShowOptions] = useState(false)
  const [imageError, setImageError] = useState(false)
  const [mediaUrl, setMediaUrl] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchMedia = async () => {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`${API_BASE}/clips/${clip.clip_id}/download`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (!response.ok) {
          throw new Error('Failed to load media')
        }

        const blob = await response.blob()
        const url = URL.createObjectURL(blob)
        setMediaUrl(url)
        setLoading(false)
      } catch (err) {
        console.error('Error loading media:', err)
        setImageError(true)
        setLoading(false)
      }
    }

    fetchMedia()

    // Cleanup blob URL on unmount
    return () => {
      if (mediaUrl) {
        URL.revokeObjectURL(mediaUrl)
      }
    }
  }, [clip.clip_id])

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

  return (
    <div className="clip-card">
      <div className="clip-media">
        {loading ? (
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            width: '100%',
            height: '100%',
            backgroundColor: '#f0f0f0'
          }}>
            <p>Loading...</p>
          </div>
        ) : imageError ? (
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
        ) : fileType === 'video' ? (
          <video controls style={{ width: '100%', height: '100%', objectFit: 'cover' }}>
            <source src={mediaUrl} type={clip.file_type} />
            Your browser does not support the video tag.
          </video>
        ) : (
          <img 
            src={mediaUrl} 
            alt={clip.caption || 'Clip'}
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
            onError={(e) => {
              setImageError(true)
            }}
          />
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
