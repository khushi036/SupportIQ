from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import random
import uvicorn

app = FastAPI(
    title="SupportIQ Support Ticket API",
    version="1.0.0"
)

TICKETS = {}
RESPONSE_HOURS = {
    "urgent": 1,
    "high": 2,
    "medium": 4,
    "low": 24
}

class CreateTicketRequest(BaseModel):
    conversation_id: str
    issue_type: str
    priority: str
    summary: str
    order_id: Optional[str] = None
    escalation_reason: Optional[str] = None

@app.post("/tickets", status_code=201)
async def create_support_ticket(body: CreateTicketRequest):
    ticket_number = f"TKT-{random.randint(10000, 99999)}"
    ticket = {
        "ticket_id": f"tid_{random.randint(100000, 999999)}",
        "ticket_number": ticket_number,
        "status": "open",
        "priority": body.priority,
        "issue_type": body.issue_type,
        "summary": body.summary,
        "order_id": body.order_id,
        "conversation_id": body.conversation_id,
        "estimated_response_hours": RESPONSE_HOURS.get(body.priority, 24),
        "created_at": "2026-01-15T15:00:00Z"
    }
    TICKETS[ticket_number] = ticket
    return ticket

@app.get("/tickets/{ticket_number}")
async def get_ticket(ticket_number: str):
    if ticket_number not in TICKETS:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_number} not found")
    return TICKETS[ticket_number]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
