"""Outreach workflow — one durable Temporal workflow per lead (resumes on crash)."""
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

from activities import (
    send_cold_email,
    send_followup,
    check_reply,
    handle_reply,
    flag_order,
    mark_closed,
)

FOLLOWUP_DELAY = timedelta(days=4)
FINAL_DELAY = timedelta(days=5)


@workflow.defn
class LeadOutreachWorkflow:
    @workflow.run
    async def run(self, lead: dict) -> str:
        # 1. Cold email
        await workflow.execute_activity(
            send_cold_email, lead,
            start_to_close_timeout=timedelta(minutes=3),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )

        # 2. Wait, then check for a reply
        await workflow.sleep(FOLLOWUP_DELAY)
        replied = await workflow.execute_activity(
            check_reply, lead,
            start_to_close_timeout=timedelta(minutes=1),
        )

        if not replied:
            # 3. Follow-up
            await workflow.execute_activity(
                send_followup, lead,
                start_to_close_timeout=timedelta(minutes=3),
                retry_policy=RetryPolicy(maximum_attempts=3),
            )
            await workflow.sleep(FINAL_DELAY)
            replied = await workflow.execute_activity(
                check_reply, lead,
                start_to_close_timeout=timedelta(minutes=1),
            )

        if replied:
            # 4. CLOSETER handles the reply
            intent = await workflow.execute_activity(
                handle_reply, lead,
                start_to_close_timeout=timedelta(minutes=5),
            )
            if intent == "ORDER":
                await workflow.execute_activity(
                    flag_order, lead,
                    start_to_close_timeout=timedelta(minutes=1),
                )
                return "ORDER_FLAGGED"
            return intent

        # 5. No reply after follow-up → closed
        await workflow.execute_activity(
            mark_closed, lead,
            start_to_close_timeout=timedelta(minutes=1),
        )
        return "CLOSED"
