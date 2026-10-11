
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from app import app
import numpy as np


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_valid_message():
    fake_model = Mock()
    fake_model.predict_proba.return_value = np.array([[0.1, 0.9]])
    fake_model.classes_ = ["ham", "spam"]

    with patch("app.get_model", return_value=fake_model):
        response = client.post(
            "/predict",
            json={"text": "Claim your free prize now"},
        )

    assert response.status_code == 200
    assert response.json()["label"] == "spam"
    assert response.json()["confidence"] == 0.9


def test_reject_empty_message():
    response = client.post("/predict", json={"text": ""})

    assert response.status_code == 422


def test_reject_whitespace_message():
    response = client.post("/predict", json={"text": "   "})

    assert response.status_code == 422


def test_reject_long_message():
    response = client.post("/predict", json={"text": "a" * 5001})

    assert response.status_code == 422


def test_ready_when_model_loads():
    with patch("app.get_model", return_value=Mock()):
        response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_ready_when_model_fails():
    with patch("app.get_model", side_effect=RuntimeError("load failed")):
        response = client.get("/ready")

    assert response.status_code == 503
