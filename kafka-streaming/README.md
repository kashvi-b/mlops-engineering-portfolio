# kafka-streaming/ — Real-time inference pipeline (Kafka)

A streaming pipeline that classifies messages as they arrive:

```
producer ──► [messages topic] ──► consumer ──► POST /predict ──► [predictions topic]
                                     │                              │
                                 (Kafka)                     spam-api (serving)
```

- **producer** publishes a stream of messages to the `messages` topic.
- **consumer** reads each message, calls the serving API for a prediction, and
  publishes the result to the `predictions` topic.
- **kafka** runs as a single-node broker in **KRaft mode** (no ZooKeeper).

## What this demonstrates
- Running Kafka in Docker (KRaft mode) and configuring listeners/advertised listeners.
- Producer/consumer clients with consumer groups and offset management.
- Decoupling a streaming layer from a model service so they scale independently.

## Run it
```bash
# from this folder
docker compose up --build

# in another terminal, watch predictions flowing:
docker compose logs -f consumer
```
The first predictions take ~1–2 minutes to appear (Kafka boot + the model API's
slow first import). Stop everything with:
```bash
docker compose down
```

## Be able to explain (interview-ready)
- What KRaft mode is and why it replaces ZooKeeper.
- The difference between `KAFKA_LISTENERS` and `KAFKA_ADVERTISED_LISTENERS`, and
  why containers must advertise `kafka:9092` (not `localhost`).
- What a consumer group and `auto_offset_reset=earliest` do.
- Why inference lives in a separate service instead of inside the consumer.
