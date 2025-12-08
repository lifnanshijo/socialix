import React, { useEffect, useState } from 'react'
import { useClips } from '../hooks/useClips'
import { ClipCard } from './ClipCard'
import { useAuth } from '../context/AuthContext'
import '../styles/clips.css'

export function ClipsView({ showUserClips = false, userId }) {
  const { user } = useAuth()
  const [deleteError, setDeleteError] = useState(null)
  const {
    clips,
    userClips,
    loading,
    error,
    fetchFollowedClips,
    fetchUserClips,
    deleteClip
  } = useClips()

  useEffect(() => {
    if (showUserClips && userId) {
      fetchUserClips(userId)
    } else {
      fetchFollowedClips()
    }
  }, [showUserClips, userId])

  const handleDelete = async (clipId) => {
    try {
      setDeleteError(null)
      await deleteClip(clipId)
      // Refresh the clips after successful delete
      if (showUserClips && userId) {
        await fetchUserClips(userId)
      } else {
        await fetchFollowedClips()
      }
    } catch (err) {
      setDeleteError(err.message || 'Failed to delete clip')
    }
  }

  const displayClips = showUserClips ? userClips : clips

  if (loading) {
    return <div className="clips-loading">Loading clips...</div>
  }

  if (error || deleteError) {
    return <div className="clips-error">Error: {error || deleteError}</div>
  }

  if (displayClips.length === 0) {
    return (
      <div className="clips-empty">
        <p>📭 No clips available</p>
        <small>
          {showUserClips ? 'Upload your first story!' : 'Follow users to see their stories!'}
        </small>
      </div>
    )
  }

  return (
    <div className="clips-container">
      {deleteError && (
        <div className="clips-error" style={{ marginBottom: '1rem' }}>
          Error: {deleteError}
        </div>
      )}
      <div className="clips-grid">
        {displayClips.map(clip => (
          <ClipCard
            key={clip.clip_id}
            clip={clip}
            isOwner={clip.user_id === user?.id}
            onDelete={handleDelete}
          />
        ))}
      </div>
    </div>
  )
}
