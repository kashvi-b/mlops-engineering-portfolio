"""FastAPI service that serves the spam classifier over HTTP.

Endpoints:
  GET  /health            -> liveness probe (fast; used by Docker / Kubernetes)
  POST /predict {text}    -> {label, confidence}

The model is loaded lazily on the first prediction so the process starts fast
and the liveness probe never blocks on model loading.
"""
import os

import joblib
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

app = FastAPI(title="Spam Classifier API", version="1.0.0")

_clf = None


def get_model():
    """Load and cache the model on first use."""
    global _clf
    if _clf is None:
        _clf = joblib.load(MODEL_PATH)
    return _clf


class Message(BaseModel):
    text: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(msg: Message):
    clf = get_model()
    label = clf.predict([msg.text])[0]
    confidence = float(max(clf.predict_proba([msg.text])[0]))
    return {"text": msg.text, "label": label, "confidence": round(confidence, 4)}
