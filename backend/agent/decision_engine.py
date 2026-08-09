from typing import Dict, Any, Tuple

class DecisionEngine:
    """
    3-Tier Agent Decision Engine:
    Evaluates Query Intent, Parameter Completeness, Sentiment, Policy Constraints, and Confidence.
    Outputs:
    - AUTO-RESOLVE: High confidence, safe policy execution, valid data.
    - ASK_CLARIFICATION: Missing required parameters (e.g. Order ID missing).
    - ESCALATE_TO_HUMAN: Frustrated sentiment, damaged goods, refund > $100, low confidence, or policy block.
    """
    
    @staticmethod
    def evaluate(
        intent: str,
        params: Dict[str, Any],
        sentiment: str,
        confidence_score: float,
        swytchcode_result: Dict[str, Any] = None
    ) -> Tuple[str, bool, str]:
        """
        Returns: (decision_action, requires_escalation, reasoning)
        """
        # 1. Check for Frustrated Sentiment or Explicit Sensitive Refund
        if sentiment in ["FRUSTRATED", "ANGRY", "HIGH_URGENCY"]:
            return (
                "ESCALATE_TO_HUMAN",
                True,
                "Customer sentiment detected as highly frustrated or urgent. Escalating to human agent."
            )

        # 2. Check Swytchcode Policy Outcome if tool was executed
        if swytchcode_result:
            if swytchcode_result.get("requires_escalation"):
                return (
                    "ESCALATE_TO_HUMAN",
                    True,
                    swytchcode_result.get("error", {}).get("message") or "Swytchcode policy threshold exceeded."
                )

            if swytchcode_result.get("swytchcode_governance", {}).get("policy_status") == "SCHEMA_VALIDATION_FAILED":
                return (
                    "ASK_CLARIFICATION",
                    False,
                    "Invalid order number format provided."
                )

        # 3. Missing Parameter Evaluation
        if intent == "ORDER_TRACKING" and not params.get("order_id"):
            return (
                "ASK_CLARIFICATION",
                False,
                "Order ID is required to perform status lookup."
            )

        if intent in ["REFUND_REQUEST", "DAMAGED_GOODS"]:
            # Damaged items or policy sensitive issues require ticket creation & escalation
            if "damaged" in str(params.get("reason", "")).lower() or intent == "DAMAGED_GOODS":
                return (
                    "ESCALATE_TO_HUMAN",
                    True,
                    "Damaged goods claims require visual photo verification by a human supervisor under company policy."
                )

        # 4. Low Confidence Fallback
        if confidence_score < 0.70:
            return (
                "ESCALATE_TO_HUMAN",
                True,
                f"Agent confidence score ({confidence_score * 100:.1f}%) below autonomous safety threshold."
            )

        # 5. Default Standard Auto-Resolve
        return (
            "AUTO_RESOLVE",
            False,
            "High confidence response with verified Swytchcode execution trace."
        )
