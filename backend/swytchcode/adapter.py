import os
import uuid
import time
import logging
import httpx
from typing import Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ExecutionStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    POLICY_BLOCKED = "policy_blocked"
    VALIDATION_ERROR = "validation_error"
    TIMEOUT = "timeout"
    NOT_FOUND = "not_found"

@dataclass
class SwytchcodeResult:
    success: bool
    execution_id: str
    status: ExecutionStatus
    data: Optional[dict] = None
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    latency_ms: Optional[int] = None
    policy_check: str = "permitted"
    validation_status: str = "valid"
    tool_name: Optional[str] = None
    integration: Optional[str] = None
    operation: Optional[str] = None
    input_params: Optional[dict] = None

class IntegrationMode(Enum):
    SWYTCHCODE_SDK = "swytchcode_sdk"
    SWYTCHCODE_MCP = "swytchcode_mcp"
    SWYTCHCODE_REST = "swytchcode_rest"
    MOCK_DIRECT = "mock_direct"

class SwytchcodeAdapter:
    def __init__(self):
        self.api_key = os.getenv("SWYTCHCODE_API_KEY", "")
        self.base_url = os.getenv("SWYTCHCODE_BASE_URL", "https://api.swytchcode.com")
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.mode = self._detect_mode()
        logger.info(f"SwytchcodeAdapter initialized in mode: {self.mode.value}")

    def _detect_mode(self) -> IntegrationMode:
        if os.getenv("SWYTCHCODE_MODE"):
            mode_str = os.getenv("SWYTCHCODE_MODE")
            for m in IntegrationMode:
                if m.value == mode_str:
                    return m
        if self._sdk_available():
            return IntegrationMode.SWYTCHCODE_SDK
        if os.getenv("SWYTCHCODE_MCP_URL"):
            return IntegrationMode.SWYTCHCODE_MCP
        if self.api_key and self.api_key != "your_swytchcode_api_key_here":
            return IntegrationMode.SWYTCHCODE_REST
        logger.info("Running in MOCK_DIRECT execution mode.")
        return IntegrationMode.MOCK_DIRECT

    def _sdk_available(self) -> bool:
        try:
            import sys
            if "swytchcode_sdk" in sys.modules:
                return True
            import swytchcode_sdk  # check actual external SDK module name
            return True
        except ImportError:
            return False

    async def execute(
        self,
        integration: str,
        operation: str,
        parameters: dict,
        conversation_id: str,
        session_id: str
    ) -> SwytchcodeResult:
        execution_id = f"exec_{str(uuid.uuid4())[:8]}"
        start_time = time.time()
        logger.info(f"[{execution_id}] Swytchcode execution: {integration}.{operation}")

        try:
            if self.mode == IntegrationMode.SWYTCHCODE_SDK:
                result_data = await self._execute_via_sdk(integration, operation, parameters)
            elif self.mode == IntegrationMode.SWYTCHCODE_MCP:
                result_data = await self._execute_via_mcp(integration, operation, parameters)
            elif self.mode == IntegrationMode.SWYTCHCODE_REST:
                result_data = await self._execute_via_rest(integration, operation, parameters)
            else:
                result_data = await self._execute_mock(integration, operation, parameters)

            latency_ms = int((time.time() - start_time) * 1000)
            logger.info(f"[{execution_id}] SUCCESS in {latency_ms}ms")

            return SwytchcodeResult(
                success=True,
                execution_id=execution_id,
                status=ExecutionStatus.SUCCESS,
                data=result_data,
                latency_ms=latency_ms,
                policy_check="permitted",
                validation_status="valid",
                tool_name=f"{integration}.{operation}",
                integration=integration,
                operation=operation,
                input_params=parameters
            )
        except httpx.TimeoutException:
            latency_ms = int((time.time() - start_time) * 1000)
            logger.error(f"[{execution_id}] TIMEOUT after {latency_ms}ms")
            return SwytchcodeResult(
                success=False,
                execution_id=execution_id,
                status=ExecutionStatus.TIMEOUT,
                error_type="timeout",
                error_message="API request timed out",
                latency_ms=latency_ms,
                integration=integration,
                operation=operation,
                input_params=parameters
            )
        except httpx.HTTPStatusError as e:
            latency_ms = int((time.time() - start_time) * 1000)
            if e.response.status_code == 404:
                return SwytchcodeResult(
                    success=False,
                    execution_id=execution_id,
                    status=ExecutionStatus.NOT_FOUND,
                    error_type="not_found",
                    error_message="Resource not found",
                    latency_ms=latency_ms,
                    integration=integration,
                    operation=operation,
                    input_params=parameters
                )
            return SwytchcodeResult(
                success=False,
                execution_id=execution_id,
                status=ExecutionStatus.FAILED,
                error_type="http_error",
                error_message=str(e),
                latency_ms=latency_ms,
                integration=integration,
                operation=operation,
                input_params=parameters
            )
        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            logger.error(f"[{execution_id}] ERROR: {e}")
            return SwytchcodeResult(
                success=False,
                execution_id=execution_id,
                status=ExecutionStatus.FAILED,
                error_type="unexpected_error",
                error_message=str(e),
                latency_ms=latency_ms,
                integration=integration,
                operation=operation,
                input_params=parameters
            )

    async def _execute_via_sdk(self, integration, operation, parameters):
        import swytchcode as sc
        client = sc.Client(api_key=self.api_key)
        result = await client.exec(f"{integration}.{operation}", params=parameters)
        return result.data

    async def _execute_via_mcp(self, integration, operation, parameters):
        mcp_url = os.getenv("SWYTCHCODE_MCP_URL")
        tool_name = f"{integration}__{operation}"
        from mcp import ClientSession
        from mcp.client.sse import sse_client
        import json

        async with sse_client(mcp_url) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(name=tool_name, arguments=parameters)
                if result.content:
                    content = result.content[0]
                    if hasattr(content, 'text'):
                        return json.loads(content.text)
        return {}

    async def _execute_via_rest(self, integration, operation, parameters):
        url = f"{self.base_url}/v1/exec/{integration}/{operation}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {"params": parameters, "environment": self.environment}
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get("data") or data.get("result") or data

    async def _execute_mock(self, integration, operation, parameters):
        MOCK_ROUTES = {
            "ecommerce_api": {
                "get_order_status": {
                    "method": "GET",
                    "url": "http://localhost:8001/orders/{order_id}/status",
                    "path_params": ["order_id"]
                },
                "track_shipment": {
                    "method": "GET",
                    "url": "http://localhost:8001/orders/{order_id}/track",
                    "path_params": ["order_id"]
                },
                "check_cancellation_eligibility": {
                    "method": "GET",
                    "url": "http://localhost:8001/orders/{order_id}/cancellation-eligibility",
                    "path_params": ["order_id"]
                },
                "cancel_order": {
                    "method": "POST",
                    "url": "http://localhost:8001/orders/{order_id}/cancel",
                    "path_params": ["order_id"]
                },
                "create_refund_request": {
                    "method": "POST",
                    "url": "http://localhost:8001/orders/{order_id}/refund",
                    "path_params": ["order_id"]
                }
            },
            "support_api": {
                "create_support_ticket": {
                    "method": "POST",
                    "url": "http://localhost:8002/tickets",
                    "path_params": []
                }
            }
        }

        if integration not in MOCK_ROUTES:
            raise Exception(f"Unknown integration: {integration}")
        if operation not in MOCK_ROUTES[integration]:
            raise Exception(f"Unknown operation: {operation}")

        route = MOCK_ROUTES[integration][operation]
        url = route["url"]
        body = {}

        for param in route.get("path_params", []):
            if param in parameters:
                url = url.replace(f"{{{param}}}", parameters[param])

        if route["method"] == "POST":
            body = {k: v for k, v in parameters.items() if k not in route.get("path_params", [])}

        async with httpx.AsyncClient(timeout=10.0) as client:
            if route["method"] == "GET":
                response = await client.get(url)
            else:
                response = await client.post(url, json=body)
            response.raise_for_status()
            return response.json()
