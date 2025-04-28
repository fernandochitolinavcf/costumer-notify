#!/bin/sh

# Inicia o cron service
crond -f &

# Sobe o servidor FastAPI (Webhook)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
