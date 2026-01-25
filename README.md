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
   git clone https://github.com/ps2program/MLOPS_ASSIGNMENT_2.git
   cd MLOPS_ASSIGNMENT_2
   dvc init
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download dataset:**
   - Dataset: [bhavikjikadara/dog-and-cat-classification-dataset](https://www.kaggle.com/datasets/bhavikjikadara/dog-and-cat-classification-dataset)
   - Total: 25,038 images (12,519 cats, 12,519 dogs)
   - Use Kaggle CLI: `kaggle datasets download -d bhavikjikadara/dog-and-cat-classification-dataset -p data/raw --unzip`
   - Or use the script: `./scripts/download_dataset.sh` (after setting up Kaggle credentials)
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

## Dataset

- **Source:** [bhavikjikadara/dog-and-cat-classification-dataset](https://www.kaggle.com/datasets/bhavikjikadara/dog-and-cat-classification-dataset)
- **Size:** 25,038 images (12,519 cats, 12,519 dogs)
- **Tracked with:** DVC (Data Version Control)
- See `DATASET_INFO.md` for detailed information

## Modules

- **M1**: Model Development & Experiment Tracking (✅ Complete)
- **M2**: Model Packaging & Containerization (✅ Complete)
- **M3**: CI Pipeline for Build, Test & Image Creation (✅ Complete)
- **M4**: CD Pipeline & Deployment (✅ Complete)
- **M5**: Monitoring, Logs & Final Submission (✅ Complete)

## Repository

- **GitHub:** https://github.com/ps2program/MLOPS_ASSIGNMENT_2
- **Status:** All modules implemented and tested

