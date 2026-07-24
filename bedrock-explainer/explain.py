"""Use AWS Bedrock to explain a spam/ham prediction in plain language.

This adds a GenAI layer on top of the classifier: after the model labels a
message, a Bedrock-hosted LLM explains *why* in a sentence a non-technical user
can understand.

REQUIRES real AWS credentials with Bedrock access and the model enabled in your
account/region. Without them this script cannot run — see README.md.
"""
import json
import os

import boto3

REGION = os.environ.get("AWS_REGION", "us-east-1")
MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")


def explain(text: str, label: str, confidence: float) -> str:
    client = boto3.client("bedrock-runtime", region_name=REGION)
    prompt = (
        f"A spam classifier labeled this message '{label}' with "
        f"{confidence:.0%} confidence:\n\n\"{text}\"\n\n"
        "In two sentences, explain to a non-technical user why it may have been "
        "classified this way."
    )
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 200,
        "messages": [{"role": "user", "content": prompt}],
    }
    resp = client.invoke_model(modelId=MODEL_ID, body=json.dumps(body))
    payload = json.loads(resp["body"].read())
    return payload["content"][0]["text"]


if __name__ == "__main__":
    sample = "Congratulations you won a free prize claim now send your bank details"
    print(explain(sample, "spam", 0.68))
