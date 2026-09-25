from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from support_platform.db.session import get_db
from support_platform.models.ticket import Ticket
from support_platform.schemas.ticket import TicketCreate


app = FastAPI(
    title="AI Support Operations Platform",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/tickets", status_code=201)
def create_ticket(
    payload: TicketCreate,
    db: Session = Depends(get_db),
) -> dict:
    ticket = Ticket(
        customer_email=str(payload.customer_email),
        subject=payload.subject,
        body=payload.body,
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return {
        "id": ticket.id,
        "customer_email": ticket.customer_email,
        "subject": ticket.subject,
        "body": ticket.body,
        "status": ticket.status,
        "created_at": ticket.created_at,
    }