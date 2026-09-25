from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class TicketCreate(BaseModel):
    customer_email: EmailStr
    subject: str
    body: str


class TicketRead(BaseModel):
    id: UUID
    customer_email: EmailStr
    subject: str
    body: str
    status: str
    created_at: datetime