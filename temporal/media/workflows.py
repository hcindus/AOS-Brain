"""Media & Advertising workflows — one workflow per agent job (or a batch)."""
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

from activities import generate_content


@workflow.defn
class MediaAgentWorkflow:
    """Runs a single media agent's content job."""

    @workflow.run
    async def run(self, agent: str) -> str:
        return await workflow.execute_activity(
            generate_content,
            agent,
            start_to_close_timeout=timedelta(minutes=10),
            retry_policy=RetryPolicy(maximum_attempts=2),
        )


@workflow.defn
class MediaBatchWorkflow:
    """Runs all 6 agents sequentially (daily sweep)."""

    @workflow.run
    async def run(self) -> list:
        results = []
        for agent in ["sage", "iris", "reed", "echo", "nova"]:
            r = await workflow.execute_activity(
                generate_content,
                agent,
                start_to_close_timeout=timedelta(minutes=10),
                retry_policy=RetryPolicy(maximum_attempts=2),
            )
            results.append(r)
        return results


@workflow.defn
class MediaCalendarWorkflow:
    """Weekly Max calendar orchestration."""

    @workflow.run
    async def run(self) -> str:
        return await workflow.execute_activity(
            generate_content,
            "max",
            start_to_close_timeout=timedelta(minutes=10),
            retry_policy=RetryPolicy(maximum_attempts=2),
        )
