#!/usr/bin/env python3
"""Script to fix Dark Factory logging issue"""

import os
import sys

# The fix - make logging robust for CI
old_logging = '''# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('/var/log/dark_factory/pipeline.log'),
        logging.StreamHandler()
    ]
)'''

new_logging = '''# Setup logging - works in both CI and local environments
log_dir = os.environ.get('DF_LOG_DIR', '/var/log/dark_factory')
log_file = os.path.join(log_dir, 'pipeline.log')

# Try to ensure log directory exists, fallback to local if needed
try:
    os.makedirs(log_dir, exist_ok=True)
    handlers = [logging.FileHandler(log_file), logging.StreamHandler()]
except (OSError, PermissionError):
    # CI or restricted environment - use local logs
    local_log = os.path.join(os.path.dirname(__file__), 'logs', 'pipeline.log')
    os.makedirs(os.path.dirname(local_log), exist_ok=True)
    handlers = [logging.FileHandler(local_log), logging.StreamHandler()]
    log_file = local_log

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=handlers
)'''

print("Fix created. Apply this change to dark_factory_pipeline.py")
print("\nOLD CODE:")
print(old_logging)
print("\nNEW CODE:")
print(new_logging)
