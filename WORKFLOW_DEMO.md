# MLOps Pipeline Demo Documentation

Complete demonstration guide for the Cats vs Dogs MLOps pipeline, covering all five modules (M1--M5). Every command below has been verified to work end-to-end.

---

## Pre-Recording Checklist

Run these before starting your screen recording:

```bash
# 1. Start MLflow UI (background)
mlflow ui --port 5000 &

# 2. Verify kind cluster is running
kind get clusters
# Expected: mlops-cluster

# 3. Verify pods are healthy
kubectl get pods
# Expected: 2/2 Running

# 4. Start port-forward to K8s service (background)
kubectl port-forward svc/cats-dogs-classifier-service 8080:80 &

# 5. Quick health check
curl -s http://localhost:8080/health
# Expected: {"status":"healthy","model_loaded":true}
```

Browser tabs to have ready:
- `http://localhost:5000` -- MLflow UI
- `http://localhost:9090` -- Prometheus (optional, if Docker Compose is running)

---

## M1: Model Development & Experiment Tracking (~60 sec)

### 1.1 Project Structure and Git/DVC Versioning

```bash
# Show recent Git history
git log --oneline -5
```

Expected output:

```
68eb272 Add detailed workflow explanation document
79867c4 Add comprehensive MLOps workflow documentation
b2ee181 Add project run status documentation
f781102 Update documentation with actual dataset information
d353b2b Add DVC configuration files and dataset setup documentation
```

```bash
# Show DVC is configured with local remote storage
ls .dvc/
cat .dvc/config
```

Expected output:

```
['remote "local"']
url = /tmp/dvc-storage
['core']
remote = local
```

```bash
# Show dataset is DVC-tracked (25,038 images, ~849 MB)
cat data/raw.dvc
```

Expected output:

```
outs:
- md5: d05fcaba3390134fe2790c29938f1965.dir
  size: 848922890
  nfiles: 25038
  hash: md5
  path: raw
```

### 1.2 Model Code (show in IDE)

- Open `src/models/cnn_model.py` -- a CNN with conv layers, batch norm, dropout, and fully connected head.
- Open `src/data/preprocessing.py` -- 224x224 resize, 80/10/10 train/val/test split, data augmentation.

### 1.3 Training & MLflow Experiment Tracking

Switch to browser at `http://localhost:5000`:

1. Click experiment **cats_dogs_classification**
2. Click the run to show:
   - **Parameters**: epochs, batch_size, learning_rate
   - **Metrics**: train/val accuracy, loss, precision, recall, F1 (click a metric to see the graph)
   - **Artifacts**: `confusion_matrix.png`, saved model (`.pt`)

---

## M2: Model Packaging & Containerization (~45 sec)

### 2.1 Inference Service Code (show in IDE)

- Open `src/inference/app.py` -- FastAPI app with `/health`, `/predict`, `/predict/batch`, and `/metrics` endpoints.
- Open `requirements.txt` -- version-pinned dependencies.

### 2.2 Docker Build & Run

```bash
# Show the image already exists (2.59 GB with model baked in)
docker images | grep cats-dogs
```

Expected output:

```
cats-dogs-classifier   latest   dbeddf8118aa   ...   2.59GB
```

```bash
# Run a container
docker run -d --name demo-container -p 8000:8000 cats-dogs-classifier:latest

# Test health endpoint
curl -s http://localhost:8000/health
```

Expected output:

```json
{
    "status": "healthy",
    "model_loaded": true
}
```

```bash
# Test prediction with a real cat image
curl -s -X POST -F "file=@data/raw/cats/1.jpg" http://localhost:8000/predict
```

Expected output:

```json
{
    "prediction": "cat",
    "class_probabilities": {
        "cat": 0.5969,
        "dog": 0.4031
    },
    "confidence": 0.5969
}
```

```bash
# Clean up
docker stop demo-container && docker rm demo-container
```

---

## M3: CI Pipeline (~30 sec)

### 3.1 Unit Tests

```bash
PYTHONPATH=. pytest tests/ -v
```

Expected output:

```
tests/test_inference.py::test_preprocess_image PASSED
tests/test_inference.py::test_preprocess_image_invalid PASSED
tests/test_inference.py::test_predict PASSED
tests/test_inference.py::test_model_creation PASSED
tests/test_inference.py::test_model_output_shape PASSED
tests/test_inference.py::test_model_classes PASSED
tests/test_inference.py::test_load_model PASSED
tests/test_preprocessing.py::test_load_image_paths PASSED
tests/test_preprocessing.py::test_load_image_paths_empty_dir PASSED
tests/test_preprocessing.py::test_preprocess_images PASSED
tests/test_preprocessing.py::test_preprocess_images_ratios PASSED
tests/test_preprocessing.py::test_get_data_transforms PASSED
tests/test_preprocessing.py::test_cats_dogs_dataset PASSED
tests/test_preprocessing.py::test_preprocess_images_no_data PASSED

======================== 14 passed in 3.60s ========================
```

### 3.2 CI Pipeline Config (show in IDE)

Open `.github/workflows/ci.yml` and narrate:
> "On push or PR, it checks out code, installs dependencies, runs pytest, builds Docker image, and pushes to GitHub Container Registry."

---

## M4: CD Pipeline & Deployment (~60 sec)

### 4.1 Kubernetes Manifests (show in IDE)

Open `deployment/kubernetes/deployment.yaml` and point out:
- Deployment with **2 replicas**
- Liveness and readiness **health probes**
- **Resource limits** (512Mi--1Gi memory, 250m--500m CPU)
- NodePort **Service**

### 4.2 CD Pipeline Config (show in IDE)

Open `.github/workflows/cd.yml` and narrate:
> "On push to main, it creates a kind cluster, builds the image, loads it into kind, deploys via kubectl, and runs smoke tests."

### 4.3 Live Kubernetes Deployment

```bash
kubectl get pods,svc,deployment
```

Expected output:

```
NAME                                        READY   STATUS    RESTARTS   AGE
pod/cats-dogs-classifier-755558f7f7-dbdb4   1/1     Running   0          69m
pod/cats-dogs-classifier-755558f7f7-vg2sz   1/1     Running   0          69m

NAME                                   TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/cats-dogs-classifier-service   NodePort    10.96.112.188   <none>        80:31477/TCP   69m

NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/cats-dogs-classifier   2/2     2            2           69m
```

```bash
# Test deployed service through K8s
curl -s http://localhost:8080/health
```

```json
{"status":"healthy","model_loaded":true}
```

```bash
curl -s -X POST -F "file=@data/raw/dogs/1.jpg" http://localhost:8080/predict
```

```json
{
    "prediction": "dog",
    "class_probabilities": {
        "cat": 0.1412,
        "dog": 0.8588
    },
    "confidence": 0.8588
}
```

### 4.4 Smoke Tests

```bash
bash scripts/smoke_tests.sh http://localhost:8080
```

Expected output:

```
Running smoke tests against: http://localhost:8080
Test 1: Health check endpoint
✓ Health check passed
✓ Health response format is correct

Test 2: Metrics endpoint
✓ Metrics endpoint accessible
✓ Metrics contain expected data

Test 3: Prediction endpoint
✓ Prediction endpoint accessible
✓ Prediction response format is correct
✓ Prediction includes confidence score

✓ All smoke tests passed!
```

---

## M5: Monitoring, Logs & Evaluation (~45 sec)

### 5.1 Prometheus Metrics

```bash
curl -s http://localhost:8080/metrics | grep -E "(inference_requests_total |inference_request_duration_seconds_count|predictions_total)"
```

Expected output:

```
inference_requests_total 34.0
inference_request_duration_seconds_count 34.0
predictions_total{class="dog"} 16.0
predictions_total{class="cat"} 18.0
```

Key metrics exposed:
| Metric | Description |
|--------|-------------|
| `inference_requests_total` | Total number of inference requests |
| `inference_request_duration_seconds` | Latency histogram (p50, p90, p99) |
| `predictions_total{class="cat/dog"}` | Prediction count by class |

### 5.2 Application Logs

```bash
kubectl logs deployment/cats-dogs-classifier --tail=10
```

Shows structured logs with prediction confidence and latency:

```
2026-02-11 08:25:20 - src.inference.app - INFO - Prediction: dog, Confidence: 0.9895, Latency: 0.7850s
2026-02-11 08:25:21 - src.inference.app - INFO - Prediction: dog, Confidence: 0.9991, Latency: 0.8955s
2026-02-11 08:25:21 - src.inference.app - INFO - Prediction: dog, Confidence: 0.9403, Latency: 0.6869s
```

### 5.3 Post-Deployment Model Evaluation

```bash
python scripts/evaluate_deployed_model.py --url http://localhost:8080 --num-samples 20
```

Expected output:

```
============================================================
Post-Deployment Model Performance Evaluation
============================================================
API URL: http://localhost:8080
Requested samples: 20

[1/4] Checking API health...
  Status: healthy

[2/4] Loading test images...
  Using 20 real images from data/raw

[3/4] Sending prediction requests...

[4/4] Computing metrics (20 successful predictions)...

============================================================
EVALUATION RESULTS
============================================================
  Total samples evaluated: 20
  Correct predictions:     13
  Accuracy:                0.6500
  Precision (weighted):    0.6515
  Recall (weighted):       0.6500
  F1 Score (weighted):     0.6508
  Average confidence:      0.6956

Confusion Matrix:
                Predicted Cat  Predicted Dog
  Actual Cat           6              4
  Actual Dog           3              7

============================================================
Evaluation complete using real images.
============================================================
```

---

## Closing (~15 sec)

> "This demonstrates the complete MLOps pipeline -- from model development with experiment tracking, through containerization, CI/CD with automated testing and deployment to Kubernetes, to post-deployment monitoring and performance evaluation."

---

## Timing Guide

| Section | Target Time |
|---------|-------------|
| M1: Model Dev + MLflow UI | ~60s |
| M2: Docker build + curl test | ~45s |
| M3: pytest + CI config | ~30s |
| M4: K8s deploy + smoke tests | ~60s |
| M5: Metrics + logs + eval script | ~45s |
| Closing | ~15s |
| **Total** | **~4 min 15 sec** |

---

## Architecture Overview

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│  Data (DVC)  │───▶│  Train (CNN)  │───▶│  MLflow Logs  │
│  25K images  │    │  PyTorch      │    │  Params/Metrics│
└─────────────┘    └──────┬───────┘    └──────────────┘
                          │
                   ┌──────▼───────┐
                   │  best_model.pt│
                   └──────┬───────┘
                          │
                   ┌──────▼───────┐    ┌──────────────┐
                   │  Dockerfile   │───▶│ Docker Image  │
                   │  FastAPI App  │    │  2.59 GB      │
                   └──────────────┘    └──────┬───────┘
                                              │
              ┌───────────────────────────────┘
              │
    ┌─────────▼─────────┐    ┌──────────────┐
    │  CI: GitHub Actions │───▶│ CD: kind K8s  │
    │  pytest (14 tests)  │    │ 2 replicas    │
    └─────────────────────┘    └──────┬───────┘
                                      │
                         ┌────────────▼────────────┐
                         │  Monitoring & Evaluation  │
                         │  Prometheus metrics       │
                         │  Structured logs          │
                         │  evaluate_deployed_model  │
                         └───────────────────────────┘
```

---

## Quick Reference Commands

```bash
# Start everything
mlflow ui --port 5000 &
kubectl port-forward svc/cats-dogs-classifier-service 8080:80 &

# Health check
curl http://localhost:8080/health

# Predict
curl -X POST -F "file=@data/raw/cats/1.jpg" http://localhost:8080/predict

# Metrics
curl http://localhost:8080/metrics | grep inference

# Logs
kubectl logs deployment/cats-dogs-classifier --tail=20

# Tests
PYTHONPATH=. pytest tests/ -v

# Smoke tests
bash scripts/smoke_tests.sh http://localhost:8080

# Post-deployment evaluation
python scripts/evaluate_deployed_model.py --url http://localhost:8080 --num-samples 20

# K8s status
kubectl get pods,svc,deployment
```
