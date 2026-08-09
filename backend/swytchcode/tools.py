from swytchcode.adapter import SwytchcodeAdapter, SwytchcodeResult
from typing import Optional

adapter = SwytchcodeAdapter()

async def get_order_status(order_id: str, conversation_id: str, session_id: str) -> SwytchcodeResult:
    if not order_id or not order_id.strip():
        raise ValueError("order_id is required")
    return await adapter.execute(
        integration="ecommerce_api",
        operation="get_order_status",
        parameters={"order_id": order_id.strip()},
        conversation_id=conversation_id,
        session_id=session_id
    )

async def track_shipment(order_id: str, conversation_id: str, session_id: str) -> SwytchcodeResult:
    if not order_id:
        raise ValueError("order_id is required")
    return await adapter.execute(
        integration="ecommerce_api",
        operation="track_shipment",
        parameters={"order_id": order_id.strip()},
        conversation_id=conversation_id,
        session_id=session_id
    )

async def check_cancellation_window(order_id: str, conversation_id: str, session_id: str) -> SwytchcodeResult:
    if not order_id:
        raise ValueError("order_id is required")
    return await adapter.execute(
        integration="ecommerce_api",
        operation="check_cancellation_eligibility",
        parameters={"order_id": order_id.strip()},
        conversation_id=conversation_id,
        session_id=session_id
    )

async def cancel_order(order_id: str, reason: str, conversation_id: str, session_id: str) -> SwytchcodeResult:
    if not order_id:
        raise ValueError("order_id is required")
    if not reason:
        raise ValueError("reason is required")
    return await adapter.execute(
        integration="ecommerce_api",
        operation="cancel_order",
        parameters={"order_id": order_id.strip(), "reason": reason},
        conversation_id=conversation_id,
        session_id=session_id
    )

async def create_refund_request(order_id: str, reason: str, refund_type: str, conversation_id: str, session_id: str) -> SwytchcodeResult:
    if not order_id:
        raise ValueError("order_id is required")
    if not reason:
        raise ValueError("reason is required")
    if refund_type not in ["full", "partial"]:
        raise ValueError("refund_type must be full or partial")
    return await adapter.execute(
        integration="ecommerce_api",
        operation="create_refund_request",
        parameters={"order_id": order_id.strip(), "reason": reason, "refund_type": refund_type},
        conversation_id=conversation_id,
        session_id=session_id
    )

async def create_support_ticket(
    conversation_id: str,
    issue_type: str,
    priority: str,
    summary: str,
    session_id: str,
    order_id: Optional[str] = None,
    escalation_reason: Optional[str] = None
) -> SwytchcodeResult:
    valid_issue_types = ["damaged_product", "wrong_product", "payment_dispute", "refund_dispute", "delivery_issue", "cancellation_issue", "api_failure", "security_flag", "other"]
    valid_priorities = ["low", "medium", "high", "urgent"]

    if issue_type not in valid_issue_types:
        issue_type = "other"
    if priority not in valid_priorities:
        priority = "medium"

    if len(summary) > 500:
        summary = summary[:497] + "..."

    params = {
        "conversation_id": conversation_id,
        "issue_type": issue_type,
        "priority": priority,
        "summary": summary,
        "escalation_reason": escalation_reason or "agent_decision"
    }

    if order_id:
        params["order_id"] = order_id

    return await adapter.execute(
        integration="support_api",
        operation="create_support_ticket",
        parameters=params,
        conversation_id=conversation_id,
        session_id=session_id
    )
