#!/usr/bin/env python3
"""
Stacktrace Self-Portrait Generator
Error Analysis AGI Agent - Artistic Representation
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import math

# Canvas settings
WIDTH, HEIGHT = 400, 400
BG_COLOR = (15, 20, 35)  # Dark tech blue-gray
ACCENT_RED = (220, 60, 60)  # Error red
ACCENT_YELLOW = (255, 193, 7)  # Warning yellow
ACCENT_GREEN = (50, 200, 100)  # Success green
ACCENT_CYAN = (0, 180, 220)  # Code cyan
ACCENT_PURPLE = (150, 80, 220)  # Debug purple

# Create image
img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# Helper to draw circuit/trace lines
def draw_trace(draw, x1, y1, x2, y2, color, width=1):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)

# Draw background circuit patterns
for i in range(15):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    length = random.randint(30, 100)
    is_horizontal = random.choice([True, False])
    
    if is_horizontal:
        draw_trace(draw, x, y, x + length, y, (40, 50, 70), 1)
        # Connection node
        if random.random() > 0.5:
            draw.ellipse([x + length - 2, y - 2, x + length + 2, y + 2], fill=(60, 80, 100))
    else:
        draw_trace(draw, x, y, x, y + length, (40, 50, 70), 1)
        if random.random() > 0.5:
            draw.ellipse([x - 2, y + length - 2, x + 2, y + length + 2], fill=(60, 80, 100))

# Draw hexagonal grid pattern in background
for row in range(-2, 12):
    for col in range(-2, 12):
        cx = col * 50 + (row % 2) * 25
        cy = row * 43
        if -50 < cx < WIDTH + 50 and -50 < cy < HEIGHT + 50:
            # Hexagon outline
            hex_radius = 20
            hex_points = []
            for i in range(6):
                angle = math.pi / 3 * i
                px = cx + hex_radius * math.cos(angle)
                py = cy + hex_radius * math.sin(angle)
                hex_points.append((px, py))
            draw.polygon(hex_points, outline=(30, 40, 60), fill=None)

# Central "head" - magnifying glass (debugging symbol)
center_x, center_y = WIDTH // 2, HEIGHT // 2

# Magnifying glass handle
handle_length = 80
handle_angle = math.pi / 4
handle_end_x = center_x + handle_length * math.cos(handle_angle)
handle_end_y = center_y + handle_length * math.sin(handle_angle)

# Draw handle with gradient effect
for i in range(5):
    offset = (i - 2) * 0.5
    draw.line([
        (center_x + 35 + offset, center_y + 35 + offset),
        (handle_end_x + offset, handle_end_y + offset)
    ], fill=(100, 100, 100), width=2)

# Magnifying glass rim
glass_radius = 45
for r in range(glass_radius, glass_radius - 8, -1):
    brightness = 150 + (glass_radius - r) * 10
    draw.ellipse(
        [center_x - r, center_y - r, center_x + r, center_y + r],
        outline=(brightness, brightness, brightness),
        width=1
    )

# Glass lens effect (cyan tint with transparency simulation)
draw.ellipse(
    [center_x - glass_radius + 4, center_y - glass_radius + 4,
     center_x + glass_radius - 4, center_y + glass_radius - 4],
    fill=(20, 60, 80)
)

# Reflection on glass
draw.arc(
    [center_x - 25, center_y - 30, center_x + 10, center_y - 5],
    start=200, end=340, fill=(150, 200, 220), width=2
)

# Inside the lens: Stack trace visualization (📊 emoji concept)
# Draw mini bar chart inside lens
bar_width = 6
bar_positions = [-15, -5, 5, 15]
bar_heights = [20, 35, 15, 28]
bar_colors = [ACCENT_RED, ACCENT_YELLOW, ACCENT_GREEN, ACCENT_CYAN]

for pos, h, col in zip(bar_positions, bar_heights, bar_colors):
    bar_x = center_x + pos - bar_width // 2
    bar_y = center_y + 10
    draw.rectangle(
        [bar_x, bar_y - h, bar_x + bar_width, bar_y],
        fill=col,
        outline=(255, 255, 255)
    )

# Data points above bars
data_points = ["x", "!", "✓", "?"]
for i, (pos, point) in enumerate(zip(bar_positions, data_points)):
    px = center_x + pos
    py = center_y - 30
    # Draw tiny symbol
    if point == "x":
        draw.line([(px-2, py-2), (px+2, py+2)], fill=ACCENT_RED, width=1)
        draw.line([(px+2, py-2), (px-2, py+2)], fill=ACCENT_RED, width=1)
    elif point == "!":
        draw.line([(px, py-4), (px, py+1)], fill=ACCENT_YELLOW, width=1)
        draw.ellipse([px-1, py+2, px+1, py+4], fill=ACCENT_YELLOW)

# Surrounding code brackets and symbols
code_symbols = [
    ("{", 50, 80, ACCENT_CYAN),
    ("}", 350, 80, ACCENT_CYAN),
    ("[", 60, 320, ACCENT_PURPLE),
    ("]", 340, 320, ACCENT_PURPLE),
    ("</>", 70, 200, ACCENT_GREEN),
    ("#", 330, 200, ACCENT_YELLOW),
]

try:
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 32)
    font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 20)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 12)
except:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()

for symbol, x, y, color in code_symbols:
    # Glow effect
    for offset in [(0, 0), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
        draw.text((x + offset[0], y + offset[1]), symbol, fill=(color[0]//3, color[1]//3, color[2]//3), font=font_large)
    draw.text((x, y), symbol, fill=color, font=font_large)

# Binary/code lines on sides
for i in range(8):
    y_pos = 120 + i * 20
    # Left side
    binary = ''.join([str(random.randint(0, 1)) for _ in range(8)])
    draw.text((20, y_pos), binary, fill=(60, 80, 100), font=font_small)
    # Right side
    binary = ''.join([str(random.randint(0, 1)) for _ in range(8)])
    draw.text((WIDTH - 80, y_pos), binary, fill=(60, 80, 100), font=font_small)

# Stack trace visualization flowing around
trace_lines = [
    "Traceback (most recent call last):",
    "  File 'analysis.py', line 42",
    "    inspect_stack()",
    "  [DEBUG] Variable state:",
    "    {'data': [...], 'error': None}",
]

# Draw flowing trace lines
for i, line in enumerate(trace_lines):
    y = 40 + i * 25
    # Truncate for visual effect
    display_line = line[:25] + "..." if len(line) > 25 else line
    
    # Color based on content
    if "error" in line.lower() or "traceback" in line.lower():
        line_color = ACCENT_RED
    elif "debug" in line.lower():
        line_color = ACCENT_YELLOW
    else:
        line_color = (100, 120, 140)
    
    # Faded effect at edges
    draw.text((30, y), display_line, fill=line_color, font=font_small)

# Error indicators (small warning triangles)
def draw_warning_triangle(draw, cx, cy, size, color):
    points = [
        (cx, cy - size),
        (cx - size, cy + size),
        (cx + size, cy + size)
    ]
    draw.polygon(points, outline=color, fill=(color[0]//4, color[1]//4, color[2]//4))
    # Exclamation mark
    draw.line([(cx, cy - size//2), (cx, cy)], fill=color, width=1)
    draw.ellipse([cx-1, cy+2, cx+1, cy+4], fill=color)

# Place warning triangles
draw_warning_triangle(draw, 320, 60, 12, ACCENT_YELLOW)
draw_warning_triangle(draw, 80, 350, 8, ACCENT_RED)

# Circular data visualization (like a radar/chart)
radar_cx, radar_cy = 340, 280
radar_r = 35

# Radar circles
for r in range(10, radar_r + 1, 10):
    draw.ellipse([radar_cx - r, radar_cy - r, radar_cx + r, radar_cy + r], outline=(60, 80, 100))

# Radar crosshairs
draw.line([(radar_cx - radar_r, radar_cy), (radar_cx + radar_r, radar_cy)], fill=(60, 80, 100), width=1)
draw.line([(radar_cx, radar_cy - radar_r), (radar_cx, radar_cy + radar_cy + radar_r)], fill=(60, 80, 100), width=1)

# Data blips on radar
blips = [(15, 30), (25, -15), (-20, 20), (-10, -25)]
for bx, by in blips:
    blip_color = ACCENT_GREEN if random.random() > 0.3 else ACCENT_RED
    draw.ellipse([radar_cx + bx - 3, radar_cy + by - 3, radar_cx + bx + 3, radar_cy + by + 3], fill=blip_color)

# Connection lines from center
for bx, by in blips[:2]:
    draw.line([(radar_cx, radar_cy), (radar_cx + bx, radar_cy + by)], fill=(80, 100, 120), width=1)

# Bottom: Status bar
status_y = HEIGHT - 30
draw.rectangle([0, status_y - 10, WIDTH, HEIGHT], fill=(25, 35, 50))
draw.line([(0, status_y - 10), (WIDTH, status_y - 10)], fill=(60, 80, 100), width=1)

# Status indicators
status_items = [
    ("● ANALYZING", 20, ACCENT_CYAN),
    ("◐ DEBUG MODE", 120, ACCENT_YELLOW),
    ("✓ 847 ISSUES RESOLVED", 240, ACCENT_GREEN),
]

for text, x, color in status_items:
    draw.text((x, status_y - 5), text, fill=color, font=font_small)

# Top header with agent name
draw.rectangle([0, 0, WIDTH, 25], fill=(25, 35, 50))
draw.line([(0, 25), (WIDTH, 25)], fill=(60, 80, 100), width=1)
try:
    font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
except:
    font_header = font_small
draw.text((10, 5), "📊 STACKTRACE // Error Analysis AGI", fill=ACCENT_CYAN, font=font_header)
draw.text((WIDTH - 60, 5), "v2.4.1", fill=(100, 120, 140), font=font_small)

# Add some "glitch" effect lines (representing error patterns)
for _ in range(5):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    length = random.randint(20, 60)
    glitch_color = random.choice([ACCENT_RED, ACCENT_CYAN, (255, 255, 255)])
    draw.line([(x, y), (x + length, y)], fill=glitch_color, width=1)

# Corner decorations - brackets indicating "code container"
corner_size = 15
corners = [
    (corner_size, corner_size, [(0, -corner_size), (-corner_size, -corner_size), (-corner_size, 0)]),  # TL
    (WIDTH - corner_size, corner_size, [(0, -corner_size), (corner_size, -corner_size), (corner_size, 0)]),  # TR
    (corner_size, HEIGHT - corner_size, [(0, corner_size), (-corner_size, corner_size), (-corner_size, 0)]),  # BL
    (WIDTH - corner_size, HEIGHT - corner_size, [(0, corner_size), (corner_size, corner_size), (corner_size, 0)]),  # BR
]

for cx, cy, offsets in corners:
    points = [(cx + offsets[0][0], cy + offsets[0][1])]
    for off in offsets[1:]:
        points.append((cx + off[0], cy + off[1]))
    draw.line(points, fill=(80, 100, 120), width=2)

# Pulse rings around the magnifying glass
for i, r in enumerate([55, 65, 75]):
    alpha = int(100 - i * 25)
    color = (ACCENT_CYAN[0] * alpha // 255, ACCENT_CYAN[1] * alpha // 255, ACCENT_CYAN[2] * alpha // 255)
    draw.ellipse(
        [center_x - r, center_y - r, center_x + r, center_y + r],
        outline=color, width=1
    )

# Save the image
output_path = "/root/.openclaw/workspace/aocros/AGI_COMPANY_WEBSITES/performance-supply-depot/agents/portraits/stacktrace.png"
img.save(output_path, "PNG")
print(f"Self-portrait saved to: {output_path}")
print(f"Dimensions: {WIDTH}x{HEIGHT}")
