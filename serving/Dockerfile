# Container image for the spam-classifier API.
# Trains the model at build time so the image is self-contained and reproducible.
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first so Docker can cache this layer.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source + data, then train the model into the image.
COPY train.py app.py ./
COPY data ./data
RUN python train.py

EXPOSE 8000

# Liveness check. start-period is generous because scikit-learn's first import
# is slow on some machines; the orchestrator won't kill the container too early.
HEALTHCHECK --interval=15s --timeout=5s --start-period=90s --retries=5 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Serve the API. 0.0.0.0 so it is reachable from outside the container.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
