# Setup Guide

This guide will help you set up and run the complete MLOps pipeline for Cats vs Dogs classification.

## Prerequisites

- Python 3.10+
- Docker and Docker Compose (for containerization)
- Git (for version control)
- DVC (for data versioning)
- Kubernetes cluster (optional, for K8s deployment)
- Kaggle account (for dataset download)

## Step 1: Clone and Initialize Repository

```bash
# Clone the repository
git clone <your-repo-url>
cd MLOps_A2

# Initialize Git (if not already initialized)
git init

# Initialize DVC
dvc init
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

```bash
# Train with default parameters
python src/training/train.py

# Or with custom parameters
python src/training/train.py \
    --raw_data_dir data/raw \
    --processed_data_dir data/processed \
    --model_save_dir models \
    --num_epochs 10 \
    --batch_size 32 \
    --learning_rate 0.001
```

The training script will:
- Preprocess images (resize to 224x224, split train/val/test)
- Train a CNN model
- Track experiments with MLflow
- Save the best model to `models/best_model.pt`

## Step 5: Test the Model Locally

```bash
# Run unit tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html
```

## Step 6: Build Docker Image

```bash
# Build the image
docker build -t cats-dogs-classifier:latest .

# Verify the image
docker images | grep cats-dogs-classifier
```

## Step 7: Run Inference Service Locally

```bash
# Run with Docker
docker run -p 8000:8000 \
    -v $(pwd)/models:/app/models:ro \
    cats-dogs-classifier:latest

# Or with Docker Compose
cd deployment/docker-compose
docker-compose up -d
```

## Step 8: Test the API

```bash
# Health check
curl http://localhost:8000/health

# Metrics
curl http://localhost:8000/metrics

# Prediction (requires an image file)
curl -X POST http://localhost:8000/predict \
    -F "file=@path/to/image.jpg"

# Run smoke tests
./scripts/smoke_tests.sh http://localhost:8000
```

## Step 9: CI/CD Setup

### GitHub Actions

The CI/CD pipelines are already configured in `.github/workflows/`:

- **CI Pipeline** (`.github/workflows/ci.yml`):
  - Runs on push/PR to main/develop
  - Runs unit tests
  - Builds and pushes Docker image to GitHub Container Registry

- **CD Pipeline** (`.github/workflows/cd.yml`):
  - Runs on push to main
  - Deploys to Kubernetes or Docker Compose
  - Runs smoke tests

### Configure GitHub Secrets (if needed)

For private registries or custom deployments, you may need to set up:
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`
- Kubernetes credentials

## Step 10: Deploy

### Option 1: Docker Compose (Local)

```bash
cd deployment/docker-compose
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Option 2: Kubernetes

```bash
# Apply Kubernetes manifests
kubectl apply -f deployment/kubernetes/deployment.yaml

# Check deployment status
kubectl get deployments
kubectl get services
kubectl get pods

# Port forward for local access
kubectl port-forward service/cats-dogs-classifier-service 8000:80
```

## Monitoring

### View Metrics

- Prometheus: http://localhost:9090 (if using Docker Compose)
- API Metrics: http://localhost:8000/metrics

### View Logs

```bash
# Docker
docker logs cats-dogs-classifier

# Docker Compose
docker-compose logs -f classifier-api

# Kubernetes
kubectl logs -f deployment/cats-dogs-classifier
```

## MLflow UI

View experiment tracking:

```bash
mlflow ui

# Access at http://localhost:5000
```

## Troubleshooting

### Model not found error

Ensure the model file exists:
```bash
ls -la models/best_model.pt
```

If missing, train the model first (Step 4).

### Port already in use

Change the port in:
- Docker: `-p 8001:8000`
- Docker Compose: Update `ports` in `docker-compose.yml`
- Kubernetes: Update `targetPort` in `deployment.yaml`

### DVC issues

If DVC cache is corrupted:
```bash
dvc cache dir
# Clear and re-add data
dvc remove data/raw.dvc
dvc add data/raw
```

## Next Steps

1. **Model Performance Tracking**: Collect real predictions and true labels
2. **Model Retraining**: Set up automated retraining pipeline
3. **A/B Testing**: Deploy multiple model versions
4. **Alerting**: Set up alerts for model drift or errors

## Support

For issues or questions, please refer to the main README.md or open an issue in the repository.

