export interface SourceCitation {
  title: string;
  filename: string;
  relevance_score: number;
  excerpt: string;
}

export interface SwytchcodeGovernanceTrace {
  execution_kernel: string;
  policy_status: string;
  tool: string;
  risk_level: string;
  latency_ms: number;
  timestamp: string;
}

export interface SwytchcodeTrace {
  swytchcode_governance: SwytchcodeGovernanceTrace;
  success: boolean;
  params_validated: Record<string, any>;
  requires_escalation?: boolean;
  data?: any;
  error?: {
    code: string;
    message: string;
  };
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'agent';
  text: string;
  timestamp: string;
  intent?: string;
  sentiment?: string;
  confidence_score?: number;
  decision_action?: 'AUTO_RESOLVE' | 'ASK_CLARIFICATION' | 'ESCALATE_TO_HUMAN';
  sources?: SourceCitation[];
  swytchcode_trace?: SwytchcodeTrace;
  requires_human_escalation?: boolean;
  escalation_reason?: string;
}

export interface DashboardMetrics {
  total_conversations: number;
  auto_resolution_rate: number;
  average_response_time_sec: number;
  escalation_count: number;
  customer_satisfaction: number;
  total_swytchcode_calls: number;
  active_conversations: number;
  recent_escalations: Array<{
    id: string;
    customer: string;
    order_id: string;
    reason: string;
    priority: string;
    status: string;
    time: string;
  }>;
  api_action_breakdown: Record<string, number>;
}
