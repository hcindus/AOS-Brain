"""Set up the monthly compliance audit schedule (1st of each month)."""
import asyncio
import os
from temporalio.client import Client, Schedule, ScheduleActionStartWorkflow, ScheduleSpec, ScheduleCalendarSpec, ScheduleRange

from workflows import MonthlyComplianceAuditWorkflow


async def main():
    host = os.environ.get("TEMPORAL_HOST", "localhost:7233")
    client = await Client.connect(host)

    # Monthly on the 1st at 06:00 UTC
    sched = Schedule(
        action=ScheduleActionStartWorkflow(
            MonthlyComplianceAuditWorkflow.run,
            # month string is computed inside the workflow via a default; pass a placeholder
            args=["AUTO"],
            id="legal-monthly-compliance-audit",
            task_queue="legal-queue",
        ),
        spec=ScheduleSpec(
            calendars=[ScheduleCalendarSpec(day_of_month=[ScheduleRange(1)], hour=[ScheduleRange(6)], minute=[ScheduleRange(0)])],
        ),
    )
    await client.create_schedule("legal-monthly-compliance-audit", sched, trigger_immediately=False)
    print("✅ Schedule created: legal-monthly-compliance-audit (1st of month, 06:00 UTC)")


if __name__ == "__main__":
    asyncio.run(main())
