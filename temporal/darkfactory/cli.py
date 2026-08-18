#!/usr/bin/env python3
"""
Dark Factory CLI
Start workflows, check status, manage the pipeline.
"""
import asyncio
import argparse
import json
from datetime import datetime
from temporalio.client import Client

from workflows.dark_factory import DarkFactoryOrder, DarkFactoryWorkflow, DarkFactoryBatchWorkflow


async def start_order(args):
    """Start a single Dark Factory order."""
    client = await Client.connect(args.server)
    
    order = DarkFactoryOrder(
        order_id=args.order_id or f"DF-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
        project_name=args.project,
        build_type=args.type,
        source_path=args.source,
        priority=args.priority,
        max_duration_minutes=args.duration,
    )
    
    print(f"🚀 Starting Dark Factory order: {order.order_id}")
    print(f"   Project: {order.project_name}")
    print(f"   Type: {order.build_type}")
    print(f"   Source: {order.source_path}")
    print(f"   Priority: {order.priority}")
    
    handle = await client.start_workflow(
        DarkFactoryWorkflow.run,
        order,
        id=f"darkfactory-{order.order_id}",
        task_queue="darkfactory-queue",
    )
    
    print(f"✅ Workflow started: {handle.id}")
    print(f"   Server: {args.server}")
    
    if args.wait:
        print("⏳ Waiting for completion...")
        result = await handle.result()
        from dataclasses import asdict, is_dataclass
        if is_dataclass(result):
            result = asdict(result)
        print(f"\n📦 Result:")
        print(json.dumps(result, indent=2))
    
    return handle.id


async def batch_orders(args):
    """Start multiple orders in batch."""
    client = await Client.connect(args.server)
    
    # Parse orders from JSON or command line
    if args.file:
        with open(args.file) as f:
            data = json.load(f)
        orders = [DarkFactoryOrder(**o) for o in data]
    else:
        orders = []
        for spec in args.orders:
            # spec format: "project:type:source"
            parts = spec.split(":")
            order = DarkFactoryOrder(
                order_id=f"DF-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}-{len(orders)}",
                project_name=parts[0],
                build_type=parts[1],
                source_path=parts[2],
                priority=args.priority,
            )
            orders.append(order)
    
    print(f"🚀 Starting batch of {len(orders)} orders")
    
    handle = await client.start_workflow(
        DarkFactoryBatchWorkflow.run,
        orders,
        id=f"darkfactory-batch-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
        task_queue="darkfactory-queue",
    )
    
    print(f"✅ Batch workflow started: {handle.id}")
    return handle.id


async def check_status(args):
    """Check status of a running workflow."""
    client = await Client.connect(args.server)
    
    handle = client.get_workflow_handle(args.workflow_id)
    
    # Query the workflow for current status
    status = await handle.query("get_status")
    
    print(f"📊 Workflow: {args.workflow_id}")
    print(json.dumps(status, indent=2))
    
    # Get workflow info
    info = await handle.describe()
    print(f"\nℹ️  Workflow Info:")
    print(f"   Status: {info.status}")
    print(f"   Start Time: {info.start_time}")
    print(f"   Task Queue: {info.task_queue}")


async def list_workflows(args):
    """List recent Dark Factory workflows."""
    client = await Client.connect(args.server)
    
    print(f"📋 Recent Dark Factory workflows:")
    print("-" * 80)
    
    # List workflows (this queries the server)
    async for workflow in client.list_workflows(
        f'TaskQueue="darkfactory-queue"'
    ):
        print(f"{workflow.id}: {workflow.status.name} (started {workflow.start_time})")


async def start_health_check(args):
    """Start the periodic health check workflow."""
    client = await Client.connect(args.server)
    
    from workflows.dark_factory import DarkFactoryHealthCheck
    
    build_types = args.types.split(",")
    
    handle = await client.start_workflow(
        DarkFactoryHealthCheck.run,
        build_types,
        id="darkfactory-health-check",
        task_queue="darkfactory-queue",
    )
    
    print(f"🩺 Health check workflow started: {handle.id}")
    print(f"   Monitoring: {', '.join(build_types)}")


def main():
    parser = argparse.ArgumentParser(description="Dark Factory CLI")
    parser.add_argument(
        "--server", "-s",
        default=os.environ.get("TEMPORAL_HOST", "localhost:7233"),
        help="Temporal server address"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Start single order
    start_parser = subparsers.add_parser("start", help="Start a build order")
    start_parser.add_argument("project", help="Project name")
    start_parser.add_argument("--type", "-t", default="apk", choices=["apk", "web", "docker", "ipa"])
    start_parser.add_argument("--source", "-src", required=True, help="Source path")
    start_parser.add_argument("--order-id", "-id", help="Custom order ID")
    start_parser.add_argument("--priority", "-p", default="normal", choices=["low", "normal", "high", "critical"])
    start_parser.add_argument("--duration", "-d", type=int, default=60, help="Max duration in minutes")
    start_parser.add_argument("--wait", "-w", action="store_true", help="Wait for completion")
    
    # Batch orders
    batch_parser = subparsers.add_parser("batch", help="Start batch of orders")
    batch_parser.add_argument("orders", nargs="*", help="Orders as 'project:type:source'")
    batch_parser.add_argument("--file", "-f", help="JSON file with orders")
    batch_parser.add_argument("--priority", "-p", default="normal")
    
    # Check status
    status_parser = subparsers.add_parser("status", help="Check workflow status")
    status_parser.add_argument("workflow_id", help="Workflow ID")
    
    # List workflows
    subparsers.add_parser("list", help="List recent workflows")
    
    # Health check
    health_parser = subparsers.add_parser("health", help="Start health check")
    health_parser.add_argument("--types", "-t", default="apk,web,docker", help="Comma-separated build types to check")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Run the appropriate command
    commands = {
        "start": start_order,
        "batch": batch_orders,
        "status": check_status,
        "list": list_workflows,
        "health": start_health_check,
    }
    
    asyncio.run(commands[args.command](args))


if __name__ == "__main__":
    import os
    main()