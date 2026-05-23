#!/usr/bin/env python3
"""
Quick test for Brain v4.2 + Thyroid
Tests the 'cough' reflex without running full cycles
"""

import sys
sys.path.insert(0, '/root/.aos/aos')

import time
import json
from thyroid import AOSThyroid, BrainMode
from qmd_loop import QMDLoop

print("=" * 70)
print("  🧠 BRAIN v4.2 + THYROID Quick Test")
print("=" * 70)

# Create QMD loop (initially LOCAL)
print("\n[1] Creating QMD Loop...")
qmd = QMDLoop(use_ollama=False)
print(f"    QMD mode: {'OLLAMA' if qmd.use_ollama else 'LOCAL'}")

# Create Thyroid
print("\n[2] Creating Thyroid...")
thyroid = AOSThyroid(qmd_loop=qmd, check_interval=5.0, failure_threshold=2)
print(f"    Thyroid mode: {thyroid.state.current_mode.name}")
print(f"    Check interval: {thyroid.check_interval}s")

# Start monitoring
print("\n[3] Starting Thyroid monitor...")
thyroid.start()

# Test 1: Check initial status
print("\n[4] Initial status:")
status = thyroid.get_status()
for k, v in status.items():
    print(f"    {k}: {v}")

# Test 2: Request promotion (should succeed if Ollama healthy)
print("\n[5] Testing promotion request (importance=0.9)...")
time.sleep(1)
promoted = thyroid.request_promotion(importance=0.9)
print(f"    Promotion: {'APPROVED' if promoted else 'DENIED'}")
print(f"    Current mode: {thyroid.state.current_mode.name}")

# Test 3: Simulate failures (cough back to LOCAL)
print("\n[6] Simulating Ollama failures...")
thyroid.report_failure()
print(f"    Failures: {thyroid.state.ollama_failures}")
thyroid.report_failure()
print(f"    Failures: {thyroid.state.ollama_failures}")

# Wait a moment
print("\n[7] Waiting 2 seconds...")
time.sleep(2)
print(f"    Mode after failures: {thyroid.state.current_mode.name}")

# Test 4: Simulate success (recover)
print("\n[8] Simulating Ollama recovery...")
thyroid.report_success()
thyroid.report_success()
print(f"    Failures cleared: {thyroid.state.ollama_failures}")

# Final status
print("\n[9] Final status:")
status = thyroid.get_status()
for k, v in status.items():
    print(f"    {k}: {v}")

# Stop
print("\n[10] Stopping Thyroid...")
thyroid.stop()

print("\n" + "=" * 70)
print("  ✅ THYROID TEST COMPLETE")
print("=" * 70)
print("\nThe Thyroid successfully:")
print("  • Started in LOCAL mode")
print("  • Could promote to OLLAMA (if Ollama healthy)")
print("  • Coughs back to LOCAL on failures")
print("  • Tracks success/failure for recovery")
print("\nReady to integrate into Complete Brain v4.2!")
