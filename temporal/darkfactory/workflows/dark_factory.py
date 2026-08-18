"""
Dark Factory Temporal Workflows
Makes the pipeline indestructible.
"""
from datetime import timedelta
from dataclasses import dataclass
from temporalio import workflow, activity
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError, ApplicationError
import asyncio

# Activity imports (will be defined in activities.py)
with workflow.unsafe.imports_passed_through():
    from activities import (
        validate_sdk_health,
        allocate_build_resources,
        execute_build,
        verify_build_output,
        validate_hold_out,
        notify_completion,
        notify_escalation,
        cleanup_resources,
    )


@dataclass
class DarkFactoryOrder:
    """A job order for Dark Factory."""
    order_id: str
    project_name: str
    build_type: str  # "apk", "ipa", "web", "docker"
    source_path: str
    priority: str = "normal"  # "low", "normal", "high", "critical"
    max_duration_minutes: int = 60


@dataclass
class BuildResult:
    """Result of a build attempt."""
    success: bool
    output_path: str | None
    file_size_bytes: int
    logs: list[str]
    error_message: str | None = None


@workflow.defn
class DarkFactoryWorkflow:
    """
    The main Dark Factory workflow.
    Validates, builds, verifies, hold-out validates, and notifies.
    Survives crashes. Resumes where it left off.
    """

    def __init__(self):
        self.order: DarkFactoryOrder | None = None
        self.current_stage: str = "INIT"

    @workflow.run
    async def run(self, order: DarkFactoryOrder) -> BuildResult:
        self.order = order
        self.current_stage = "VALIDATING"

        # Durable watchdog: the whole build must finish within 30 minutes
        # or we escalate. Temporal makes asyncio.wait_for durable — if the
        # worker crashes, the timer + workflow state resume exactly.
        try:
            result = await asyncio.wait_for(
                self._execute(order),
                timeout=timedelta(minutes=30).total_seconds(),
            )
            self.current_stage = "COMPLETE"
            return result

        except asyncio.TimeoutError:
            await workflow.execute_activity(
                notify_escalation,
                args=(order.order_id, self.current_stage, "Workflow exceeded 30 minutes"),
                start_to_close_timeout=timedelta(minutes=1),
            )
            raise ApplicationError(f"Workflow timed out at stage {self.current_stage}")

        except ActivityError as e:
            # Build failed after retries - escalate and re-raise
            await workflow.execute_activity(
                notify_escalation,
                args=(order.order_id, self.current_stage, str(e.cause)),
                start_to_close_timeout=timedelta(minutes=1),
            )
            raise

        finally:
            # Always cleanup resources, even on failure
            await workflow.execute_activity(
                cleanup_resources,
                args=(order.order_id,),
                start_to_close_timeout=timedelta(minutes=2),
            )

    async def _execute(self, order: DarkFactoryOrder) -> BuildResult:
        """Core build pipeline: validate -> allocate -> build -> verify -> hold-out -> notify."""
        # STAGE 1: Validate SDK health (fail fast if broken)
        self.current_stage = "VALIDATING_SDK"
        await workflow.execute_activity(
            validate_sdk_health,
            args=(order.build_type,),
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=10),
                backoff_coefficient=2.0,
                maximum_interval=timedelta(minutes=2),
                maximum_attempts=3,
                non_retryable_error_types=["SDKNotInstalled", "SDKCorrupted"],
            ),
        )

        # STAGE 2: Allocate build resources
        self.current_stage = "ALLOCATING"
        resources = await workflow.execute_activity(
            allocate_build_resources,
            args=(order.order_id, order.build_type, order.priority),
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=5),
                backoff_coefficient=1.5,
                maximum_attempts=5,
            ),
        )

        # STAGE 3: Execute the build with heartbeats
        self.current_stage = "BUILDING"
        result = await workflow.execute_activity(
            execute_build,
            args=(order, resources),
            start_to_close_timeout=timedelta(minutes=order.max_duration_minutes),
            heartbeat_timeout=timedelta(seconds=60),  # Must heartbeat every 60s
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=15),
                backoff_coefficient=2.0,
                maximum_interval=timedelta(minutes=5),
                maximum_attempts=3,
            ),
        )

        # STAGE 4: Verify output actually exists
        self.current_stage = "VERIFYING"
        output_path = result.get("output_path") if isinstance(result, dict) else getattr(result, "output_path", None)
        file_size = result.get("file_size_bytes", 0) if isinstance(result, dict) else getattr(result, "file_size_bytes", 0)
        verified = await workflow.execute_activity(
            verify_build_output,
            args=(output_path, file_size),
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=5),
                maximum_attempts=3,
            ),
        )

        if not verified:
            raise ApplicationError("Build verification failed - file missing or empty")

        # STAGE 4.5: Blind hold-out validation (separate validator session)
        self.current_stage = "HOLDOUT_VALIDATING"
        holdout = await workflow.execute_activity(
            validate_hold_out,
            args=(order.project_name, output_path, file_size),
            start_to_close_timeout=timedelta(minutes=3),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=5),
                maximum_attempts=2,
            ),
        )
        if not holdout.get("passed"):
            raise ApplicationError(
                f"Hold-out validation failed for {order.project_name}: {holdout.get('reason')}"
            )

        # STAGE 5: Notify completion
        self.current_stage = "NOTIFYING"
        await workflow.execute_activity(
            notify_completion,
            args=(order.order_id, result),
            start_to_close_timeout=timedelta(minutes=1),
        )

        return result

    @workflow.query
    def get_status(self) -> dict:
        """Query current workflow status."""
        return {
            "order_id": self.order.order_id if self.order else None,
            "stage": self.current_stage,
            "project": self.order.project_name if self.order else None,
        }


@workflow.defn
class DarkFactoryBatchWorkflow:
    """
    Process multiple Dark Factory orders in batch.
    Continues even if individual jobs fail.
    """

    @workflow.run
    async def run(self, orders: list[DarkFactoryOrder]) -> list[BuildResult | None]:
        results = []

        for order in orders:
            try:
                # Child workflow - each job gets its own durable execution
                result = await workflow.execute_child_workflow(
                    DarkFactoryWorkflow.run,
                    order,
                    id=f"darkfactory-{order.order_id}",
                )
                results.append(result)
            except Exception as e:
                # Log failure but continue with next order
                results.append(None)
                await workflow.execute_activity(
                    notify_escalation,
                    args=(order.order_id, "BATCH", str(e)),
                )

        return results


@workflow.defn
class DarkFactoryHealthCheck:
    """
    Periodic health check workflow.
    Validates SDK daily, alerts if broken.
    """

    @workflow.run
    async def run(self, build_types: list[str]) -> dict[str, bool]:
        results = {}

        for build_type in build_types:
            try:
                await workflow.execute_activity(
                    validate_sdk_health,
                    args=(build_type,),
                    start_to_close_timeout=timedelta(minutes=2),
                )
                results[build_type] = True
            except Exception:
                results[build_type] = False
                await workflow.execute_activity(
                    notify_escalation,
                    args=("health-check", "DAILY", f"{build_type} SDK unhealthy"),
                )

        # Schedule next check in 24 hours
        await workflow.sleep(timedelta(hours=24))

        # Continue as new for infinite loop
        raise workflow.ContinueAsNewError(build_types)

        return results  # Never reached, but type checker happy
