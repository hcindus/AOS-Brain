import json
import os
import time
from pathlib import Path

class ThalamusAgent:
    def __init__(self, cfg):
        self.cfg = cfg
        self.input_file = os.path.expanduser("~/.aos/brain/input/queue.jsonl")
        self.last_check = 0
        
        # Ensure input directory exists
        os.makedirs(os.path.dirname(self.input_file), exist_ok=True)

    def observe(self):
        """Check for external input, fallback to system_tick"""
        # Check for external input file
        if os.path.exists(self.input_file):
            try:
                with open(self.input_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        # Get first line (oldest input)
                        input_data = json.loads(lines[0].strip())
                        
                        # Remove processed line
                        with open(self.input_file, 'w') as f:
                            f.writelines(lines[1:])
                        
                        return {
                            "input": input_data.get('text', 'unknown'),
                            "source": input_data.get('source', 'external'),
                            "timestamp": input_data.get('timestamp', time.time()),
                            "type": input_data.get('type', 'user_input')
                        }
            except Exception as e:
                # If file read fails, continue to fallback
                pass
        
        # Fallback to system tick
        return {"input": "system_tick"}
