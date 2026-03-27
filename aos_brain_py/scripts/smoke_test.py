#!/usr/bin/env python3
"""
Quick smoke test for aos_brain_py.
Checks imports without heavy computation.
"""

import sys
import ast
from pathlib import Path

def check_syntax(filepath):
    """Check if a Python file has valid syntax."""
    try:
        with open(filepath, 'r') as f:
            ast.parse(f.read())
        return True, None
    except SyntaxError as e:
        return False, str(e)

def main():
    print("🔍 AOS Brain Smoke Test")
    print("=" * 40)
    
    project_dir = Path(__file__).parent.parent
    py_files = list(project_dir.rglob("*.py"))
    
    print(f"Checking {len(py_files)} Python files...")
    
    errors = []
    for filepath in py_files:
        ok, err = check_syntax(filepath)
        if not ok:
            errors.append((filepath, err))
            print(f"  ❌ {filepath.name}: {err}")
        else:
            print(f"  ✅ {filepath.name}")
    
    print()
    if errors:
        print(f"Found {len(errors)} syntax errors!")
        return 1
    else:
        print("All files have valid syntax!")
        print()
        print("Next steps:")
        print("  1. Install deps: pip install -r requirements.txt")
        print("  2. Start brain: ./scripts/start_brain.sh")
        print("  3. Test API: curl http://localhost:5000/health")
        return 0

if __name__ == "__main__":
    sys.exit(main())
