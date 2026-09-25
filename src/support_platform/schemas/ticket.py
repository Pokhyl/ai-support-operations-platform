from pydantic import BaseModel, EmailStr


class TicketCreate(BaseModel):
    customer_email: EmailStr
    subject: str
    body: str