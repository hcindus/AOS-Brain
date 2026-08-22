"""Consultative Approach workflows."""
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

from activities import consultative_recommend

TIMEOUT = timedelta(minutes=10)
RETRY = RetryPolicy(maximum_attempts=2)


@workflow.defn
class ConsultativeSalesWorkflow:
    """Run the consultative framework on a prospect and return a recommendation."""

    @workflow.run
    async def run(self, prospect_context: str) -> str:
        return await workflow.execute_activity(
            consultative_recommend, prospect_context,
            start_to_close_timeout=TIMEOUT, retry_policy=RETRY,
        )
