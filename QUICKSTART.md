# Quick Start Guide

Get up and running with the Cats vs Dogs Classifier in 5 minutes!

## Prerequisites Check

```bash
# Check Python version (3.10+)
python --version

# Check Docker
docker --version

# Check Git
git --version
```

## Step 1: Setup (2 minutes)

```bash
# Clone and navigate
cd MLOps_A2

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize DVC
dvc init
```

## Step 2: Download Dataset (1 minute)

**Dataset:** [bhavikjikadara/dog-and-cat-classification-dataset](https://www.kaggle.com/datasets/bhavikjikadara/dog-and-cat-classification-dataset)
- 25,038 images (12,519 cats, 12,519 dogs)

**Option A: Using Kaggle CLI (Recommended)**
```bash
# Place kaggle.json in ~/.kaggle/
kaggle datasets download -d bhavikjikadara/dog-and-cat-classification-dataset -p data/raw --unzip

# Organize images (if needed)
find data/raw/PetImages/Cat -type f -name "*.jpg" -exec mv {} data/raw/cats/ \;
find data/raw/PetImages/Dog -type f -name "*.jpg" -exec mv {} data/raw/dogs/ \;

# Track with DVC
dvc add data/raw
```

**Option B: Manual Download**
1. Download from: https://www.kaggle.com/datasets/bhavikjikadara/dog-and-cat-classification-dataset
2. Extract to `data/raw/` with `cats/` and `dogs/` subdirectories
3. Run: `dvc add data/raw`

## Step 3: Train Model (30-60 minutes for full dataset)

```bash
# Quick training (few epochs for testing)
PYTHONPATH=. python src/training/train.py --num_epochs 5 --batch_size 16

# Full training with full dataset (recommended)
PYTHONPATH=. python src/training/train.py \
    --raw_data_dir data/raw \
    --processed_data_dir data/processed \
    --model_save_dir models \
    --num_epochs 10 \
    --batch_size 32
```

## Step 4: Test Locally (30 seconds)

```bash
# Run tests
pytest tests/ -v

# Build Docker image
docker build -t cats-dogs-classifier .

# Run container
docker run -p 8000:8000 \
    -v $(pwd)/models:/app/models:ro \
    cats-dogs-classifier
```

## Step 5: Test API (30 seconds)

```bash
# In another terminal

# Health check
curl http://localhost:8000/health

# Prediction (replace with actual image path)
curl -X POST http://localhost:8000/predict \
    -F "file=@path/to/cat_or_dog.jpg"

# Run smoke tests
./scripts/smoke_tests.sh http://localhost:8000
```

## That's It! 🎉

Your MLOps pipeline is running. Next steps:

- **View MLflow UI**: `mlflow ui` → http://localhost:5000
- **Deploy with Docker Compose**: `cd deployment/docker-compose && docker-compose up -d`
- **Deploy to Kubernetes**: `kubectl apply -f deployment/kubernetes/deployment.yaml`

## Troubleshooting

**Model not found?**
```bash
# Train the model first
python src/training/train.py
```

**Port 8000 in use?**
```bash
# Use different port
docker run -p 8001:8000 ...
```

**Import errors?**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## Full Documentation

- **Setup Guide**: See `SETUP.md`
- **Deployment**: See `DEPLOYMENT.md`
- **Project Summary**: See `PROJECT_SUMMARY.md`

