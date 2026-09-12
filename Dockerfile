FROM python:3.14.7-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml README.md ./
COPY src ./src

RUN python -m pip install --no-cache-dir .

RUN addgroup --system app \
    && adduser --system --ingroup app app

USER app

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "support_platform.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
