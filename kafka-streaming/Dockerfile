# Shared image for the Kafka producer and consumer.
# The single image runs either script depending on the compose `command`.
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY producer.py consumer.py ./
