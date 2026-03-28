from PIL import Image, ImageDraw, ImageFont
import math

# Create 400x400 image with transparent background
size = 400
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Colors
ORANGE = (255, 140, 0)  # Vibrant orange accent
ORANGE_LIGHT = (255, 165, 60)
ORANGE_DARK = (200, 100, 0)
DARK_BG = (35, 35, 45)
LIGHT_BG = (50, 50, 65)
WHITE = (255, 255, 255)
GRAY = (180, 180, 200)

# Center point
cx, cy = size // 2, size // 2

# Background - subtle gradient circle
for r in range(200, 0, -1):
    ratio = r / 200
    color = (
        int(DARK_BG[0] + (LIGHT_BG[0] - DARK_BG[0]) * ratio),
        int(DARK_BG[1] + (LIGHT_BG[1] - DARK_BG[1]) * ratio),
        int(DARK_BG[2] + (LIGHT_BG[2] - DARK_BG[2]) * ratio),
        255
    )
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)

# Outer ring with orange accent
ring_width = 8
for r in range(195, 195-ring_width, -1):
    alpha = int(255 * (195-r+1) / ring_width)
    color = (*ORANGE, alpha)
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color, width=2)

# Inner decorative ring
for r in range(185, 183, -1):
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(*ORANGE, 80), width=1)

# Central Project Manager Symbol - Organized Checklist/Chart Design
# Base hexagon shape (suggesting structure/organization)
def draw_hexagon(draw, center, radius, color, outline=None):
    cx, cy = center
    points = []
    for i in range(6):
        angle = math.pi / 3 * i - math.pi / 2
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    draw.polygon(points, fill=color, outline=outline)

# Draw hexagon background for structure
hex_radius = 90
hex_color = (55, 55, 70, 230)
draw_hexagon(draw, (cx, cy), hex_radius, hex_color, (*ORANGE, 150))

# Project Management Elements - Horizontal bars representing tasks/progress
bar_y_positions = [cy - 35, cy - 5, cy + 25]
bar_widths = [120, 90, 100]  # Varying lengths suggest organized tasks
bar_colors = [ORANGE, ORANGE_LIGHT, ORANGE]

for i, (y, bw, color) in enumerate(zip(bar_y_positions, bar_widths, bar_colors)):
    bar_height = 20
    bar_x = cx - 60
    
    # Draw checkmark box on left
    box_size = 16
    box_x = cx - 80
    box_y = y - box_size // 2 + 2
    
    # Box background
    draw.rounded_rectangle([box_x, box_y, box_x + box_size, box_y + box_size], 
                           radius=3, fill=(70, 70, 90), outline=(*ORANGE, 200))
    
    # Checkmark (showing completion - project manager trait)
    if i < 2:  # First two tasks completed
        check_points = [
            (box_x + 3, box_y + 8),
            (box_x + 6, box_y + 11),
            (box_x + 13, box_y + 4)
        ]
        draw.line(check_points, fill=(*ORANGE, 230), width=2)
    
    # Progress bar
    draw.rounded_rectangle([bar_x, y - bar_height//2, bar_x + bw, y + bar_height//2],
                          radius=8, fill=(*color, 200), outline=(*ORANGE_DARK, 100))

# Top accent - small decorative dots representing data points
for i in range(5):
    angle = math.pi * i / 4 - math.pi / 2
    r = 145
    dot_x = cx + r * math.cos(angle)
    dot_y = cy + r * math.sin(angle) - 20
    dot_radius = 4 if i % 2 == 0 else 3
    draw.ellipse([dot_x-dot_radius, dot_y-dot_radius, dot_x+dot_radius, dot_y+dot_radius],
                 fill=(*ORANGE, 150))

# Bottom - subtle "J" initial mark
# Small decorative element
draw.ellipse([cx-8, cy+110-8, cx+8, cy+110+8], fill=(*ORANGE, 100))
draw.ellipse([cx-4, cy+110-4, cx+4, cy+110+4], fill=(*ORANGE, 180))

# Corner decorative elements - suggesting connectivity/network
for corner in [(30, 30), (370, 30), (30, 370), (370, 370)]:
    x, y = corner
    # Small corner accent
    offset = -10 if x < 200 else 10
    draw.line([(x, y), (x + offset, y), (x + offset, y + offset)],
              fill=(*ORANGE, 60), width=2)

# Add subtle glow effect around the main element
glow_radius = 100
for r in range(glow_radius, glow_radius-20, -1):
    alpha = int(30 * (glow_radius - r) / 20)
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(*ORANGE, alpha), width=1)

# Convert to RGB for PNG
img_final = Image.new('RGB', (size, size), (240, 240, 245))
img_final.paste(img, (0, 0), img)

# Save the image
output_path = '/root/.openclaw/workspace/aocros/AGI_COMPANY_WEBSITES/performance-supply-depot/agents/portraits/jordan.png'
img_final.save(output_path, 'PNG', quality=95)
print(f"Avatar saved to: {output_path}")
