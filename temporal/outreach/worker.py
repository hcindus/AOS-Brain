"""Outreach Temporal Worker — runs the outreach workflows/activities (survives crashes)."""
import asyncio, os
from temporalio.client import Client
from temporalio.worker import Worker

from workflows import LeadOutreachWorkflow, PaymentWorkflow
from activities import (
    send_cold_email, send_followup, check_reply,
    handle_reply, flag_order, process_order, mark_closed, payment_received,
)


async def main():
    host = os.environ.get("TEMPORAL_HOST", "localhost:7233")
    print(f"🔌 Connecting to Temporal at {host}...")
    client = await Client.connect(host)
    print("✅ Connected")

    worker = Worker(
        client,
        task_queue="outreach-queue",
        workflows=[LeadOutreachWorkflow, PaymentWorkflow],
        activities=[send_cold_email, send_followup, check_reply,
                     handle_reply, flag_order, process_order, mark_closed, payment_received],
        max_concurrent_activities=5,
    )
    print("🛠️ Outreach worker running (outreach-queue). Ctrl-C to stop.")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
