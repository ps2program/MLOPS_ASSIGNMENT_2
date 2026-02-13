# Prometheus Setup for Kubernetes

## Deployment Status

Prometheus has been deployed to your Kubernetes cluster.

## Quick Access

### 1. Check Prometheus Status

```bash
# Check if Prometheus pod is running
kubectl get pods -l app=prometheus

# Check Prometheus service
kubectl get svc prometheus-service

# View Prometheus logs
kubectl logs -l app=prometheus --tail=50
```

### 2. Access Prometheus UI

**Option A: Port Forward (Recommended)**
```bash
kubectl port-forward svc/prometheus-service 9090:9090
```
Then open: http://localhost:9090

**Option B: NodePort**
```bash
# Get the NodePort
kubectl get svc prometheus-service

# Access via NodePort (shown in PORT(S) column, e.g., 9090:31487/TCP)
# Use the external port (31487) on your cluster node IP
```

### 3. Verify Metrics Collection

In Prometheus UI:
1. Go to **Status → Targets**
2. Verify `classifier-api` target is **UP**
3. Go to **Graph** tab
4. Try queries:
   - `inference_requests_total`
   - `inference_request_duration_seconds`
   - `predictions_total`

### 4. Test Metrics Endpoint Directly

```bash
# Port-forward to classifier service
kubectl port-forward svc/cats-dogs-classifier-service 8080:80

# Check metrics
curl http://localhost:8080/metrics | grep inference
```

## Configuration

Prometheus is configured to scrape metrics from:
- **Target:** `cats-dogs-classifier-service:80`
- **Path:** `/metrics`
- **Interval:** 15 seconds

Configuration is stored in ConfigMap: `prometheus-config`

## Troubleshooting

### Prometheus pod not starting
```bash
# Check pod events
kubectl describe pod -l app=prometheus

# Check logs
kubectl logs -l app=prometheus
```

### Metrics not appearing
1. Verify classifier service is running:
   ```bash
   kubectl get pods -l app=cats-dogs-classifier
   ```

2. Test metrics endpoint:
   ```bash
   kubectl port-forward svc/cats-dogs-classifier-service 8080:80
   curl http://localhost:8080/metrics
   ```

3. Check Prometheus targets:
   - Open Prometheus UI → Status → Targets
   - Verify target is UP

### Configuration Issues
```bash
# View current config
kubectl get configmap prometheus-config -o yaml

# Update config (edit the file, then apply)
kubectl apply -f deployment/kubernetes/prometheus-config.yaml
```

## Cleanup

To remove Prometheus:
```bash
kubectl delete -f deployment/kubernetes/prometheus-deployment.yaml
kubectl delete -f deployment/kubernetes/prometheus-config.yaml
```
