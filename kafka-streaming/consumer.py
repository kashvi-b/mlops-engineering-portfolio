"""Consume messages, classify each via the model API, publish predictions.

Pipeline:  messages (Kafka)  ->  POST /predict (serving API)  ->  predictions (Kafka)

Keeping inference in the serving API (rather than loading the model here) mirrors
a real system: the streaming layer and the model service scale independently.
"""
import json
import os
import time

import requests
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable

BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
IN_TOPIC = os.environ.get("MESSAGES_TOPIC", "messages")
OUT_TOPIC = os.environ.get("PREDICTIONS_TOPIC", "predictions")
API = os.environ.get("MODEL_API", "http://spam-api:8000/predict")


def connect_consumer():
    while True:
        try:
            return KafkaConsumer(
                IN_TOPIC,
                bootstrap_servers=BROKER,
                auto_offset_reset="earliest",
                group_id="spam-inference",
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            )
        except NoBrokersAvailable:
            print("consumer: waiting for kafka...", flush=True)
            time.sleep(3)


def predict(text):
    """Call the model API, retrying while it finishes its slow first load."""
    for _ in range(40):
        try:
            r = requests.post(API, json={"text": text}, timeout=90)
            r.raise_for_status()
            return r.json()
        except requests.RequestException:
            print("consumer: waiting for model api...", flush=True)
            time.sleep(3)
    raise RuntimeError("model API never became available")


def main():
    consumer = connect_consumer()
    producer = KafkaProducer(
        bootstrap_servers=BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    print(f"consumer: {IN_TOPIC} -> predict -> {OUT_TOPIC}", flush=True)
    for record in consumer:
        msg = record.value
        result = predict(msg["text"])
        out = {
            "id": msg.get("id"),
            "text": msg["text"],
            "label": result["label"],
            "confidence": result["confidence"],
        }
        producer.send(OUT_TOPIC, out)
        producer.flush()
        print(f"consumer: {out['label'].upper()} ({out['confidence']}) <- {out['text']}", flush=True)


if __name__ == "__main__":
    main()
