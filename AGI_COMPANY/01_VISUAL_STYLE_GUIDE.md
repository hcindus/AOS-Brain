# AGI Company — Visual Style Guide
**A Division of Performance Supply Depot LLC**

---

## 1. Brand Positioning

### Core Identity
AGI Company is positioned as a **precision-driven, enterprise-grade AI solutions provider** built on the operational backbone of Performance Supply Depot LLC.

**Brand Values:**
- Technical authority
- Operational reliability
- Enterprise trust
- Forward-thinking innovation

### Tagline Options
1. **"Intelligence Engineered."** *(Primary)*
2. "Operational AI for the Real World."
3. "Where Applied Intelligence Meets Performance."

---

## 2. Color Palette

### Primary Colors
| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Deep Tech Blue** | `#0A1A2F` | 10, 26, 47 | Backgrounds, headers, hero sections |
| **Electric Cyan** | `#00E0FF` | 0, 224, 255 | Accents, highlights, CTAs |
| **Graphite Black** | `#111111` | 17, 17, 17 | Text, UI elements |

### Secondary Colors
| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Titanium Gray** | `#C7CCD1` | 199, 204, 209 | Dividers, secondary text |
| **Performance Orange** | `#FF7A00` | 255, 122, 0 | CTAs, alerts, brand tie-in |
| **Cloud White** | `#F8F9FA` | 248, 249, 250 | Light backgrounds, cards |

### Color Usage Rules
- **Hero sections:** Deep Tech Blue background with Electric Cyan accents
- **Text on dark:** White (#FFFFFF) or Cloud White
- **Text on light:** Graphite Black
- **Interactive elements:** Performance Orange for CTAs, Electric Cyan for hover states
- **Dividers:** Titanium Gray at 50% opacity

---

## 3. Typography

### Font Families
| Purpose | Primary | Fallback |
|---------|---------|----------|
| **Headlines** | Inter Tight | Arial Black, sans-serif |
| **Body** | Inter | Roboto, Helvetica, sans-serif |
| **Code/Tech** | JetBrains Mono | Consolas, monospace |

### Type Scale
| Level | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| **H1** | 64px | 800 | 1.1 | Hero headlines |
| **H2** | 48px | 700 | 1.2 | Section headers |
| **H3** | 32px | 600 | 1.3 | Subsection headers |
| **H4** | 24px | 600 | 1.4 | Card titles |
| **Body Large** | 20px | 400 | 1.6 | Intro paragraphs |
| **Body** | 16px | 400 | 1.6 | Standard text |
| **Small** | 14px | 400 | 1.5 | Captions, metadata |
| **Caption** | 12px | 500 | 1.4 | Labels, badges |

### Typography Rules
- **All caps** for labels, buttons, and navigation
- **Sentence case** for body text and descriptions
- **Letter spacing:** +2px for headlines, normal for body
- **Never use:** Comic Sans, Papyrus, or decorative display fonts

---

## 4. Logo System

### Primary Logo
- **Mark:** Stylized AG monogram with circuit-path motif
- **Wordmark:** "AGI Company" in Inter Tight Bold
- **Lockup:** "A division of Performance Supply Depot LLC" in Small type below

### Logo Variants
1. **Full Logo:** Mark + Wordmark + Division line
2. **Compact Logo:** Mark + "AGI" for small spaces
3. **Icon Only:** Mark for favicons, avatars
4. **Wordmark Only:** Text-only for formal documents

### Logo Usage Rules
- **Minimum clear space:** Equal to the height of the "A" in AGI
- **Minimum size:** 32px width for digital
- **Background contrast:** Always ensure Electric Cyan mark is visible
- **Never:** Stretch, rotate, add shadows, or change colors

### Logo Colors
- **Light backgrounds:** Deep Tech Blue mark
- **Dark backgrounds:** Electric Cyan mark
- **Monochrome:** White or Graphite Black only

---

## 5. Layout System

### Grid
- **Base grid:** 12-column
- **Gutter:** 24px
- **Max width:** 1440px
- **Breakpoints:** Mobile (<768px), Tablet (768-1024px), Desktop (>1024px)

### Spacing Scale
| Token | Value | Usage |
|-------|-------|-------|
| `xs` | 4px | Tight padding, icon gaps |
| `sm` | 8px | Button padding, card gaps |
| `md` | 16px | Standard padding |
| `lg` | 24px | Section padding |
| `xl` | 32px | Card padding |
| `2xl` | 48px | Section margins |
| `3xl` | 64px | Hero padding |
| `4xl` | 96px | Major section breaks |

### Container Patterns
- **Card:** White background, 8px border-radius, `shadow-sm`
- **Panel:** Deep Tech Blue background, subtle border
- **Hero:** Full-bleed Deep Tech Blue with gradient overlay
- **Modal:** Centered, max-width 640px, backdrop blur

---

## 6. Component Library

### Buttons
| Variant | Background | Text | Border | Hover |
|---------|------------|------|--------|-------|
| **Primary** | Performance Orange | White | None | Darken 10% |
| **Secondary** | Transparent | Electric Cyan | 2px Electric Cyan | Fill Cyan, dark text |
| **Tertiary** | Transparent | White | 1px Titanium Gray | Border Electric Cyan |
| **Ghost** | Transparent | Titanium Gray | None | Text White |

**Button sizing:**
- **Small:** 32px height, 12px font, 12px horizontal padding
- **Medium:** 44px height, 14px font, 20px horizontal padding
- **Large:** 56px height, 16px font, 32px horizontal padding

### Cards
```
Background: Cloud White
Border-radius: 8px
Padding: 24px
Shadow: 0 1px 3px rgba(0,0,0,0.1)
Hover shadow: 0 4px 12px rgba(0,0,0,0.15)
```

### Form Elements
- **Inputs:** 44px height, 8px border-radius, 1px Titanium Gray border
- **Focus state:** 2px Electric Cyan border
- **Labels:** 12px uppercase, Titanium Gray, letter-spacing 1px
- **Error:** Performance Orange border and text

---

## 7. Imagery Style

### Photography
- **Style:** High contrast, dramatic lighting, tech-focused
- **Color treatment:** Cool tones, slight cyan cast
- **Subjects:** Abstract technology, human hands with devices, clean workspaces
- **Avoid:** Stock photos with obvious poses, cluttered scenes

### Illustrations
- **Style:** Isometric, line-art, minimal color
- **Colors:** Electric Cyan and white on transparent or dark backgrounds
- **Stroke weight:** 2px consistent

### Icons
- **Style:** Outlined, 2px stroke, rounded corners
- **Sizes:** 16px, 24px, 32px, 48px
- **Color:** Match text color or Electric Cyan on dark

---

## 8. Accessibility Standards

### Color Contrast
- **Normal text:** 4.5:1 minimum (WCAG AA)
- **Large text:** 3:1 minimum
- **UI components:** 3:1 minimum for boundaries

### Typography
- **Minimum body size:** 16px
- **Line height:** 1.5 or greater for body text
- **Paragraph width:** Max 75 characters

### Motion
- **Respect `prefers-reduced-motion`**
- No flashing content >3Hz
- Provide pause controls for auto-playing content

---

## 9. Agent Micro-Branding

Each AGI agent has unique accent colors while maintaining brand consistency:

| Agent | Primary Accent | Icon |
|-------|-----------------|------|
| **QORA** | Gold (#FFD700) | Crown |
| **SPINDLE** | Silver (#C0C0C0) | Gear |
| **SCRIBBLE** | Purple (#9B59B6) | Pen |
| **TAPTAP** | Green (#2ECC71) | Cursor |
| **SENTINEL** | Red (#E74C3C) | Shield |
| **LEDGER-9** | Blue (#3498DB) | Chart |
| **PATRICIA** | Teal (#1ABC9C) | Checkmark |

**Usage:** Agent accents for badges, avatars, and section headers only. Maintain Deep Tech Blue as primary.

---

## 10. File Formats

### Logo Files
- **SVG:** Primary format for web
- **PNG:** 24-bit with transparency, min 2x size
- **EPS:** For print materials

### Colors
- **Web:** Hex and RGB
- **Print:** CMYK and Pantone
- **Development:** CSS custom properties

### Typography
- **Web:** WOFF2 and WOFF
- **System:** Inter and Inter Tight from Google Fonts

---

**Document Version:** 1.0  
**Last Updated:** 2026-04-05  
**Next Review:** 2026-07-05
