#!/usr/bin/env python3
"""Create Clerk agent self-portrait - Entry Admin AGI agent"""

from PIL import Image, ImageDraw, ImageFont
import math

def create_clerk_portrait():
    # Canvas 400x400
    width, height = 400, 400
    img = Image.new('RGB', (width, height), color='#F0F2F5')  # Light gray background
    draw = ImageDraw.Draw(img)
    
    # Colors
    gray_dark = '#4A5568'
    gray_medium = '#718096'
    gray_light = '#A0AEC0'
    blue_dark = '#2B4A6F'
    blue_medium = '#4A6FA5'
    blue_light = '#7A9BC8'
    accent = '#63B3ED'
    white = '#FFFFFF'
    black = '#1A202C'
    
    # === BACKGROUND: Filing Cabinet ===
    # Cabinet body
    cabinet_left = 30
    cabinet_top = 80
    cabinet_right = 130
    cabinet_bottom = 350
    
    # Cabinet shadow
    draw.rectangle([cabinet_left + 5, cabinet_top + 5, cabinet_right + 5, cabinet_bottom + 5], fill='#CBD5E0')
    
    # Cabinet main body
    draw.rectangle([cabinet_left, cabinet_top, cabinet_right, cabinet_bottom], fill=gray_medium, outline=gray_dark, width=2)
    
    # Drawers
    for i in range(4):
        drawer_y = cabinet_top + 20 + (i * 60)
        # Drawer face
        draw.rectangle([cabinet_left + 8, drawer_y, cabinet_right - 8, drawer_y + 50], fill=gray_light, outline=gray_dark, width=1)
        # Drawer handle
        draw.rounded_rectangle([cabinet_left + 35, drawer_y + 20, cabinet_right - 35, drawer_y + 30], radius=3, fill=gray_dark)
        # Label holder on drawer
        draw.rectangle([cabinet_left + 15, drawer_y + 8, cabinet_right - 15, drawer_y + 18], fill='#E2E8F0', outline=gray_medium)
    
    # === CENTER: Scanner/Document Area ===
    # Scanner bed (center feature)
    scanner_left = 140
    scanner_top = 150
    scanner_right = 260
    scanner_bottom = 320
    
    # Scanner base shadow
    draw.rectangle([scanner_left + 8, scanner_top + 8, scanner_right + 8, scanner_bottom + 8], fill='#CBD5E0')
    
    # Scanner body
    draw.rectangle([scanner_left, scanner_top, scanner_right, scanner_bottom], fill='#2D3748', outline=black, width=3)
    
    # Scanner glass bed
    draw.rectangle([scanner_left + 15, scanner_top + 40, scanner_right - 15, scanner_bottom - 20], fill='#4299E1', outline=accent, width=2)
    
    # Scan light effect
    draw.rectangle([scanner_left + 15, scanner_top + 45, scanner_right - 15, scanner_top + 55], fill='#63B3ED')
    
    # Scanner lid (partially open)
    lid_points = [
        (scanner_left + 10, scanner_top - 30),
        (scanner_right + 20, scanner_top - 10),
        (scanner_right - 5, scanner_top + 20),
        (scanner_left - 5, scanner_top + 10)
    ]
    draw.polygon(lid_points, fill='#4A5568', outline=black)
    
    # === ORGANIZED STACKS (Right side) ===
    # Stack of documents
    stack_colors = [white, '#EDF2F7', '#E2E8F0']
    stack_x = 280
    stack_y = 180
    
    for i in range(5):
        # Slight offset for realistic stack
        offset_x = (i % 2) * 3
        offset_y = i * 25
        doc_color = stack_colors[i % len(stack_colors)]
        
        # Document
        draw.rectangle([stack_x + offset_x, stack_y + offset_y, stack_x + 80, stack_y + 25 + offset_y], 
                       fill=doc_color, outline=gray_medium, width=1)
        
        # Paper lines
        for j in range(3):
            line_y = stack_y + offset_y + 6 + (j * 5)
            draw.rectangle([stack_x + offset_x + 8, line_y, stack_x + 65 + offset_x, line_y + 2], fill=gray_light)
    
    # === BARCODE ELEMENT ===
    # Barcode strip at bottom
    barcode_y = 340
    barcode_left = 150
    barcode_width = 100
    barcode_height = 35
    
    # Barcode background
    draw.rectangle([barcode_left, barcode_y, barcode_left + barcode_width, barcode_y + barcode_height], 
                   fill=white, outline=gray_dark, width=1)
    
    # Generate barcode lines
    bar_x = barcode_left + 5
    while bar_x < barcode_left + barcode_width - 5:
        bar_width = [1, 2, 3][(int(bar_x) % 3)]
        if (int(bar_x) % 7) > 2:
            draw.rectangle([bar_x, barcode_y + 5, bar_x + bar_width, barcode_y + barcode_height - 5], fill=black)
        bar_x += bar_width + 1
    
    # === TOP: Document Header/Clip ===
    # Clipboard at top
    clip_left = 170
    clip_right = 230
    clip_top = 60
    clip_bottom = 100
    
    # Clip body
    draw.rounded_rectangle([clip_left, clip_top, clip_right, clip_bottom], radius=5, fill=gray_dark, outline=black, width=2)
    
    # Clip mechanism
    draw.rounded_rectangle([clip_left + 20, clip_top - 10, clip_right - 20, clip_top + 10], radius=3, fill='#718096', outline=gray_dark, width=1)
    
    # Paper under clip
    draw.rectangle([clip_left + 5, clip_bottom, clip_right - 5, clip_bottom + 40], fill=white, outline=gray_medium, width=1)
    
    # Paper lines
    for i in range(3):
        line_y = clip_bottom + 10 + (i * 10)
        draw.rectangle([clip_left + 12, line_y, clip_right - 12, line_y + 3], fill=gray_light)
    
    # === CLERK AGENT REPRESENTATION ===
    # Main "agent" shape - stylized document/clipboard icon
    center_x, center_y = 200, 200
    
    # Document shape (the agent body)
    doc_left = 155
    doc_top = 110
    doc_right = 245
    doc_bottom = 220
    
    # Document shadow
    draw.rectangle([doc_left + 3, doc_top + 3, doc_right + 3, doc_bottom + 3], fill='#CBD5E0')
    
    # Main document
    draw.rectangle([doc_left, doc_top, doc_right, doc_bottom], fill=white, outline=blue_dark, width=3)
    
    # Document header bar
    draw.rectangle([doc_left, doc_top, doc_right, doc_top + 25], fill=blue_medium, outline=blue_dark, width=1)
    
    # Document content lines
    for i in range(4):
        line_y = doc_top + 35 + (i * 20)
        line_width = 70 if i % 2 == 0 else 50
        draw.rectangle([doc_left + 10, line_y, doc_left + 10 + line_width, line_y + 4], fill=gray_light)
    
    # Checkbox
    for i in range(3):
        cb_y = doc_top + 40 + (i * 20)
        draw.rectangle([doc_right - 25, cb_y, doc_right - 15, cb_y + 10], outline=gray_medium, width=1)
        # Checkmark
        if i < 2:
            draw.line([(doc_right - 23, cb_y + 5), (doc_right - 19, cb_y + 8)], fill=blue_medium, width=2)
            draw.line([(doc_right - 19, cb_y + 8), (doc_right - 16, cb_y + 2)], fill=blue_medium, width=2)
    
    # === AGENT "FACE" / IDENTITY ===
    # Stylized emoji-like representation at top of document
    face_center_x = 200
    face_center_y = 85
    
    # Circular background for emoji feel
    face_radius = 35
    draw.ellipse([face_center_x - face_radius - 2, face_center_y - face_radius - 2, 
                  face_center_x + face_radius + 2, face_center_y + face_radius + 2], 
                 fill=blue_dark, outline=black, width=2)
    
    draw.ellipse([face_center_x - face_radius, face_center_y - face_radius, 
                  face_center_x + face_radius, face_center_y + face_radius], 
                 fill='#63B3ED', outline=blue_dark, width=2)
    
    # 📋 Clipboard icon as "face"
    # Mini clipboard
    cb_left = face_center_x - 15
    cb_top = face_center_y - 20
    cb_right = face_center_x + 15
    cb_bottom = face_center_y + 15
    
    # Clipboard paper
    draw.rectangle([cb_left, cb_top + 5, cb_right, cb_bottom], fill=white, outline=gray_dark, width=1)
    
    # Clipboard clip
    draw.rounded_rectangle([cb_left + 8, cb_top, cb_right - 8, cb_top + 8], radius=2, fill=gray_dark)
    
    # Lines on clipboard
    for i in range(2):
        line_y = cb_top + 12 + (i * 6)
        draw.rectangle([cb_left + 3, line_y, cb_right - 3, line_y + 2], fill=gray_light)
    
    # === DECORATIVE ELEMENTS ===
    # Small barcode accent
    mini_bar_left = 40
    mini_bar_top = 370
    draw.rectangle([mini_bar_left, mini_bar_top, mini_bar_left + 40, mini_bar_top + 20], 
                   fill=white, outline=gray_medium, width=1)
    for i in range(8):
        bar_w = 2 if i % 2 == 0 else 1
        draw.rectangle([mini_bar_left + 3 + (i * 5), mini_bar_top + 3, 
                        mini_bar_left + 3 + (i * 5) + bar_w, mini_bar_top + 17], fill=black)
    
    # Document corner accent
    draw.polygon([(350, 80), (380, 110), (350, 110)], fill='#EDF2F7', outline=gray_medium, width=1)
    draw.rectangle([350, 80, 380, 110], fill='#EDF2F7', outline=gray_medium, width=1)
    draw.line([(355, 90), (375, 90)], fill=gray_light, width=1)
    draw.line([(355, 95), (375, 95)], fill=gray_light, width=1)
    
    # Save the image
    img.save('/root/.openclaw/workspace/aocros/AGI_COMPANY_WEBSITES/performance-supply-depot/agents/portraits/clerk.png', 'PNG')
    print("Clerk portrait saved successfully!")
    
    return img

if __name__ == '__main__':
    create_clerk_portrait()
