"""
AOS-H1 STL Generator
Creates 3D printable STL files for humanoid robot components
"""

import numpy as np
from stl import mesh
import os

class STLGenerator:
    """Generate STL files for AOS-H1 components"""
    
    def __init__(self, output_dir="stls"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def create_cube(self, size, center=(0,0,0), name="cube"):
        """Create a cube STL"""
        x, y, z = size
        cx, cy, cz = center
        
        # Vertices
        vertices = np.array([
            [cx-x/2, cy-y/2, cz-z/2],  # 0
            [cx+x/2, cy-y/2, cz-z/2],  # 1
            [cx+x/2, cy+y/2, cz-z/2],  # 2
            [cx-x/2, cy+y/2, cz-z/2],  # 3
            [cx-x/2, cy-y/2, cz+z/2],  # 4
            [cx+x/2, cy-y/2, cz+z/2],  # 5
            [cx+x/2, cy+y/2, cz+z/2],  # 6
            [cx-x/2, cy+y/2, cz+z/2],  # 7
        ])
        
        # Faces (triangles)
        faces = np.array([
            [0, 3, 1], [1, 3, 2],  # Bottom
            [4, 5, 7], [7, 5, 6],  # Top
            [0, 1, 4], [4, 1, 5],  # Front
            [2, 3, 6], [6, 3, 7],  # Back
            [0, 4, 3], [3, 4, 7],  # Left
            [1, 2, 5], [5, 2, 6],  # Right
        ])
        
        return self._create_mesh(vertices, faces, name)
        
    def create_cylinder(self, radius, height, segments=32, center=(0,0,0), name="cylinder"):
        """Create a cylinder STL"""
        cx, cy, cz = center
        
        vertices = []
        # Top and bottom centers
        vertices.append([cx, cy, cz + height/2])  # 0: top center
        vertices.append([cx, cy, cz - height/2])  # 1: bottom center
        
        # Rim vertices
        for i in range(segments):
            angle = 2 * np.pi * i / segments
            x = cx + radius * np.cos(angle)
            y = cy + radius * np.sin(angle)
            vertices.append([x, y, cz + height/2])  # Top rim
            vertices.append([x, y, cz - height/2])  # Bottom rim
            
        vertices = np.array(vertices)
        
        # Create faces
        faces = []
        # Top cap
        for i in range(segments):
            i1 = 2 + i * 2
            i2 = 2 + ((i + 1) % segments) * 2
            faces.append([0, i2, i1])
            
        # Bottom cap
        for i in range(segments):
            i1 = 3 + i * 2
            i2 = 3 + ((i + 1) % segments) * 2
            faces.append([1, i1, i2])
            
        # Sides
        for i in range(segments):
            top1 = 2 + i * 2
            top2 = 2 + ((i + 1) % segments) * 2
            bot1 = 3 + i * 2
            bot2 = 3 + ((i + 1) % segments) * 2
            
            faces.append([top1, bot1, top2])
            faces.append([top2, bot1, bot2])
            
        faces = np.array(faces)
        
        return self._create_mesh(vertices, faces, name)
        
    def create_sphere(self, radius, segments=16, center=(0,0,0), name="sphere"):
        """Create a sphere STL"""
        cx, cy, cz = center
        
        vertices = []
        vertices.append([cx, cy, cz + radius])  # North pole
        
        # Latitude rings
        for i in range(1, segments):
            phi = np.pi * i / segments
            for j in range(segments):
                theta = 2 * np.pi * j / segments
                x = cx + radius * np.sin(phi) * np.cos(theta)
                y = cy + radius * np.sin(phi) * np.sin(theta)
                z = cz + radius * np.cos(phi)
                vertices.append([x, y, z])
                
        vertices.append([cx, cy, cz - radius])  # South pole
        vertices = np.array(vertices)
        
        # Create faces
        faces = []
        # Top cap
        for i in range(segments):
            i1 = 1 + i
            i2 = 1 + ((i + 1) % segments)
            faces.append([0, i2, i1])
            
        # Middle bands
        for i in range(segments - 2):
            for j in range(segments):
                v1 = 1 + i * segments + j
                v2 = 1 + i * segments + ((j + 1) % segments)
                v3 = 1 + (i + 1) * segments + j
                v4 = 1 + (i + 1) * segments + ((j + 1) % segments)
                
                faces.append([v1, v2, v3])
                faces.append([v2, v4, v3])
                
        # Bottom cap
        last = len(vertices) - 1
        start = 1 + (segments - 1) * segments
        for i in range(segments):
            i1 = start + i
            i2 = start + ((i + 1) % segments)
            faces.append([last, i1, i2])
            
        faces = np.array(faces)
        
        return self._create_mesh(vertices, faces, name)
        
    def create_tube(self, outer_r, inner_r, height, segments=32, name="tube"):
        """Create a hollow tube"""
        vertices = []
        
        # Generate vertices for outer and inner surfaces
        for z in [height/2, -height/2]:
            for r in [outer_r, inner_r]:
                for i in range(segments):
                    angle = 2 * np.pi * i / segments
                    x = r * np.cos(angle)
                    y = r * np.sin(angle)
                    vertices.append([x, y, z])
                    
        vertices = np.array(vertices)
        
        # Create faces (simplified - just outer surface for now)
        faces = []
        for i in range(segments):
            i1 = i
            i2 = (i + 1) % segments
            i3 = i + segments
            i4 = (i + 1) % segments + segments
            
            faces.append([i1, i2, i3])
            faces.append([i2, i4, i3])
            
        faces = np.array(faces)
        
        return self._create_mesh(vertices, faces, name)
        
    def _create_mesh(self, vertices, faces, name):
        """Create and save mesh"""
        mesh_data = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        
        for i, f in enumerate(faces):
            for j in range(3):
                mesh_data.vectors[i][j] = vertices[f[j]]
                
        filepath = os.path.join(self.output_dir, f"{name}.stl")
        mesh_data.save(filepath)
        print(f"Created: {filepath}")
        return mesh_data
        
    def generate_all_components(self):
        """Generate all AOS-H1 STLs"""
        print("=" * 60)
        print("AOS-H1 STL Generator")
        print("=" * 60)
        
        # TORSO COMPONENTS
        print("\n--- TORSO ---")
        self.create_cube((200, 150, 120), name="torso_main_upper")
        self.create_cube((200, 150, 100), name="torso_main_lower")
        self.create_cube((80, 100, 40), name="torso_bracket_left")
        self.create_cube((80, 100, 40), name="torso_bracket_right")
        self.create_cube((180, 20, 100), name="torso_back_panel")
        self.create_cube((180, 20, 100), name="torso_front_panel")
        self.create_cube((160, 100, 60), name="torso_battery_mount")
        
        # HEAD COMPONENTS
        print("\n--- HEAD ---")
        self.create_sphere(60, name="head_skull_main")
        self.create_cube((100, 80, 20), name="head_face_panel")
        self.create_cylinder(40, 30, name="head_neck_base")
        self.create_cylinder(30, 40, name="head_neck_pivot")
        self.create_cube((40, 40, 20), name="head_camera_mount_front")
        self.create_cube((40, 40, 20), name="head_camera_mount_rear")
        self.create_cube((60, 80, 30), name="head_speaker_left")
        self.create_cube((60, 80, 30), name="head_speaker_right")
        
        # ARM COMPONENTS
        print("\n--- ARMS ---")
        self.create_cube((100, 80, 60), name="arm_shoulder_base")
        self.create_cylinder(45, 20, name="arm_shoulder_pitch")
        self.create_cylinder(45, 20, name="arm_shoulder_roll")
        self.create_tube(20, 15, 180, name="arm_upper_tube")
        self.create_cylinder(40, 25, name="arm_elbow_joint")
        self.create_tube(18, 13, 160, name="arm_forearm_tube")
        self.create_cylinder(35, 20, name="arm_wrist_pitch")
        self.create_cylinder(30, 20, name="arm_wrist_yaw")
        self.create_cube((80, 100, 40), name="arm_palm_base")
        
        # FINGERS (5 per hand × 2 hands = 10)
        print("\n--- FINGERS ---")
        for i, finger in enumerate(['index', 'middle', 'ring', 'pinky']):
            self.create_cube((15, 15, 25), name=f"finger_{finger}_base")
            self.create_tube(12, 10, 30, name=f"finger_{finger}_segment_1")
            self.create_tube(10, 8, 25, name=f"finger_{finger}_segment_2")
            self.create_sphere(8, name=f"finger_{finger}_tip")
            
        # Thumb (special design)
        self.create_cube((20, 20, 30), name="thumb_base")
        self.create_tube(14, 11, 25, name="thumb_segment_1")
        self.create_tube(11, 9, 20, name="thumb_segment_2")
        self.create_sphere(9, name="thumb_tip")
        
        # LEG COMPONENTS
        print("\n--- LEGS ---")
        self.create_cube((120, 100, 80), name="leg_hip_base")
        self.create_cylinder(50, 25, name="leg_hip_pitch")
        self.create_cylinder(50, 25, name="leg_hip_roll")
        self.create_cylinder(45, 25, name="leg_hip_yaw")
        self.create_tube(25, 20, 220, name="leg_thigh_tube")
        self.create_cylinder(45, 30, name="leg_knee_joint")
        self.create_tube(22, 18, 200, name="leg_shin_tube")
        self.create_cylinder(40, 25, name="leg_ankle_pitch")
        self.create_cylinder(35, 25, name="leg_ankle_roll")
        self.create_cube((150, 80, 40), name="leg_foot_base")
        self.create_cube((150, 80, 10), name="leg_foot_sole")
        
        # WAIST
        print("\n--- WAIST ---")
        self.create_cube((140, 120, 60), name="waist_pelvis_upper")
        self.create_cube((140, 120, 50), name="waist_pelvis_lower")
        self.create_cylinder(60, 25, name="waist_rotation_gear")
        self.create_cylinder(45, 30, name="waist_bearing_housing")
        
        # SERVO MOUNTS (generic)
        print("\n--- SERVO MOUNTS ---")
        self.create_cube((45, 25, 40), name="mount_mg996r")
        self.create_cube((50, 30, 45), name="mount_ds3218")
        self.create_cube((25, 15, 30), name="mount_sg90")
        
        # BEARING HOLDERS
        print("\n--- BEARING HOLDERS ---")
        self.create_tube(30, 16, 10, name="bearing_holder_608")
        self.create_tube(25, 12, 8, name="bearing_holder_625")
        
        print("\n" + "=" * 60)
        print("STL Generation Complete!")
        print(f"Output directory: {self.output_dir}")
        print("=" * 60)
        

def generate_simple_stl_placeholder():
    """Generate a simple placeholder STL file"""
    # Create a simple cube as placeholder
    vertices = np.array([
        [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # Bottom
        [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1],  # Top
    ])
    
    faces = np.array([
        [0, 3, 1], [1, 3, 2],  # Bottom
        [4, 5, 7], [7, 5, 6],  # Top
        [0, 1, 4], [4, 1, 5],  # Front
        [2, 3, 6], [6, 3, 7],  # Back
        [0, 4, 3], [3, 4, 7],  # Left
        [1, 2, 5], [5, 2, 6],  # Right
    ])
    
    mesh_data = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            mesh_data.vectors[i][j] = vertices[f[j]]
            
    return mesh_data


if __name__ == "__main__":
    # Check if numpy-stl is installed
    try:
        from stl import mesh
    except ImportError:
        print("Installing numpy-stl...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'numpy-stl'])
        from stl import mesh
        
    generator = STLGenerator()
    generator.generate_all_components()
    
    print("\nNote: These are simplified geometric shapes.")
    print("For production, replace with proper CAD designs from Fusion 360 or SolidWorks.")
    print("Recommended workflow:")
    print("  1. Design in Fusion 360 (free for hobbyists)")
    print("  2. Export as STEP files")
    print("  3. Convert to STL with proper tolerances")
    print("  4. Test print and iterate")
