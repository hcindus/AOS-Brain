"""Media & Advertising workflows — generate → Jordan review → Patricia review."""
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

from activities import generate_content, jordan_review, patricia_review

DEFAULT_TIMEOUT = timedelta(minutes=15)
RETRY = RetryPolicy(maximum_attempts=2)


@workflow.defn
class MediaAgentWorkflow:
    """Generate a draft, then run it through Jordan -> Patricia review."""

    @workflow.run
    async def run(self, agent: str) -> dict:
        draft_path = await workflow.execute_activity(
            generate_content, agent, start_to_close_timeout=DEFAULT_TIMEOUT, retry_policy=RETRY,
        )
        jordan = await workflow.execute_activity(
            jordan_review, agent, draft_path, start_to_close_timeout=DEFAULT_TIMEOUT, retry_policy=RETRY,
        )
        patricia = await workflow.execute_activity(
            patricia_review, agent, draft_path, start_to_close_timeout=DEFAULT_TIMEOUT, retry_policy=RETRY,
        )
        return {"draft": draft_path, "jordan": jordan, "patricia": patricia}


@workflow.defn
class MediaBatchWorkflow:
    """Run all 5 content agents through generate + review."""

    @workflow.run
    async def run(self) -> list:
        results = []
        for agent in ["sage", "iris", "reed", "echo", "nova"]:
            r = await workflow.execute_activity(
                generate_content, agent, start_to_close_timeout=DEFAULT_TIMEOUT, retry_policy=RETRY,
            )
            await workflow.execute_activity(jordan_review, agent, r, start_to_close_timeout=DEFAULT_TIMEOUT, retry_policy=RETRY)
            await workflow.execute_activity(patricia_review, agent, r, start_to_close_timeout=DEFAULT_TIMEOUT, retry_policy=RETRY)
            results.append(r)
        return results


@workflow.defn
class MediaCalendarWorkflow:
    """Weekly Max calendar (generate + review)."""

    @workflow.run
    async def run(self) -> dict:
        draft_path = await workflow.execute_activity(
            generate_content, "max", start_to_close_timeout=DEFAULT_TIMEOUT, retry_policy=RETRY,
        )
        await workflow.execute_activity(jordan_review, "max", draft_path, start_to_close_timeout=DEFAULT_TIMEOUT, retry_policy=RETRY)
        await workflow.execute_activity(patricia_review, "max", draft_path, start_to_close_timeout=DEFAULT_TIMEOUT, retry_policy=RETRY)
        return {"draft": draft_path}
