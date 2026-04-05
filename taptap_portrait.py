from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

# Create 400x400 image with dark background
width, height = 400, 400
img = Image.new('RGB', (width, height), '#0d1117')
draw = ImageDraw.Draw(img)

# Colors - cyan/green theme
cyan = '#00d4ff'
light_cyan = '#7dd3fc'
green = '#22c55e'
light_green = '#86efac'
dark_green = '#14532d'
white = '#ffffff'
gray = '#8b949e'
dark_gray = '#30363d'
accent_pink = '#ff6b9d'

# Background subtle grid pattern
for i in range(0, width, 20):
    draw.line([(i, 0), (i, height)], fill='#161b22', width=1)
for i in range(0, height, 20):
    draw.line([(0, i), (width, i)], fill='#161b22', width=1)

# Draw code diff background elements (subtle)
# Left side - removed lines (red tint)
for i in range(5):
    y = 60 + i * 25
    draw.rectangle([(20, y), (35, y + 15)], fill='#3d1f1f')
    draw.text((45, y), f"- line_{42+i}", fill='#ff7b72', font=None)

# Right side - added lines (green tint)
for i in range(5):
    y = 60 + i * 25
    draw.rectangle([(300, y), (315, y + 15)], fill='#1f3d1f')
    draw.text((325, y), f"+ new_line", fill='#7ee787', font=None)

# Central character - Taptap the Code Reviewer
cx, cy = width // 2, height // 2 + 20

# Draw body/base (stylized robot/reviewer figure)
# Body - rounded rectangle with gradient effect
body_color = '#1f2937'
for i in range(5):
    offset = i * 2
    alpha = 255 - i * 40
    draw.rounded_rectangle(
        [(cx - 70 - offset, cy + 40 - offset), (cx + 70 + offset, cy + 130 + offset)],
        radius=20, fill='#1f2937', outline=cyan if i == 0 else None, width=2
    )

# Main body
body_gradient = ['#1f2937', '#111827', '#0d1117']
for i, color in enumerate(body_gradient):
    inset = i * 3
    draw.rounded_rectangle(
        [(cx - 70 + inset, cy + 40 + inset), (cx + 70 - inset, cy + 130 - inset)],
        radius=18, fill=color
    )

# Neck
draw.rectangle([(cx - 15, cy + 20), (cx + 15, cy + 45)], fill='#374151')

# Head - main circle (slightly larger for presence)
head_size = 65
# Head glow effect
for i in range(8, 0, -1):
    glow_size = head_size + i * 3
    alpha = 30 - i * 3
    draw.ellipse(
        [(cx - glow_size, cy - 60 - glow_size), (cx + glow_size, cy - 60 + glow_size)],
        outline=light_cyan, width=1
    )

# Main head
draw.ellipse(
    [(cx - head_size, cy - 60 - head_size), (cx + head_size, cy - 60 + head_size)],
    fill='#1f2937', outline=cyan, width=3
)

# Face/screen area inside head
face_size = 50
draw.ellipse(
    [(cx - face_size, cy - 60 - face_size), (cx + face_size, cy - 60 + face_size)],
    fill='#0d1117', outline=dark_gray, width=1
)

# Eyes - the iconic 👀 look
# Left eye
left_eye_x, left_eye_y = cx - 25, cy - 65
# Eye glow
for i in range(4, 0, -1):
    glow_r = 12 + i * 2
    draw.ellipse(
        [(left_eye_x - glow_r, left_eye_y - glow_r), 
         (left_eye_x + glow_r, left_eye_y + glow_r)],
        fill=None, outline=light_cyan, width=1
    )
# Eye white
draw.ellipse(
    [(left_eye_x - 10, left_eye_y - 10), (left_eye_x + 10, left_eye_y + 10)],
    fill=white
)
# Eye shine
draw.ellipse(
    [(left_eye_x - 3, left_eye_y - 3), (left_eye_x + 2, left_eye_y + 2)],
    fill='#e0f2fe'
)
# Pupil - looking at code (slightly down/right)
draw.ellipse(
    [(left_eye_x + 2, left_eye_y + 2), (left_eye_x + 7, left_eye_y + 7)],
    fill='#0d1117'
)

# Right eye
right_eye_x, right_eye_y = cx + 25, cy - 65
for i in range(4, 0, -1):
    glow_r = 12 + i * 2
    draw.ellipse(
        [(right_eye_x - glow_r, right_eye_y - glow_r), 
         (right_eye_x + glow_r, right_eye_y + glow_r)],
        fill=None, outline=light_cyan, width=1
    )
draw.ellipse(
    [(right_eye_x - 10, right_eye_y - 10), (right_eye_x + 10, right_eye_y + 10)],
    fill=white
)
draw.ellipse(
    [(right_eye_x - 3, right_eye_y - 3), (right_eye_x + 2, right_eye_y + 2)],
    fill='#e0f2fe'
)
draw.ellipse(
    [(right_eye_x + 2, right_eye_y + 2), (right_eye_x + 7, right_eye_y + 7)],
    fill='#0d1117'
)

# Magnifying glass held by the character
# Handle
handle_start = (cx + 50, cy + 20)
handle_end = (cx + 90, cy + 60)
draw.line([handle_start, handle_end], fill='#9ca3af', width=8)
draw.line([handle_start, handle_end], fill='#d1d5db', width=4)

# Magnifying glass rim
mg_x, mg_y = cx + 35, cy + 5
mg_radius = 35
draw.ellipse(
    [(mg_x - mg_radius, mg_y - mg_radius), (mg_x + mg_radius, mg_y + mg_radius)],
    fill='#1f2937', outline='#9ca3af', width=6
)
draw.ellipse(
    [(mg_x - mg_radius + 3, mg_y - mg_radius + 3), 
     (mg_x + mg_radius - 3, mg_y + mg_radius - 3)],
    fill='#0d1117', outline='#6b7280', width=2
)

# Glass lens effect - showing code being examined
# Mini code lines inside magnifying glass
for i, color in enumerate([green, light_green, cyan, green, light_cyan]):
    y_offset = mg_y - 15 + i * 8
    line_width = 20 - abs(i - 2) * 5
    draw.rectangle(
        [(mg_x - line_width//2, y_offset - 2), (mg_x + line_width//2, y_offset + 2)],
        fill=color
    )

# Magnifying glass highlight
draw.arc(
    [(mg_x - mg_radius + 8, mg_y - mg_radius + 8), 
     (mg_x - 5, mg_y - 5)],
    start=200, end=300, fill=white, width=3
)

# Arms - holding the magnifying glass
# Right arm reaching to hold
draw.line([(cx + 55, cy + 50), (cx + 65, cy + 35)], fill='#374151', width=12)
draw.line([(cx + 65, cy + 35), (cx + 75, cy + 25)], fill='#374151', width=10)

# Left arm resting
draw.line([(cx - 60, cy + 50), (cx - 80, cy + 80)], fill='#374151', width=12)
draw.ellipse([(cx - 85, cy + 75), (cx - 75, cy + 85)], fill='#6b7280')

# Checkmarks floating around (code review approved!)
# Function to draw checkmark
def draw_checkmark(x, y, size, color):
    points = [
        (x - size//2, y),
        (x - size//4, y + size//2),
        (x + size//2, y - size//2)
    ]
    draw.line(points, fill=color, width=4)
    # Glow effect
    draw.line(points, fill=color, width=6)
    draw.line(points, fill=color, width=2)

# Checkmarks in various positions
check_positions = [
    (80, 120, green),
    (320, 150, light_green),
    (100, 280, cyan),
    (330, 300, light_cyan),
    (cx, 50, green),
]

for x, y, color in check_positions:
    draw_checkmark(x, y, 20, color)
    # Glow
    for i in range(1, 4):
        draw.ellipse([(x - 15 - i, y - 15 - i), (x + 15 + i, y + 15 + i)], 
                     outline=color, width=1)

# Diff indicators (+/-) floating
draw.text((60, 180), "+", fill=green, font=None)
draw.text((330, 200), "−", fill='#ff7b72', font=None)
draw.text((85, 320), "+", fill=cyan, font=None)
draw.text((310, 340), "✓", fill=light_green, font=None)

# Code review badge/label at bottom
badge_y = height - 50
draw.rounded_rectangle(
    [(cx - 80, badge_y - 15), (cx + 80, badge_y + 15)],
    radius=10, fill='#1f2937', outline=cyan, width=2
)

# "CODE REVIEW" text simulation with blocks
text_color = cyan
# C
draw.arc([(cx - 70, badge_y - 8), (cx - 55, badge_y + 8)], 
         start=90, end=270, fill=text_color, width=2)
# O
draw.ellipse([(cx - 45, badge_y - 8), (cx - 30, badge_y + 8)], 
             outline=text_color, width=2)
# D
draw.line([(cx - 20, badge_y - 8), (cx - 20, badge_y + 8)], fill=text_color, width=2)
draw.arc([(cx - 20, badge_y - 8), (cx - 5, badge_y + 8)], 
         start=270, end=90, fill=text_color, width=2)
# E
draw.line([(cx + 5, badge_y - 8), (cx + 5, badge_y + 8)], fill=text_color, width=2)
draw.line([(cx + 5, badge_y - 8), (cx + 18, badge_y - 8)], fill=text_color, width=2)
draw.line([(cx + 5, badge_y), (cx + 15, badge_y)], fill=text_color, width=2)
draw.line([(cx + 5, badge_y + 8), (cx + 18, badge_y + 8)], fill=text_color, width=2)

# R
draw.line([(cx + 28, badge_y - 8), (cx + 28, badge_y + 8)], fill=text_color, width=2)
draw.arc([(cx + 28, badge_y - 8), (cx + 43, badge_y)], 
         start=270, end=90, fill=text_color, width=2)
draw.line([(cx + 35, badge_y), (cx + 43, badge_y + 8)], fill=text_color, width=2)
# E
draw.line([(cx + 48, badge_y - 8), (cx + 48, badge_y + 8)], fill=text_color, width=2)
draw.line([(cx + 48, badge_y - 8), (cx + 60, badge_y - 8)], fill=text_color, width=2)
draw.line([(cx + 48, badge_y), (cx + 55, badge_y)], fill=text_color, width=2)
draw.line([(cx + 48, badge_y + 8), (cx + 60, badge_y + 8)], fill=text_color, width=2)
# V
draw.line([(cx + 65, badge_y - 8), (cx + 72, badge_y + 8)], fill=text_color, width=2)
draw.line([(cx + 72, badge_y + 8), (cx + 79, badge_y - 8)], fill=text_color, width=2)
# I
draw.line([(cx + 85, badge_y - 8), (cx + 85, badge_y + 8)], fill=text_color, width=2)
# E
draw.line([(cx + 90, badge_y - 8), (cx + 90, badge_y + 8)], fill=text_color, width=2)
draw.line([(cx + 90, badge_y - 8), (cx + 100, badge_y - 8)], fill=text_color, width=2)
draw.line([(cx + 90, badge_y), (cx + 97, badge_y)], fill=text_color, width=2)
draw.line([(cx + 90, badge_y + 8), (cx + 100, badge_y + 8)], fill=text_color, width=2)
# W
draw.line([(cx + 105, badge_y - 8), (cx + 108, badge_y + 8)], fill=text_color, width=2)
draw.line([(cx + 108, badge_y + 8), (cx + 112, badge_y + 2)], fill=text_color, width=2)
draw.line([(cx + 112, badge_y + 2), (cx + 116, badge_y + 8)], fill=text_color, width=2)
draw.line([(cx + 116, badge_y + 8), (cx + 120, badge_y - 8)], fill=text_color, width=2)

# Add some decorative code symbols in corners
# Corner brackets
corner_color = dark_gray
draw.line([(10, 10), (30, 10)], fill=corner_color, width=2)
draw.line([(10, 10), (10, 30)], fill=corner_color, width=2)

draw.line([(width - 30, 10), (width - 10, 10)], fill=corner_color, width=2)
draw.line([(width - 10, 10), (width - 10, 30)], fill=corner_color, width=2)

draw.line([(10, height - 30), (10, height - 10)], fill=corner_color, width=2)
draw.line([(10, height - 10), (30, height - 10)], fill=corner_color, width=2)

draw.line([(width - 10, height - 30), (width - 10, height - 10)], fill=corner_color, width=2)
draw.line([(width - 30, height - 10), (width - 10, height - 10)], fill=corner_color, width=2)

# Scan line effect (subtle)
for y in range(0, height, 4):
    draw.line([(0, y), (width, y)], fill='#0d1117', width=1)

# Add subtle vignette
for i in range(50):
    alpha = i * 2
    draw.rectangle(
        [(i, i), (width - i, height - i)],
        outline=f'#{max(0, 13-i//4):02x}{max(0, 17-i//4):02x}{max(0, 23-i//4):02x}',
        width=1
    )

# Save the image
output_path = '/root/.openclaw/workspace/aocros/AGI_COMPANY_WEBSITES/performance-supply-depot/agents/portraits/taptap.png'
img.save(output_path, 'PNG')
print(f"Portrait saved to: {output_path}")
