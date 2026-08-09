from typing import Dict, Any
import time
import random

# Realistic Mock Database for E-commerce Backend
MOCK_ORDERS = {
    "48291": {
        "order_id": "48291",
        "customer_name": "Akshay Saxena",
        "customer_id": "CUST-8821",
        "order_date": "2026-08-07",
        "status": "OUT_FOR_DELIVERY",
        "items": ["Ergonomic Wireless Keyboard", "USB-C Hub Pro"],
        "carrier": "BlueDart Express",
        "tracking_number": "BD-889102-IN",
        "estimated_delivery": "Today by 8:00 PM IST",
        "delivery_address": "Paytm Tech Park, Sector 5, Noida, UP",
        "total_amount": 129.99,
        "is_cancelable": False
    },
    "10244": {
        "order_id": "10244",
        "customer_name": "Priya Sharma",
        "customer_id": "CUST-3310",
        "order_date": "2026-08-08",
        "status": "PROCESSING",
        "items": ["Noise Cancelling Headphones"],
        "carrier": "Delhivery",
        "tracking_number": "DL-99412-IN",
        "estimated_delivery": "2026-08-11",
        "delivery_address": "Connaught Place, New Delhi",
        "total_amount": 249.50,
        "is_cancelable": True
    },
    "55912": {
        "order_id": "55912",
        "customer_name": "Rohan Gupta",
        "customer_id": "CUST-4192",
        "order_date": "2026-08-01",
        "status": "DELIVERED",
        "items": ["Smart Watch Series 5"],
        "carrier": "FedEx",
        "tracking_number": "FX-11029-IN",
        "estimated_delivery": "Delivered on Aug 4",
        "delivery_address": "Cyber City, Gurugram",
        "total_amount": 199.00,
        "is_cancelable": False
    }
}

MOCK_TICKETS = []
MOCK_REFUNDS = []

class MockEcommerceService:
    @staticmethod
    def execute(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "get_order_status":
            order_id = str(params.get("order_id", "")).strip()
            order = MOCK_ORDERS.get(order_id)
            if order:
                return {
                    "found": True,
                    "order": order,
                    "status_description": f"Order #{order_id} is currently {order['status'].replace('_', ' ').title()}. Estimated delivery: {order['estimated_delivery']} via {order['carrier']} (Tracking: {order['tracking_number']})."
                }
            else:
                return {
                    "found": False,
                    "order_id": order_id,
                    "message": f"Order #{order_id} was not found in the database. Please verify the order number."
                }

        elif tool_name == "get_customer_details":
            customer_id = str(params.get("customer_id", "CUST-8821"))
            return {
                "customer_id": customer_id,
                "name": "Akshay Saxena",
                "email": "akshay@example.com",
                "tier": "Gold VIP",
                "total_orders": 14,
                "active_orders": ["48291"]
            }

        elif tool_name == "create_support_ticket":
            ticket_id = f"TCK-{random.randint(1000, 9999)}"
            ticket = {
                "ticket_id": ticket_id,
                "order_id": params.get("order_id", "N/A"),
                "issue": params.get("issue", "Unspecified Support Request"),
                "priority": params.get("priority", "HIGH"),
                "status": "OPEN_HUMAN_QUEUE",
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            MOCK_TICKETS.append(ticket)
            return {
                "ticket_created": True,
                "ticket": ticket,
                "message": f"Support ticket {ticket_id} has been opened and assigned to a senior human agent."
            }

        elif tool_name == "request_refund":
            order_id = params.get("order_id")
            amount = params.get("amount")
            reason = params.get("reason", "Customer requested refund")
            refund_id = f"RFD-{random.randint(10000, 99999)}"
            refund = {
                "refund_id": refund_id,
                "order_id": order_id,
                "amount": amount,
                "reason": reason,
                "status": "PROCESSED",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            MOCK_REFUNDS.append(refund)
            return {
                "refund_processed": True,
                "refund": refund,
                "message": f"Refund of ${amount} for order #{order_id} has been processed under refund reference {refund_id}."
            }

        elif tool_name == "cancel_order":
            order_id = str(params.get("order_id"))
            order = MOCK_ORDERS.get(order_id)
            if order and order["is_cancelable"]:
                order["status"] = "CANCELLED"
                return {
                    "cancelled": True,
                    "order_id": order_id,
                    "message": f"Order #{order_id} has been successfully cancelled and refund initiated."
                }
            else:
                return {
                    "cancelled": False,
                    "order_id": order_id,
                    "message": f"Order #{order_id} cannot be cancelled automatically because its status is '{order['status'] if order else 'NOT_FOUND'}'."
                }

        else:
            raise ValueError(f"Unknown mock tool name: {tool_name}")
