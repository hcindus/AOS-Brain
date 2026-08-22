"""Media & Advertising Temporal worker."""
import asyncio
import os
from temporalio.client import Client
from temporalio.worker import Worker

from workflows import MediaAgentWorkflow, MediaBatchWorkflow, MediaCalendarWorkflow
from activities import generate_content, jordan_review, patricia_review


async def main():
    host = os.environ.get("TEMPORAL_HOST", "localhost:7233")
    client = await Client.connect(host)
    worker = Worker(
        client,
        task_queue="media-queue",
        workflows=[MediaAgentWorkflow, MediaBatchWorkflow, MediaCalendarWorkflow],
        activities=[generate_content, jordan_review, patricia_review],
        max_concurrent_activities=2,
    )
    print(f"🚀 Media worker on {host} (queue: media-queue)")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
