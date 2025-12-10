import React, { useState } from 'react'
import '../styles/colorSystemPalette.css'

function ColorSystemPalette() {
  const [copiedColor, setCopiedColor] = useState(null)

  const colorSystem = {
    primary: [
      { name: 'Calm Cyan', hex: '#2ACCEB', rgb: 'rgb(42, 204, 235)', usage: 'Primary CTA, focus states, hero elements' },
      { name: 'Professional Violet', hex: '#6E62F9', rgb: 'rgb(110, 98, 249)', usage: 'Accent elements, secondary CTAs, highlights' },
      { name: 'Gradient', hex: 'linear-gradient(135deg, #2ACCEB, #6E62F9)', rgb: 'Cyan to Violet', usage: 'Buttons, cards, visual interest' }
    ],
    backgrounds: [
      { name: 'Neutral Deep Dark', hex: '#0C0F14', rgb: 'rgb(12, 15, 20)', usage: 'Page background, deep elements' },
      { name: 'Card Background', hex: '#13171F', rgb: 'rgb(19, 23, 31)', usage: 'Cards, panels, elevated surfaces' },
      { name: 'Card Background', hex: '#13171F', rgb: 'rgb(19, 23, 31)', usage: 'Secondary panels, modals, overlays' }
    ],
    text: [
      { name: 'Neutral Text', hex: '#D6DAE0', rgb: 'rgb(214, 218, 224)', usage: 'Main headings, body text, primary content', contrast: 'AAA' },
      { name: 'Secondary Text', hex: '#A4A7AE', rgb: 'rgb(164, 167, 174)', usage: 'Labels, hints, supporting text', contrast: 'AA' },
      { name: 'Muted Text', hex: '#70737A', rgb: 'rgb(112, 115, 122)', usage: 'Disabled text, placeholders, timestamps', contrast: 'A' }
    ],
    states: [
      { name: 'Success', hex: '#3AE67F', rgb: 'rgb(58, 230, 127)', usage: 'Success messages, confirmations, valid states' },
      { name: 'Warning', hex: '#FFC343', rgb: 'rgb(255, 195, 67)', usage: 'Warnings, pending actions, cautions' },
      { name: 'Error', hex: '#FF4D5A', rgb: 'rgb(255, 77, 90)', usage: 'Errors, destructive actions, alerts' }
    ]
  }

  const copyToClipboard = (text, type) => {
    navigator.clipboard.writeText(text)
    setCopiedColor(`${type}-${text}`)
    setTimeout(() => setCopiedColor(null), 2000)
  }

  const ColorCard = ({ color }) => (
    <div className="color-card">
      <div className="color-preview" style={{ backgroundColor: color.hex }}></div>
      <div className="color-details">
        <h4>{color.name}</h4>
        <div className="color-codes">
          <div className="code-item" onClick={() => copyToClipboard(color.hex, 'hex')} title="Click to copy">
            <span className="label">HEX</span>
            <span className="value">{color.hex}</span>
          </div>
          <div className="code-item" onClick={() => copyToClipboard(color.rgb, 'rgb')} title="Click to copy">
            <span className="label">RGB</span>
            <span className="value">{color.rgb}</span>
          </div>
        </div>
        <p className="usage">{color.usage}</p>
        {color.contrast && <span className="contrast-badge">{color.contrast} Contrast</span>}
      </div>
    </div>
  )

  return (
    <div className="color-system-container">
      <div className="system-header">
        <h1>SocialX Color System</h1>
        <p>Futuristic neon aesthetic with production-ready dark mode palette</p>
      </div>

      {/* Primary Brand Colors */}
      <section className="color-section">
        <div className="section-header">
          <h2>Primary Brand Colors</h2>
          <p>Core colors for CTAs, accents, and primary interactions</p>
        </div>
        <div className="color-grid">
          {colorSystem.primary.map((color) => (
            <ColorCard key={color.hex} color={color} />
          ))}
        </div>
      </section>

      {/* Backgrounds */}
      <section className="color-section">
        <div className="section-header">
          <h2>Background System</h2>
          <p>Layered background hierarchy for depth and visual hierarchy</p>
        </div>
        <div className="color-grid">
          {colorSystem.backgrounds.map((color) => (
            <ColorCard key={color.hex} color={color} />
          ))}
        </div>
        <div className="background-demo">
          <div className="demo-level-1">Main Background (#0A0A0F)</div>
          <div className="demo-level-2">Card Background (#11131A)</div>
          <div className="demo-level-3">Panel Background (#1A1D26)</div>
        </div>
      </section>

      {/* Text Colors */}
      <section className="color-section">
        <div className="section-header">
          <h2>Text Colors</h2>
          <p>Semantic text hierarchy with WCAG contrast compliance</p>
        </div>
        <div className="color-grid">
          {colorSystem.text.map((color) => (
            <ColorCard key={color.hex} color={color} />
          ))}
        </div>
      </section>

      {/* UI State Colors */}
      <section className="color-section">
        <div className="section-header">
          <h2>UI State Colors</h2>
          <p>Semantic colors for system feedback and status indication</p>
        </div>
        <div className="color-grid">
          {colorSystem.states.map((color) => (
            <ColorCard key={color.hex} color={color} />
          ))}
        </div>
      </section>

      {/* CSS Variables */}
      <section className="color-section">
        <div className="section-header">
          <h2>CSS Variables</h2>
          <p>Ready-to-use CSS custom properties for your stylesheets</p>
        </div>
        <div className="code-block">
          <pre>{`:root {
  /* Primary Brand Colors */
  --color-primary-cyan: #2ACCEB;
  --color-primary-violet: #6E62F9;
  
  /* Background System */
  --color-bg-main: #0C0F14;
  --color-bg-card: #13171F;
  
  /* Text Colors */
  --color-text-primary: #D6DAE0;
  --color-text-secondary: #A4A7AE;
  --color-text-muted: #70737A;
  
  /* Gradient */
  --color-gradient: linear-gradient(135deg, #2ACCEB, #6E62F9);
  
  /* UI States */
  --color-success: #3AE67F;
  --color-warning: #FFC343;
  --color-error: #FF4D5A;
  
  /* Glow Effect */
  --color-glow: rgba(255, 255, 255, 0.15);
}`}</pre>
        </div>
      </section>

      {/* Guidelines */}
      <section className="color-section guidelines-section">
        <div className="section-header">
          <h2>Usage Guidelines</h2>
          <p>Best practices for applying colors throughout your interface</p>
        </div>

        <div className="guidelines-grid">
          <div className="guideline-card">
            <h3>🎯 Primary Actions</h3>
            <p><strong>Button:</strong> Neon Cyan (#00E7FF)</p>
            <p><strong>Hover:</strong> Add cyan glow (opacity 0.8)</p>
            <p><strong>Active:</strong> Darken by 20%</p>
          </div>

          <div className="guideline-card">
            <h3>🎨 Backgrounds</h3>
            <p><strong>Level 1:</strong> Main (#0A0A0F) - Page background</p>
            <p><strong>Level 2:</strong> Card (#11131A) - Content cards</p>
            <p><strong>Level 3:</strong> Panel (#1A1D26) - Modals, overlays</p>
          </div>

          <div className="guideline-card">
            <h3>📝 Typography</h3>
            <p><strong>Headings:</strong> Primary Text (#F4F6F8)</p>
            <p><strong>Body:</strong> Primary Text with reduced opacity</p>
            <p><strong>Support:</strong> Secondary/Muted Text</p>
          </div>

          <div className="guideline-card">
            <h3>⚡ Accents</h3>
            <p><strong>Secondary CTA:</strong> Purple Glow (#9D4DFF)</p>
            <p><strong>Highlights:</strong> Magenta Accent (#FF3EFF)</p>
            <p><strong>Focus states:</strong> Use primary cyan</p>
          </div>

          <div className="guideline-card">
            <h3>✅ Feedback States</h3>
            <p><strong>Success:</strong> Green (#3AE67F)</p>
            <p><strong>Warning:</strong> Yellow (#FFC343)</p>
            <p><strong>Error:</strong> Red (#FF4D5A)</p>
          </div>

          <div className="guideline-card">
            <h3>♿ Accessibility</h3>
            <p><strong>Contrast:</strong> AAA for primary text</p>
            <p><strong>Ensure:</strong> No color-only indicators</p>
            <p><strong>Alt:</strong> Combine with icons/text</p>
          </div>
        </div>
      </section>

      {/* Gradient Combinations */}
      <section className="color-section">
        <div className="section-header">
          <h2>Gradient Combinations</h2>
          <p>Recommended gradient pairings for visual interest</p>
        </div>
        <div className="gradients-grid">
          <div className="gradient-card">
            <div className="gradient-preview" style={{
              background: 'linear-gradient(135deg, #2ACCEB 0%, #6E62F9 100%)'
            }}></div>
            <p>Cyan → Violet</p>
          </div>
          <div className="gradient-card">
            <div className="gradient-preview" style={{
              background: 'linear-gradient(135deg, #6E62F9 0%, #2ACCEB 100%)'
            }}></div>
            <p>Violet → Cyan</p>
          </div>
          <div className="gradient-card">
            <div className="gradient-preview" style={{
              background: 'linear-gradient(135deg, #2ACCEB 0%, #D6DAE0 100%)'
            }}></div>
            <p>Cyan → Text</p>
          </div>
          <div className="gradient-card">
            <div className="gradient-preview" style={{
              background: 'linear-gradient(135deg, #0C0F14, #13171F)'
            }}></div>
            <p>Dark to Card</p>
          </div>
        </div>
      </section>
    </div>
  )
}

export default ColorSystemPalette
