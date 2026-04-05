#!/bin/bash
echo "Stopping security probes..."
systemctl stop auditd 2>/dev/null || true
systemctl stop node-exporter 2>/dev/null || true
echo "✓ Probes stopped"
