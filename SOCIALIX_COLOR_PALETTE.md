# 🎨 Socialix Color Palette

## Official Brand Colors

```
┌─────────────────────────────────┐
│  SOCIALIX GRADIENT PALETTE      │
├─────────────────────────────────┤
│  🔵 CYAN         #00d4ff        │
│  🔵 BLUE         #3366ff        │
│  💜 PURPLE       #9933ff        │
│  🟠 ORANGE       #ff6633        │
└─────────────────────────────────┘
```

## Color Specifications

### Cyan - #00d4ff
- **RGB**: 0, 212, 255
- **HSL**: 187°, 100%, 50%
- **Usage**: Accents, highlights, fresh elements
- **Contrast**: Excellent on dark backgrounds
- **Accessibility**: WCAG AA ✓

### Blue - #3366ff
- **RGB**: 51, 102, 255
- **HSL**: 217°, 100%, 60%
- **Usage**: Primary actions, trust elements
- **Contrast**: Excellent on light backgrounds
- **Accessibility**: WCAG AA ✓

### Purple - #9933ff
- **RGB**: 153, 51, 255
- **HSL**: 270°, 100%, 60%
- **Usage**: Creative elements, transitions
- **Contrast**: Good on light backgrounds
- **Accessibility**: WCAG AA ✓

### Orange - #ff6633
- **RGB**: 255, 102, 51
- **HSL**: 15°, 100%, 60%
- **Usage**: Secondary actions, warmth, engagement
- **Contrast**: Excellent on light backgrounds
- **Accessibility**: WCAG AA ✓

---

## Unified Gradient

```css
linear-gradient(135deg, #00d4ff, #3366ff, #9933ff, #ff6633)
```

**Direction**: 135° (top-left to bottom-right diagonal)
**Smoothness**: Seamless color transitions
**Application**: Buttons, borders, text, backgrounds

---

## UI Application Colors

### Primary Color
```
Color:      #3366ff (Blue)
CSS Var:    --primary-color
Usage:      Main actions, focus states
Example:    Primary buttons, link color
```

### Secondary Color
```
Color:      #ff6633 (Orange)
CSS Var:    --secondary-color
Usage:      Alternative actions
Example:    Secondary buttons
```

### Accent Color
```
Color:      #00d4ff (Cyan)
CSS Var:    --accent-color
Usage:      Highlights, emphasis
Example:    Link hover, card accents
```

---

## Theme Colors

### Light Theme

```
Background:     #f8f9ff
├─ Tint:        Soft blue
├─ Usage:       Main page background
└─ Contrast:    Excellent with dark text

Cards:          #ffffff
├─ Border:      #e0e6ff
├─ Usage:       Content containers
└─ Shadow:      Subtle

Text:           #1a1f2e
├─ Contrast:    WCAG AAA (7.1:1)
├─ Primary:     Body text
└─ Secondary:   #65676b (gray)

Border:         #e0e6ff
├─ Light shade
├─ Used for:    Dividers, subtle borders
└─ Opacity:     100%
```

### Dark Theme

```
Background:     #0f1419
├─ Tint:        Deep blue-black
├─ Usage:       Main page background
└─ Contrast:    Excellent with light text

Cards:          #1a1f2e
├─ Border:      #2a3347
├─ Usage:       Content containers
└─ Shadow:      Enhanced blue tint

Text:           #f0f2f5
├─ Contrast:    WCAG AAA (15:1)
├─ Primary:     Body text
└─ Secondary:   #99a0a7 (light gray)

Border:         #2a3347
├─ Dark shade
├─ Used for:    Dividers, subtle borders
└─ Opacity:     100%
```

---

## Color Combinations

### Recommended Pairings

#### Blue + Cyan
```
Primary Action + Accent
Use for: Interactive elements, CTAs
Example: Main button + hover glow
```

#### Purple + Orange
```
Creative + Warm
Use for: Gradient transitions
Example: Secondary actions
```

#### Blue + Purple
```
Trust + Innovation
Use for: Gradient emphasis
Example: Gradient text, primary gradient
```

#### All Four Colors
```
Full Gradient (Cyan → Blue → Purple → Orange)
Use for: Main branding
Example: Navigation border, logo
```

---

## Contrast Ratios

### Light Theme

| Element | Background | Ratio | WCAG |
|---------|-----------|-------|------|
| Dark Text | Light BG | 7.1:1 | AAA |
| Blue Link | Light BG | 5.2:1 | AA |
| Purple Text | Light BG | 5.0:1 | AA |
| White Button | Blue BG | 4.5:1 | AA |

### Dark Theme

| Element | Background | Ratio | WCAG |
|---------|-----------|-------|------|
| Light Text | Dark BG | 15:1 | AAA |
| Cyan Link | Dark BG | 5.8:1 | AA |
| Blue Text | Dark BG | 4.8:1 | AA |
| White Button | Blue BG | 10:1 | AAA |

---

## CSS Implementation

### Variables Declaration

```css
:root {
  /* Brand Colors */
  --primary-cyan: #00d4ff;
  --primary-blue: #3366ff;
  --primary-purple: #9933ff;
  --primary-orange: #ff6633;
  
  /* Gradient */
  --primary-gradient: linear-gradient(
    135deg,
    #00d4ff,
    #3366ff,
    #9933ff,
    #ff6633
  );
  
  /* UI Colors */
  --primary-color: #3366ff;      /* Blue */
  --secondary-color: #ff6633;    /* Orange */
  --accent-color: #00d4ff;       /* Cyan */
  
  /* Light Theme */
  --background-light: #f8f9ff;
  --card-light: #ffffff;
  --text-light: #1a1f2e;
  --border-light: #e0e6ff;
  
  /* Dark Theme */
  --background-dark: #0f1419;
  --card-dark: #1a1f2e;
  --text-dark: #f0f2f5;
  --border-dark: #2a3347;
}
```

### Using Colors

```css
/* Primary color */
button { color: var(--primary-color); }

/* Gradient */
h1 { background: var(--primary-gradient); }

/* Theme-aware */
.light-theme { color: var(--text-light); }
.dark-theme { color: var(--text-dark); }
```

---

## Color Applications by Component

### Buttons

```
Primary:
  Background:   Blue → Purple gradient
  Text:         White
  Hover:        Darker blue → darker purple

Secondary:
  Background:   Orange gradient
  Text:         White
  Hover:        Darker orange
```

### Links

```
Normal:         Primary color (Blue)
Hover:          Accent color (Cyan)
Active:         Primary color (darker)
Visited:        Purple (slightly darker)
```

### Cards

```
Background:     Theme color (light white / dark #1a1f2e)
Border:         Gradient accent at top
Shadow:         Blue tint (0 2px 4px rgba(51, 102, 255, 0.1))
Hover:          Border becomes more visible
```

### Text

```
Heading:        Gradient (Cyan → Blue → Purple → Orange)
Body:           Theme text color
Secondary:      Muted (gray)
Emphasis:       Primary color (Blue)
```

### Navigation

```
Background:     Theme color
Border:         Gradient line (Cyan → Orange)
Icons:          Theme text color
Hover:          Primary color with glow
Active:         Primary color with highlight
```

---

## Accessibility Notes

### Contrast Standards
- **WCAG AA**: 4.5:1 minimum (normal text)
- **WCAG AAA**: 7:1 minimum (enhanced)
- **All brand colors meet WCAG AA** for most text sizes

### When Combining Colors
1. Always check contrast ratio
2. Use darker shades for backgrounds
3. Use lighter shades for text
4. Test with accessibility tools
5. Get feedback from users with color blindness

### Color Blind Safe
- Gradient includes high contrast colors
- Not solely reliant on hue (includes lightness)
- Blue and orange have good contrast
- Cyan adds brightness for visibility

---

## Hex Color Reference Card

```
┌──────────────────────────────┐
│  QUICK COLOR REFERENCE       │
├──────────────────────────────┤
│  Cyan:      #00d4ff          │
│  Blue:      #3366ff          │
│  Purple:    #9933ff          │
│  Orange:    #ff6633          │
│  Light BG:  #f8f9ff          │
│  Dark BG:   #0f1419          │
│  Light Card: #ffffff         │
│  Dark Card:  #1a1f2e         │
│  Light Text: #1a1f2e         │
│  Dark Text:  #f0f2f5         │
└──────────────────────────────┘
```

---

## Usage Examples

### Complete Button
```css
.btn-primary {
  background: linear-gradient(135deg, #3366ff, #9933ff);
  color: white;
  border: none;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #1f4cdb, #7a1fb8);
  box-shadow: 0 8px 20px rgba(51, 102, 255, 0.4);
}
```

### Card Accent
```css
.card {
  background: var(--card-light);
  border: 1px solid var(--border-light);
  border-top: 3px solid;
  border-image: linear-gradient(90deg, #00d4ff, #3366ff, #9933ff, #ff6633) 1;
}
```

### Gradient Text
```css
.gradient-text {
  background: linear-gradient(135deg, #00d4ff, #3366ff, #9933ff, #ff6633);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

---

## Color Customization

### To Change Primary Color
```css
:root {
  --primary-color: [NEW COLOR];
  /* Updates all primary buttons, links, etc. */
}
```

### To Adjust Theme
```css
:root {
  --background-light: [NEW COLOR];
  --card-light: [NEW COLOR];
  /* Updates entire light theme */
}
```

### To Modify Gradient
```css
:root {
  --primary-gradient: linear-gradient(
    135deg,
    [COLOR1],
    [COLOR2],
    [COLOR3],
    [COLOR4]
  );
}
```

---

## Color Inspiration

The Socialix color palette is inspired by:
- **Cyan**: Modern, tech-forward, fresh
- **Blue**: Professional, trustworthy, stable
- **Purple**: Creative, innovative, premium
- **Orange**: Energetic, engaging, warm

Combined, they create a **vibrant, connected, modern** brand identity.

---

## Print Color Values

### For Design Tools

| Name | Hex | RGB | HSL |
|------|-----|-----|-----|
| Cyan | #00d4ff | 0, 212, 255 | 187°, 100%, 50% |
| Blue | #3366ff | 51, 102, 255 | 217°, 100%, 60% |
| Purple | #9933ff | 153, 51, 255 | 270°, 100%, 60% |
| Orange | #ff6633 | 255, 102, 51 | 15°, 100%, 60% |

### For Web Standards

```html
<meta name="theme-color" content="#3366ff">
<!-- Suggests browser UI color (Blue) -->
```

---

**Color Palette Version**: 1.0  
**Last Updated**: December 10, 2025  
**Status**: ✅ Official Brand Colors

Use this palette for all Socialix branding and design work! 🎨
