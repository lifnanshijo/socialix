# Socialix Brand Guide

## Overview
Socialix is a modern social media platform with a vibrant, dynamic brand identity. The design language emphasizes connection, creativity, and movement through a sophisticated gradient color palette and smooth animations.

---

## Color Palette

### Primary Colors
- **Cyan**: `#00d4ff` - Fresh, modern, and energetic
- **Blue**: `#3366ff` - Trust and reliability
- **Purple**: `#9933ff` - Creativity and innovation
- **Orange**: `#ff6633` - Warmth and engagement

### Primary Gradient
```
linear-gradient(135deg, #00d4ff, #3366ff, #9933ff, #ff6633)
```

### Supporting Colors
- **Primary Action**: `#3366ff`
- **Secondary Action**: `#ff6633`
- **Accent**: `#00d4ff`

### Background Colors
- **Light Mode**: `#f8f9ff` (Soft blue-tinted white)
- **Dark Mode**: `#0f1419` (Deep blue-black)

### Text Colors
- **Light Mode**: `#1a1f2e` (Dark blue)
- **Dark Mode**: `#f0f2f5` (Light gray)

---

## Logo & Branding

### Logo Specifications
The Socialix logo features:
- A flowing "S" shape representing connection and flow
- An "X" shape representing crossing connections
- Gradient coloring from cyan through blue, purple, to orange
- Modern, minimalist design

### Logo Usage
- **Full Logo**: Use with text "Socialix" for main branding
- **Icon Only**: Use the SX symbol for navigation bars and favicons
- **Minimum Size**: 32px for clarity
- **Clear Space**: Maintain 10px padding around the logo

### Logo File
Location: `client/src/components/SocialixLogo.jsx`

---

## Typography

### Font Family
`-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif`

### Font Weights
- **Regular**: 400 - Body text
- **Medium**: 500 - Secondary headings
- **Semi-Bold**: 600 - Button text, emphasis
- **Bold**: 700 - Main headings, gradient text

### Heading Sizes
- **H1**: 32px - Page titles
- **H2**: 22-26px - Section titles
- **H3**: 18-20px - Subsection titles
- **H4**: 16px - Card titles

---

## Components

### Buttons

#### Primary Button
```css
background: linear-gradient(135deg, #3366ff, #9933ff);
padding: 10px 20px;
border-radius: 6px;
color: white;
font-weight: 600;
```

**Hover State**: Darker gradient with elevation effect
```css
transform: translateY(-2px);
box-shadow: 0 8px 20px rgba(51, 102, 255, 0.4);
```

#### Secondary Button
```css
background: linear-gradient(135deg, #ff6633, #ff8844);
padding: 10px 20px;
border-radius: 6px;
color: white;
font-weight: 600;
```

### Cards
- **Border Radius**: 8-16px
- **Padding**: 20px
- **Shadow**: 0 2px 4px rgba(0, 0, 0, 0.1)
- **Accent**: Top gradient border (3px height)

### Input Fields
- **Border Radius**: 6px
- **Padding**: 12px
- **Focus State**: Blue outline (2px)
- **Background**: Inherits from theme

### Navigation Bar
- **Position**: Fixed, sticky top
- **Height**: Auto (with padding)
- **Gradient Border**: Bottom border with Socialix gradient
- **Shadow**: Enhanced shadow with blue tint

---

## Animations & Interactions

### Transition Timing
- **Default**: 0.3s cubic-bezier(0.4, 0, 0.2, 1)
- **Fast**: 0.2s ease (buttons, links)
- **Slow**: 0.6s ease (page transitions)

### Hover Effects
1. **Buttons**: Lift effect + glow shadow
2. **Links**: Color change + underline
3. **Cards**: Border opacity increase + subtle lift
4. **Navigation**: Highlight with primary color

### Gradient Animations
```css
@keyframes gradientFlow {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
```

---

## Theme Implementation

### Light Theme
- Background: `#f8f9ff`
- Cards: `#ffffff` with blue-tinted borders
- Text: `#1a1f2e`
- Borders: `#e0e6ff`

### Dark Theme
- Background: `#0f1419`
- Cards: `#1a1f2e` with gradient accents
- Text: `#f0f2f5`
- Borders: `#2a3347`

### Theme Toggle
Located in Navbar - click moon/sun icon to switch

---

## Layout & Spacing

### Spacing Scale
- **XS**: 4px
- **S**: 8px
- **M**: 12px
- **L**: 16px
- **XL**: 20px
- **2XL**: 40px

### Container Sizes
- **Mobile**: Full width - 20px padding
- **Tablet**: 600px max-width
- **Desktop**: 800-1200px max-width

### Responsive Breakpoints
- **Mobile**: 0-600px
- **Tablet**: 601px-900px
- **Desktop**: 900px+

---

## CSS Variables Reference

```css
--primary-cyan: #00d4ff
--primary-blue: #3366ff
--primary-purple: #9933ff
--primary-orange: #ff6633
--primary-gradient: linear-gradient(135deg, #00d4ff, #3366ff, #9933ff, #ff6633)
--primary-color: #3366ff
--secondary-color: #ff6633
--accent-color: #00d4ff
--background-light: #f8f9ff
--background-dark: #0f1419
--card-light: #ffffff
--card-dark: #1a1f2e
--text-light: #1a1f2e
--text-dark: #f0f2f5
--border-light: #e0e6ff
--border-dark: #2a3347
```

---

## Usage Guidelines

### Do's ✓
- Use the gradient for primary actions
- Maintain adequate contrast for accessibility
- Apply hover states consistently
- Use white space effectively
- Keep animations subtle and purposeful

### Don'ts ✗
- Don't use the old blue (#1877f2) - use the new Socialix blue (#3366ff)
- Don't apply multiple overlapping animations
- Don't reduce the logo size below 32px
- Don't change the gradient order
- Don't use low contrast text combinations

---

## Accessibility

### Color Contrast
- Text on buttons: 4.5:1 (WCAG AA standard)
- Text on backgrounds: 4.5:1 minimum
- Focus indicators: 2px solid outline

### Interactive Elements
- Minimum touch target: 44x44px
- Clear focus states on all interactive elements
- Proper ARIA labels on buttons and navigation

---

## Component Locations

- **Logo**: `client/src/components/SocialixLogo.jsx`
- **Navbar**: `client/src/components/Navbar.jsx`
- **Global Styles**: `client/src/styles/index.css`
- **Auth Styles**: `client/src/styles/auth.css`
- **Home Styles**: `client/src/styles/home.css`
- **Navbar Styles**: `client/src/styles/navbar.css`

---

## Future Enhancements

- [ ] Custom SVG icons with gradient fills
- [ ] Animated loading states with gradient
- [ ] Smooth page transitions with gradient overlays
- [ ] Gradient-based data visualizations
- [ ] Parallax effects with brand colors

---

**Last Updated**: December 10, 2025
**Version**: 1.0
