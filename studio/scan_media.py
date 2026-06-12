#!/usr/bin/env python3
"""
Media Scanner for OpenClaw Studio
Scans workspace for images, audio, and video files
"""

import os
import json
from pathlib import Path
from datetime import datetime

MEDIA_EXTENSIONS = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp'],
    'audio': ['.mp3', '.wav', '.ogg', '.m4a', '.flac', '.aac'],
    'video': ['.mp4', '.webm', '.mov', '.avi', '.mkv', '.flv']
}

SCAN_PATHS = [
    '/root/.openclaw/media',
    '/root/.openclaw/workspace',
]

EXCLUDE_DIRS = ['node_modules', '.git', '__pycache__', '.venv', 'venv', 'dist', 'build']

def get_file_size(path):
    """Get human-readable file size"""
    size = os.path.getsize(path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def scan_media():
    """Scan for media files"""
    media_files = []
    
    for base_path in SCAN_PATHS:
        if not os.path.exists(base_path):
            continue
        
        for root, dirs, files in os.walk(base_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                ext = Path(file).suffix.lower()
                
                # Determine file type
                file_type = None
                for type_name, extensions in MEDIA_EXTENSIONS.items():
                    if ext in extensions:
                        file_type = type_name
                        break
                
                if file_type:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, '/root/.openclaw')
                    
                    media_files.append({
                        'name': file,
                        'type': file_type,
                        'path': '/' + rel_path.replace('\\', '/'),
                        'full_path': full_path,
                        'date': datetime.fromtimestamp(os.path.getmtime(full_path)).strftime('%Y-%m-%d'),
                        'size': get_file_size(full_path)
                    })
    
    return sorted(media_files, key=lambda x: x['date'], reverse=True)

def generate_json():
    """Generate JSON file for gallery"""
    media_files = scan_media()
    
    output = {
        'scan_date': datetime.now().isoformat(),
        'total_files': len(media_files),
        'files': media_files
    }
    
    # Save to JSON file
    os.makedirs('/root/.openclaw/workspace/studio', exist_ok=True)
    with open('/root/.openclaw/workspace/studio/media_data.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    return output

if __name__ == '__main__':
    print("Scanning for media files...")
    result = generate_json()
    print(f"Found {result['total_files']} media files")
    print(f"  - Images: {sum(1 for f in result['files'] if f['type'] == 'image')}")
    print(f"  - Audio: {sum(1 for f in result['files'] if f['type'] == 'audio')}")
    print(f"  - Video: {sum(1 for f in result['files'] if f['type'] == 'video')}")
    print(f"\nData saved to: studio/media_data.json")
