# kubernetes/ — Container orchestration (Kubernetes)

Deploys the containerized spam-classifier API to Kubernetes with 2 replicas,
readiness/liveness probes, resource limits, and a Service to reach it.

## Prerequisites
Enable a local cluster:
- **Docker Desktop** → Settings → Kubernetes → *Enable Kubernetes* (easiest), or
- install `kind` / `minikube`.

Confirm it's up:
```bash
kubectl cluster-info
```

## Run it
```bash
# 1. build the image so the local cluster can use it
docker build -t mlops-serving:latest ../serving

# (kind only) load the image into the cluster:
# kind load docker-image mlops-serving:latest

# 2. deploy
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# 3. watch pods become ready (takes ~1–2 min due to slow first import)
kubectl get pods -l app=spam-api -w

# 4. reach the API
kubectl port-forward service/spam-api 8000:8000
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"claim your free prize now"}'

# 5. clean up
kubectl delete -f service.yaml -f deployment.yaml
```

## What this demonstrates
- Deployments, ReplicaSets, Pods, and Services.
- Readiness vs. liveness probes (and why the initial delay is generous here).
- Resource requests/limits and `imagePullPolicy: IfNotPresent` for local images.

## Be able to explain (interview-ready)
- The difference between a Deployment, a ReplicaSet, and a Pod.
- Readiness probe (route traffic?) vs. liveness probe (restart?).
- What a Service does and how `NodePort` differs from `ClusterIP`/`LoadBalancer`.
- Why `port-forward` is used for local access.
