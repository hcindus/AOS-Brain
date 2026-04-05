# Background Art Tools Research

**Task:** Research 8-bit pixel art tools for Milk Man Game backgrounds  
**Completed:** 2026-03-16  
**Status:** ✅ COMPLETE

---

## Executive Summary

For the Milk Man Game's three levels (Dairyopolis Streets, Vil Laine's Lair, Shoezete's Fortress), we need professional 8-bit pixel art background creation tools. This research evaluates four primary options and recommends the best workflow.

## Tools Evaluated

### 1. Aseprite ⭐ RECOMMENDED

**Type:** Desktop application (Windows, macOS, Linux)  
**Price:** $19.99 (Steam) / Free (compile from source)  
**Website:** https://www.aseprite.org/

#### Pros
- Industry standard for pixel art
- Purpose-built for game asset creation
- Excellent animation tools (for parallax backgrounds)
- Layer support with blend modes
- Palette management and color cycling
- Tilemap mode for seamless backgrounds
- Export to PNG, GIF, sprite sheets
- Active development & community

#### Cons
- Paid (though worth it)
- Learning curve for advanced features
- No built-in 3D or vector tools

#### Best For
- Professional-quality game backgrounds
- Animated/parallax scrolling scenes
- Tile-based level design

#### Milk Man Game Suitability: **EXCELLENT**

---

### 2. GraphicsGale

**Type:** Desktop application (Windows)  
**Price:** FREE (legacy) / $25 (Pro version)  
**Website:** https://graphicsgale.com/

#### Pros
- Completely free (legacy version)
- Animation preview in real-time
- Good for sprite animation
- Lightweight and fast
- Onion skinning for animation

#### Cons
- Windows only
- Dated interface (Windows 95 era)
- No longer actively developed
- Limited layer functionality vs Aseprite
- No tilemap features

#### Best For
- Budget-conscious projects
- Windows-only workflows
- Simple sprite/background work

#### Milk Man Game Suitability: **GOOD** (if budget is tight)

---

### 3. Pixilart (Web)

**Type:** Browser-based  
**Price:** FREE (with premium options)  
**Website:** https://www.pixilart.com/

#### Pros
- No installation required
- Works on any device with browser
- Built-in community and asset sharing
- Simple interface for beginners
- Good for quick sketches
- Collaborative features

#### Cons
- Requires internet connection
- Limited advanced features
- Performance issues with large files
- Export limitations on free tier
- Not professional-grade

#### Best For
- Quick prototypes
- Beginners learning pixel art
- Collaborative brainstorming
- Situations where software can't be installed

#### Milk Man Game Suitability: **FAIR** (for prototyping only)

---

### 4. GIMP + Plugins

**Type:** Desktop application (Windows, macOS, Linux)  
**Price:** FREE (open source)  
**Website:** https://www.gimp.org/

#### Pros
- Completely free and open source
- Powerful image editing capabilities
- Extensive plugin ecosystem
- Can be configured for pixel art
- Layer support
- Scriptable (Python-Fu, Script-Fu)

#### Cons
- Not designed for pixel art (workarounds needed)
- Steep learning curve
- No animation tools (without plugins)
- Overkill for simple pixel art
- No tilemap features

#### Best For
- Users already familiar with GIMP
- Projects needing heavy post-processing
- Budget of exactly $0

#### Milk Man Game Suitability: **GOOD** (with configuration)

---

## Recommended Workflow

### Primary Recommendation: **Aseprite**

For the Milk Man Game backgrounds, Aseprite is the clear winner:

1. **Industry Standard** - Most professional pixel artists use it
2. **Tilemap Support** - Essential for seamless scrolling backgrounds
3. **Animation Tools** - For parallax effects, animated elements
4. **Export Options** - PNG sequences, sprite sheets for DroidScript
5. **Reasonable Price** - $20 one-time purchase

### Alternative: **GraphicsGale (Free)**

If budget is absolutely zero:
- Use GraphicsGale for static backgrounds
- Export to PNG
- Accept limitations in animation/tile features

---

## Background Specifications for Milk Man Game

### Level 1: Dairyopolis Streets

**Theme:** Urban dairy-themed cityscape  
**Colors:** Bright, cheerful (blues, whites, yellows)  
**Elements:**
- Milk bottle buildings
- Cheese-cart street vendors
- Citizens walking
- Daytime sky

**Technical Specs:**
- Resolution: 320x180 (16:9, 8-bit style)
- Parallax layers: 3 (sky, buildings, street)
- Tileable: Yes (horizontal scrolling)
- Palette: Limited (16-32 colors)

### Level 2: Vil Laine's Lair

**Theme:** Industrial factory district  
**Colors:** Dark, smoggy (purples, blacks, grays)  
**Elements:**
- Smokestacks with smog
- Industrial machinery
- Conveyor belts
- Dark lighting

**Technical Specs:**
- Resolution: 320x180
- Parallax layers: 2 (background machinery, foreground platforms)
- Tileable: Yes
- Palette: Dark (16-24 colors)
- Effects: Animated smoke, flickering lights

### Level 3: Shoezete's Fortress

**Theme:** Campy villain lair, fashion/milk couture  
**Colors:** Dramatic (reds, golds, blacks)  
**Elements:**
- Giant shoe sculptures
- Milk fountain
- Fashion runway platforms
- Dramatic lighting

**Technical Specs:**
- Resolution: 320x180
- Parallax layers: 3 (background fortress, midground platforms, foreground details)
- Tileable: Partial (boss arena section)
- Palette: Rich (24-32 colors)
- Effects: Crown glow, milk flowing

---

## Asset Pipeline

### Recommended File Structure
```
assets/backgrounds/
├── level1_dairyopolis/
│   ├── sky.png
│   ├── buildings.png
│   ├── street.png
│   └── tileset.png
├── level2_vil_lair/
│   ├── background.png
│   ├── machinery.png
│   ├── platforms.png
│   └── smoke_animation/
│       ├── frame_01.png
│       ├── frame_02.png
│       └── ...
└── level3_shoe_fortress/
    ├── fortress_back.png
    ├── platforms.png
    ├── foreground.png
    └── crown_glow.png
```

### DroidScript Implementation
```javascript
// Load parallax layers
var bg1 = app.CreateImage("backgrounds/level1/sky.png");
var bg2 = app.CreateImage("backgrounds/level1/buildings.png");
var bg3 = app.CreateImage("backgrounds/level1/street.png");

// Scroll at different speeds for parallax
function UpdateBackground() {
    bg1.Scroll(speed * 0.2);  // Slowest (far)
    bg2.Scroll(speed * 0.5);  // Medium
    bg3.Scroll(speed * 1.0);  // Fastest (near)
}
```

---

## Tool Comparison Matrix

| Feature | Aseprite | GraphicsGale | Pixilart | GIMP |
|---------|----------|--------------|----------|------|
| Price | $19.99 | Free | Free | Free |
| Pixel Art Focus | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| Animation | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| Tilemap Support | ⭐⭐⭐ | ⭐ | ⭐ | ⭐ |
| Layer Support | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Export Options | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Learning Curve | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐ |
| Community | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Overall** | **⭐⭐⭐** | **⭐⭐** | **⭐⭐** | **⭐⭐** |

---

## Final Recommendation

**Use Aseprite** for Milk Man Game backgrounds.

### Justification:
1. **Professional Results** - Industry-standard tool ensures quality
2. **Tilemap Feature** - Critical for seamless scrolling backgrounds
3. **Animation Support** - Needed for smoke, glow effects, parallax
4. **Reasonable Cost** - $20 is negligible for game development
5. **Time Efficiency** - Purpose-built features save development time

### Budget Alternative:
If $20 is not available, use **GraphicsGale (free)** with acceptance of:
- No tilemap features (manual alignment)
- Limited animation tools
- Windows-only development

---

## Next Steps

1. **Purchase/Install Aseprite** ($19.99 on Steam)
2. **Create color palettes** for each level
3. **Sketch background concepts** (can use Pixilart for quick drafts)
4. **Produce final assets** in Aseprite
5. **Export PNGs** and integrate into DroidScript
6. **Test parallax scrolling** on target Android device

---

*Research completed: 2026-03-16*  
*Recommended tool: Aseprite ($19.99)*
