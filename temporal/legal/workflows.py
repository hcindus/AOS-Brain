"""Legal department workflows — monthly compliance audit (Redactor + Velum)."""
from datetime import timedelta
from datetime import datetime, timezone
from temporalio import workflow
from temporalio.common import RetryPolicy

from activities import redactor_compliance_audit, velum_privacy_audit

TIMEOUT = timedelta(minutes=15)
RETRY = RetryPolicy(maximum_attempts=2)


@workflow.defn
class MonthlyComplianceAuditWorkflow:
    """Run Redactor (compliance) + Velum (privacy) audits for a given month."""

    @workflow.run
    async def run(self, month: str = "AUTO") -> dict:
        if month == "AUTO":
            month = datetime.now(timezone.utc).strftime("%Y-%m")
        compliance = await workflow.execute_activity(
            redactor_compliance_audit, month, start_to_close_timeout=TIMEOUT, retry_policy=RETRY,
        )
        privacy = await workflow.execute_activity(
            velum_privacy_audit, month, start_to_close_timeout=TIMEOUT, retry_policy=RETRY,
        )
        return {"compliance_report": compliance, "privacy_report": privacy}
