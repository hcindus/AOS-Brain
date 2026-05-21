#!/usr/bin/env python3
"""Create Executive agent self-portrait - C-Suite Executive Assistant"""

from PIL import Image, ImageDraw

# Canvas size
SIZE = 400
CENTER = SIZE // 2

# Colors
CHARCOAL = "#36454F"  # Dark charcoal for suit
WHITE = "#FFFFFF"     # White for shirt/background accents
LIGHT_GRAY = "#E8E8E8"  # Light gray for background
SILVER = "#C0C0C0"    # Silver for briefcase accents
DARK_GRAY = "#2C3E50" # Darker charcoal
TIE_COLOR = "#1A1A2E" # Dark navy for tie
SKIN_TONE = "#F5D5C5" # Light skin tone

# Create image
img = Image.new('RGB', (SIZE, SIZE), LIGHT_GRAY)
draw = ImageDraw.Draw(img)

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    """Draw a rounded rectangle"""
    x1, y1, x2, y2 = xy
    # Draw main rectangle
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    # Draw four corners
    draw.ellipse([x1, y1, x1 + radius * 2, y1 + radius * 2], fill=fill)
    draw.ellipse([x2 - radius * 2, y1, x2, y1 + radius * 2], fill=fill)
    draw.ellipse([x1, y2 - radius * 2, x1 + radius * 2, y2], fill=fill)
    draw.ellipse([x2 - radius * 2, y2 - radius * 2, x2, y2], fill=fill)

# === BACKGROUND EXECUTIVE OFFICE ===
# Window/frame in background
draw.rectangle([20, 20, 120, 150], fill="#D4E5F7", outline=CHARCOAL, width=2)
draw.line([(70, 20), (70, 150)], fill=CHARCOAL, width=2)
draw.line([(20, 85), (120, 85)], fill=CHARCOAL, width=2)

# Cityscape silhouette through window
for i, h in enumerate([30, 45, 25, 55, 35]):
    x = 25 + i * 18
    draw.rectangle([x, 150 - h, x + 12, 150], fill=CHARCOAL)

# === EXECUTIVE CHAIR (behind figure) ===
# Chair back - high executive chair
chair_x1, chair_y1 = 130, 80
chair_x2, chair_y2 = 270, 280
draw.rounded_rectangle([chair_x1, chair_y1, chair_x2, chair_y2], 
                        radius=20, fill=DARK_GRAY, outline=CHARCOAL, width=3)
# Chair cushion detail
draw.rounded_rectangle([chair_x1 + 15, chair_y1 + 15, chair_x2 - 15, chair_y2 - 50],
                        radius=15, fill=CHARCOAL)

# === THE EXECUTIVE FIGURE ===
# Shoulders/Suit body
draw.ellipse([110, 200, 290, 380], fill=CHARCOAL)
draw.ellipse([120, 220, 280, 380], fill=CHARCOAL)

# White shirt collar area
draw.polygon([(CENTER - 25, 200), (CENTER, 240), (CENTER + 25, 200)], fill=WHITE)
draw.polygon([(CENTER - 25, 200), (CENTER - 10, 240), (CENTER, 240)], fill=WHITE)
draw.polygon([(CENTER + 25, 200), (CENTER + 10, 240), (CENTER, 240)], fill=WHITE)

# Tie
draw.polygon([(CENTER - 8, 205), (CENTER + 8, 205), 
              (CENTER + 12, 320), (CENTER, 340), (CENTER - 12, 320)], fill=TIE_COLOR)
# Tie knot
draw.ellipse([CENTER - 10, 200, CENTER + 10, 220], fill=TIE_COLOR)

# Neck
draw.rectangle([CENTER - 20, 180, CENTER + 20, 210], fill=SKIN_TONE)

# Head
draw.ellipse([CENTER - 45, 100, CENTER + 45, 190], fill=SKIN_TONE)

# Hair (executive style - neat, professional)
draw.arc([CENTER - 48, 95, CENTER + 48, 160], start=0, end=180, fill=CHARCOAL, width=15)
draw.pieslice([CENTER - 48, 95, CENTER + 48, 160], start=0, end=180, fill=CHARCOAL)
# Side hair
draw.rectangle([CENTER - 48, 120, CENTER - 40, 160], fill=CHARCOAL)
draw.rectangle([CENTER + 40, 120, CENTER + 48, 160], fill=CHARCOAL)

# Eyes (professional, attentive)
draw.ellipse([CENTER - 22, 135, CENTER - 12, 145], fill=WHITE)
draw.ellipse([CENTER + 12, 135, CENTER + 22, 145], fill=WHITE)
draw.ellipse([CENTER - 19, 137, CENTER - 15, 143], fill=CHARCOAL)  # Left pupil
draw.ellipse([CENTER + 15, 137, CENTER + 19, 143], fill=CHARCOAL)   # Right pupil

# Professional glasses
draw.arc([CENTER - 28, 128, CENTER - 6, 150], start=0, end=180, fill=CHARCOAL, width=2)
draw.arc([CENTER + 6, 128, CENTER + 28, 150], start=0, end=180, fill=CHARCOAL, width=2)
draw.line([(CENTER - 6, 138), (CENTER + 6, 138)], fill=CHARCOAL, width=2)

# Professional smile
draw.arc([CENTER - 18, 155, CENTER + 18, 175], start=200, end=340, fill=CHARCOAL, width=2)

# === BRIEFCASE (to the side) ===
# Briefcase body
br_x1, br_y1 = 280, 280
br_x2, br_y2 = 360, 360
draw.rectangle([br_x1, br_y1, br_x2, br_y2], fill=CHARCOAL, outline=DARK_GRAY, width=2)
# Handle
draw.arc([br_x1 + 20, br_y1 - 15, br_x1 + 40, br_y1 + 5], start=0, end=180, fill=DARK_GRAY, width=3)
# Latches (silver)
draw.rectangle([br_x1 + 15, br_y1 + 5, br_x1 + 25, br_y1 + 15], fill=SILVER)
draw.rectangle([br_x1 + 55, br_y1 + 5, br_x1 + 65, br_y1 + 15], fill=SILVER)
# Corner protectors
draw.rectangle([br_x1, br_y1, br_x1 + 10, br_y1 + 10], fill=DARK_GRAY)
draw.rectangle([br_x2 - 10, br_y1, br_x2, br_y1 + 10], fill=DARK_GRAY)
draw.rectangle([br_x1, br_y2 - 10, br_x1 + 10, br_y2], fill=DARK_GRAY)
draw.rectangle([br_x2 - 10, br_y2 - 10, br_x2, br_y2], fill=DARK_GRAY)

# === CALENDAR (on the desk/wall area) ===
# Calendar frame
cal_x, cal_y = 60, 220
draw.rectangle([cal_x, cal_y, cal_x + 70, cal_y + 80], fill=WHITE, outline=CHARCOAL, width=2)
# Calendar header (red/salmon typical calendar)
draw.rectangle([cal_x, cal_y, cal_x + 70, cal_y + 20], fill="#E74C3C")
# Calendar rings
draw.ellipse([cal_x + 10, cal_y - 5, cal_x + 20, cal_y + 5], fill=SILVER)
draw.ellipse([cal_x + 50, cal_y - 5, cal_x + 60, cal_y + 5], fill=SILVER)
# Calendar date number
draw.text((cal_x + 25, cal_y + 35), "15", fill=CHARCOAL)
# Calendar grid lines
draw.line([(cal_x, cal_y + 20), (cal_x + 70, cal_y + 20)], fill=CHARCOAL, width=1)

# === EXECUTIVE DETAILS ===
# Watch on wrist (left side)
draw.ellipse([115, 260, 135, 280], fill=SILVER, outline=DARK_GRAY, width=2)
draw.ellipse([120, 265, 130, 275], fill=WHITE)

# === EMOJI BADGE (👔) ===
# Small tie emoji representation as badge
emoji_x, emoji_y = 320, 100
# Tie shape
draw.ellipse([emoji_x, emoji_y, emoji_x + 20, emoji_y + 20], fill=TIE_COLOR)  # Knot
draw.polygon([(emoji_x, emoji_y + 15), (emoji_x + 20, emoji_y + 15),
              (emoji_x + 25, emoji_y + 50), (emoji_x + 10, emoji_y + 60), (emoji_x - 5, emoji_y + 50)], 
             fill=TIE_COLOR)

# === DESK/WORKSPACE ELEMENTS ===
# Subtle desk line at bottom
draw.rectangle([0, 360, SIZE, SIZE], fill="#B8B8B8")
# Mouse pad
draw.rounded_rectangle([150, 370, 250, 395], radius=5, fill="#4A4A4A")
# Coffee cup
draw.ellipse([30, 340, 60, 360], fill=WHITE, outline=CHARCOAL, width=1)
draw.rectangle([30, 330, 60, 350], fill=WHITE, outline=CHARCOAL, width=1)
# Steam from coffee
for i in range(3):
    x = 38 + i * 6
    draw.arc([x, 310 + i*5, x + 8, 325 + i*5], start=180, end=0, fill="#CCCCCC", width=2)

# Save the portrait
img.save('/root/.openclaw/workspace/aocros/AGI_COMPANY_WEBSITES/performance-supply-depot/agents/portraits/executive.png')
print("Executive portrait saved successfully!")
