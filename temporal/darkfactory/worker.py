"""
Dark Factory Temporal Worker
Runs activities and workflows. Survives crashes.
"""
import asyncio
import os
from temporalio.client import Client
from temporalio.worker import Worker

from workflows.dark_factory import (
    DarkFactoryWorkflow,
    DarkFactoryBatchWorkflow,
    DarkFactoryHealthCheck,
)
from activities import (
    validate_sdk_health,
    allocate_build_resources,
    execute_build,
    verify_build_output,
    validate_hold_out,
    deploy_blue_green,
    notify_completion,
    notify_escalation,
    cleanup_resources,
)


async def main():
    """Start the Dark Factory worker."""
    
    # Connect to Temporal server
    # Use Miles.cloud Temporal server
    temporal_host = os.environ.get("TEMPORAL_HOST", "localhost:7233")
    
    print(f"🔌 Connecting to Temporal at {temporal_host}...")
    client = await Client.connect(temporal_host)
    
    print("✅ Connected to Temporal server")
    
    # Create worker with all workflows and activities
    worker = Worker(
        client,
        task_queue="darkfactory-queue",
        workflows=[
            DarkFactoryWorkflow,
            DarkFactoryBatchWorkflow,
            DarkFactoryHealthCheck,
        ],
        activities=[
            validate_sdk_health,
            allocate_build_resources,
            execute_build,
            verify_build_output,
            validate_hold_out,
            deploy_blue_green,
            notify_completion,
            notify_escalation,
            cleanup_resources,
        ],
        max_concurrent_activities=5,  # Don't overwhelm the build system
    )
    
    print("🚀 Dark Factory worker starting...")
    print("   Task queue: darkfactory-queue")
    print("   Workflows: DarkFactoryWorkflow, DarkFactoryBatchWorkflow, DarkFactoryHealthCheck")
    print("   Activities: 9 build + validation + deploy activities")
    
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())