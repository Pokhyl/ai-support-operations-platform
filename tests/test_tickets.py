from datetime import datetime, timezone
from uuid import uuid4

from fastapi.testclient import TestClient

from support_platform.api.main import app
from support_platform.db.session import get_db
from support_platform.models.ticket import Ticket


client = TestClient(app)


def test_create_ticket_returns_created_ticket() -> None:
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

    try:
        response = client.post(
            "/tickets",
            json={
                "customer_email": "test@example.com",
                "subject": "Cannot login",
                "body": "I cannot log into my account",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201

    data = response.json()

    assert data["customer_email"] == "test@example.com"
    assert data["subject"] == "Cannot login"
    assert data["body"] == "I cannot log into my account"
    assert data["status"] == "new"
    assert data["id"]
    assert data["created_at"]


def test_get_ticket_returns_ticket() -> None:
    ticket_id = uuid4()

    ticket = Ticket(
        customer_email="test@example.com",
        subject="Cannot login",
        body="I cannot log into my account",
    )
    ticket.id = ticket_id
    ticket.status = "new"
    ticket.created_at = datetime.now(timezone.utc)

    class FakeGetSession:
        def get(self, model, requested_id):
            if requested_id == ticket_id:
                return ticket

            return None

    def override_get_db():
        yield FakeGetSession()

    app.dependency_overrides[get_db] = override_get_db

    try:
        response = client.get(f"/tickets/{ticket_id}")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(ticket_id)
    assert data["customer_email"] == "test@example.com"
    assert data["subject"] == "Cannot login"
    assert data["body"] == "I cannot log into my account"
    assert data["status"] == "new"


def test_get_ticket_returns_404_when_missing() -> None:
    ticket_id = uuid4()

    class FakeMissingSession:
        def get(self, model, requested_id):
            return None

    def override_get_db():
        yield FakeMissingSession()

    app.dependency_overrides[get_db] = override_get_db

    try:
        response = client.get(f"/tickets/{ticket_id}")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}