from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from uuid import UUID
from support_platform.db.session import get_db
from support_platform.models.ticket import Ticket
from support_platform.schemas.ticket import TicketCreate, TicketRead


app = FastAPI(
    title="AI Support Operations Platform",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/tickets", status_code=201, response_model=TicketRead)
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
@app.get("/tickets/{ticket_id}", response_model=TicketRead)
def get_ticket(
    ticket_id: UUID,
    db: Session = Depends(get_db),
) -> Ticket:
    ticket = db.get(Ticket, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    return ticket
@app.get("/tickets", response_model=list[TicketRead])
def get_tickets(
    db: Session = Depends(get_db),
) -> list[Ticket]:
    statement = select(Ticket).order_by(Ticket.created_at.desc())

    tickets = db.scalars(statement).all()

    return list(tickets)