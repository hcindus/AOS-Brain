# AGI Company — Motion Design System
**A Division of Performance Supply Depot LLC**

---

## Motion Philosophy

### Core Principles
1. **Purposeful Movement:** Every animation should serve a purpose
2. **Performance First:** Animations must be smooth (60fps minimum)
3. **Subtle Enhancement:** Motion should feel natural, not distracting
4. **Brand Personality:** Motion reflects technical precision and intelligence

### Motion Values
- **Precision:** Sharp, intentional movements
- **Fluidity:** Smooth transitions between states
- **Responsiveness:** Immediate feedback to user actions
- **Depth:** Subtle layering and spatial relationships

---

## Timing Curves

### Standard Easing Functions
```css
:root {
  /* Default - Smooth and natural */
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
  
  /* Enter - Elements appearing */
  --ease-enter: cubic-bezier(0, 0, 0.2, 1);
  
  /* Exit - Elements disappearing */
  --ease-exit: cubic-bezier(0.4, 0, 1, 1);
  
  /* Bounce - Playful emphasis */
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
  
  /* Sharp - Technical precision */
  --ease-sharp: cubic-bezier(0.4, 0, 0.6, 1);
  
  /* Elastic - AI/tech feel */
  --ease-elastic: cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
```

### Duration Scale
| Token | Value | Usage |
|-------|-------|-------|
| `--duration-instant` | 0ms | State changes, no motion |
| `--duration-fast` | 150ms | Micro-interactions, hovers |
| `--duration-normal` | 300ms | Standard transitions |
| `--duration-slow` | 500ms | Page transitions, reveals |
| `--duration-dramatic` | 800ms | Hero animations, emphasis |

---

## Animation Patterns

### Fade Transitions
```css
/* Fade In */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Fade In Up */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Fade In Scale */
@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
```

### Slide Transitions
```css
/* Slide In Right */
@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Slide In Left */
@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Staggered Children */
.stagger-children > * {
  opacity: 0;
  animation: fadeInUp 0.4s var(--ease-enter) forwards;
}

.stagger-children > *:nth-child(1) { animation-delay: 0ms; }
.stagger-children > *:nth-child(2) { animation-delay: 100ms; }
.stagger-children > *:nth-child(3) { animation-delay: 200ms; }
.stagger-children > *:nth-child(4) { animation-delay: 300ms; }
.stagger-children > *:nth-child(5) { animation-delay: 400ms; }
```

---

## Micro-interactions

### Button Hover States
```css
.btn-primary {
  transition: all 0.2s var(--ease-default);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 122, 0, 0.3);
}

.btn-primary:active {
  transform: translateY(0);
  transition-duration: 0.1s;
}
```

### Card Hover Effects
```css
.card {
  transition: transform 0.3s var(--ease-default),
              box-shadow 0.3s var(--ease-default);
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}
```

### Link Hover
```css
.link-animated {
  position: relative;
  text-decoration: none;
}

.link-animated::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--color-electric-cyan);
  transition: width 0.3s var(--ease-default);
}

.link-animated:hover::after {
  width: 100%;
}
```

### Input Focus
```css
.input-field {
  border: 2px solid var(--color-titanium-gray);
  transition: border-color 0.2s var(--ease-default),
              box-shadow 0.2s var(--ease-default);
}

.input-field:focus {
  border-color: var(--color-electric-cyan);
  box-shadow: 0 0 0 4px rgba(0, 224, 255, 0.1);
  outline: none;
}
```

---

## Page Transitions

### Fade Through
```css
.page-enter {
  opacity: 0;
}

.page-enter-active {
  opacity: 1;
  transition: opacity 300ms var(--ease-enter);
}

.page-exit {
  opacity: 1;
}

.page-exit-active {
  opacity: 0;
  transition: opacity 200ms var(--ease-exit);
}
```

### Slide Through
```css
.page-slide-enter {
  opacity: 0;
  transform: translateX(20px);
}

.page-slide-enter-active {
  opacity: 1;
  transform: translateX(0);
  transition: all 400ms var(--ease-enter);
}

.page-slide-exit {
  opacity: 1;
  transform: translateX(0);
}

.page-slide-exit-active {
  opacity: 0;
  transform: translateX(-20px);
  transition: all 300ms var(--ease-exit);
}
```

---

## Agent-Specific Motion Signatures

Each agent has a unique motion language that reflects their personality:

### QORA (Executive)
- **Motion Style:** Confident, deliberate, authoritative
- **Easing:** `--ease-sharp` (precise, no bounce)
- **Timing:** 400ms (measured, not rushed)
- **Signature Move:** Smooth fade with subtle scale (1.0 → 1.02)

```css
.qora-enter {
  animation: qoraEnter 0.4s var(--ease-sharp) forwards;
}

@keyframes qoraEnter {
  from {
    opacity: 0;
    transform: scale(0.98);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
```

### SPINDLE (CTO)
- **Motion Style:** Technical, calculated, efficient
- **Easing:** `--ease-elastic` (slight overshoot)
- **Timing:** 350ms (slightly faster)
- **Signature Move:** Mechanical slide with precision snap

```css
.spindle-enter {
  animation: spindleEnter 0.35s var(--ease-elastic) forwards;
}

@keyframes spindleEnter {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
```

### SCRIBBLE (Creative)
- **Motion Style:** Playful, energetic, fluid
- **Easing:** `--ease-bounce` (lively movement)
- **Timing:** 500ms (more expressive)
- **Signature Move:** Bounce in with rotation

```css
.scribble-enter {
  animation: scribbleEnter 0.5s var(--ease-bounce) forwards;
}

@keyframes scribbleEnter {
  from {
    opacity: 0;
    transform: scale(0.5) rotate(-10deg);
  }
  to {
    opacity: 1;
    transform: scale(1) rotate(0);
  }
}
```

### TAPTAP (UX)
- **Motion Style:** Smooth, responsive, user-friendly
- **Easing:** `--ease-default` (natural flow)
- **Timing:** 250ms (quick response)
- **Signature Move:** Gentle fade up with soft glow

```css
.taptap-enter {
  animation: taptapEnter 0.25s var(--ease-default) forwards;
}

@keyframes taptapEnter {
  from {
    opacity: 0;
    transform: translateY(10px);
    filter: brightness(1.2);
  }
  to {
    opacity: 1;
    transform: translateY(0);
    filter: brightness(1);
  }
}
```

### SENTINEL (Security)
- **Motion Style:** Sharp, vigilant, protective
- **Easing:** `--ease-sharp` (no nonsense)
- **Timing:** 300ms (quick alert)
- **Signature Move:** Alert pulse with border glow

```css
.sentinel-enter {
  animation: sentinelEnter 0.3s var(--ease-sharp) forwards;
}

.sentinel-alert {
  animation: sentinelPulse 2s var(--ease-default) infinite;
}

@keyframes sentinelEnter {
  from {
    opacity: 0;
    border-color: transparent;
  }
  to {
    opacity: 1;
    border-color: var(--color-electric-cyan);
  }
}

@keyframes sentinelPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(0, 224, 255, 0.4); }
  50% { box-shadow: 0 0 0 8px rgba(0, 224, 255, 0); }
}
```

### LEDGER-9 (Finance)
- **Motion Style:** Precise, methodical, data-driven
- **Easing:** Linear with stepped finish
- **Timing:** 450ms (deliberate counting)
- **Signature Move:** Number tick-up with precise snap

```css
.ledger-enter {
  animation: ledgerEnter 0.45s linear forwards;
}

.ledger-count {
  animation: ledgerCount 0.8s steps(10) forwards;
}

@keyframes ledgerEnter {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### PATRICIA (Process)
- **Motion Style:** Clean, organized, systematic
- **Easing:** `--ease-enter` (smooth arrival)
- **Timing:** 350ms (consistent, reliable)
- **Signature Move:** Sequential reveal with checkmark

```css
.patricia-enter {
  animation: patriciaEnter 0.35s var(--ease-enter) forwards;
}

.patricia-check {
  stroke-dasharray: 20;
  stroke-dashoffset: 20;
  animation: patriciaCheck 0.3s var(--ease-enter) forwards;
}

@keyframes patriciaEnter {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes patriciaCheck {
  to {
    stroke-dashoffset: 0;
  }
}
```

---

## Cognitive Architecture Transitions

### 7-Region Brain Visualization
When showing the brain regions, use this choreography:

1. **SuperiorHeart** - Pulse animation (800ms)
2. **Stomach** - Slide from bottom (600ms, 100ms delay)
3. **Intestines** - Slide from right (600ms, 200ms delay)
4. **Brain v4** - Fade in center (500ms, 300ms delay)
5. **3D Cortex** - Scale up (600ms, 400ms delay)
6. **TracRay** - Draw line (800ms, 500ms delay)
7. **Consciousness** - Layer reveal (700ms, 600ms delay)

```css
.brain-region {
  opacity: 0;
}

.brain-region:nth-child(1) { animation: pulseIn 0.8s forwards; }
.brain-region:nth-child(2) { animation: slideUp 0.6s 0.1s forwards; }
.brain-region:nth-child(3) { animation: slideRight 0.6s 0.2s forwards; }
.brain-region:nth-child(4) { animation: fadeIn 0.5s 0.3s forwards; }
.brain-region:nth-child(5) { animation: scaleIn 0.6s 0.4s forwards; }
.brain-region:nth-child(6) { animation: drawLine 0.8s 0.5s forwards; }
.brain-region:nth-child(7) { animation: layerReveal 0.7s 0.6s forwards; }
```

---

## Loading States

### Skeleton Loading
```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-titanium-gray) 25%,
    var(--color-cloud-white) 50%,
    var(--color-titanium-gray) 75%
  );
  background-size: 200% 100%;
  animation: skeleton 1.5s infinite;
}

@keyframes skeleton {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### Spinner
```css
.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid var(--color-titanium-gray);
  border-top-color: var(--color-electric-cyan);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

### Progress Bar
```css
.progress-bar {
  height: 4px;
  background: var(--color-titanium-gray);
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-electric-cyan), var(--color-performance-orange));
  transform-origin: left;
  animation: progress 2s var(--ease-default) forwards;
}

@keyframes progress {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
```

---

## Accessibility

### Reduced Motion Support
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Safe Motion Guidelines
- No flashing content >3Hz (can trigger seizures)
- Provide pause controls for auto-playing animations
- Ensure focus states are visible without animation
- Don't use motion as the only indicator of state change

---

## Implementation Checklist

**CSS Setup:**
- [ ] Define all CSS custom properties
- [ ] Create animation keyframes
- [ ] Set up reduced-motion media query
- [ ] Test on target devices (60fps)

**JavaScript (if using libraries):**
- [ ] Install Framer Motion or GSAP (optional)
- [ ] Create reusable animation components
- [ ] Implement intersection observer for scroll triggers
- [ ] Add animation callbacks for completion events

**Performance:**
- [ ] Test on low-end devices
- [ ] Use `will-change` sparingly
- [ ] Avoid animating layout properties (width, height)
- [ ] Prefer transforms and opacity
- [ ] Test with browser DevTools Performance panel

---

**Document Version:** 1.0  
**Last Updated:** 2026-04-05
