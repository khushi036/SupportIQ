import re
from typing import Dict, Any, List, Tuple
from backend.models.schemas import ChatRequest, AgentResponse, SourceCitation
from backend.agent.rag import rag_retriever
from backend.agent.decision_engine import DecisionEngine
from swytchcode.execution_engine import swytchcode_engine

class SupportIQAgentOrchestrator:
    """
    Main Agent Orchestrator for SupportIQ.
    Integrates Perception (Intent/Sentiment), Knowledge (RAG), Governance (Swytchcode),
    and Cognition (Decision Matrix).
    """

    def process_message(self, request: ChatRequest) -> AgentResponse:
        message = request.message.strip()
        
        # 1. Intent Detection & Entity Extraction
        intent, extracted_params, sentiment = self._analyze_query(message)
        
        # 2. Knowledge Base RAG Retrieval
        citations: List[SourceCitation] = rag_retriever.search(message, top_k=2)
        
        # 3. Determine Required Tool & Execute via Swytchcode Governance Layer
        swytchcode_trace = None
        tool_executed = None
        confidence = 0.94
        
        if intent == "ORDER_TRACKING" and extracted_params.get("order_id"):
            tool_executed = "get_order_status"
            swytchcode_trace = swytchcode_engine.execute_tool(tool_executed, extracted_params)
            
        elif intent == "REFUND_REQUEST" or intent == "DAMAGED_GOODS":
            order_id = extracted_params.get("order_id", "48291")
            amount = extracted_params.get("amount", 129.99)
            reason = "damaged product received" if intent == "DAMAGED_GOODS" else "customer requested refund"
            
            # Execute Swytchcode ticket creation or refund evaluation
            tool_executed = "create_support_ticket" if intent == "DAMAGED_GOODS" else "request_refund"
            swytchcode_trace = swytchcode_engine.execute_tool(
                tool_executed,
                {"order_id": order_id, "amount": amount, "issue": reason, "priority": "HIGH"}
            )
            confidence = 0.88 if intent == "DAMAGED_GOODS" else 0.92

        elif intent == "CANCEL_ORDER" and extracted_params.get("order_id"):
            tool_executed = "cancel_order"
            swytchcode_trace = swytchcode_engine.execute_tool(tool_executed, extracted_params)

        # 4. Evaluate 3-Tier Decision Engine
        decision_action, requires_escalation, reasoning = DecisionEngine.evaluate(
            intent=intent,
            params=extracted_params,
            sentiment=sentiment,
            confidence_score=confidence,
            swytchcode_result=swytchcode_trace
        )

        # 5. Generate Natural Grounded Response Text
        response_text = self._generate_response_text(
            intent=intent,
            params=extracted_params,
            decision_action=decision_action,
            swytchcode_trace=swytchcode_trace,
            citations=citations,
            reasoning=reasoning
        )

        return AgentResponse(
            conversation_id=request.conversation_id or "conv_demo",
            message=response_text,
            intent=intent,
            sentiment=sentiment,
            confidence_score=confidence if decision_action == "AUTO_RESOLVE" else 0.72,
            decision_action=decision_action,
            sources=citations,
            swytchcode_trace=swytchcode_trace,
            requires_human_escalation=requires_escalation,
            escalation_reason=reasoning if requires_escalation else None
        )

    def _analyze_query(self, query: str) -> Tuple[str, Dict[str, Any], str]:
        q_lower = query.lower()
        params = {}
        
        # Extract 5-digit Order ID (e.g. #48291, 48291, order 10244)
        order_match = re.search(r'#?([0-9]{5})\b', query)
        if order_match:
            params["order_id"] = order_match.group(1)

        # Sentiment Analysis
        sentiment = "NEUTRAL"
        if any(w in q_lower for w in ["angry", "upset", "terrible", "worst", "unacceptable", "furious", "damaged"]):
            sentiment = "FRUSTRATED"
        elif any(w in q_lower for w in ["urgent", "asap", "immediately", "help"]):
            sentiment = "HIGH_URGENCY"
        elif any(w in q_lower for w in ["thanks", "great", "awesome", "good"]):
            sentiment = "POSITIVE"

        # Intent Classifier
        if "order" in q_lower and any(w in q_lower for w in ["where", "status", "track", "delivery", "arrive", "shipping"]):
            intent = "ORDER_TRACKING"
        elif "damaged" in q_lower or "broken" in q_lower or "defective" in q_lower:
            intent = "DAMAGED_GOODS"
        elif "refund" in q_lower or "money back" in q_lower:
            intent = "REFUND_REQUEST"
        elif "cancel" in q_lower:
            intent = "CANCEL_ORDER"
        elif any(w in q_lower for w in ["warranty", "guarantee", "repair"]):
            intent = "WARRANTY_QUERY"
        elif any(w in q_lower for w in ["payment", "bank", "failed", "upi"]):
            intent = "PAYMENT_QUERY"
        elif "don't know" in q_lower or "dont know" in q_lower or "lost order" in q_lower:
            intent = "MISSING_ORDER_NUMBER"
        else:
            intent = "GENERAL_KNOWLEDGE"

        return intent, params, sentiment

    def _generate_response_text(
        self,
        intent: str,
        params: Dict[str, Any],
        decision_action: str,
        swytchcode_trace: Dict[str, Any],
        citations: List[SourceCitation],
        reasoning: str
    ) -> str:
        
        # Scenario: Missing Information / Clarification required
        if decision_action == "ASK_CLARIFICATION":
            return "Sure, I can help check that right away! Could you please provide your 5-digit Order Number (e.g., #48291) so I can fetch your live shipment details?"

        # Scenario: Escalation to Human Agent
        if decision_action == "ESCALATE_TO_HUMAN":
            ticket_info = ""
            if swytchcode_trace and swytchcode_trace.get("data", {}).get("ticket"):
                t_id = swytchcode_trace["data"]["ticket"]["ticket_id"]
                ticket_info = f" I have opened high-priority Support Ticket #{t_id} on your behalf."
                
            return (
                f"I understand your concern completely.{ticket_info} Because this involves a sensitive "
                f"issue ({reasoning.lower()}), I am immediately transferring your conversation to a senior human support specialist. "
                f"An agent will join this chat within 2 minutes."
            )

        # Scenario: Order Tracking Auto-Resolve
        if intent == "ORDER_TRACKING" and swytchcode_trace and swytchcode_trace.get("success"):
            order_data = swytchcode_trace["data"]["order"]
            return (
                f"Your order #{order_data['order_id']} ({', '.join(order_data['items'])}) is currently **{order_data['status'].replace('_', ' ')}**. "
                f"It is being handled by {order_data['carrier']} (Tracking ID: `{order_data['tracking_number']}`) and is expected to arrive **{order_data['estimated_delivery']}**."
            )

        # Scenario: Cancellation Auto-Resolve
        if intent == "CANCEL_ORDER" and swytchcode_trace:
            msg = swytchcode_trace["data"].get("message") if swytchcode_trace.get("success") else swytchcode_trace["error"]["message"]
            return msg

        # Scenario: RAG Grounded Answer Fallback
        citation_text = ""
        if citations:
            best_cite = citations[0]
            citation_text = f"\n\n*(Grounded in {best_cite.title})*"

        return f"According to our company policy: {citations[0].excerpt if citations else 'Please contact support for detailed policy queries.'}{citation_text}"

agent_orchestrator = SupportIQAgentOrchestrator()
