import React, { useEffect } from 'react'
import { useClips } from '../hooks/useClips'
import { ClipCard } from './ClipCard'
import '../styles/clips.css'

export function ClipsView({ showUserClips = false, userId }) {
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

  const displayClips = showUserClips ? userClips : clips

  if (loading) {
    return <div className="clips-loading">Loading clips...</div>
  }

  if (error) {
    return <div className="clips-error">Error: {error}</div>
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
  )
}
