# serving/ — Containerized ML model API (Docker)

A TF-IDF + Logistic Regression spam classifier served as a REST API and packaged
as a Docker image. This is the model the rest of the repo streams, provisions for,
and deploys.

## What this demonstrates
- Writing a **Dockerfile** from a base image, layer caching, and a reproducible build.
- Training a model at build time so the image is self-contained.
- Serving a model behind a health-checked HTTP API (FastAPI + uvicorn).

## Run it
```bash
# from the repo root
docker build -t mlops-serving ./serving
docker run -d -p 8000:8000 --name spam-api mlops-serving

# health check
curl http://localhost:8000/health

# prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Congratulations you won a free prize claim now"}'

# stop it
docker rm -f spam-api
```

> **Note:** the first `/predict` after startup can take ~40s while scikit-learn
> loads for the first time (slower on some machines); every call after that is
> instant. `/health` is always fast because model loading is lazy.

## Be able to explain (interview-ready)
- Why we install `requirements.txt` before copying source (build-cache layering).
- The difference between `EXPOSE` and `-p` (documentation vs. actual port publishing).
- Why the API binds to `0.0.0.0` instead of `127.0.0.1` inside a container.
- What `/health` is for (container/orchestrator liveness probes).
