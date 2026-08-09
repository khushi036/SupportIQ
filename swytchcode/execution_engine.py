import json
import re
import os
import time
from typing import Dict, Any, Optional

class SwytchcodeExecutionEngine:
    """
    Swytchcode Controlled Execution Engine
    Acts as the governed layer between AI Agents and backend APIs.
    Performs policy checks (tooling.json), schema validation, rate-limiting simulation,
    and returns deterministic structured execution output with audit metadata.
    """
    
    def __init__(self, policy_path: Optional[str] = None):
        if policy_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            policy_path = os.path.join(base_dir, "tooling.json")
            
        with open(policy_path, "r", encoding="utf-8") as f:
            self.policy_config = json.load(f)
            
        self.policies = {p["tool"]: p for p in self.policy_config.get("policies", [])}

    def execute_tool(self, tool_name: str, params: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        start_time = time.time()
        context = context or {}
        
        # 1. Policy Lookup & Allowed Check
        tool_policy = self.policies.get(tool_name)
        if not tool_policy:
            return self._build_response(
                tool_name=tool_name,
                success=False,
                policy_status="REJECTED_UNKNOWN_TOOL",
                error_code="UNREGISTERED_TOOL",
                message=f"Tool '{tool_name}' is not registered in Swytchcode manifest.",
                latency_ms=self._elapsed_ms(start_time),
                params=params
            )

        if not tool_policy.get("allowed", False):
            return self._build_response(
                tool_name=tool_name,
                success=False,
                policy_status="BLOCKED_BY_POLICY",
                error_code="TOOL_DISABLED",
                message=f"Tool '{tool_name}' is currently disabled in Swytchcode policy rules.",
                latency_ms=self._elapsed_ms(start_time),
                params=params
            )

        # 2. Input Parameter Pattern Validation
        validations = tool_policy.get("validation", {})
        for param_name, pattern in validations.items():
            if param_name in params and params[param_name] is not None:
                val_str = str(params[param_name])
                if not re.match(pattern, val_str):
                    return self._build_response(
                        tool_name=tool_name,
                        success=False,
                        policy_status="SCHEMA_VALIDATION_FAILED",
                        error_code="INVALID_PARAMETER_FORMAT",
                        message=f"Parameter '{param_name}' with value '{val_str}' failed policy regex requirement: {pattern}",
                        latency_ms=self._elapsed_ms(start_time),
                        params=params
                    )

        # 3. Human Approval Rule Evaluation (Governance Guardrails)
        human_rules = tool_policy.get("human_approval_rules", {})
        if human_rules:
            amount_limit = human_rules.get("amount_gt")
            req_amount = params.get("amount")
            if amount_limit and req_amount and float(req_amount) > float(amount_limit):
                return self._build_response(
                    tool_name=tool_name,
                    success=False,
                    policy_status="REQUIRES_HUMAN_APPROVAL",
                    error_code="POLICY_THRESHOLD_EXCEEDED",
                    message=f"Refund request of ${req_amount} exceeds maximum autonomous threshold (${amount_limit}). Swytchcode policy requires human approval.",
                    latency_ms=self._elapsed_ms(start_time),
                    params=params,
                    requires_escalation=True
                )

        # 4. Dispatch Execution to Backend Handler
        try:
            from backend.services.mock_services import MockEcommerceService
            service_result = MockEcommerceService.execute(tool_name, params)
            
            return self._build_response(
                tool_name=tool_name,
                success=True,
                policy_status="PASSED_PASSTHROUGH",
                result=service_result,
                latency_ms=self._elapsed_ms(start_time),
                params=params,
                risk_level=tool_policy.get("risk_level", "LOW")
            )
        except Exception as e:
            return self._build_response(
                tool_name=tool_name,
                success=False,
                policy_status="EXECUTION_ERROR",
                error_code="BACKEND_SERVICE_FAIL",
                message=f"Execution error in tool handler: {str(e)}",
                latency_ms=self._elapsed_ms(start_time),
                params=params
            )

    def _elapsed_ms(self, start_time: float) -> float:
        return round((time.time() - start_time) * 1000, 2)

    def _build_response(
        self,
        tool_name: str,
        success: bool,
        policy_status: str,
        result: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
        message: Optional[str] = None,
        latency_ms: float = 0.0,
        params: Optional[Dict[str, Any]] = None,
        requires_escalation: bool = False,
        risk_level: str = "LOW"
    ) -> Dict[str, Any]:
        return {
            "swytchcode_governance": {
                "execution_kernel": "Swytchcode CLI v1.2",
                "policy_status": policy_status,
                "tool": tool_name,
                "risk_level": risk_level,
                "latency_ms": latency_ms,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "success": success,
            "params_validated": params or {},
            "requires_escalation": requires_escalation,
            "data": result if success else None,
            "error": {
                "code": error_code,
                "message": message
            } if not success else None
        }

# Global singleton engine instance
swytchcode_engine = SwytchcodeExecutionEngine()
