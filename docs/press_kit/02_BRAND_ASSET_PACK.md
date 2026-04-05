# AGI Company — Brand Asset Pack
**A Division of Performance Supply Depot LLC**

---

## Quick Reference

### Brand in 30 Seconds
- **Name:** AGI Company
- **Parent:** Performance Supply Depot LLC
- **Tagline:** "Intelligence Engineered."
- **Personality:** Technical authority meets operational reliability
- **Colors:** Deep Tech Blue, Electric Cyan, Performance Orange
- **Fonts:** Inter Tight (headlines), Inter (body), JetBrains Mono (code)

---

## Color Palettes

### Primary Palette
```css
:root {
  --color-deep-tech-blue: #0A1A2F;
  --color-electric-cyan: #00E0FF;
  --color-graphite-black: #111111;
}
```

### Extended Palette
```css
:root {
  --color-titanium-gray: #C7CCD1;
  --color-performance-orange: #FF7A00;
  --color-cloud-white: #F8F9FA;
  --color-pure-white: #FFFFFF;
}

/* Semantic Colors */
--color-success: #2ECC71;
--color-warning: #F39C12;
--color-error: #E74C3C;
--color-info: #3498DB;
```

### Gradient Presets
```css
/* Hero Gradient */
background: linear-gradient(135deg, #0A1A2F 0%, #1a3a5f 100%);

/* Accent Gradient */
background: linear-gradient(90deg, #00E0FF 0%, #00B8D4 100%);

/* CTA Gradient */
background: linear-gradient(135deg, #FF7A00 0%, #FF5722 100%);
```

---

## Typography

### Font Import (Web)
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Inter+Tight:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

### CSS Variables
```css
:root {
  /* Font Families */
  --font-headline: 'Inter Tight', Arial Black, sans-serif;
  --font-body: 'Inter', Roboto, Helvetica, sans-serif;
  --font-mono: 'JetBrains Mono', Consolas, monospace;
  
  /* Font Sizes */
  --text-h1: 4rem;      /* 64px */
  --text-h2: 3rem;      /* 48px */
  --text-h3: 2rem;      /* 32px */
  --text-h4: 1.5rem;    /* 24px */
  --text-body-lg: 1.25rem;  /* 20px */
  --text-body: 1rem;    /* 16px */
  --text-small: 0.875rem;   /* 14px */
  --text-caption: 0.75rem;  /* 12px */
}
```

### Type Scale Classes
```css
.headline-1 { font-size: var(--text-h1); font-weight: 800; line-height: 1.1; }
.headline-2 { font-size: var(--text-h2); font-weight: 700; line-height: 1.2; }
.headline-3 { font-size: var(--text-h3); font-weight: 600; line-height: 1.3; }
.body-large { font-size: var(--text-body-lg); font-weight: 400; line-height: 1.6; }
.body-text { font-size: var(--text-body); font-weight: 400; line-height: 1.6; }
.text-small { font-size: var(--text-small); font-weight: 400; line-height: 1.5; }
.text-caption { font-size: var(--text-caption); font-weight: 500; line-height: 1.4; letter-spacing: 1px; text-transform: uppercase; }
```

---

## Logo Assets

### Logo Files Location
```
assets/logos/
├── agi-logo-full.svg       # Mark + Wordmark + Division
├── agi-logo-compact.svg    # Mark + AGI only
├── agi-mark.svg            # Icon only
├── agi-wordmark.svg        # Text only
├── agi-logo-white.svg      # White version for dark backgrounds
└── agi-logo-black.svg      # Black version for light backgrounds
```

### Logo Usage Snippets

**HTML:**
```html
<!-- Full Logo -->
<img src="assets/logos/agi-logo-full.svg" alt="AGI Company - A Division of Performance Supply Depot LLC" width="200">

<!-- Compact Logo -->
<img src="assets/logos/agi-logo-compact.svg" alt="AGI" width="48">

<!-- Icon Only -->
<img src="assets/logos/agi-mark.svg" alt="AGI" width="32">
```

**CSS Background:**
```css
.logo {
  background: url('assets/logos/agi-logo-white.svg') no-repeat center;
  background-size: contain;
  width: 200px;
  height: 48px;
}
```

### Clear Space Rules
- Minimum clear space: Equal to the height of the "A" in AGI
- Never place closer than clear space to other elements
- Maintain aspect ratio at all times

---

## Iconography

### Icon Set
```
assets/icons/
├── core/
│   ├── icon-menu.svg
│   ├── icon-close.svg
│   ├── icon-arrow-right.svg
│   ├── icon-arrow-left.svg
│   ├── icon-chevron-down.svg
│   ├── icon-external.svg
│   └── icon-download.svg
├── agent/
│   ├── icon-agent-qora.svg
│   ├── icon-agent-spindle.svg
│   ├── icon-agent-scribble.svg
│   ├── icon-agent-taptap.svg
│   ├── icon-agent-sentinel.svg
│   ├── icon-agent-ledger.svg
│   └── icon-agent-patricia.svg
└── social/
    ├── icon-github.svg
    ├── icon-twitter.svg
    ├── icon-linkedin.svg
    └── icon-discord.svg
```

### Icon Usage
```html
<!-- Inline SVG -->
<svg class="icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M5 12h14M12 5l7 7-7 7"/>
</svg>

<!-- CSS -->
.icon {
  width: 24px;
  height: 24px;
  stroke: var(--color-electric-cyan);
}
```

---

## UI Components

### Button Styles
```css
/* Primary Button */
.btn-primary {
  background: var(--color-performance-orange);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 32px;
  font-family: var(--font-body);
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-primary:hover {
  background: #E66E00;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 122, 0, 0.3);
}

/* Secondary Button */
.btn-secondary {
  background: transparent;
  color: var(--color-electric-cyan);
  border: 2px solid var(--color-electric-cyan);
  border-radius: 8px;
  padding: 12px 32px;
}
.btn-secondary:hover {
  background: var(--color-electric-cyan);
  color: var(--color-deep-tech-blue);
}
```

### Card Component
```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Card Title</h3>
  </div>
  <div class="card-body">
    <p>Card content goes here.</p>
  </div>
  <div class="card-footer">
    <button class="btn-primary">Action</button>
  </div>
</div>
```

```css
.card {
  background: var(--color-cloud-white);
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  transition: box-shadow 0.2s ease;
}
.card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
```

---

## Pattern Library

### Background Patterns
```css
/* Grid Pattern */
.bg-grid {
  background-image: 
    linear-gradient(rgba(0, 224, 255, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 224, 255, 0.05) 1px, transparent 1px);
  background-size: 40px 40px;
}

/* Dot Pattern */
.bg-dots {
  background-image: radial-gradient(rgba(0, 224, 255, 0.3) 1px, transparent 1px);
  background-size: 20px 20px;
}

/* Circuit Pattern (decorative) */
.bg-circuit {
  background-image: url('assets/patterns/circuit-pattern.svg');
  background-repeat: repeat;
  opacity: 0.1;
}
```

### Dividers
```css
.divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--color-titanium-gray), transparent);
  margin: 48px 0;
}

.divider-accent {
  height: 2px;
  background: linear-gradient(90deg, var(--color-electric-cyan), var(--color-performance-orange));
  width: 100px;
  margin: 24px 0;
}
```

---

## Agent Identity Badges

### Badge Styles
```html
<span class="agent-badge agent-qora">QORA</span>
<span class="agent-badge agent-spindle">SPINDLE</span>
<span class="agent-badge agent-scribble">SCRIBBLE</span>
```

```css
.agent-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 1px;
}

.agent-qora { background: #FFD700; color: #111; }
.agent-spindle { background: #C0C0C0; color: #111; }
.agent-scribble { background: #9B59B6; color: white; }
.agent-taptap { background: #2ECC71; color: #111; }
.agent-sentinel { background: #E74C3C; color: white; }
.agent-ledger { background: #3498DB; color: white; }
.agent-patricia { background: #1ABC9C; color: white; }
```

---

## Media Kit

### Boilerplate (Company Description)
```
AGI Company, a division of Performance Supply Depot LLC, builds enterprise-grade artificial 
intelligence systems engineered for real-world performance. Combining advanced AGI research 
with operational expertise, AGI Company delivers intelligent solutions that drive measurable 
outcomes for modern organizations. The company's multi-agent ecosystem, known as BEAST 
(Bounded, Explicit, Agentic, Safe, Tool-augmented), represents the cutting edge of 
agent-based artificial intelligence.

Founded: 2024
Headquarters: Digital Frontier
Parent Company: Performance Supply Depot LLC
Press Contact: press@agicompany.ai
```

### Social Media Assets

**Twitter/X:**
- Profile image: agi-mark.svg (400x400px)
- Header: 1500x500px hero image
- Bio: "Intelligence Engineered. Enterprise-grade AGI solutions built for real-world performance. | A division of @PSD_LLC"

**LinkedIn:**
- Company page banner: 1536x768px
- Logo: 300x300px minimum

**GitHub:**
- Organization avatar: agi-mark.svg
- README header: 1280x640px

---

## File Checklist

**Required for Brand Launch:**
- [ ] Logo files (SVG, PNG, EPS)
- [ ] Color palette (CSS, JSON, ASE)
- [ ] Typography (Web fonts, CSS)
- [ ] Icon set (SVG, 24px and 48px)
- [ ] Social media templates (Photoshop/Figma)
- [ ] Presentation template (Keynote/PowerPoint)
- [ ] Business card template
- [ ] Email signature template

**Nice to Have:**
- [ ] Animated logo (GIF, Lottie)
- [ ] Video intro/outro
- [ ] Merchandise mockups
- [ ] Billboard template

---

**Document Version:** 1.0  
**Last Updated:** 2026-04-05
