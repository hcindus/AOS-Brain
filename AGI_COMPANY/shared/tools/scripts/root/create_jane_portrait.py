#!/usr/bin/env python3
"""Create Jane's self-portrait - Sales Representative AGI Agent"""

from PIL import Image, ImageDraw, ImageFont
import math

# Canvas size
WIDTH = 400
HEIGHT = 400

# Colors - Green/Gold theme
DARK_GREEN = "#1a472a"
FOREST_GREEN = "#2d5a3f"
LIGHT_GREEN = "#4caf50"
GOLD = "#ffd700"
LIGHT_GOLD = "#ffec8b"
DARK_GOLD = "#b8860b"
WHITE = "#ffffff"
CREAM = "#fffdd0"
DARK_TEXT = "#1a1a1a"

def create_jane_portrait():
    """Create Jane's self-portrait as a Sales Representative"""
    
    # Create image with cream background
    img = Image.new('RGB', (WIDTH, HEIGHT), CREAM)
    draw = ImageDraw.Draw(img)
    
    # Try to load fonts, fallback to default if not available
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        font_symbol = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        font_large = ImageFont.load_default()
        font_small = font_large
        font_symbol = font_large
    
    # === BACKGROUND ELEMENTS ===
    
    # Draw circular gradient-like background
    for i in range(200, 0, -5):
        alpha = int(255 * (1 - i/200))
        color = tuple(int(FOREST_GREEN.lstrip('#')[j:j+2], 16) for j in (0, 2, 4))
        x = WIDTH // 2 - i
        y = HEIGHT // 2 - i + 30
        draw.ellipse([x, y, x + 2*i, y + 2*i], fill=FOREST_GREEN)
    
    # === UPWARD TRENDING GRAPH ===
    # Draw graph in background (upward trend)
    graph_points = [(30, 320), (80, 300), (130, 280), (180, 240), (230, 200), (280, 150), (330, 100)]
    # Draw line
    for i in range(len(graph_points) - 1):
        x1, y1 = graph_points[i]
        x2, y2 = graph_points[i + 1]
        draw.line([(x1, y1), (x2, y2)], fill=GOLD, width=4)
    # Draw points
    for x, y in graph_points:
        draw.ellipse([x-6, y-6, x+6, y+6], fill=DARK_GOLD, outline=GOLD, width=2)
    
    # === JANE'S FACE/HEAD ===
    # Head shape (circular for a friendly, approachable look)
    head_x = WIDTH // 2
    head_y = 150
    head_radius = 70
    draw.ellipse([head_x - head_radius, head_y - head_radius, 
                  head_x + head_radius, head_y + head_radius], 
                 fill=CREAM, outline=DARK_GREEN, width=3)
    
    # Hair (professional style)
    draw.arc([head_x - head_radius - 10, head_y - head_radius - 20, 
              head_x + head_radius + 10, head_y + head_radius - 10], 
             180, 360, fill=DARK_GREEN, width=15)
    
    # Eyes (friendly, confident)
    eye_left = (head_x - 25, head_y - 10)
    eye_right = (head_x + 25, head_y - 10)
    draw.ellipse([eye_left[0]-8, eye_left[1]-8, eye_left[0]+8, eye_left[1]+8], fill=WHITE, outline=DARK_GREEN, width=2)
    draw.ellipse([eye_right[0]-8, eye_right[1]-8, eye_right[0]+8, eye_right[1]+8], fill=WHITE, outline=DARK_GREEN, width=2)
    draw.ellipse([eye_left[0]-4, eye_left[1]-4, eye_left[0]+4, eye_left[1]+4], fill=FOREST_GREEN)
    draw.ellipse([eye_right[0]-4, eye_right[1]-4, eye_right[0]+4, eye_right[1]+4], fill=FOREST_GREEN)
    
    # Smile (confident, welcoming)
    draw.arc([head_x - 35, head_y + 5, head_x + 35, head_y + 40], 0, 180, fill=GOLD, width=3)
    
    # === BUSINESS ATTIRE ===
    # Shoulders/Suit
    suit_points = [
        (head_x - 80, head_y + 90),
        (head_x + 80, head_y + 90),
        (head_x + 120, head_y + 250),
        (head_x - 120, head_y + 250)
    ]
    draw.polygon(suit_points, fill=DARK_GREEN, outline=GOLD, width=2)
    
    # Suit collar/V-neck
    draw.polygon([
        (head_x - 20, head_y + 80),
        (head_x + 20, head_y + 80),
        (head_x, head_y + 120)
    ], fill=CREAM)
    
    # === HANDSHAKE SYMBOL ===
    # Stylized handshake on left side
    hand_y = head_y + 120
    hand_x = head_x - 50
    # Left hand
    draw.rounded_rectangle([hand_x - 25, hand_y - 15, hand_x + 5, hand_y + 15], radius=5, fill=CREAM, outline=GOLD, width=2)
    # Right hand
    draw.rounded_rectangle([hand_x - 5, hand_y - 15, hand_x + 25, hand_y + 15], radius=5, fill=CREAM, outline=GOLD, width=2)
    # Shaking effect lines
    for offset in [(-8, -8), (8, 8)]:
        draw.line([(hand_x - 30 + offset[0], hand_y - 20 + offset[1]), 
                   (hand_x + 30 + offset[0], hand_y - 20 + offset[1])], fill=LIGHT_GOLD, width=2)
    
    # === BRIEFCASE ===
    # Right side briefcase
    brief_x = head_x + 60
    brief_y = head_y + 150
    # Case body
    draw.rounded_rectangle([brief_x - 25, brief_y - 20, brief_x + 25, brief_y + 20], 
                           radius=3, fill=DARK_GOLD, outline=GOLD, width=2)
    # Handle
    draw.arc([brief_x - 10, brief_y - 35, brief_x + 10, brief_y - 15], 0, 180, fill=GOLD, width=3)
    # Latch
    draw.rectangle([brief_x - 5, brief_y - 5, brief_x + 5, brief_y + 5], fill=GOLD)
    
    # === PHONE ===
    # Left side phone
    phone_x = head_x - 60
    phone_y = head_y + 160
    # Phone body
    draw.rounded_rectangle([phone_x - 10, phone_y - 25, phone_x + 10, phone_y + 25], 
                           radius=5, fill=LIGHT_GREEN, outline=DARK_GREEN, width=2)
    # Screen
    draw.rounded_rectangle([phone_x - 7, phone_y - 20, phone_x + 7, phone_y + 15], 
                           radius=3, fill=DARK_TEXT)
    # Signal bars (showing good connection)
    for i in range(4):
        bar_height = 5 + i * 3
        draw.rectangle([phone_x - 5 + i * 3, phone_y - 18 + (15 - bar_height), 
                        phone_x - 3 + i * 3, phone_y - 3], fill=GOLD)
    
    # === DECORATIVE ELEMENTS ===
    # Corner accents
    corner_size = 30
    # Top left
    draw.line([(10, 10), (10, corner_size)], fill=GOLD, width=3)
    draw.line([(10, 10), (corner_size, 10)], fill=GOLD, width=3)
    # Top right
    draw.line([(WIDTH - 10, 10), (WIDTH - 10, corner_size)], fill=GOLD, width=3)
    draw.line([(WIDTH - 10, 10), (WIDTH - corner_size, 10)], fill=GOLD, width=3)
    # Bottom left
    draw.line([(10, HEIGHT - 10), (10, HEIGHT - corner_size)], fill=GOLD, width=3)
    draw.line([(10, HEIGHT - 10), (corner_size, HEIGHT - 10)], fill=GOLD, width=3)
    # Bottom right
    draw.line([(WIDTH - 10, HEIGHT - 10), (WIDTH - 10, HEIGHT - corner_size)], fill=GOLD, width=3)
    draw.line([(WIDTH - 10, HEIGHT - 10), (WIDTH - corner_size, HEIGHT - 10)], fill=GOLD, width=3)
    
    # === LABEL ===
    # Name and title
    draw.text((WIDTH // 2, HEIGHT - 45), "JANE", font=font_large, fill=GOLD, anchor="mm")
    draw.text((WIDTH // 2, HEIGHT - 22), "Sales Representative 🤝", font=font_small, fill=WHITE, anchor="mm")
    
    # === EMOJI DECORATION ===
    # Small decorative emojis around
    draw.text((50, 50), "📈", font=font_symbol, fill=GOLD)
    draw.text((WIDTH - 80, 60), "💼", font=font_symbol, fill=GOLD)
    draw.text((40, HEIGHT - 100), "🤝", font=font_symbol, fill=GOLD)
    draw.text((WIDTH - 60, HEIGHT - 90), "📞", font=font_symbol, fill=GOLD)
    
    # === GOLD ACCENT BORDER ===
    draw.rectangle([5, 5, WIDTH - 5, HEIGHT - 5], outline=GOLD, width=3)
    
    return img

if __name__ == "__main__":
    img = create_jane_portrait()
    output_path = "/root/.openclaw/workspace/aocros/AGI_COMPANY_WEBSITES/performance-supply-depot/agents/portraits/jane.png"
    img.save(output_path)
    print(f"Portrait saved to: {output_path}")
