from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ChatRequest(BaseModel):
    message: str = Field(..., example="Where is my order #48291?")
    conversation_id: Optional[str] = Field(default="conv_default")
    customer_id: Optional[str] = Field(default="CUST-8821")

class SourceCitation(BaseModel):
    title: str
    filename: str
    relevance_score: float
    excerpt: str

class SwytchcodeAuditLog(BaseModel):
    tool: str
    policy_status: str
    latency_ms: float
    risk_level: str
    params_validated: Dict[str, Any]
    timestamp: str

class AgentResponse(BaseModel):
    conversation_id: str
    message: str
    intent: str
    sentiment: str
    confidence_score: float
    decision_action: str  # AUTO_RESOLVE | ASK_CLARIFICATION | ESCALATE_TO_HUMAN
    sources: List[SourceCitation] = []
    swytchcode_trace: Optional[Dict[str, Any]] = None
    requires_human_escalation: bool = False
    escalation_reason: Optional[str] = None

class DashboardMetrics(BaseModel):
    total_conversations: int
    auto_resolution_rate: float
    average_response_time_sec: float
    escalation_count: int
    customer_satisfaction: float
    total_swytchcode_calls: int
    active_conversations: int
    recent_escalations: List[Dict[str, Any]]
    api_action_breakdown: Dict[str, int]
