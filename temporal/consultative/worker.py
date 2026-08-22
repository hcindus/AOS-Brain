"""Sales department Temporal worker (consultative approach)."""
import asyncio
import os
from temporalio.client import Client
from temporalio.worker import Worker

from workflows import ConsultativeSalesWorkflow
from activities import consultative_recommend


async def main():
    host = os.environ.get("TEMPORAL_HOST", "localhost:7233")
    client = await Client.connect(host)
    worker = Worker(
        client,
        task_queue="sales-queue",
        workflows=[ConsultativeSalesWorkflow],
        activities=[consultative_recommend],
        max_concurrent_activities=2,
    )
    print(f"🤝 Sales worker on {host} (queue: sales-queue) — Consultative Approach")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
