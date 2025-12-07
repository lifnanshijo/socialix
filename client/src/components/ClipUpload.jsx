import React, { useState } from 'react'
import { useClips } from '../hooks/useClips'
import '../styles/clips.css'

export function ClipUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null)
  const [caption, setCaption] = useState('')
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)
  const { uploadClip } = useClips()

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      // Validate file size (100MB)
      if (selectedFile.size > 100 * 1024 * 1024) {
        setError('File size exceeds 100MB limit.')
        return
      }

      setFile(selectedFile)
      setError(null)
    }
  }

  const handleCaptionChange = (e) => {
    const text = e.target.value
    if (text.length <= 500) {
      setCaption(text)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!file) {
      setError('Please select a file.')
      return
    }

    setUploading(true)
    setError(null)
    setSuccess(false)

    try {
      const uploadedClip = await uploadClip(file, caption)
      setSuccess(true)
      setFile(null)
      setCaption('')

      // Reset form
      e.target.reset()

      // Notify parent component - this will trigger a refresh
      if (onUploadSuccess) {
        onUploadSuccess(uploadedClip)
      }

      // Clear success message after 5 seconds
      setTimeout(() => setSuccess(false), 5000)
    } catch (err) {
      setError(err.message || 'Upload failed. Please try again.')
      console.error('Upload error:', err)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="clip-upload-container">
      <h2>📹 Upload Your Story</h2>

      <form onSubmit={handleSubmit} className="clip-upload-form">
        <div className="upload-input-group">
          <label htmlFor="clip-file" className="file-input-label">
            <input
              id="clip-file"
              type="file"
              accept="video/*,image/*"
              onChange={handleFileChange}
              disabled={uploading}
            />
            <span className="file-label-text">
              {file ? `📄 ${file.name}` : '📁 Choose file'}
            </span>
          </label>
          <small>Supported: MP4, AVI, PNG, JPG, GIF (Max 100MB)</small>
        </div>

        <div className="caption-input-group">
          <textarea
            placeholder="Add caption (optional)"
            value={caption}
            onChange={handleCaptionChange}
            disabled={uploading}
            rows={3}
            maxLength={500}
          />
          <small>{caption.length}/500 characters</small>
        </div>

        {error && <div className="error-message">❌ {error}</div>}
        {success && <div className="success-message">✅ Clip uploaded successfully!</div>}

        <button
          type="submit"
          disabled={uploading || !file}
          className="submit-button"
        >
          {uploading ? 'Uploading...' : 'Upload Clip'}
        </button>
      </form>
    </div>
  )
}
