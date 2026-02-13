# Grafana Setup for Kubernetes

## Deployment Status

Grafana has been deployed to your Kubernetes cluster and is configured to connect to Prometheus.

## Quick Access

### 1. Check Grafana Status

```bash
# Check if Grafana pod is running
kubectl get pods -l app=grafana

# Check Grafana service
kubectl get svc grafana-service

# View Grafana logs
kubectl logs -l app=grafana --tail=50
```

### 2. Access Grafana UI

**Option A: Port Forward (Recommended)**
```bash
kubectl port-forward svc/grafana-service 3000:3000
```
Then open: http://localhost:3000

**Option B: NodePort**
```bash
# Get the NodePort
kubectl get svc grafana-service

# Access via NodePort (shown in PORT(S) column, e.g., 3000:31920/TCP)
# Use the external port (31920) on your cluster node IP
```

### 3. Login Credentials

- **Username:** `admin`
- **Password:** `admin`

⚠️ **Important:** Change the default password after first login in production!

### 4. Verify Prometheus Connection

1. Login to Grafana
2. Go to **Configuration → Data Sources**
3. Verify **Prometheus** datasource is configured and shows **"Data source is working"**
4. The datasource should point to: `http://prometheus-service:9090`

## Using Grafana Dashboards

### Pre-configured Dashboard

A custom MLOps dashboard is available (if configured):
- Go to **Dashboards → Browse**
- Look for **"MLOps - Cats vs Dogs Classifier"**

### Create Your Own Dashboard

1. Click **"+" → Create Dashboard**
2. Add a new panel
3. Select **Prometheus** as data source
4. Use these queries:

#### Key Metrics to Visualize

**Total Requests:**
```
inference_requests_total
```

**Request Rate:**
```
rate(inference_requests_total[5m])
```

**Latency Percentiles:**
```
# p50
histogram_quantile(0.50, inference_request_duration_seconds_bucket)

# p90
histogram_quantile(0.90, inference_request_duration_seconds_bucket)

# p99
histogram_quantile(0.99, inference_request_duration_seconds_bucket)
```

**Average Latency:**
```
rate(inference_request_duration_seconds_sum[5m]) / rate(inference_request_duration_seconds_count[5m])
```

**Predictions by Class:**
```
predictions_total{class="cat"}
predictions_total{class="dog"}
```

**Prediction Distribution:**
```
predictions_total
```

### Example Dashboard Panels

1. **Stat Panel** - Total Requests
   - Query: `inference_requests_total`
   - Visualization: Stat

2. **Graph Panel** - Request Rate Over Time
   - Query: `rate(inference_requests_total[5m])`
   - Visualization: Time series

3. **Graph Panel** - Latency Percentiles
   - Queries:
     - `histogram_quantile(0.50, inference_request_duration_seconds_bucket)` (p50)
     - `histogram_quantile(0.90, inference_request_duration_seconds_bucket)` (p90)
     - `histogram_quantile(0.99, inference_request_duration_seconds_bucket)` (p99)
   - Visualization: Time series

4. **Pie Chart** - Predictions by Class
   - Query: `predictions_total`
   - Visualization: Pie chart

5. **Bar Gauge** - Prediction Counts
   - Query: `predictions_total`
   - Visualization: Bar gauge

## Quick Test

```bash
# 1. Port-forward Grafana
kubectl port-forward svc/grafana-service 3000:3000 &

# 2. Port-forward classifier service
kubectl port-forward svc/cats-dogs-classifier-service 8080:80 &

# 3. Make some predictions to generate metrics
curl -X POST -F "file=@data/raw/cats/cat_000.jpg" http://localhost:8080/predict
curl -X POST -F "file=@data/raw/dogs/dog_000.jpg" http://localhost:8080/predict

# 4. Open Grafana UI
# Open http://localhost:3000
# Login: admin/admin
# Go to Explore → Select Prometheus → Query: inference_requests_total
```

## Configuration

### Datasource Configuration

The Prometheus datasource is automatically configured via ConfigMap:
- **Name:** Prometheus
- **URL:** `http://prometheus-service:9090`
- **Access:** Proxy
- **Default:** Yes

Configuration file: `grafana-datasource.yaml`

### Grafana Configuration

Main configuration is in ConfigMap: `grafana-config`
- Admin user: `admin`
- Admin password: `admin` (change in production!)

## Troubleshooting

### Grafana pod not starting
```bash
# Check pod events
kubectl describe pod -l app=grafana

# Check logs
kubectl logs -l app=grafana
```

### Cannot connect to Prometheus
1. Verify Prometheus is running:
   ```bash
   kubectl get pods -l app=prometheus
   ```

2. Verify Prometheus service:
   ```bash
   kubectl get svc prometheus-service
   ```

3. Test connectivity from Grafana pod:
   ```bash
   kubectl exec -it $(kubectl get pod -l app=grafana -o jsonpath='{.items[0].metadata.name}') -- wget -O- http://prometheus-service:9090/api/v1/status/config
   ```

### Dashboard not showing data
1. Verify Prometheus has metrics:
   ```bash
   kubectl port-forward svc/prometheus-service 9090:9090
   curl http://localhost:9090/api/v1/query?query=inference_requests_total
   ```

2. Check time range in Grafana (top right)
3. Verify query syntax in Grafana Explore

### Reset Grafana Admin Password

If you need to reset the password:
```bash
# Edit the deployment
kubectl edit deployment grafana

# Update GF_SECURITY_ADMIN_PASSWORD environment variable
# Or delete the pod to recreate with new password
kubectl delete pod -l app=grafana
```

## Cleanup

To remove Grafana:
```bash
kubectl delete -f deployment/kubernetes/grafana-deployment.yaml
kubectl delete -f deployment/kubernetes/grafana-config.yaml
kubectl delete -f deployment/kubernetes/grafana-datasource.yaml
kubectl delete -f deployment/kubernetes/grafana-dashboard-provisioning.yaml
kubectl delete -f deployment/kubernetes/grafana-dashboard.yaml
```

## Production Recommendations

1. **Change Default Password:** Update admin password immediately
2. **Persistent Storage:** Use PersistentVolume instead of emptyDir for data persistence
3. **HTTPS:** Configure TLS/SSL for production
4. **Authentication:** Set up OAuth or LDAP authentication
5. **Backup:** Regular backups of Grafana dashboards and datasources
6. **Resource Limits:** Adjust based on usage patterns
7. **Monitoring:** Monitor Grafana itself with Prometheus

## Files Created

- `grafana-config.yaml` - Main Grafana configuration
- `grafana-datasource.yaml` - Prometheus datasource configuration
- `grafana-deployment.yaml` - Deployment and Service
- `grafana-dashboard.yaml` - Custom dashboard (optional)
- `grafana-dashboard-provisioning.yaml` - Dashboard provisioning config
