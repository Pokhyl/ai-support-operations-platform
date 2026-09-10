# AI Support Operations Platform

Production-style customer support processing platform built as a learning project.

## Current milestone

M0 — Foundation

## Current state

Implemented:

- Python project with `src` layout
- FastAPI application skeleton
- `GET /health`
- automated health endpoint test

Planned core components:

- FastAPI
- PostgreSQL
- RabbitMQ
- worker
- n8n
- Docker Compose
- pytest
- GitHub Actions
- AI / RAG
- observability

## Architecture principles

- PostgreSQL is the source of truth.
- Long-running processing is asynchronous.
- RabbitMQ is used for messaging, not persistent state.
- AI is not a source of truth.
- Risky external actions require an explicit approval boundary.
