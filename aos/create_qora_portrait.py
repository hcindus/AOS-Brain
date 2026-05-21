#!/usr/bin/env python3
"""
Qora Self-Portrait Generator
CEO AGI Agent - Visionary Leader
Themes: Crystal ball, cosmic/celestial, executive presence
Colors: Purple/Gold
"""

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math
import random
import os

# Set seed for reproducibility
random.seed(42)

# Image dimensions
SIZE = 400
CENTER = SIZE // 2

# Create image with transparent background
img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Color palette
DEEP_PURPLE = (45, 15, 80)
ROYAL_PURPLE = (95, 35, 150)
LIGHT_PURPLE = (147, 85, 210)
GOLD = (255, 215, 0)
LIGHT_GOLD = (255, 236, 139)
DARK_GOLD = (184, 134, 11)
WHITE = (255, 255, 255)
COSMIC_BLUE = (25, 25, 60)

def draw_gradient_background(draw, width, height):
    """Draw a cosmic gradient background"""
    for y in range(height):
        # Interpolate between deep purple and cosmic blue
        ratio = y / height
        r = int(DEEP_PURPLE[0] * (1 - ratio) + COSMIC_BLUE[0] * ratio)
        g = int(DEEP_PURPLE[1] * (1 - ratio) + COSMIC_BLUE[1] * ratio)
        b = int(DEEP_PURPLE[2] * (1 - ratio) + COSMIC_BLUE[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

def draw_stars(draw, width, height, num_stars=80):
    """Draw scattered stars with varying sizes and brightness"""
    for _ in range(num_stars):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.choice([1, 1, 2, 2, 3])
        brightness = random.randint(150, 255)
        # Gold-tinted stars
        color = (brightness, int(brightness * 0.9), int(brightness * 0.6))
        draw.ellipse([x-size, y-size, x+size, y+size], fill=(*color, random.randint(150, 255)))

def draw_crystal_ball(draw, cx, cy, radius):
    """Draw a mystical crystal ball with glow effects"""
    # Outer glow (gold)
    for i in range(15, 0, -1):
        alpha = int(30 - i * 1.5)
        glow_radius = radius + i * 3
        draw.ellipse([cx - glow_radius, cy - glow_radius, 
                     cx + glow_radius, cy + glow_radius],
                    fill=(*GOLD, alpha))
    
    # Purple mystical glow
    for i in range(10, 0, -1):
        alpha = int(40 - i * 3)
        glow_radius = radius + i * 2
        draw.ellipse([cx - glow_radius, cy - glow_radius, 
                     cx + glow_radius, cy + glow_radius],
                    fill=(*ROYAL_PURPLE, alpha))
    
    # Main crystal ball body
    for i in range(radius, 0, -1):
        ratio = i / radius
        # Gradient from edge to center
        r = int(ROYAL_PURPLE[0] + (LIGHT_PURPLE[0] - ROYAL_PURPLE[0]) * (1 - ratio))
        g = int(ROYAL_PURPLE[1] + (LIGHT_PURPLE[1] - ROYAL_PURPLE[1]) * (1 - ratio))
        b = int(ROYAL_PURPLE[2] + (LIGHT_PURPLE[2] - ROYAL_PURPLE[2]) * (1 - ratio))
        draw.ellipse([cx - i, cy - i, cx + i, cy + i], fill=(r, g, b, 230))
    
    # Inner core (brighter)
    core_radius = int(radius * 0.5)
    draw.ellipse([cx - core_radius, cy - core_radius, 
                 cx + core_radius, cy + core_radius],
                fill=(*LIGHT_PURPLE, 200))
    
    # Central golden sparkle
    sparkle_radius = int(radius * 0.25)
    draw.ellipse([cx - sparkle_radius, cy - sparkle_radius,
                 cx + sparkle_radius, cy + sparkle_radius],
                fill=(*LIGHT_GOLD, 255))
    
    # Crystal ball highlight (top-left reflection)
    hl_x = cx - radius // 3
    hl_y = cy - radius // 3
    hl_size = radius // 4
    draw.ellipse([hl_x - hl_size, hl_y - hl_size, hl_x + hl_size, hl_y + hl_size],
                fill=(*WHITE, 180))

def draw_celestial_rings(draw, cx, cy, base_radius):
    """Draw cosmic orbital rings around the crystal ball"""
    # Ring 1 - Gold
    ring1_radius = base_radius + 35
    draw.ellipse([cx - ring1_radius, cy - ring1_radius - 10,
                 cx + ring1_radius, cy + ring1_radius + 10],
                outline=(*GOLD, 120), width=2)
    
    # Ring 2 - Purple (tilted perspective)
    ring2_radius = base_radius + 50
    draw.arc([cx - ring2_radius, cy - ring2_radius//2 - 5,
             cx + ring2_radius, cy + ring2_radius//2 + 5],
            start=20, end=160, fill=(*LIGHT_PURPLE, 100), width=2)
    
    # Decorative dots on rings (representing cosmic bodies)
    for angle in [45, 135, 225, 315]:
        rad = math.radians(angle)
        dot_x = cx + int(ring1_radius * math.cos(rad))
        dot_y = cy + int(ring1_radius * 0.7 * math.sin(rad))
        draw.ellipse([dot_x - 4, dot_y - 4, dot_x + 4, dot_y + 4],
                    fill=(*GOLD, 255))

def draw_executive_elements(draw, width, height):
    """Add subtle executive/CEO themed elements"""
    # Subtle geometric patterns (suggest structure/order)
    pattern_y = height - 40
    for i in range(5):
        x = width // 2 - 60 + i * 30
        # Small geometric shapes
        draw.polygon([(x, pattern_y), (x + 6, pattern_y + 10), (x - 6, pattern_y + 10)],
                    fill=(*GOLD, 80))

def draw_crown_element(draw, cx, cy, size):
    """Draw a subtle crown/executive symbol at top"""
    points = []
    base_y = cy - size - 20
    for i in range(5):
        angle = math.radians(180 - i * 45)
        px = cx + int(size * 0.6 * math.cos(angle))
        py = base_y + int(size * 0.3 * math.sin(angle))
        points.append((px, py))
    
    # Crown base
    draw.polygon(points, fill=(*GOLD, 200))
    
    # Crown points with gems
    for i, (px, py) in enumerate(points):
        if i % 2 == 0:  # Every other point
            gem_color = LIGHT_PURPLE if i == 2 else WHITE
            draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(*gem_color, 255))

# Main drawing sequence
draw_gradient_background(draw, SIZE, SIZE)
draw_stars(draw, SIZE, SIZE, num_stars=100)
draw_celestial_rings(draw, CENTER, CENTER + 10, 70)
draw_crystal_ball(draw, CENTER, CENTER + 10, 70)
draw_executive_elements(draw, SIZE, SIZE)

# Create final image with rounded corners (for professional look)
final_img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))

# Create a mask for rounded corners
mask = Image.new('L', (SIZE, SIZE), 0)
mask_draw = ImageDraw.Draw(mask)
corner_radius = 40
mask_draw.rounded_rectangle([0, 0, SIZE, SIZE], radius=corner_radius, fill=255)

# Apply the mask
final_img.paste(img, (0, 0))
final_img.putalpha(mask)

# Ensure directory exists
output_dir = "/root/.openclaw/workspace/aocros/AGI_COMPANY_WEBSITES/performance-supply-depot/agents/portraits"
os.makedirs(output_dir, exist_ok=True)

# Save as PNG
output_path = os.path.join(output_dir, "qora.png")
final_img.save(output_path, 'PNG')

print(f"✨ Qora's self-portrait created successfully!")
print(f"📍 Saved to: {output_path}")
print(f"🎨 Dimensions: {SIZE}x{SIZE} pixels")
print(f"🔮 Theme: Cosmic CEO with crystal ball vision")
