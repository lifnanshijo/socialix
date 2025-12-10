import React from 'react'
import '../styles/colorPalette.css'

function ColorPalette() {
  const colors = [
    {
      name: 'Calm Cyan',
      hex: '#2ACCEB',
      rgb: 'rgb(42, 204, 235)',
      className: 'color-cyan'
    },
    {
      name: 'Calm Cyan',
      hex: '#2ACCEB',
      rgb: 'rgb(42, 204, 235)',
      className: 'color-cyan'
    },
    {
      name: 'Professional Violet',
      hex: '#6E62F9',
      rgb: 'rgb(110, 98, 249)',
      className: 'color-violet'
    },
    {
      name: 'Neutral Deep Dark',
      hex: '#0C0F14',
      rgb: 'rgb(12, 15, 20)',
      className: 'color-black'
    }
  ]

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
  }

  return (
    <div className="color-palette-container">
      <div className="palette-header">
        <h2>SocialX Color Palette</h2>
        <p>Premium brand colors for modern design</p>
      </div>

      <div className="palette-grid">
        {colors.map((color) => (
          <div key={color.name} className="color-card">
            <div className={`color-swatch ${color.className}`}></div>
            
            <div className="color-info">
              <h3>{color.name}</h3>
              
              <div className="color-value">
                <span className="label">HEX</span>
                <span 
                  className="value copyable" 
                  onClick={() => copyToClipboard(color.hex)}
                  title="Click to copy"
                >
                  {color.hex}
                </span>
              </div>
              
              <div className="color-value">
                <span className="label">RGB</span>
                <span 
                  className="value copyable" 
                  onClick={() => copyToClipboard(color.rgb)}
                  title="Click to copy"
                >
                  {color.rgb}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="palette-gradient">
        <h3>Master Gradient</h3>
        <div className="gradient-preview"></div>
        <p className="gradient-code">linear-gradient(135deg, #2ACCEB, #6E62F9)</p>
      </div>
    </div>
  )
}

export default ColorPalette
