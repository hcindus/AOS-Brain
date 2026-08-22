"""Legal department Temporal worker (Redactor + Velum)."""
import asyncio
import os
from temporalio.client import Client
from temporalio.worker import Worker

from workflows import MonthlyComplianceAuditWorkflow
from activities import redactor_compliance_audit, velum_privacy_audit


async def main():
    host = os.environ.get("TEMPORAL_HOST", "localhost:7233")
    client = await Client.connect(host)
    worker = Worker(
        client,
        task_queue="legal-queue",
        workflows=[MonthlyComplianceAuditWorkflow],
        activities=[redactor_compliance_audit, velum_privacy_audit],
        max_concurrent_activities=2,
    )
    print(f"⚖️ Legal worker on {host} (queue: legal-queue)")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
