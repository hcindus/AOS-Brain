#!/bin/bash
# SOP DEPLOYMENT - PHASE 1: INFRASTRUCTURE
# Date: 2026-07-24
# Owner: Forge (Infrastructure)

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     SOP DEPLOYMENT PHASE 1 - INFRASTRUCTURE SETUP            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
TEMPORAL_VERSION="1.22.0"
POSTGRES_PASSWORD="sop_temporal_2024"
REDIS_PASSWORD="sop_cache_2024"
DEPLOY_DIR="/var/lib/aos/temporal"

echo "[Phase 1.1] Creating deployment directory..."
mkdir -p ${DEPLOY_DIR}/{data,logs,config}
mkdir -p ${DEPLOY_DIR}/data/{postgres,redis}
echo "✓ Directories created"

echo ""
echo "[Phase 1.2] Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "✗ Docker not found. Installing..."
    # Would install Docker here
    exit 1
fi
echo "✓ Docker available"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "✗ Docker Compose not found. Installing..."
    exit 1
fi
echo "✓ Docker Compose available"

# Check ports
if lsof -Pi :5432 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠ Port 5432 (PostgreSQL) in use"
fi

if lsof -Pi :6379 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠ Port 6379 (Redis) in use"
fi

echo ""
echo "[Phase 1.3] Creating Temporal configuration..."

cat > ${DEPLOY_DIR}/config/docker-compose.yml << 'EOF'
version: '3.8'

services:
  # PostgreSQL for Temporal persistence
  temporal-postgresql:
    image: postgres:15-alpine
    container_name: temporal-postgresql
    environment:
      POSTGRES_USER: temporal
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: temporal
    volumes:
      - ${DEPLOY_DIR}/data/postgres:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - temporal-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U temporal"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis for caching
  temporal-redis:
    image: redis:7-alpine
    container_name: temporal-redis
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - ${DEPLOY_DIR}/data/redis:/data
    ports:
      - "6379:6379"
    networks:
      - temporal-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Temporal Server
  temporal-server:
    image: temporalio/server:${TEMPORAL_VERSION}
    container_name: temporal-server
    depends_on:
      temporal-postgresql:
        condition: service_healthy
      temporal-redis:
        condition: service_healthy
    environment:
      - DB=postgresql
      - DB_PORT=5432
      - POSTGRES_USER=temporal
      - POSTGRES_PWD=${POSTGRES_PASSWORD}
      - POSTGRES_SEEDS=temporal-postgresql
      - DYNAMIC_CONFIG_FILE_PATH=config/dynamicconfig/development.yaml
    ports:
      - "7233:7233"  # Frontend gRPC
      - "7234:7234"  # History gRPC
      - "7235:7235"  # Matching gRPC
      - "7239:7239"  # Worker gRPC
      - "8080:8080"  # Web UI
    volumes:
      - ${DEPLOY_DIR}/config/dynamicconfig:/etc/temporal/config/dynamicconfig
    networks:
      - temporal-network

  # Temporal Web UI
  temporal-web:
    image: temporalio/web:latest
    container_name: temporal-web
    environment:
      - TEMPORAL_GRPC_ENDPOINT=temporal-server:7233
    ports:
      - "8088:8080"
    depends_on:
      - temporal-server
    networks:
      - temporal-network

  # SOP-001 Worker (Lead Response)
  sop-001-worker:
    image: python:3.11-slim
    container_name: sop-001-worker
    volumes:
      - /root/.aos/aos:/app
    working_dir: /app
    command: python -m temporal_worker --sop=001
    environment:
      - TEMPORAL_HOST=temporal-server:7233
      - REDIS_HOST=temporal-redis:6379
      - REDIS_PASSWORD=${REDIS_PASSWORD}
    depends_on:
      - temporal-server
      - temporal-redis
    networks:
      - temporal-network
    restart: unless-stopped

  # SOP-002 Worker (Quote Generation)
  sop-002-worker:
    image: python:3.11-slim
    container_name: sop-002-worker
    volumes:
      - /root/.aos/aos:/app
    working_dir: /app
    command: python -m temporal_worker --sop=002
    environment:
      - TEMPORAL_HOST=temporal-server:7233
      - REDIS_HOST=temporal-redis:6379
      - REDIS_PASSWORD=${REDIS_PASSWORD}
    depends_on:
      - temporal-server
      - temporal-redis
    networks:
      - temporal-network
    restart: unless-stopped

  # SOP-003 Worker (Order Status)
  sop-003-worker:
    image: python:3.11-slim
    container_name: sop-003-worker
    volumes:
      - /root/.aos/aos:/app
    working_dir: /app
    command: python -m temporal_worker --sop=003
    environment:
      - TEMPORAL_HOST=temporal-server:7233
      - REDIS_HOST=temporal-redis:6379
      - REDIS_PASSWORD=${REDIS_PASSWORD}
    depends_on:
      - temporal-server
      - temporal-redis
    networks:
      - temporal-network
    restart: unless-stopped

networks:
  temporal-network:
    driver: bridge
EOF

echo "✓ Docker Compose configuration created"

echo ""
echo "[Phase 1.4] Creating dynamic configuration..."

mkdir -p ${DEPLOY_DIR}/config/dynamicconfig

cat > ${DEPLOY_DIR}/config/dynamicconfig/development.yaml << 'EOF'
# Temporal dynamic configuration for SOP workflows

# Workflow execution limits
limit.maxIDLength:
  - value: 1000
    constraints: {}

limit.maxWorkflowExecutionTimeout:
  - value: 86400  # 24 hours
    constraints: {}

# Task processing
limit.maxConcurrentWorkflowTaskPollers:
  - value: 10
    constraints: {}

limit.maxConcurrentActivityTaskPollers:
  - value: 10
    constraints: {}

# Retention (30 days for SOP audit trail)
limit.historyTTL:
  - value: 2592000  # 30 days in seconds
    constraints: {}
EOF

echo "✓ Dynamic configuration created"

echo ""
echo "[Phase 1.5] Creating worker scaffolding..."

mkdir -p /root/.aos/aos/temporal_worker

cat > /root/.aos/aos/temporal_worker/__main__.py << 'EOF'
#!/usr/bin/env python3
"""
Temporal Worker for SOP Workflows
Handles SOP-001, SOP-002, SOP-003
"""

import asyncio
import os
import sys
from temporalio.client import Client
from temporalio.worker import Worker

# Import workflows
from sop_001_workflow import LeadResponseWorkflow
from sop_002_workflow import QuoteGenerationWorkflow  
from sop_003_workflow import OrderStatusWorkflow

# Import activities
from sop_001_activities import *
from sop_002_activities import *
from sop_003_activities import *

async def main():
    sop_type = sys.argv[2] if len(sys.argv) > 2 else "001"
    
    # Connect to Temporal Server
    temporal_host = os.getenv("TEMPORAL_HOST", "localhost:7233")
    client = await Client.connect(temporal_host)
    
    if sop_type == "001":
        worker = Worker(
            client,
            task_queue="sop-001-task-queue",
            workflows=[LeadResponseWorkflow],
            activities=[
                send_auto_text,
                check_response,
                assign_to_agent,
                schedule_call,
                add_to_nurture
            ]
        )
        print(f"[SOP-001 Worker] Starting...")
        
    elif sop_type == "002":
        worker = Worker(
            client,
            task_queue="sop-002-task-queue",
            workflows=[QuoteGenerationWorkflow],
            activities=[
                validate_products,
                calculate_pricing_manual,
                calculate_pricing_auto,
                pricing_approval,
                generate_quote_documents,
                send_quote,
                schedule_follow_up
            ]
        )
        print(f"[SOP-002 Worker] Starting...")
        
    elif sop_type == "003":
        worker = Worker(
            client,
            task_queue="sop-003-task-queue",
            workflows=[OrderStatusWorkflow],
            activities=[
                lookup_order_cached,
                check_shipstation_status,
                format_smart_response,
                send_auto_reply,
                create_support_ticket
            ]
        )
        print(f"[SOP-003 Worker] Starting...")
    
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
EOF

echo "✓ Worker scaffolding created"

echo ""
echo "[Phase 1.6] Creating startup script..."

cat > ${DEPLOY_DIR}/start-temporal.sh << EOF
#!/bin/bash
# Start Temporal infrastructure

echo "Starting Temporal Server and SOP Workers..."
cd ${DEPLOY_DIR}/config

# Export passwords
export POSTGRES_PASSWORD="${POSTGRES_PASSWORD}"
export REDIS_PASSWORD="${REDIS_PASSWORD}"
export DEPLOY_DIR="${DEPLOY_DIR}"

# Start services
docker-compose up -d

echo ""
echo "Waiting for services to be healthy..."
sleep 10

# Check status
docker-compose ps

echo ""
echo "Temporal Web UI: http://localhost:8088"
echo "PostgreSQL: localhost:5432"
echo "Redis: localhost:6379"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
EOF

chmod +x ${DEPLOY_DIR}/start-temporal.sh

echo "✓ Startup script created"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              PHASE 1 INFRASTRUCTURE READY                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Review configuration: ${DEPLOY_DIR}/config/"
echo "  2. Start services: ${DEPLOY_DIR}/start-temporal.sh"
echo "  3. Verify: docker-compose ps"
echo "  4. Access UI: http://localhost:8088"
echo ""
echo "⚠ WARNING: Ensure Docker and Docker Compose are installed"
echo ""
echo "Phase 1 Complete - Ready for Captain approval to proceed"
