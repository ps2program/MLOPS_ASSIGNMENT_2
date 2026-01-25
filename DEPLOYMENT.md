# Deployment Guide

This document describes the deployment options and configurations for the Cats vs Dogs Classifier.

## Deployment Options

### 1. Docker Compose (Recommended for Local/Development)

Best for:
- Local development
- Single-machine deployments
- Quick testing

**Deploy:**
```bash
cd deployment/docker-compose
docker-compose up -d
```

**Access:**
- API: http://localhost:8000
- Prometheus: http://localhost:9090

**Stop:**
```bash
docker-compose down
```

### 2. Kubernetes

Best for:
- Production environments
- Scalability requirements
- Multi-node clusters

**Prerequisites:**
- Kubernetes cluster (kind, minikube, or cloud provider)
- kubectl configured

**Deploy:**
```bash
# Ensure model is available in cluster
kubectl create secret generic model-secret --from-file=models/best_model.pt

# Or use PersistentVolume
kubectl apply -f deployment/kubernetes/deployment.yaml
```

**Access:**
```bash
# Get service endpoint
kubectl get service cats-dogs-classifier-service

# Port forward for local access
kubectl port-forward service/cats-dogs-classifier-service 8000:80
```

### 3. Docker (Standalone)

Best for:
- Simple deployments
- Single container

**Deploy:**
```bash
docker run -d \
  --name cats-dogs-classifier \
  -p 8000:8000 \
  -v $(pwd)/models:/app/models:ro \
  cats-dogs-classifier:latest
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_PATH` | `models/best_model.pt` | Path to model file |
| `PYTHONUNBUFFERED` | `1` | Disable Python output buffering |

### Resource Requirements

**Minimum:**
- CPU: 250m
- Memory: 512Mi

**Recommended:**
- CPU: 500m
- Memory: 1Gi

## Health Checks

The service includes health checks at `/health`:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## Monitoring

### Prometheus Metrics

Metrics are available at `/metrics`:

- `inference_requests_total`: Total requests
- `inference_request_duration_seconds`: Request latency
- `predictions_total{class="cat|dog"}`: Prediction counts

### Logging

Logs include:
- Request/response summaries (excluding sensitive data)
- Error messages
- Performance metrics

View logs:
```bash
# Docker
docker logs cats-dogs-classifier

# Kubernetes
kubectl logs -f deployment/cats-dogs-classifier
```

## Scaling

### Docker Compose

Edit `docker-compose.yml`:
```yaml
services:
  classifier-api:
    deploy:
      replicas: 3
```

### Kubernetes

```bash
kubectl scale deployment cats-dogs-classifier --replicas=3
```

## Rolling Updates

### Kubernetes

```bash
# Update image
kubectl set image deployment/cats-dogs-classifier \
  classifier-api=cats-dogs-classifier:v2.0

# Monitor rollout
kubectl rollout status deployment/cats-dogs-classifier
```

## Smoke Tests

After deployment, run smoke tests:

```bash
./scripts/smoke_tests.sh http://your-service-url:8000
```

Tests verify:
- Health endpoint
- Metrics endpoint
- Prediction endpoint

## Troubleshooting

### Service not responding

1. Check if container is running:
   ```bash
   docker ps
   # or
   kubectl get pods
   ```

2. Check logs:
   ```bash
   docker logs cats-dogs-classifier
   # or
   kubectl logs deployment/cats-dogs-classifier
   ```

3. Check health endpoint:
   ```bash
   curl http://localhost:8000/health
   ```

### Model loading errors

1. Verify model file exists:
   ```bash
   ls -la models/best_model.pt
   ```

2. Check volume mounts:
   - Docker: `-v $(pwd)/models:/app/models:ro`
   - Kubernetes: Check PVC and volume mounts

### High latency

1. Check resource limits
2. Monitor metrics: `curl http://localhost:8000/metrics`
3. Consider scaling horizontally

## Security Considerations

1. **API Authentication**: Add authentication for production
2. **HTTPS**: Use TLS/SSL for production deployments
3. **Resource Limits**: Set appropriate CPU/memory limits
4. **Network Policies**: Restrict network access in Kubernetes
5. **Secrets Management**: Use Kubernetes secrets or external secret managers

## Production Checklist

- [ ] Model file is available and accessible
- [ ] Health checks are configured
- [ ] Monitoring is set up (Prometheus/Grafana)
- [ ] Logging is configured
- [ ] Resource limits are set
- [ ] Smoke tests pass
- [ ] HTTPS/TLS is configured
- [ ] Authentication is enabled
- [ ] Backup strategy for models
- [ ] Disaster recovery plan

