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

## Local Docker run

Build the API image:

```bash
docker build -t ai-support-operations-api:dev .
```

Run the API container:

```bash
docker run --rm --name ai-support-api -p 8000:8000 ai-support-operations-api:dev
```

Check the health endpoint:

```bash
curl http://127.0.0.1:8000/health
```
