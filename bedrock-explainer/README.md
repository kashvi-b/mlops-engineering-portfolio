# bedrock-explainer/ — LLM explanations with AWS Bedrock

Adds a GenAI layer to the classifier: after the model labels a message, a
Bedrock-hosted LLM explains *why* in plain language. This ties the project's
Explainable-AI theme to a managed LLM.

> **Status: requires real AWS Bedrock access to run.**
> This module goes on the résumé only once you have actually run it against
> Bedrock. Until then it is intentionally left unverified — no faking.

## Prerequisites
- An AWS account with **Amazon Bedrock** enabled.
- **Model access** granted for the chosen model (e.g. Anthropic Claude 3 Haiku)
  in the AWS Bedrock console, in your region.
- Credentials configured locally (`aws configure`, an SSO profile, or env vars).
  Never hard-code keys.

## Run it
```bash
pip install -r requirements.txt
export AWS_REGION=us-east-1
export BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
python explain.py
```

## What this demonstrates (once run)
- Calling a managed LLM via the AWS SDK (`boto3` / `bedrock-runtime`).
- Structuring a request/response for a hosted foundation model.
- Composing classical ML (the classifier) with GenAI (the explainer).

## Be able to explain (interview-ready)
- What Amazon Bedrock is and how it differs from self-hosting a model.
- Why credentials come from the environment, never the code.
- Where an LLM adds value over the classifier (explanation, not classification).
