#!/usr/bin/env python3
"""
Pipeline - CI/CD AGI Agent Self-Portrait
🔄 Flow master with pipeline diagrams, arrows, conveyor belts
Teal and white color scheme
"""

from PIL import Image, ImageDraw, ImageFont
import math

# Create 400x400 image
size = 400
img = Image.new('RGB', (size, size), '#0a1628')  # Dark blue-black background
draw = ImageDraw.Draw(img)

# Colors
TEAL = '#00d4aa'
TEAL_LIGHT = '#4de4c8'
TEAL_DARK = '#008f75'
WHITE = '#ffffff'
WHITE_SOFT = '#e0f2ef'
ARROW_COLOR = '#00d4aa'

# Helper function to draw a rounded rectangle
def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    x1, y1, x2, y2 = xy
    # Draw main rectangle
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

# Background pattern - subtle pipeline nodes
for i in range(5):
    y = 50 + i * 75
    # Horizontal flow lines
    draw.line([(20, y), (380, y)], fill=TEAL_DARK, width=1)

# Main pipeline stages (left to right flow)
stage_width = 80
stage_height = 60
stage_y = 200
stage_gap = 20
stages = [
    ('BUILD', '#008f75'),
    ('TEST', '#00b894'),
    ('DEPLOY', '#00d4aa'),
]

start_x = 40
for i, (label, color) in enumerate(stages):
    x = start_x + i * (stage_width + stage_gap)
    
    # Stage box with gradient effect
    draw.rounded_rectangle(
        [(x, stage_y - stage_height//2), (x + stage_width, stage_y + stage_height//2)],
        radius=8,
        fill=color,
        outline=WHITE,
        width=2
    )
    
    # Stage label
    bbox = draw.textbbox((0, 0), label)
    text_width = bbox[2] - bbox[0]
    text_x = x + (stage_width - text_width) // 2
    text_y = stage_y - 7
    draw.text((text_x, text_y), label, fill=WHITE)
    
    # Arrow to next stage
    if i < len(stages) - 1:
        arrow_x = x + stage_width + 2
        arrow_y = stage_y
        # Arrow body
        draw.line([(arrow_x, arrow_y), (arrow_x + stage_gap - 4, arrow_y)], fill=ARROW_COLOR, width=3)
        # Arrow head
        draw.polygon(
            [(arrow_x + stage_gap - 4, arrow_y - 5), 
             (arrow_x + stage_gap - 4, arrow_y + 5), 
             (arrow_x + stage_gap + 4, arrow_y)],
            fill=ARROW_COLOR
        )

# Conveyor belt at bottom
belt_y = 320
draw.rectangle([(20, belt_y), (380, belt_y + 40)], fill='#1a2d3d', outline=TEAL, width=2)

# Conveyor belt rollers
for i in range(8):
    x = 35 + i * 45
    draw.ellipse([(x, belt_y + 5), (x + 30, belt_y + 35)], fill=TEAL_DARK, outline=WHITE, width=1)

# Flowing packages on conveyor
package_positions = [60, 150, 240, 330]
for px in package_positions:
    # Package box
    draw.rectangle([(px, belt_y - 25), (px + 30, belt_y + 5)], fill=TEAL, outline=WHITE, width=2)
    # Package label lines
    draw.line([(px + 5, belt_y - 18), (px + 25, belt_y - 18)], fill=WHITE_SOFT, width=1)
    draw.line([(px + 5, belt_y - 12), (px + 20, belt_y - 12)], fill=WHITE_SOFT, width=1)

# Circular flow arrows around the edges (representing continuous integration)
for angle in range(0, 360, 45):
    rad = math.radians(angle)
    cx = 200 + 140 * math.cos(rad)
    cy = 200 + 140 * math.sin(rad)
    
    # Small directional arrows
    arrow_size = 8
    end_x = cx + arrow_size * math.cos(rad + math.pi/2)
    end_y = cy + arrow_size * math.sin(rad + math.pi/2)
    
    draw.line([(cx, cy), (end_x, end_y)], fill=TEAL_LIGHT, width=2)

# Central emoji indicator
emoji = "🔄"
try:
    # Try to use a larger font for emoji
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
except:
    font = ImageFont.load_default()

bbox = draw.textbbox((0, 0), emoji, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
draw.text((200 - text_width//2, 80), emoji, font=font, fill=WHITE)

# Title text
try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
except:
    title_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

# Pipeline name
name = "Pipeline"
bbox = draw.textbbox((0, 0), name, font=title_font)
text_width = bbox[2] - bbox[0]
draw.text((200 - text_width//2, 25), name, font=title_font, fill=TEAL)

# CI/CD subtitle
sub = "CI/CD Agent"
bbox = draw.textbbox((0, 0), sub, font=small_font)
text_width = bbox[2] - bbox[0]
draw.text((200 - text_width//2, 375), sub, font=small_font, fill=TEAL_LIGHT)

# Flow lines connecting elements - curved flow
from PIL import ImagePath

# Top flowing arrows (indicating flow direction)
for i in range(3):
    y_base = 110 + i * 15
    # Dashed flow lines
    for dash in range(0, 360, 30):
        x1 = 50 + dash
        x2 = min(x1 + 15, 350)
        if x2 > x1:
            draw.line([(x1, y_base), (x2, y_base)], fill=TEAL_DARK, width=2)

# Status indicators (green dots showing active stages)
status_y = 160
for i in range(3):
    x = 80 + i * 100
    # Glowing status dot
    draw.ellipse([(x - 6, status_y - 6), (x + 6, status_y + 6)], fill='#00ffaa', outline=WHITE, width=2)

# Save the image
output_path = "/root/.openclaw/workspace/aocros/AGI_COMPANY_WEBSITES/performance-supply-depot/agents/portraits/pipeline.png"
img.save(output_path, 'PNG')
print(f"Saved Pipeline portrait to {output_path}")
