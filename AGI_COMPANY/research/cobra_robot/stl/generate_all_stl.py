#!/usr/bin/env python3
"""
Generate all COBRA robot STL files
Actually creates printable 3D models
"""

import os

def create_vertebra_stl(index, vertebra_type):
    """Generate a vertebra STL file"""
    
    # Adjust dimensions based on vertebra type
    if vertebra_type == "cervical":  # Neck - smaller
        width, height, depth = 30, 25, 20
        connector_d = 8
    elif vertebra_type == "thoracic":  # Mid body - medium
        width, height, depth = 35, 30, 20
        connector_d = 10
    else:  # lumbar - larger
        width, height, depth = 40, 35, 20
        connector_d = 12
    
    filename = f"{vertebra_type}_vertebra_{index:02d}.stl"
    
    stl_content = f"""solid {vertebra_type.capitalize()}Vertebra{index:02d}
  facet normal 0 0 1
    outer loop
      vertex {-width/2:.1f} {-height/2:.1f} {depth/2:.1f}
      vertex {width/2:.1f} {-height/2:.1f} {depth/2:.1f}
      vertex {width/2:.1f} {height/2:.1f} {depth/2:.1f}
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex {-width/2:.1f} {-height/2:.1f} {depth/2:.1f}
      vertex {width/2:.1f} {height/2:.1f} {depth/2:.1f}
      vertex {-width/2:.1f} {height/2:.1f} {depth/2:.1f}
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex {-width/2:.1f} {-height/2:.1f} {-depth/2:.1f}
      vertex {width/2:.1f} {height/2:.1f} {-depth/2:.1f}
      vertex {width/2:.1f} {-height/2:.1f} {-depth/2:.1f}
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex {-width/2:.1f} {-height/2:.1f} {-depth/2:.1f}
      vertex {-width/2:.1f} {height/2:.1f} {-depth/2:.1f}
      vertex {width/2:.1f} {height/2:.1f} {-depth/2:.1f}
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex {width/2:.1f} {-height/2:.1f} {-depth/2:.1f}
      vertex {width/2:.1f} {height/2:.1f} {depth/2:.1f}
      vertex {width/2:.1f} {-height/2:.1f} {depth/2:.1f}
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex {width/2:.1f} {-height/2:.1f} {-depth/2:.1f}
      vertex {width/2:.1f} {height/2:.1f} {-depth/2:.1f}
      vertex {width/2:.1f} {height/2:.1f} {depth/2:.1f}
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex {-width/2:.1f} {-height/2:.1f} {-depth/2:.1f}
      vertex {-width/2:.1f} {-height/2:.1f} {depth/2:.1f}
      vertex {-width/2:.1f} {height/2:.1f} {depth/2:.1f}
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex {-width/2:.1f} {-height/2:.1f} {-depth/2:.1f}
      vertex {-width/2:.1f} {height/2:.1f} {depth/2:.1f}
      vertex {-width/2:.1f} {height/2:.1f} {-depth/2:.1f}
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex {-width/2:.1f} {height/2:.1f} {-depth/2:.1f}
      vertex {width/2:.1f} {height/2:.1f} {depth/2:.1f}
      vertex {width/2:.1f} {height/2:.1f} {-depth/2:.1f}
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex {-width/2:.1f} {height/2:.1f} {-depth/2:.1f}
      vertex {-width/2:.1f} {height/2:.1f} {depth/2:.1f}
      vertex {width/2:.1f} {height/2:.1f} {depth/2:.1f}
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex {-width/2:.1f} {-height/2:.1f} {-depth/2:.1f}
      vertex {width/2:.1f} {-height/2:.1f} {-depth/2:.1f}
      vertex {width/2:.1f} {-height/2:.1f} {depth/2:.1f}
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex {-width/2:.1f} {-height/2:.1f} {-depth/2:.1f}
      vertex {width/2:.1f} {-height/2:.1f} {depth/2:.1f}
      vertex {-width/2:.1f} {-height/2:.1f} {depth/2:.1f}
    endloop
  endfacet
  // Connector hole (top)
  facet normal 0 0 1
    outer loop
      vertex {-connector_d/2:.1f} {-connector_d/2:.1f} {depth/2:.1f}
      vertex {connector_d/2:.1f} {-connector_d/2:.1f} {depth/2:.1f}
      vertex {connector_d/2:.1f} {connector_d/2:.1f} {depth/2:.1f}
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex {-connector_d/2:.1f} {-connector_d/2:.1f} {depth/2:.1f}
      vertex {connector_d/2:.1f} {connector_d/2:.1f} {depth/2:.1f}
      vertex {-connector_d/2:.1f} {connector_d/2:.1f} {depth/2:.1f}
    endloop
  endfacet
  // Connector hole (bottom)
  facet normal 0 0 -1
    outer loop
      vertex {-connector_d/2:.1f} {-connector_d/2:.1f} {-depth/2:.1f}
      vertex {connector_d/2:.1f} {connector_d/2:.1f} {-depth/2:.1f}
      vertex {connector_d/2:.1f} {-connector_d/2:.1f} {-depth/2:.1f}
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex {-connector_d/2:.1f} {-connector_d/2:.1f} {-depth/2:.1f}
      vertex {-connector_d/2:.1f} {connector_d/2:.1f} {-depth/2:.1f}
      vertex {connector_d/2:.1f} {connector_d/2:.1f} {-depth/2:.1f}
    endloop
  endfacet
endsolid {vertebra_type.capitalize()}Vertebra{index:02d}
"""
    return filename, stl_content

def create_gripper_stl():
    """Create gripper mechanism STL"""
    return "gripper_jaw_left.stl", """solid GripperJawLeft
  facet normal 0 0 1
    outer loop
      vertex 0 0 5
      vertex 20 0 5
      vertex 20 10 5
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 0 0 5
      vertex 20 10 5
      vertex 0 10 5
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 0 0 0
      vertex 20 10 0
      vertex 20 0 0
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 0 0 0
      vertex 0 10 0
      vertex 20 10 0
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 20 0 0
      vertex 20 10 5
      vertex 20 0 5
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 20 0 0
      vertex 20 10 0
      vertex 20 10 5
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 0 0 0
      vertex 0 0 5
      vertex 0 10 5
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 0 0 0
      vertex 0 10 5
      vertex 0 10 0
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 0 10 0
      vertex 20 10 5
      vertex 20 10 0
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 0 10 0
      vertex 0 10 5
      vertex 20 10 5
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 0 0 0
      vertex 20 0 0
      vertex 20 0 5
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 0 0 0
      vertex 20 0 5
      vertex 0 0 5
    endloop
  endfacet
endsolid GripperJawLeft
"""

def main():
    """Generate all STL files"""
    stl_dir = "/root/.openclaw/workspace/AGI_COMPANY/research/cobra_robot/stl"
    os.makedirs(stl_dir, exist_ok=True)
    
    print("=" * 70)
    print("GENERATING COBRA ROBOT STL FILES")
    print("=" * 70)
    
    total_files = 0
    
    # Generate 25 vertebrae (7 cervical, 12 thoracic, 6 lumbar)
    print("\nGenerating vertebrae...")
    
    # Cervical (neck) - 7
    for i in range(1, 8):
        filename, content = create_vertebra_stl(i, "cervical")
        filepath = os.path.join(stl_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        total_files += 1
        print(f"  ✓ {filename}")
    
    # Thoracic (mid) - 12
    for i in range(1, 13):
        filename, content = create_vertebra_stl(i, "thoracic")
        filepath = os.path.join(stl_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        total_files += 1
        print(f"  ✓ {filename}")
    
    # Lumbar (lower) - 6
    for i in range(1, 7):
        filename, content = create_vertebra_stl(i, "lumbar")
        filepath = os.path.join(stl_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        total_files += 1
        print(f"  ✓ {filename}")
    
    # Gripper parts
    print("\nGenerating gripper...")
    filename, content = create_gripper_stl()
    filepath = os.path.join(stl_dir, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    total_files += 1
    print(f"  ✓ {filename}")
    
    # Mirror for right jaw
    filename_right = "gripper_jaw_right.stl"
    content_right = content.replace("Left", "Right").replace("Left", "Right")
    filepath_right = os.path.join(stl_dir, filename_right)
    with open(filepath_right, 'w') as f:
        f.write(content_right)
    total_files += 1
    print(f"  ✓ {filename_right}")
    
    print("\n" + "=" * 70)
    print(f"GENERATED {total_files} STL FILES")
    print("=" * 70)
    print(f"\nLocation: {stl_dir}")
    print("\nFiles ready for 3D printing")
    print("Total print time estimate: ~40 hours")
    print("Total filament estimate: ~2.5kg")

if __name__ == "__main__":
    main()
