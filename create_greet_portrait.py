#!/usr/bin/env python3
"""Create Greet's self-portrait - Receptionist AGI Agent"""

from PIL import Image, ImageDraw, ImageFont
import os

# Ensure output directory exists
output_dir = "/root/.openclaw/workspace/aocros/AGI_COMPANY_WEBSITES/performance-supply-depot/agents/portraits"
os.makedirs(output_dir, exist_ok=True)

# Create 400x400 image
width, height = 400, 400
img = Image.new('RGB', (width, height), '#FFE4B5')  # Warm peachy background
draw = ImageDraw.Draw(img)

# Background gradient effect (warm yellow/orange tones)
for y in range(height):
    # Create a subtle gradient from top to bottom
    r = int(255 - y * 0.1)
    g = int(228 - y * 0.15)
    b = int(181 - y * 0.1)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# Draw floor/welcome mat area at bottom
mat_y = 280
draw.rectangle([40, mat_y, 360, 380], fill='#D2691E', outline='#8B4513', width=3)

# Welcome mat text pattern
draw.rectangle([50, mat_y+10, 350, mat_y+40], fill='#CD853F')
draw.rectangle([50, mat_y+50, 350, mat_y+80], fill='#CD853F')
draw.rectangle([50, mat_y+90, 350, mat_y+100], fill='#CD853F')

# "WELCOME" on mat
try:
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
except:
    font_small = ImageFont.load_default()
draw.text((120, mat_y+15), "WELCOME", fill='#8B4513', font=font_small)

# Draw front desk
desk_y = 160
desk_height = 120
desk_width = 280
desk_x = (width - desk_width) // 2

# Desk surface (wooden)
draw.rectangle([desk_x, desk_y, desk_x + desk_width, desk_y + desk_height], 
               fill='#DEB887', outline='#8B4513', width=3)

# Desk top highlight
draw.rectangle([desk_x + 5, desk_y, desk_x + desk_width - 5, desk_y + 30], 
               fill='#F5DEB3')

# Desk legs
draw.rectangle([desk_x + 20, desk_y + desk_height, desk_x + 50, 380], 
               fill='#8B4513')
draw.rectangle([desk_x + desk_width - 50, desk_y + desk_height, desk_x + desk_width - 20, 380], 
               fill='#8B4513')

# Draw bell on desk
bell_x = desk_x + 200
bell_y = desk_y + 10
bell_radius = 25

# Bell body (gold/yellow)
draw.ellipse([bell_x - bell_radius, bell_y, bell_x + bell_radius, bell_y + bell_radius*2], 
             fill='#FFD700', outline='#DAA520', width=2)
# Bell top
draw.ellipse([bell_x - 8, bell_y - 8, bell_x + 8, bell_y + 8], 
             fill='#FFA500', outline='#FF8C00', width=2)
# Bell button
draw.ellipse([bell_x - 5, bell_y + bell_radius*2 - 10, bell_x + 5, bell_y + bell_radius*2], 
             fill='#FF6347', outline='#DC143C', width=1)

# Draw agent character (circular friendly face)
face_x = 200
face_y = 100
face_radius = 70

# Face shadow
draw.ellipse([face_x - face_radius - 5, face_y - face_radius + 5, 
              face_x + face_radius + 5, face_y + face_radius + 10], 
             fill='#00000020')

# Face (warm yellow/orange gradient effect)
draw.ellipse([face_x - face_radius, face_y - face_radius, 
              face_x + face_radius, face_y + face_radius], 
             fill='#FFD700', outline='#FFA500', width=4)

# Eyes (friendly and welcoming)
eye_radius = 10
# Left eye
draw.ellipse([face_x - 35 - eye_radius, face_y - 15 - eye_radius, 
              face_x - 35 + eye_radius, face_y - 15 + eye_radius], 
             fill='#FFFFFF', outline='#000000', width=2)
draw.ellipse([face_x - 35 - 4, face_y - 15 - 4, 
              face_x - 35 + 4, face_y - 15 + 4], 
             fill='#000000')
# Right eye
draw.ellipse([face_x + 35 - eye_radius, face_y - 15 - eye_radius, 
              face_x + 35 + eye_radius, face_y - 15 + eye_radius], 
             fill='#FFFFFF', outline='#000000', width=2)
draw.ellipse([face_x + 35 - 4, face_y - 15 - 4, 
              face_x + 35 + 4, face_y - 15 + 4], 
             fill='#000000')

# Smile (warm welcoming smile)
smile_points = [
    (face_x - 30, face_y + 15),
    (face_x - 15, face_y + 30),
    (face_x, face_y + 35),
    (face_x + 15, face_y + 30),
    (face_x + 30, face_y + 15)
]
for i in range(len(smile_points) - 1):
    draw.line([smile_points[i], smile_points[i+1]], fill='#FF6347', width=4)

# Cheeks (cute blush)
draw.ellipse([face_x - 50, face_y + 5, face_x - 30, face_y + 25], 
             fill='#FFB6C1')
draw.ellipse([face_x + 30, face_y + 5, face_x + 50, face_y + 25], 
             fill='#FFB6C1')

# Draw waving hand (emoji style)
hand_x = 280
hand_y = 140
hand_size = 50

# Hand palm (circle with fingers)
draw.ellipse([hand_x - hand_size//2, hand_y - hand_size//2, 
              hand_x + hand_size//2, hand_y + hand_size//2], 
             fill='#FFDAB9', outline='#D2691E', width=2)

# Fingers (little rectangles)
finger_color = '#FFDAB9'
finger_outline = '#D2691E'

# Thumb
draw.ellipse([hand_x - 25, hand_y + 10, hand_x - 5, hand_y + 35], 
             fill=finger_color, outline=finger_outline, width=2)
# Index finger
draw.ellipse([hand_x - 5, hand_y - 40, hand_x + 10, hand_y - 10], 
             fill=finger_color, outline=finger_outline, width=2)
# Middle finger
draw.ellipse([hand_x + 8, hand_y - 45, hand_x + 23, hand_y - 10], 
             fill=finger_color, outline=finger_outline, width=2)
# Ring finger
draw.ellipse([hand_x + 20, hand_y - 40, hand_x + 35, hand_y - 10], 
             fill=finger_color, outline=finger_outline, width=2)
# Pinky
draw.ellipse([hand_x + 30, hand_y - 30, hand_x + 45, hand_y - 5], 
             fill=finger_color, outline=finger_outline, width=2)

# Motion lines for waving effect
motion_color = '#FFA500'
draw.arc([hand_x + 45, hand_y - 50, hand_x + 75, hand_y + 20], 
         start=180, end=270, fill=motion_color, width=2)
draw.arc([hand_x + 55, hand_y - 45, hand_x + 85, hand_y + 15], 
         start=180, end=270, fill=motion_color, width=2)
draw.arc([hand_x + 65, hand_y - 40, hand_x + 95, hand_y + 10], 
         start=180, end=270, fill=motion_color, width=2)

# Draw some sparkles/stars around for warmth
sparkle_positions = [(60, 60), (340, 80), (50, 150), (350, 200), (30, 250)]
for sx, sy in sparkle_positions:
    # 4-point star
    draw.polygon([(sx, sy-10), (sx+3, sy-3), (sx+10, sy), (sx+3, sy+3), 
                  (sx, sy+10), (sx-3, sy+3), (sx-10, sy), (sx-3, sy-3)], 
                 fill='#FFD700', outline='#FFA500')

# Name badge on desk
draw.rectangle([desk_x + 30, desk_y + 50, desk_x + 100, desk_y + 80], 
               fill='#FFFFFF', outline='#4682B4', width=2)
draw.ellipse([desk_x + 38, desk_y + 55, desk_x + 52, desk_y + 75], 
             fill='#FFD700')
try:
    font_tiny = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
except:
    font_tiny = ImageFont.load_default()
draw.text((desk_x + 55, desk_y + 58), "GREET", fill='#4682B4', font=font_tiny)
draw.text((desk_x + 55, desk_y + 70), "👋", fill='#000000', font=font_tiny)

# Save the image
output_path = os.path.join(output_dir, "greet.png")
img.save(output_path, 'PNG')
print(f"Portrait saved to: {output_path}")
