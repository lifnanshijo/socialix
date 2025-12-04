import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/auth.css';

const TokenExpired = () => {
  const navigate = useNavigate();

  return (
    <div className="auth-container">
      <div className="auth-card card">
        <h1>Session Expired</h1>
        <p style={{ marginBottom: '20px', color: 'var(--text-secondary)' }}>
          Your session has expired. Please log in again to continue.
        </p>
        <button 
          className="btn btn-primary"
          onClick={() => navigate('/login')}
          style={{ width: '100%' }}
        >
          Go to Login
        </button>
      </div>
    </div>
  );
};

export default TokenExpired;
