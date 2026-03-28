#!/usr/bin/env python3
"""
MilkMan Game - STL Generator
Generate 3D printable models for the MilkMan Game
"""

import numpy as np
import struct
import os

def write_stl(filename, vertices, faces):
    """Write a binary STL file from vertices and faces."""
    # Calculate normals for each face
    def normal(v1, v2, v3):
        u = v2 - v1
        v = v3 - v1
        n = np.cross(u, v)
        length = np.linalg.norm(n)
        if length > 0:
            return n / length
        return np.array([0, 0, 0])
    
    with open(filename, 'wb') as f:
        # 80 byte header
        f.write(b'MilkMan Game STL Model' + b'\x00' * (80 - 22))
        
        # Number of triangles
        f.write(struct.pack('<I', len(faces)))
        
        for face in faces:
            v1, v2, v3 = vertices[face[0]], vertices[face[1]], vertices[face[2]]
            n = normal(v1, v2, v3)
            
            # Normal vector (float32 x 3)
            f.write(struct.pack('<fff', n[0], n[1], n[2]))
            # Vertex 1
            f.write(struct.pack('<fff', v1[0], v1[1], v1[2]))
            # Vertex 2
            f.write(struct.pack('<fff', v2[0], v2[1], v2[2]))
            # Vertex 3
            f.write(struct.pack('<fff', v3[0], v3[1], v3[2]))
            # Attribute byte count (2 bytes, unused)
            f.write(struct.pack('<H', 0))

def create_box(w, h, d, x=0, y=0, z=0):
    """Create a box mesh. Returns (vertices, faces)."""
    hw, hh, hd = w/2, h/2, d/2
    vertices = np.array([
        # Bottom face
        [x-hw, y-hh, z-hd], [x+hw, y-hh, z-hd], [x+hw, y-hh, z+hd], [x-hw, y-hh, z+hd],
        # Top face
        [x-hw, y+hh, z-hd], [x+hw, y+hh, z-hd], [x+hw, y+hh, z+hd], [x-hw, y+hh, z+hd],
    ])
    faces = [
        [0, 2, 1], [0, 3, 2],  # Bottom
        [4, 5, 6], [4, 6, 7],  # Top
        [0, 1, 5], [0, 5, 4],  # Front
        [1, 2, 6], [1, 6, 5],  # Right
        [2, 3, 7], [2, 7, 6],  # Back
        [3, 0, 4], [3, 4, 7],  # Left
    ]
    return vertices, faces

def milk_bottle(filename, golden=False):
    """Create a classic milk bottle."""
    radius = 8
    body_height = 30
    neck_height = 10
    neck_radius = 4
    vertices = []
    faces = []
    
    # Create cylinder-like body with square base
    # Bottom (flat for printing)
    base = [
        [-10, -10, 0], [10, -10, 0], [10, 10, 0], [-10, 10, 0],  # Base
    ]
    for v in base:
        vertices.append(v)
    
    # Body corners
    for z in [0, body_height]:
        for x, y in [(-8, -8), (8, -8), (8, 8), (-8, 8)]:
            vertices.append([x, y, z])
    
    # Neck
    for z in [body_height, body_height + neck_height]:
        for x, y in [(-4, -4), (4, -4), (4, 4), (-4, 4)]:
            vertices.append([x, y, z])
    
    # Cap
    for x, y in [(-5, -5), (5, -5), (5, 5), (-5, 5)]:
        vertices.append([x, y, body_height + neck_height + 3])
    
    vertices = np.array(vertices)
    
    # Create faces
    # Base
    faces.append([0, 1, 2])
    faces.append([0, 2, 3])
    
    # Body sides
    for i in range(4):
        v1 = 4 + i
        v2 = 4 + (i+1) % 4
        v3 = 8 + i
        v4 = 8 + (i+1) % 4
        faces.append([v1, v2, v4])
        faces.append([v1, v4, v3])
    
    # Shoulder transition
    for i in range(4):
        v1 = 8 + i
        v2 = 8 + (i+1) % 4
        v3 = 12 + i
        v4 = 12 + (i+1) % 4
        faces.append([v1, v2, v4])
        faces.append([v1, v4, v3])
    
    # Neck
    for i in range(4):
        v1 = 12 + i
        v2 = 12 + (i+1) % 4
        v3 = 16 + i
        v4 = 16 + (i+1) % 4
        faces.append([v1, v2, v4])
        faces.append([v1, v4, v3])
    
    # Cap
    cap_start = 16
    faces.append([cap_start, cap_start+2, cap_start+1])
    faces.append([cap_start, cap_start+3, cap_start+2])
    
    # Cap sides
    for i in range(4):
        v1 = 16 + i
        v2 = 16 + (i+1) % 4
        v3 = 20 + i
        faces.append([v1, v2, v3])
    
    # Cap top
    faces.append([20, 21, 22])
    faces.append([20, 22, 23])
    
    write_stl(filename, vertices, faces)
    print(f"Created: {filename}")

def sour_milk_enemy(filename):
    """Create a grumpy sour milk carton enemy."""
    vertices = []
    faces = []
    
    # Main carton body (slanted top like a milk carton)
    vertices = [
        # Bottom face
        [-10, -6, 0], [10, -6, 0], [10, 6, 0], [-10, 6, 0],
        # Lower body
        [-10, -6, 20], [10, -6, 20], [10, 6, 20], [-10, 6, 20],
        # Upper body (slanted in)
        [-8, -5, 30], [8, -5, 30], [8, 5, 30], [-8, 5, 30],
    ]
    
    vertices = np.array(vertices)
    
    # Front face with angry "mouth"
    faces = [
        [0, 1, 2], [0, 2, 3],  # Bottom
        [0, 4, 5], [0, 5, 1],  # Front
        [1, 5, 6], [1, 6, 2],  # Right
        [2, 6, 7], [2, 7, 3],  # Back
        [3, 7, 4], [3, 4, 0],  # Left
        [4, 8, 9], [4, 9, 5],  # Front upper
        [5, 9, 10], [5, 10, 6],  # Right upper
        [6, 10, 11], [6, 11, 7],  # Back upper
        [7, 11, 8], [7, 8, 4],  # Left upper
        [8, 11, 10], [8, 10, 9],  # Top
    ]
    
    write_stl(filename, vertices, faces)
    print(f"Created: {filename}")

def spill_monster(filename):
    """Create a puddle-like spill monster."""
    vertices = []
    faces = []
    
    # Create irregular puddle shape using vertices
    vertices = [
        # Base layer (flat bottom)
        [-15, -8, 0], [10, -12, 0], [18, -5, 0], [12, 8, 0], 
        [-5, 12, 0], [-18, 5, 0], [-12, -15, 0],
        # Raised center (body)
        [-8, -4, 5], [6, -7, 4], [10, -3, 5], [7, 5, 4],
        [-3, 7, 5], [-10, 3, 4], [-7, -9, 4],
        # Drips
        [15, -8, 0], [16, -6, 3], [14, -10, 0],  # Drip 1
        [-15, 10, 0], [-17, 8, 4], [-13, 12, 0],  # Drip 2
        [5, 15, 0], [6, 13, 3], [4, 17, 0],  # Drip 3
    ]
    
    vertices = np.array(vertices)
    
    # Base face (triangulated polygon)
    faces = [
        [0, 1, 6], [1, 2, 6], [2, 5, 6], [2, 3, 5], [3, 4, 5],  # Base bottom
        # Sides connecting base to body
        [0, 7, 1], [1, 7, 8], [1, 8, 2], [2, 8, 9], [2, 9, 3],
        [3, 9, 10], [3, 10, 4], [4, 10, 11], [4, 11, 5], [5, 11, 12], [5, 12, 0], [0, 12, 7],
        # Top of body
        [7, 12, 8], [8, 12, 9], [9, 12, 11], [9, 11, 10],
        # Drip 1
        [13, 14, 15], [13, 15, 2], [14, 9, 15],
        # Drip 2  
        [16, 17, 18], [16, 5, 17], [5, 11, 17],
        # Drip 3
        [19, 20, 21], [19, 4, 20], [4, 10, 20],
    ]
    
    write_stl(filename, vertices, faces)
    print(f"Created: {filename}")

def coin_token(filename):
    """Create a simple coin/token."""
    vertices = []
    faces = []
    
    radius = 12
    thickness = 3
    segments = 16
    
    # Create cylinder
    for z in [0, thickness]:
        # Center point
        vertices.append([0, 0, z])
        # Rim points
        for i in range(segments):
            angle = 2 * np.pi * i / segments
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            vertices.append([x, y, z])
    
    vertices = np.array(vertices)
    
    # Faces
    faces = []
    
    # Bottom face
    for i in range(segments):
        faces.append([0, (i+1) % segments + 1, i + 1])
    
    # Top face  
    for i in range(segments):
        faces.append([segments+1, segments+1 + i, segments+1 + (i+1) % segments])
    
    # Side faces
    for i in range(segments):
        v1 = i + 1
        v2 = (i+1) % segments + 1
        v3 = v1 + segments + 1
        v4 = v2 + segments + 1
        faces.append([v1, v3, v2])
        faces.append([v2, v3, v4])
    
    write_stl(filename, vertices, faces)
    print(f"Created: {filename}")

def straw_powerup(filename):
    """Create a drinking straw with spiral design."""
    vertices = []
    faces = []
    
    radius = 4
    height = 40
    segments = 8
    spiral_turns = 3
    
    # Create spiral straw
    for i in range(segments + 1):
        t = i / segments
        z = height * t
        # Spiral offset
        angle = 2 * np.pi * spiral_turns * t
        cx = 3 * np.cos(angle)
        cy = 3 * np.sin(angle)
        
        # Ring of vertices at this height
        for j in range(8):
            ring_angle = 2 * np.pi * j / 8
            x = cx + radius * np.cos(ring_angle)
            y = cy + radius * np.sin(ring_angle)
            vertices.append([x, y, z])
    
    vertices = np.array(vertices)
    
    # Create faces
    faces = []
    for i in range(segments):
        for j in range(8):
            v1 = i * 8 + j
            v2 = i * 8 + (j+1) % 8
            v3 = (i+1) * 8 + j
            v4 = (i+1) * 8 + (j+1) % 8
            faces.append([v1, v2, v4])
            faces.append([v1, v4, v3])
    
    write_stl(filename, vertices, faces)
    print(f"Created: {filename}")

def cream_bonus(filename):
    """Create a whipped cream dollop."""
    vertices = []
    faces = []
    
    # Dollop shape - stacked cylinders getting smaller
    layers = [
        (10, 5),   # Base
        (8, 5),    # 
        (6, 5),    #
        (4, 4),    #
        (2, 3),    # Peak
    ]
    
    z = 0
    for radius, height in layers:
        # Create ring of vertices
        for i in range(8):
            angle = 2 * np.pi * i / 8
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            vertices.append([x, y, z])
            vertices.append([x * 0.7, y * 0.7, z + height])
        z += height * 0.8
    
    vertices = np.array(vertices)
    
    # Create faces
    faces = []
    base_idx = 0
    for layer in range(len(layers)):
        # This is simplified - just create some connecting faces
        for i in range(8):
            v1 = layer * 16 + i * 2
            v2 = layer * 16 + ((i+1) % 8) * 2
            v3 = v1 + 1
            faces.append([v1, v2, v3])
    
    write_stl(filename, vertices, faces)
    print(f"Created: {filename}")

def milk_carton_crate(filename):
    """Create a crate made of milk cartons (breakable block)."""
    vertices = []
    faces = []
    
    # Outer crate shell
    w, h, d = 30, 30, 30
    hw, hh, hd = w/2, h/2, d/2
    
    vertices = [
        # Bottom
        [-hw, -hd, 0], [hw, -hd, 0], [hw, hd, 0], [-hw, hd, 0],
        # Lower
        [-hw, -hd, 5], [hw, -hd, 5], [hw, hd, 5], [-hw, hd, 5],
        # Upper (with open grid pattern)
        [-hw+3, -hd+3, hh], [hw-3, -hd+3, hh], [hw-3, hd-3, hh], [-hw+3, hd-3, hh],
    ]
    
    vertices = np.array(vertices)
    
    faces = [
        [0, 2, 1], [0, 3, 2],  # Bottom
        [0, 1, 5], [0, 5, 4],  # Front outer
        [1, 2, 6], [1, 6, 5],  # Right outer
        [2, 3, 7], [2, 7, 6],  # Back outer
        [3, 0, 4], [3, 4, 7],  # Left outer
        [4, 5, 9], [4, 9, 8],  # Front inner
        [5, 6, 10], [5, 10, 9],  # Right inner
        [6, 7, 11], [6, 11, 10],  # Back inner
        [7, 4, 8], [7, 8, 11],  # Left inner
        [8, 9, 10], [8, 10, 11],  # Top inner
    ]
    
    write_stl(filename, vertices, faces)
    print(f"Created: {filename}")

def main():
    output_dir = "/root/.openclaw/workspace/MilkMan-Game/hardware"
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 50)
    print("MilkMan Game - STL Generator")
    print("=" * 50)
    
    # Collectibles
    milk_bottle(f"{output_dir}/milk_bottle.stl", golden=False)
    milk_bottle(f"{output_dir}/golden_milk.stl", golden=True)
    coin_token(f"{output_dir}/coin.stl")
    
    # Enemies
    sour_milk_enemy(f"{output_dir}/sour_milk_enemy.stl")
    spill_monster(f"{output_dir}/spill_monster.stl")
    
    # Powerups
    straw_powerup(f"{output_dir}/straw_powerup.stl")
    cream_bonus(f"{output_dir}/cream_bonus.stl")
    
    # Environment
    milk_carton_crate(f"{output_dir}/milk_carton_crate.stl")
    
    print("=" * 50)
    print("All STL files generated successfully!")
    print(f"Output directory: {output_dir}")

if __name__ == "__main__":
    main()
