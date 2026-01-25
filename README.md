# MLOps Assignment 2: Cats vs Dogs Classification Pipeline

End-to-end MLOps pipeline for binary image classification (Cats vs Dogs) for a pet adoption platform.

## Project Structure

```
.
├── data/                  # Data directory (tracked by DVC)
│   ├── raw/              # Raw dataset
│   ├── processed/        # Preprocessed data
│   └── .gitignore
├── src/                   # Source code
│   ├── data/             # Data processing scripts
│   ├── models/           # Model definitions
│   ├── training/         # Training scripts
│   └── inference/       # Inference service
├── tests/                # Unit tests
├── notebooks/            # Jupyter notebooks for exploration
├── mlruns/               # MLflow experiment tracking
├── deployment/           # Deployment manifests
│   ├── kubernetes/      # K8s manifests
│   └── docker-compose/  # Docker Compose config
├── .github/
│   └── workflows/       # GitHub Actions CI/CD
├── Dockerfile           # Container image definition
├── requirements.txt     # Python dependencies
├── .dvcignore          # DVC ignore patterns
├── .gitignore          # Git ignore patterns
└── README.md           # This file
```

## Setup Instructions

1. **Clone and initialize:**
   ```bash
   git clone <repo-url>
   cd MLOps_A2
   git init
   dvc init
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download dataset:**
   - Download Cats and Dogs dataset from Kaggle
   - Place in `data/raw/`
   - Run `dvc add data/raw/` to track with DVC

4. **Train model:**
   ```bash
   python src/training/train.py
   ```

5. **Run inference service:**
   ```bash
   docker build -t cats-dogs-classifier .
   docker run -p 8000:8000 cats-dogs-classifier
   ```

## Modules

- **M1**: Model Development & Experiment Tracking
- **M2**: Model Packaging & Containerization
- **M3**: CI Pipeline for Build, Test & Image Creation
- **M4**: CD Pipeline & Deployment
- **M5**: Monitoring, Logs & Final Submission

