FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY src/ src/
COPY .env .env
COPY service-account.json service-account.json

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8002

# Health check - idk if this should be checked here
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8002/health || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8002"]



