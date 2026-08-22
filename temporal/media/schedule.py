"""Set up Temporal schedules for the media agents (cron)."""
import asyncio
import os
from temporalio.client import Client, Schedule, ScheduleActionStartWorkflow, ScheduleSpec, ScheduleCalendarSpec, ScheduleRange

from workflows import MediaAgentWorkflow, MediaBatchWorkflow, MediaCalendarWorkflow

async def main():
    host = os.environ.get("TEMPORAL_HOST", "localhost:7233")
    client = await Client.connect(host)

    # Daily batch (sage, iris, reed, echo, nova) at 08:00 UTC
    daily = Schedule(
        action=ScheduleActionStartWorkflow(
            MediaBatchWorkflow.run,
            id="media-daily-sweep",
            task_queue="media-queue",
        ),
        spec=ScheduleSpec(
            calendars=[ScheduleCalendarSpec(hour=[ScheduleRange(8)], minute=[ScheduleRange(0)])],
        ),
    )
    await client.create_schedule("media-daily-sweep", daily, trigger_immediately=False)

    # Weekly calendar (max) Monday 09:00 UTC
    weekly = Schedule(
        action=ScheduleActionStartWorkflow(
            MediaCalendarWorkflow.run,
            id="media-weekly-calendar",
            task_queue="media-queue",
        ),
        spec=ScheduleSpec(
            calendars=[ScheduleCalendarSpec(day_of_week=[ScheduleRange(1)], hour=[ScheduleRange(9)], minute=[ScheduleRange(0)])],
        ),
    )
    await client.create_schedule("media-weekly-calendar", weekly, trigger_immediately=False)

    print("✅ Schedules created: media-daily-sweep (08:00 UTC daily), media-weekly-calendar (Mon 09:00 UTC)")


if __name__ == "__main__":
    asyncio.run(main())
