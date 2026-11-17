"""Outreach workflow — one durable Temporal workflow per lead (recurring nurture loop)."""
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

from activities import (
    send_cold_email,
    send_followup,
    check_reply,
    handle_reply,
    flag_order,
    process_order,
    mark_closed,
    log_contact,
    ask_prices,
)

FOLLOWUP_DELAY = timedelta(days=4)
FINAL_DELAY = timedelta(days=5)
RENGAGE_DELAY = timedelta(days=21)  # ~3 weeks between nurture touches


def _contact(lead, outcome, channel, want_prices=None, notes=""):
    return {
        "vendor_id": lead.get("vendor_id"),
        "lead_name": lead.get("name"),
        "contact_type": "email",
        "channel": channel,
        "outcome": outcome,
        "want_prices": want_prices,
        "notes": notes,
        "contact_preference": lead.get("contact_preference", "email"),
        "next_touch": lead.get("next_touch"),
    }


@workflow.defn
class LeadOutreachWorkflow:
    @workflow.run
    async def run(self, lead: dict) -> str:
        # 1. Cold email + log
        await workflow.execute_activity(
            send_cold_email, lead,
            start_to_close_timeout=timedelta(minutes=3),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )
        await workflow.execute_activity(
            log_contact, _contact(lead, "sent", "outbound", notes="cold email"),
            start_to_close_timeout=timedelta(minutes=1),
        )

        # 2. Wait, then check reply
        await workflow.sleep(FOLLOWUP_DELAY)
        replied = await workflow.execute_activity(
            check_reply, lead, start_to_close_timeout=timedelta(minutes=1),
        )

        # 3. Follow-up if no reply
        if not replied:
            await workflow.execute_activity(
                send_followup, lead,
                start_to_close_timeout=timedelta(minutes=3),
                retry_policy=RetryPolicy(maximum_attempts=3),
            )
            await workflow.execute_activity(
                log_contact, _contact(lead, "followup", "outbound", notes="follow-up"),
                start_to_close_timeout=timedelta(minutes=1),
            )
            await workflow.sleep(FINAL_DELAY)
            replied = await workflow.execute_activity(
                check_reply, lead, start_to_close_timeout=timedelta(minutes=1),
            )

        # 4. Handle reply (if any) + log
        intent = "NO_REPLY"
        if replied:
            intent = await workflow.execute_activity(
                handle_reply, lead, start_to_close_timeout=timedelta(minutes=5),
            )
            await workflow.execute_activity(
                log_contact, _contact(lead, intent.lower(), "inbound", notes="reply"),
                start_to_close_timeout=timedelta(minutes=1),
            )
            if intent == "ORDER":
                await workflow.execute_activity(
                    process_order, lead, start_to_close_timeout=timedelta(minutes=3),
                )
                return "ORDER_PROCESSED"

        # 5. Hard opt-out → close. Otherwise, nurture re-engagement loop.
        if intent == "NOT-INTERESTED":
            await workflow.execute_activity(
                mark_closed, lead, start_to_close_timeout=timedelta(minutes=1),
            )
            return "CLOSED_OPTOUT"

        want = await workflow.execute_activity(
            ask_prices, {"want_prices": lead.get("want_prices", "")},
            start_to_close_timeout=timedelta(minutes=1),
        )
        await workflow.execute_activity(
            log_contact, _contact(lead, "reengage", "outbound", want_prices=want, notes="nurture touch"),
            start_to_close_timeout=timedelta(minutes=1),
        )

        # Re-queue for the next nurture touch (recurring, not a hard close).
        await workflow.sleep(RENGAGE_DELAY)
        lead["want_prices"] = want
        workflow.continue_as_new(lead)


@workflow.defn
class PaymentWorkflow:
    @workflow.run
    async def run(self, lead: dict) -> str:
        return await workflow.execute_activity(
            payment_received, lead,
            start_to_close_timeout=timedelta(minutes=2),
        )
