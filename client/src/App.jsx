import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { GoogleOAuthProvider } from '@react-oauth/google'
import { AuthProvider } from './context/AuthContext'
import { ThemeProvider } from './context/ThemeContext'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Profile from './pages/Profile'
import Home from './pages/Home'
import Chat from './pages/Chat'
import UserProfile from './pages/UserProfile'
import PrivateRoute from './components/PrivateRoute'
import Navbar from './components/Navbar'
import MobileBottomNav from './components/MobileBottomNav'

function App() {
  const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID || ''

  return (
    <GoogleOAuthProvider clientId={googleClientId}>
      <Router>
        <ThemeProvider>
          <AuthProvider>
            <div className="app">
              <Navbar />
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<Signup />} />
                <Route path="/home" element={
                  <PrivateRoute>
                    <Home />
                  </PrivateRoute>
                } />
                <Route path="/profile" element={
                  <PrivateRoute>
                    <Profile />
                  </PrivateRoute>
                } />
                <Route path="/profile/:userId" element={
                  <PrivateRoute>
                    <UserProfile />
                  </PrivateRoute>
                } />
                <Route path="/chat" element={
                  <PrivateRoute>
                    <Chat />
                  </PrivateRoute>
                } />
                <Route path="/" element={<Navigate to="/home" replace />} />
              </Routes>
              <MobileBottomNav />
            </div>
          </AuthProvider>
        </ThemeProvider>
      </Router>
    </GoogleOAuthProvider>
  )
}

export default App
