import React from 'react'

function SocialixLogo({ size = 40, variant = 'full' }) {
  if (variant === 'icon') {
    return (
      <svg
        width={size}
        height={size}
        viewBox="0 0 200 200"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style={{ cursor: 'pointer' }}
      >
        <defs>
          <linearGradient
            id="sGradient"
            x1="0%"
            y1="0%"
            x2="100%"
            y2="100%"
          >
            <stop offset="0%" stopColor="#00d4ff" />
            <stop offset="33%" stopColor="#3366ff" />
            <stop offset="66%" stopColor="#9933ff" />
            <stop offset="100%" stopColor="#ff6633" />
          </linearGradient>
        </defs>
        
        {/* S shape - text letter S */}
        <text
          x="60"
          y="130"
          fontSize="120"
          fontWeight="700"
          fontFamily="Arial, sans-serif"
          fill="url(#sGradient)"
        >
          S
        </text>
        
        {/* X shape - right side */}
        <path
          d="M 110 45 L 145 155"
          stroke="url(#sGradient)"
          strokeWidth="16"
          strokeLinecap="round"
        />
        {/* X shape - right part */}
        <path
          d="M 155 45 L 120 155"
          stroke="url(#sGradient)"
          strokeWidth="16"
          strokeLinecap="round"
        />
      </svg>
    )
  }

  // Full variant with text
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
      <svg
        width={size}
        height={size}
        viewBox="0 0 200 200"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style={{ cursor: 'pointer' }}
      >
        <defs>
          <linearGradient
            id="sGradient"
            x1="0%"
            y1="0%"
            x2="100%"
            y2="100%"
          >
            <stop offset="0%" stopColor="#00d4ff" />
            <stop offset="33%" stopColor="#3366ff" />
            <stop offset="66%" stopColor="#9933ff" />
            <stop offset="100%" stopColor="#ff6633" />
          </linearGradient>
        </defs>
        
        {/* S shape - text letter S */}
        <text
          x="60"
          y="130"
          fontSize="120"
          fontWeight="700"
          fontFamily="Arial, sans-serif"
          fill="url(#sGradient)"
        >
          S
        </text>
        
        {/* X shape - right side */}
        <path
          d="M 110 50 L 145 140"
          stroke="url(#sGradient)"
          strokeWidth="18"
          strokeLinecap="round"
        />
        {/* X shape - right part */}
        <path
          d="M 150 50 L 115 140"
          stroke="url(#sGradient)"
          strokeWidth="18"
          strokeLinecap="round"
        />
      </svg>
      <div className="gradient-text" style={{ fontSize: '24px', fontWeight: '700' }}>
        Socialix
      </div>
    </div>
  )
}

export default SocialixLogo
