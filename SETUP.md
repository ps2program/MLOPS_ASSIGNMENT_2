# Setup Guide

This guide will help you set up and run the complete MLOps pipeline for Cats vs Dogs classification.

## Prerequisites

- Python 3.10+ (tested with 3.10 and 3.13)
- Docker Desktop (for containerization)
- Git (for version control)
- [kind](https://kind.sigs.k8s.io/) (for local Kubernetes deployment)
- Kaggle account (for dataset download)

## Step 1: Clone and Initialize Repository

```bash
# Clone the repository
git clone https://github.com/ps2program/MLOPS_ASSIGNMENT_2.git
cd MLOPS_ASSIGNMENT_2

# DVC is already initialized in this repo
```

## Step 2: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt
```

## Step 3: Download Dataset

### Option 1: Using Kaggle CLI (Recommended)

**Dataset:** [bhavikjikadara/dog-and-cat-classification-dataset](https://www.kaggle.com/datasets/bhavikjikadara/dog-and-cat-classification-dataset)
- **Total Images:** 25,038 (12,519 cats, 12,519 dogs)
- **Size:** ~775MB

1. Download your Kaggle API credentials from https://www.kaggle.com/settings
2. Place `kaggle.json` in `~/.kaggle/`
3. Run the download script:

```bash
# Update the script to use the correct dataset, or run directly:
kaggle datasets download -d bhavikjikadara/dog-and-cat-classification-dataset -p data/raw --unzip

# Organize the dataset (if needed)
# The script will handle organization automatically
```

### Option 2: Manual Download

1. Download from: https://www.kaggle.com/datasets/bhavikjikadara/dog-and-cat-classification-dataset
2. Extract and organize into:
   ```
   data/raw/
     cats/
       *.jpg  (12,519 images)
     dogs/
       *.jpg  (12,519 images)
   ```

### Track Data with DVC

```bash
# Add data to DVC
dvc add data/raw

# Commit DVC files
git add data/raw.dvc .gitignore
git commit -m "Add dataset with DVC"
```

## Step 4: Train the Model

> **Important:** You must set `PYTHONPATH` to the project root so that `src` is importable.

```bash
# Train with default parameters
PYTHONPATH=. python src/training/train.py

# Or with custom parameters
PYTHONPATH=. python src/training/train.py \
    --raw_data_dir data/raw \
    --processed_data_dir data/processed \
    --model_save_dir models \
    --num_epochs 10 \
    --batch_size 32 \
    --learning_rate 0.001
```

The training script will:
- Preprocess images (resize to 224x224, split 80/10/10 train/val/test)
- Apply data augmentation (random horizontal flip, rotation, color jitter)
- Train a CNN model with batch normalization and dropout
- Track experiments with MLflow (parameters, metrics, confusion matrix)
- Save the best model to `models/best_model.pt`

### View Training Results in MLflow

```bash
mlflow ui --port 5000
# Open http://localhost:5000
```

Click the **cats_dogs_classification** experiment, then click the run to see:
- **Parameters:** epochs, batch_size, learning_rate
- **Metrics:** train/val accuracy, loss, precision, recall, F1
- **Artifacts:** confusion_matrix.png, saved model

## Step 5: Run Tests

```bash
# Run unit tests (14 tests)
PYTHONPATH=. pytest tests/ -v

# Run with coverage report
PYTHONPATH=. pytest tests/ -v --cov=src --cov-report=html
```

## Step 6: Build Docker Image

The model (`models/best_model.pt`) is baked into the image during build.

```bash
# Build the image (use --load if Docker sign-in enforcement is enabled)
docker build --load -t cats-dogs-classifier:latest .

# Verify the image
docker images | grep cats-dogs-classifier
```

## Step 7: Run Inference Service Locally

```bash
# Run with Docker (model is already inside the image)
docker run -d --name cats-dogs-api -p 8000:8000 cats-dogs-classifier:latest

# Or with Docker Compose (includes Prometheus)
cd deployment/docker-compose
docker compose up -d
cd ../..
```

## Step 8: Test the API

```bash
# Health check
curl http://localhost:8000/health
# Expected: {"status":"healthy","model_loaded":true}

# Prediction with a cat image
curl -X POST -F "file=@data/raw/cats/cat_000.jpg" http://localhost:8000/predict

# Prediction with a dog image
curl -X POST -F "file=@data/raw/dogs/dog_000.jpg" http://localhost:8000/predict

# Prometheus metrics
curl http://localhost:8000/metrics | grep inference

# Run smoke tests
bash scripts/smoke_tests.sh http://localhost:8000

# Clean up
docker stop cats-dogs-api && docker rm cats-dogs-api
```

## Step 9: CI/CD Setup

### GitHub Actions

The CI/CD pipelines are already configured in `.github/workflows/`:

- **CI Pipeline** (`.github/workflows/ci.yml`):
  - Triggers on push/PR to main/develop
  - Runs unit tests with pytest
  - Builds Docker image
  - Pushes to GitHub Container Registry

- **CD Pipeline** (`.github/workflows/cd.yml`):
  - Triggers on push to main
  - Provisions a kind cluster
  - Builds and loads the Docker image into kind
  - Deploys to Kubernetes via `kubectl apply`
  - Runs smoke tests
  - Cleans up the cluster

No additional secrets are required -- the CD pipeline uses kind for local-style deployment within the GitHub Actions runner.

## Step 10: Deploy to Local Kubernetes (kind)

### Option 1: Docker Compose (Local)

```bash
cd deployment/docker-compose
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f classifier-api

# Tear down
docker compose down
cd ../..
```

### Option 2: Kubernetes with kind (Recommended)

```bash
# Install kind (if not already installed)
# macOS:
brew install kind
# Linux:
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind && sudo mv ./kind /usr/local/bin/kind

# Create a cluster
kind create cluster --name mlops-cluster --wait 60s

# Build and load the Docker image into kind
docker build --load -t cats-dogs-classifier:latest .
kind load docker-image cats-dogs-classifier:latest --name mlops-cluster

# Deploy
kubectl apply -f deployment/kubernetes/deployment.yaml

# Wait for pods to be ready
kubectl rollout status deployment/cats-dogs-classifier --timeout=120s

# Check status (expect 2/2 pods Running)
kubectl get pods,svc,deployment

# Port-forward to access the service
kubectl port-forward svc/cats-dogs-classifier-service 8080:80 &

# Test health
curl http://localhost:8080/health

# Test prediction
curl -X POST -F "file=@data/raw/cats/cat_000.jpg" http://localhost:8080/predict

# Run smoke tests
bash scripts/smoke_tests.sh http://localhost:8080
```

### Tear Down Kubernetes

```bash
# Delete the cluster when done
kind delete cluster --name mlops-cluster
```

## Step 11: Monitoring & Evaluation

### Prometheus Metrics

The API exposes Prometheus-compatible metrics at `/metrics`:

```bash
# View key metrics
curl http://localhost:8080/metrics | grep -E "(inference_requests_total |inference_request_duration|predictions_total)"
```

Key metrics:
| Metric | Description |
|--------|-------------|
| `inference_requests_total` | Total number of inference requests |
| `inference_request_duration_seconds` | Latency histogram (p50, p90, p99) |
| `predictions_total{class="cat/dog"}` | Prediction count by class |

#### Prometheus Setup

**Docker Compose:**
Prometheus UI is automatically available at `http://localhost:9090` when using Docker Compose.

**Kubernetes:**
To deploy Prometheus with Kubernetes:

```bash
# Deploy Prometheus configuration and service
kubectl apply -f deployment/kubernetes/prometheus-config.yaml
kubectl apply -f deployment/kubernetes/prometheus-deployment.yaml

# Port-forward to access Prometheus UI
kubectl port-forward svc/prometheus-service 9090:9090

# Access Prometheus UI at http://localhost:9090
```

Prometheus will automatically scrape metrics from your classifier service pods.

#### Grafana Setup

**Kubernetes:**
To deploy Grafana for visualization:

```bash
# Deploy Grafana configuration and service
kubectl apply -f deployment/kubernetes/grafana-config.yaml
kubectl apply -f deployment/kubernetes/grafana-datasource.yaml
kubectl apply -f deployment/kubernetes/grafana-deployment.yaml

# Port-forward to access Grafana UI
kubectl port-forward svc/grafana-service 3000:3000

# Access Grafana UI at http://localhost:3000
# Login: admin / admin
```

Grafana is pre-configured to connect to Prometheus. You can create dashboards to visualize:
- Total inference requests
- Request rate over time
- Latency percentiles (p50, p90, p99)
- Prediction distribution by class

See `deployment/kubernetes/GRAFANA_SETUP.md` for detailed instructions.

### Application Logs

```bash
# Docker
docker logs cats-dogs-api

# Docker Compose
docker compose logs -f classifier-api

# Kubernetes
kubectl logs deployment/cats-dogs-classifier --tail=20
```

Logs include structured prediction entries with confidence and latency:

```
2026-02-11 08:25:20 - src.inference.app - INFO - Prediction: dog, Confidence: 0.9895, Latency: 0.7850s
```

### Post-Deployment Model Evaluation

Run the evaluation script to assess model performance on real images:

```bash
python scripts/evaluate_deployed_model.py --url http://localhost:8080 --num-samples 20
```

This sends images with known labels (from `data/raw/cats/` and `data/raw/dogs/`) to the deployed API and reports accuracy, precision, recall, F1 score, and a confusion matrix. If real images are not available, it falls back to simulated test images.

### MLflow UI

View experiment tracking:

```bash
mlflow ui --port 5000
# Open http://localhost:5000
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'src'`

You need `PYTHONPATH` set to the project root:

```bash
PYTHONPATH=. python src/training/train.py
PYTHONPATH=. pytest tests/ -v
```

### Model not found error

Ensure the model file exists:

```bash
ls -la models/best_model.pt
```

If missing, train the model first (Step 4).

### Docker sign-in enforcement error

If `docker build` fails with a sign-in error, use the `--load` flag:

```bash
docker build --load -t cats-dogs-classifier:latest .
```

### Port already in use

Change the host port:
- Docker: `-p 8001:8000`
- Docker Compose: Update `ports` in `docker-compose.yml`
- Kubernetes port-forward: `kubectl port-forward svc/cats-dogs-classifier-service 8081:80`

### DVC issues

If DVC cache is corrupted:

```bash
dvc cache dir
# Clear and re-add data
dvc remove data/raw.dvc
dvc add data/raw
```

### kind cluster issues

```bash
# Check if cluster exists
kind get clusters

# Delete and recreate if broken
kind delete cluster --name mlops-cluster
kind create cluster --name mlops-cluster --wait 60s
```

## Project Structure

```
MLOPS_ASSIGNMENT_2/
├── src/
│   ├── models/cnn_model.py          # CNN architecture
│   ├── data/preprocessing.py        # Data loading, splits, augmentation
│   ├── training/train.py            # Training with MLflow tracking
│   └── inference/app.py             # FastAPI inference service
├── tests/
│   ├── test_inference.py            # Inference unit tests (7 tests)
│   └── test_preprocessing.py        # Preprocessing unit tests (7 tests)
├── deployment/
│   ├── kubernetes/deployment.yaml   # K8s Deployment + Service
│   └── docker-compose/
│       ├── docker-compose.yml       # API + Prometheus
│       └── prometheus.yml           # Prometheus config
├── scripts/
│   ├── smoke_tests.sh               # Post-deployment smoke tests
│   └── evaluate_deployed_model.py   # Post-deployment model evaluation
├── .github/workflows/
│   ├── ci.yml                       # CI pipeline (test + build)
│   └── cd.yml                       # CD pipeline (deploy to kind)
├── data/
│   ├── raw/                         # Cat/dog images (DVC-tracked)
│   └── raw.dvc                      # DVC tracking file
├── models/
│   └── best_model.pt                # Trained model (~100MB)
├── mlruns/                          # MLflow experiment logs
├── Dockerfile                       # Multi-stage Docker build
├── requirements.txt                 # Python dependencies
└── .dvc/config                      # DVC remote config
```

## Support

For issues or questions, please open an issue in the repository.

