# MLOps Portfolio — Serving, Streaming & Deploying an ML Model

An end-to-end, container-first project that takes a single machine-learning model
(a TF-IDF + Logistic Regression **spam classifier**) and operates it five ways:
serving it, streaming through it, provisioning infrastructure for it, deploying it,
and explaining its predictions with an LLM.

Everything runs in Docker, so the project is reproducible on any machine with Docker
installed — no local Python/Java version juggling required.

## Modules

| Module | Focus | Runs with |
|--------|-------|-----------|
| [`serving/`](serving/) | Model API in a container | Docker + FastAPI |
| [`kafka-streaming/`](kafka-streaming/) | Real-time inference pipeline | Kafka (Docker) + Python |
| [`terraform-localstack/`](terraform-localstack/) | Infrastructure as Code | Terraform + LocalStack |
| [`kubernetes/`](kubernetes/) | Container orchestration | kubectl + local cluster |
| [`bedrock-explainer/`](bedrock-explainer/) | LLM explains predictions | AWS Bedrock |

## Architecture

```
                       ┌─────────────────────┐
   messages ──Kafka──► │  spam-classifier    │ ──► predictions ──Kafka──►
                       │  (FastAPI, Docker)   │
                       └──────────┬──────────┘
                                  │ deployed by
                        ┌─────────┴─────────┐
                        │  Kubernetes        │  infra by  ┌────────────┐
                        │  Deployment/Service│ ◄───────── │ Terraform  │
                        └────────────────────┘            └────────────┘
```

## Prerequisites
- Docker Desktop (running)
- Terraform CLI
- kubectl + a local cluster (Docker Desktop's built-in Kubernetes, or kind/minikube)
- (Optional) AWS account with Bedrock model access — for `bedrock-explainer/`

## Quickstart
Each module has its own README with exact commands. Start with [`serving/`](serving/).

## Status
- ✅ serving · kafka-streaming · terraform-localstack · kubernetes — runnable locally
- ⏳ bedrock-explainer — requires AWS Bedrock access
