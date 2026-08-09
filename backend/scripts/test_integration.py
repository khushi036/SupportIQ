import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swytchcode.tools import (
    get_order_status,
    track_shipment,
    check_cancellation_window,
    cancel_order,
    create_refund_request,
    create_support_ticket
)

async def run_tests():
    print("=" * 50)
    print(" SupportIQ — Swytchcode Integration Test")
    print("=" * 50)

    session_id = "test-session-001"
    conversation_id = "test-conv-001"
    passed = 0
    failed = 0

    # Test 1
    print("\n[TEST 1] get_order_status — order 48291")
    result = await get_order_status("48291", conversation_id, session_id)
    if result.success and result.data.get("status") == "out_for_delivery":
        print(f" PASS — Status: {result.data['status']} | Latency: {result.latency_ms}ms | ExecID: {result.execution_id}")
        passed += 1
    else:
        print(f" FAIL — {result.error_message}")
        failed += 1

    # Test 2
    print("\n[TEST 2] track_shipment — order 48291")
    result = await track_shipment("48291", conversation_id, session_id)
    if result.success and result.data.get("tracking_number"):
        print(f" PASS — Tracking: {result.data['tracking_number']} | Location: {result.data['current_location']}")
        passed += 1
    else:
        print(f" FAIL — {result.error_message}")
        failed += 1

    # Test 3
    print("\n[TEST 3] check_cancellation_window — order 48100 (should be cancellable)")
    result = await check_cancellation_window("48100", conversation_id, session_id)
    if result.success and result.data.get("cancellable") == True:
        print(f" PASS — Cancellable: {result.data['cancellable']}")
        passed += 1
    else:
        print(f" FAIL — {result.error_message}")
        failed += 1

    # Test 4
    print("\n[TEST 4] check_cancellation_window — order 48291 (should NOT be cancellable)")
    result = await check_cancellation_window("48291", conversation_id, session_id)
    if result.success and result.data.get("cancellable") == False:
        print(f" PASS — Correctly not cancellable | Reason: {result.data['reason']}")
        passed += 1
    else:
        print(f" FAIL — {result.error_message}")
        failed += 1

    # Test 5
    print("\n[TEST 5] cancel_order — order 48100")
    result = await cancel_order("48100", "customer changed mind", conversation_id, session_id)
    if result.success and result.data.get("status") == "cancelled":
        print(f" PASS — Cancelled | Refund: {result.data['refund_timeline']}")
        passed += 1
    else:
        print(f" FAIL — {result.error_message}")
        failed += 1

    # Test 6
    print("\n[TEST 6] create_refund_request — order 48500")
    result = await create_refund_request("48500", "wrong size", "full", conversation_id, session_id)
    if result.success and result.data.get("refund_id"):
        print(f" PASS — Refund ID: {result.data['refund_id']} | Timeline: {result.data['estimated_processing_days']} days")
        passed += 1
    else:
        print(f" FAIL — {result.error_message}")
        failed += 1

    # Test 7
    print("\n[TEST 7] create_support_ticket — damaged product")
    result = await create_support_ticket(
        conversation_id=conversation_id,
        issue_type="damaged_product",
        priority="high",
        summary="Customer received shattered screen. Highly distressed.",
        session_id=session_id,
        order_id="48291",
        escalation_reason="intent_always_requires_human_review"
    )
    if result.success and result.data.get("ticket_number"):
        print(f" PASS — Ticket: {result.data['ticket_number']} | Priority: {result.data['priority']} | ETA: {result.data['estimated_response_hours']}h")
        passed += 1
    else:
        print(f" FAIL — {result.error_message}")
        failed += 1

    # Test 8
    print("\n[TEST 8] get_order_status — order 99999 (should return not found)")
    result = await get_order_status("99999", conversation_id, session_id)
    if not result.success and result.status.value == "not_found":
        print(f" PASS — Correctly returned not_found")
        passed += 1
    else:
        print(f" FAIL — Expected not_found but got: {result.status}")
        failed += 1

    print("\n" + "=" * 50)
    print(f" Results: {passed} passed | {failed} failed")
    print("=" * 50)

    if failed == 0:
        print("\n ALL TESTS PASSED — Ready for demo\n")
    else:
        print(f"\n {failed} TEST(S) FAILED — Fix before demo\n")

if __name__ == "__main__":
    asyncio.run(run_tests())
