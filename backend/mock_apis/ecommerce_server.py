from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import uvicorn

app = FastAPI(
    title="SupportIQ E-commerce API",
    version="1.0.0"
)

ORDERS = {
    "48291": {
        "order_id": "48291",
        "status": "out_for_delivery",
        "status_detail": "Package is on the delivery vehicle",
        "carrier": "FedEx",
        "tracking_number": "FX8291047263",
        "estimated_delivery": "Today by 8:00 PM",
        "current_location": "Local distribution center, Austin TX",
        "placed_at": "2026-01-12T09:30:00Z",
        "updated_at": "2026-01-15T06:12:00Z",
        "cancellable": False
    },
    "48100": {
        "order_id": "48100",
        "status": "processing",
        "status_detail": "Order is being prepared at warehouse",
        "carrier": None,
        "tracking_number": None,
        "estimated_delivery": "3-5 business days",
        "current_location": "Warehouse Austin TX",
        "placed_at": "2026-01-15T13:45:00Z",
        "updated_at": "2026-01-15T13:50:00Z",
        "cancellable": True
    },
    "48500": {
        "order_id": "48500",
        "status": "delivered",
        "status_detail": "Package delivered to front door",
        "carrier": "UPS",
        "tracking_number": "UP5003847261",
        "estimated_delivery": "Delivered",
        "current_location": "Delivered",
        "placed_at": "2026-01-10T08:00:00Z",
        "updated_at": "2026-01-12T14:30:00Z",
        "cancellable": False
    }
}

TRACKING_HISTORY = {
    "48291": [
        {
            "timestamp": "2026-01-15T06:12:00Z",
            "location": "Austin TX Distribution Center",
            "event": "Out for delivery"
        },
        {
            "timestamp": "2026-01-14T22:45:00Z",
            "location": "Dallas TX Sort Facility",
            "event": "Arrived at sort facility"
        },
        {
            "timestamp": "2026-01-14T18:30:00Z",
            "location": "Chicago IL Hub",
            "event": "In transit"
        },
        {
            "timestamp": "2026-01-13T10:00:00Z",
            "location": "Warehouse Austin TX",
            "event": "Shipment picked up"
        }
    ]
}

@app.get("/orders/{order_id}/status")
async def get_order_status(order_id: str):
    if order_id not in ORDERS:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return ORDERS[order_id]

@app.get("/orders/{order_id}/track")
async def track_shipment(order_id: str):
    if order_id not in ORDERS:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    order = ORDERS[order_id]
    history = TRACKING_HISTORY.get(order_id, [])
    return {
        "order_id": order_id,
        "tracking_number": order["tracking_number"],
        "carrier": order["carrier"],
        "current_status": order["status"],
        "current_location": order["current_location"],
        "estimated_delivery": order["estimated_delivery"],
        "tracking_history": history
    }

@app.get("/orders/{order_id}/cancellation-eligibility")
async def check_cancellation_eligibility(order_id: str):
    if order_id not in ORDERS:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    order = ORDERS[order_id]
    cancellable = order["cancellable"]
    return {
        "order_id": order_id,
        "cancellable": cancellable,
        "order_status": order["status"],
        "placed_at": order["placed_at"],
        "reason": (
            "Order is still in processing status and can be cancelled"
            if cancellable else f"Order cannot be cancelled — current status is {order['status']}"
        ),
        "alternative": (
            None if cancellable else "You may return the item after delivery for a full refund"
        )
    }

class CancelRequest(BaseModel):
    reason: str

@app.post("/orders/{order_id}/cancel")
async def cancel_order(order_id: str, body: CancelRequest):
    if order_id not in ORDERS:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    order = ORDERS[order_id]
    if not order["cancellable"]:
        raise HTTPException(status_code=400, detail=f"Order {order_id} is not cancellable")
    ORDERS[order_id]["status"] = "cancelled"
    ORDERS[order_id]["cancellable"] = False
    return {
        "order_id": order_id,
        "status": "cancelled",
        "cancelled_at": "2026-01-15T15:00:00Z",
        "refund_timeline": "3-5 business days",
        "confirmation_number": f"CANCEL-{random.randint(10000, 99999)}"
    }

class RefundRequest(BaseModel):
    reason: str
    refund_type: str = "full"

@app.post("/orders/{order_id}/refund")
async def create_refund_request(order_id: str, body: RefundRequest):
    if order_id not in ORDERS:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return {
        "refund_id": f"REF-{random.randint(10000, 99999)}",
        "order_id": order_id,
        "status": "pending_review",
        "refund_type": body.refund_type,
        "reason": body.reason,
        "estimated_processing_days": 5,
        "refund_method": "Original payment method",
        "created_at": "2026-01-15T15:00:00Z"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
