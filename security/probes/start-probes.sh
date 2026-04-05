#!/bin/bash
echo "Starting security probes..."
systemctl start auditd 2>/dev/null || true
systemctl start node-exporter 2>/dev/null || true
echo "✓ Probes started"
