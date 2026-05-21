#!/usr/bin/env python3
"""
Dusty - Research AGI Agent Self-Portrait
Specializes in lead enrichment and data mining
Emoji: 🔍
"""

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math
import random

# Set seed for consistent generation
random.seed(42)

# Canvas setup
WIDTH, HEIGHT = 400, 400
img = Image.new('RGB', (WIDTH, HEIGHT), '#1a1a2e')
draw = ImageDraw.Draw(img)

# Background gradient effect - deep analytical blue to purple
for y in range(HEIGHT):
    ratio = y / HEIGHT
    r = int(26 + ratio * 40)
    g = int(26 + ratio * 30)
    b = int(46 + ratio * 40)
    draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

# Add subtle grid pattern (data/analysis theme)
for i in range(0, WIDTH, 20):
    draw.line([(i, 0), (i, HEIGHT)], fill=(40, 40, 60))
for i in range(0, HEIGHT, 20):
    draw.line([(0, i), (WIDTH, i)], fill=(40, 40, 60))

# Draw magnifying glass (🔍) as the central element
cx, cy = WIDTH // 2, HEIGHT // 2
lens_radius = 70

# Glass lens - circular with gradient effect
for r in range(lens_radius, 0, -1):
    ratio = r / lens_radius
    blue_val = int(100 + (1 - ratio) * 100)
    draw.ellipse([cx - r, cy - r - 10, cx + r, cy + r - 10], 
                 fill=(int(50 + ratio * 100), int(100 + ratio * 100), blue_val + 50))

# Lens highlight (glass reflection)
draw.ellipse([cx - 40, cy - 50, cx - 10, cy - 20], fill=(200, 220, 255))

# Lens rim
draw.ellipse([cx - lens_radius - 5, cy - lens_radius - 15, 
              cx + lens_radius + 5, cy + lens_radius - 5], 
             outline='#4a90d9', width=6)

# Handle of magnifying glass
handle_length = 80
handle_angle = math.radians(45)
hx1 = cx + int(lens_radius * math.cos(handle_angle))
hy1 = cy - 10 + int(lens_radius * math.sin(handle_angle))
hx2 = hx1 + int(handle_length * math.cos(handle_angle))
hy2 = hy1 + int(handle_length * math.sin(handle_angle))

# Handle with thickness
for offset in range(-6, 7):
    draw.line([(hx1 + offset * math.sin(handle_angle), hy1 - offset * math.cos(handle_angle)),
               (hx2 + offset * math.sin(handle_angle), hy2 - offset * math.cos(handle_angle))], 
              fill='#2d5a8a', width=1)

# Handle outline
draw.line([(hx1, hy1), (hx2, hy2)], fill='#5a9fd4', width=12)
draw.line([(hx1, hy1), (hx2, hy2)], fill='#8ac4f0', width=8)

# Handle grip
draw.ellipse([hx2 - 12, hy2 - 12, hx2 + 12, hy2 + 12], fill='#1a3a5c')

# Data visualization elements around the lens
# Floating data points (representing lead enrichment)
data_colors = ['#00d4aa', '#ff6b6b', '#4ecdc4', '#ffe66d', '#95e1d3']
for i in range(15):
    angle = (i / 15) * 2 * math.pi
    dist = lens_radius + 35 + random.randint(0, 30)
    dx = cx + int(dist * math.cos(angle))
    dy = cy - 10 + int(dist * math.sin(angle))
    size = random.randint(3, 8)
    color = data_colors[i % len(data_colors)]
    draw.ellipse([dx - size, dy - size, dx + size, dy + size], fill=color)
    # Connection lines to center (network visualization)
    if i % 3 == 0:
        draw.line([(dx, dy), (cx + int(lens_radius * 0.7 * math.cos(angle)), 
                               cy - 10 + int(lens_radius * 0.7 * math.sin(angle)))], 
                  fill=color, width=1)

# Bar chart inside lens (data analysis visualization)
bar_width = 8
bar_start_x = cx - 30
bars = [25, 40, 30, 55, 45, 35, 50]
for i, height in enumerate(bars):
    bx = bar_start_x + i * (bar_width + 4)
    by_top = cy + 20 - height
    by_bottom = cy + 20
    draw.rectangle([bx, by_top, bx + bar_width, by_bottom], fill='#00d4aa')

# Add "DATA" text inside lens
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
except:
    font = ImageFont.load_default()
draw.text((cx - 22, cy - 35), "DATA", fill='#ffffff', font=font)

# Pie chart segment inside lens
pie_start = 200
pie_end = 300
draw.pieslice([cx - 25, cy - 15, cx + 25, cy + 35], pie_start, pie_end, fill='#ff6b6b')

# Line graph overlay
points = [(cx - 25, cy + 25), (cx - 10, cy + 10), (cx + 5, cy + 20), (cx + 20, cy + 5), (cx + 35, cy + 15)]
for i in range(len(points) - 1):
    draw.line([points[i], points[i+1]], fill='#ffe66d', width=2)

# Add binary code/decorative text around edges
try:
    small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 10)
except:
    small_font = ImageFont.load_default()

binary_text = "01001000 01001001 01010010 01000101 00100000 01001101 01000101"
draw.text((10, 10), binary_text, fill=(60, 60, 80), font=small_font)
draw.text((10, HEIGHT - 20), binary_text[::-1], fill=(60, 60, 80), font=small_font)

# Add agent name "DUSTY" at bottom
try:
    name_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
except:
    name_font = ImageFont.load_default()

# Draw name with glow effect
for offset in range(3, 0, -1):
    draw.text((WIDTH // 2 - 35 - offset, HEIGHT - 50 - offset), "DUSTY", fill='#2d5a8a', font=name_font)
draw.text((WIDTH // 2 - 35, HEIGHT - 50), "DUSTY", fill='#5a9fd4', font=name_font)

# Add emoji using unicode since we can't load emoji fonts reliably
draw.text((WIDTH - 45, 10), "o", fill='#ffcc00', font=font)  # placeholder for search

# Add subtle vignette effect
vignette = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
vignette_draw = ImageDraw.Draw(vignette)
for i in range(50):
    alpha = int(i * 1.5)
    vignette_draw.rectangle([i, i, WIDTH - i, HEIGHT - i], outline=(0, 0, 0, alpha))

# Composite vignette
img = img.convert('RGBA')
img = Image.alpha_composite(img, vignette)

# Final blur for polish
img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

# Convert back to RGB and save
img_rgb = img.convert('RGB')
img_rgb.save('/root/.openclaw/workspace/aocros/AGI_COMPANY_WEBSITES/performance-supply-depot/agents/portraits/dusty.png')

print("Dusty self-portrait created successfully!")
