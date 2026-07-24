"""Publish a stream of messages to the Kafka 'messages' topic.

Simulates a live feed of incoming messages that need spam classification.
"""
import json
import os
import time

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
TOPIC = os.environ.get("MESSAGES_TOPIC", "messages")

SAMPLES = [
    "Congratulations you won a free prize claim now",
    "Hey are we still meeting for lunch tomorrow",
    "URGENT verify your account now to claim your reward",
    "Can you send me the notes from today lecture",
    "Free entry into our weekly prize draw text WIN to 80085",
    "I will be late to the office due to traffic",
    "Claim your lottery winnings today send your bank details",
    "Please review the document and share your feedback",
]


def connect():
    """Retry until the broker is reachable (it starts slower than this client)."""
    while True:
        try:
            return KafkaProducer(
                bootstrap_servers=BROKER,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
        except NoBrokersAvailable:
            print("producer: waiting for kafka...", flush=True)
            time.sleep(3)


def main():
    producer = connect()
    print(f"producer: connected, streaming to '{TOPIC}'", flush=True)
    i = 0
    while True:
        text = SAMPLES[i % len(SAMPLES)]
        producer.send(TOPIC, {"id": i, "text": text})
        producer.flush()
        print(f"producer: sent #{i}: {text}", flush=True)
        i += 1
        time.sleep(2)


if __name__ == "__main__":
    main()
