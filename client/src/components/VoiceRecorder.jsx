import React, { useState, useRef } from 'react';
import '../styles/voiceRecorder.css';

const VoiceRecorder = ({ onRecordingComplete, onCancel }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioBlob, setAudioBlob] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerRef = useRef(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm' // Most compatible format
      });

      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        setAudioBlob(audioBlob);
        
        // Stop all audio tracks
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
      setRecordingTime(0);

      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);

    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Could not access microphone. Please check your permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    }
  };

  const sendRecording = () => {
    if (audioBlob) {
      onRecordingComplete(audioBlob);
      resetRecorder();
    }
  };

  const resetRecorder = () => {
    setAudioBlob(null);
    setRecordingTime(0);
    audioChunksRef.current = [];
    
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }
  };

  const handleCancel = () => {
    if (isRecording) {
      stopRecording();
    }
    resetRecorder();
    onCancel();
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="voice-recorder">
      {!audioBlob ? (
        <div className="recording-controls">
          {!isRecording ? (
            <button className="record-btn" onClick={startRecording}>
              <span className="mic-icon">🎤</span>
              Start Recording
            </button>
          ) : (
            <div className="recording-active">
              <div className="recording-indicator">
                <span className="recording-dot"></span>
                <span className="recording-time">{formatTime(recordingTime)}</span>
              </div>
              <button className="stop-btn" onClick={stopRecording}>
                ⏹ Stop
              </button>
            </div>
          )}
          <button className="cancel-btn" onClick={handleCancel}>
            Cancel
          </button>
        </div>
      ) : (
        <div className="recording-preview">
          <div className="preview-header">
            <span className="audio-icon">🔊</span>
            <span className="preview-duration">{formatTime(recordingTime)}</span>
          </div>
          <audio controls src={URL.createObjectURL(audioBlob)} />
          <div className="preview-actions">
            <button className="send-voice-btn" onClick={sendRecording}>
              ✓ Send Voice Message
            </button>
            <button className="rerecord-btn" onClick={resetRecorder}>
              ↻ Re-record
            </button>
            <button className="cancel-btn" onClick={handleCancel}>
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default VoiceRecorder;
