from datetime import datetime, timezone
from uuid import uuid4

from fastapi.testclient import TestClient

from support_platform.api.main import app
from support_platform.db.session import get_db


class FakeSession:
    def add(self, ticket) -> None:
        self.ticket = ticket

    def commit(self) -> None:
        pass

    def refresh(self, ticket) -> None:
        ticket.id = uuid4()
        ticket.status = "new"
        ticket.created_at = datetime.now(timezone.utc)


def override_get_db():
    yield FakeSession()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_ticket_returns_created_ticket() -> None:
    response = client.post(
        "/tickets",
        json={
            "customer_email": "test@example.com",
            "subject": "Cannot login",
            "body": "I cannot log into my account",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["customer_email"] == "test@example.com"
    assert data["subject"] == "Cannot login"
    assert data["body"] == "I cannot log into my account"
    assert data["status"] == "new"
    assert data["id"]
    assert data["created_at"]