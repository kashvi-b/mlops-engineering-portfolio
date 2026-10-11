
"""FastAPI service for the spam-classification model."""

import os
from functools import lru_cache

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

app = FastAPI(
    title="Spam Classifier API",
    description="A containerized ML inference service.",
    version="2.0.0",
)

class Message(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=5000,
        description="Message to classify",
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Message cannot contain only whitespace.")
        return value


@lru_cache(maxsize=1)
def get_model():
    """Load the trained model once and reuse it."""
    if not os.path.isfile(MODEL_PATH):
        raise FileNotFoundError("Trained model file is missing.")
    return joblib.load(MODEL_PATH)


@app.get("/health")
def health():
    """Liveness check: confirms the API process is responding."""
    return {"status": "ok"}


@app.get("/ready")
def ready():
    """Readiness check: confirms the model can be loaded."""
    try:
        get_model()
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Model is not ready.",
        )
    return {"status": "ready", "model": "loaded"}


@app.post("/predict")
def predict(msg: Message):
    """Return a predicted label and its confidence."""
    try:
        model = get_model()
        probabilities = model.predict_proba([msg.text])[0]
        index = int(probabilities.argmax())
        label = str(model.classes_[index])
        confidence = float(probabilities[index])

        return {
            "text": msg.text,
            "label": label,
            "confidence": round(confidence, 4),
        }
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Prediction service is temporarily unavailable.",
        )
