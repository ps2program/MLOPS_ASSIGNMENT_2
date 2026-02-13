# Dataset and Code Versioning Guide

This document explains how dataset and code versioning is implemented in this project.

---

## Overview

This project uses a **dual versioning system**:
- **Git** for code versioning (source code, configs, scripts)
- **DVC** (Data Version Control) for dataset versioning (large files, data)

---

## 1. Code Versioning with Git

### What Gets Versioned with Git

✅ **Tracked in Git:**
- Source code (`src/`)
- Configuration files (`.yaml`, `.yml`, `.json`)
- Scripts (`scripts/`)
- Documentation (`*.md`)
- DVC metadata files (`*.dvc`)
- CI/CD workflows (`.github/workflows/`)
- Docker files (`Dockerfile`, `docker-compose.yml`)
- Kubernetes manifests (`deployment/kubernetes/`)
- Requirements (`requirements.txt`)
- Test files (`tests/`)

❌ **Excluded from Git:**
- Large data files (`data/raw/`, `data/processed/`)
- Model files (`models/*.pt`, `models/*.pkl`)
- Python cache (`__pycache__/`, `*.pyc`)
- Virtual environments (`venv/`, `env/`)
- MLflow runs (`mlruns/`)
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`)

### Git Configuration

**Repository:** `https://github.com/ps2program/MLOPS_ASSIGNMENT_2.git`

**`.gitignore` includes:**
```gitignore
# Data (tracked by DVC)
data/raw/
data/processed/
*.pkl
*.h5
*.pt
*.pth

# MLflow
mlruns/
mlartifacts/
mlflow.db

# DVC cache
.dvc/cache
.dvc/tmp
.dvc/state

# Python
__pycache__/
*.pyc
venv/
env/

# IDE
.vscode/
.idea/
```

### Git Workflow

```bash
# Check status
git status

# Add code changes
git add src/ tests/ scripts/

# Commit with meaningful message
git commit -m "Add new preprocessing function"

# Push to remote
git push origin main
```

### Git History

Recent commits show code versioning:
```bash
git log --oneline -10
```

Example:
```
fdcf615 Enhance documentation with re-verification results
27256d6 Add dataset with DVC
1fd53d6 Complete MLOPs
68eb272 Add detailed workflow explanation document
79867c4 Add comprehensive MLOps workflow documentation
```

---

## 2. Dataset Versioning with DVC

### What Gets Versioned with DVC

✅ **Tracked with DVC:**
- Raw dataset (`data/raw/`) - ~775MB, 25,038 images
- Processed data (`data/processed/`) - Preprocessed images
- Large model files (optional)

### How DVC Works

**DVC stores:**
- **Metadata** (`.dvc` files) → Committed to Git
- **Actual data** → Stored in DVC cache/remote storage

**Benefits:**
- Git repository stays small (only metadata)
- Can version large files efficiently
- Reproducible datasets across machines
- Track data lineage

### DVC Configuration

**Config File:** `.dvc/config`
```ini
['remote "local"']
url = /tmp/dvc-storage
['core']
remote = local
```

**Current Setup:**
- Remote storage: Local (`/tmp/dvc-storage`)
- Hash algorithm: MD5
- Dataset tracked: `data/raw/`

### DVC Files

**`data/raw.dvc`** (committed to Git):
```yaml
outs:
- md5: 39ac063e70f5c4e825b3a9e7504cde5b.dir
  size: 70603
  nfiles: 50
  hash: md5
  path: raw
```

This small file (101 bytes) represents the entire dataset!

### DVC Workflow

#### Initial Setup
```bash
# Initialize DVC (already done)
dvc init

# Add dataset to DVC
dvc add data/raw

# Commit DVC metadata to Git
git add data/raw.dvc .gitignore
git commit -m "Add dataset with DVC"
git push
```

#### Working with Versioned Data
```bash
# Pull dataset (on another machine)
git pull
dvc pull

# Check dataset status
dvc status

# Update dataset version
# ... modify data/raw/ ...
dvc add data/raw
git add data/raw.dvc
git commit -m "Update dataset to v2"
git push
dvc push  # Push data to remote storage
```

#### View Dataset Versions
```bash
# See what changed
dvc diff

# List tracked files
dvc list data/

# Show dataset info
dvc show data/raw.dvc
```

### DVC Remote Storage Options

**Current:** Local storage (`/tmp/dvc-storage`)

**For Production/Team Use:**
```bash
# Add cloud remote (S3 example)
dvc remote add -d s3remote s3://my-bucket/dvc-storage

# Add Google Cloud Storage
dvc remote add -d gcsremote gs://my-bucket/dvc-storage

# Add Azure Blob Storage
dvc remote add -d azureremote azure://my-container/dvc-storage
```

---

## 3. Combined Workflow

### Typical Development Cycle

```bash
# 1. Update code
vim src/models/cnn_model.py
git add src/models/cnn_model.py
git commit -m "Improve CNN architecture"
git push

# 2. Update dataset (if needed)
# ... download new data to data/raw/ ...
dvc add data/raw
git add data/raw.dvc
git commit -m "Add new training samples"
git push
dvc push  # Push data to remote

# 3. Train model (uses versioned data)
PYTHONPATH=. python src/training/train.py

# 4. Commit model metadata (not the model file itself)
git add mlruns/  # MLflow tracks model versions
git commit -m "Add training run results"
git push
```

### Reproducing Experiments

**On a new machine:**
```bash
# 1. Clone repository
git clone https://github.com/ps2program/MLOPS_ASSIGNMENT_2.git
cd MLOPS_ASSIGNMENT_2

# 2. Pull code (Git)
git pull

# 3. Pull dataset (DVC)
dvc pull

# 4. Install dependencies
pip install -r requirements.txt

# 5. Reproduce training
PYTHONPATH=. python src/training/train.py
```

**Result:** Exact same code + exact same data = reproducible results!

---

## 4. Versioning Best Practices

### Code Versioning (Git)

✅ **Do:**
- Commit frequently with clear messages
- Use meaningful commit messages
- Create branches for features
- Tag releases (`git tag v1.0.0`)
- Keep `.gitignore` updated

❌ **Don't:**
- Commit large files directly
- Commit sensitive data (API keys, passwords)
- Commit generated files
- Force push to main branch

### Dataset Versioning (DVC)

✅ **Do:**
- Use DVC for files > 100MB
- Commit `.dvc` files to Git
- Use descriptive commit messages
- Set up remote storage for team collaboration
- Document dataset changes

❌ **Don't:**
- Commit actual data files to Git
- Forget to run `dvc push` after `dvc add`
- Store sensitive data without encryption
- Mix code and data in same commit

---

## 5. Current Versioning Status

### Git Repository
- **Remote:** `https://github.com/ps2program/MLOPS_ASSIGNMENT_2.git`
- **Branches:** `main`, `develop`
- **Files tracked:** ~50+ files (code, configs, docs)
- **Repository size:** Small (~few MB, excluding data)

### DVC Repository
- **Dataset tracked:** `data/raw/` (25,038 images)
- **Dataset size:** ~775MB
- **DVC metadata:** `data/raw.dvc` (101 bytes in Git)
- **Remote storage:** Local (`/tmp/dvc-storage`)

### Versioned Components

| Component | Tool | Location | Status |
|-----------|------|----------|--------|
| Source Code | Git | `src/` | ✅ Versioned |
| Tests | Git | `tests/` | ✅ Versioned |
| Configs | Git | `*.yaml`, `*.yml` | ✅ Versioned |
| Scripts | Git | `scripts/` | ✅ Versioned |
| Raw Dataset | DVC | `data/raw/` | ✅ Versioned |
| Processed Data | DVC | `data/processed/` | ✅ Ready |
| Models | MLflow | `mlruns/` | ✅ Tracked |
| Docker Images | GHCR | `ghcr.io/...` | ✅ Versioned |

---

## 6. Checking Version Status

### Git Status
```bash
# See what's changed
git status

# See commit history
git log --oneline --graph

# See file changes
git diff

# See remote status
git remote -v
```

### DVC Status
```bash
# Check DVC status
dvc status

# List tracked files
dvc list data/

# Show dataset info
cat data/raw.dvc

# Check DVC config
cat .dvc/config
```

### Combined Status
```bash
# See both Git and DVC changes
git status
dvc status
```

---

## 7. Troubleshooting

### Dataset Not Found
```bash
# Pull dataset from DVC
dvc pull

# Verify dataset exists
ls -lh data/raw/
```

### DVC Cache Issues
```bash
# Clear DVC cache
dvc cache dir
dvc cache clean

# Re-add dataset
dvc add data/raw
```

### Git Ignoring DVC Files
```bash
# Ensure .dvc files are tracked
git add data/*.dvc
git commit -m "Add DVC metadata"
```

### Remote Storage Issues
```bash
# Check remote configuration
dvc remote list

# Test remote connection
dvc push

# Update remote URL
dvc remote modify local url /new/path
```

---

## 8. Migration to Cloud Storage

To use cloud storage for DVC (recommended for teams):

### AWS S3
```bash
dvc remote add -d s3remote s3://bucket-name/dvc-storage
dvc push
```

### Google Cloud Storage
```bash
dvc remote add -d gcsremote gs://bucket-name/dvc-storage
dvc push
```

### Azure Blob Storage
```bash
dvc remote add -d azureremote azure://container-name/dvc-storage
dvc push
```

---

## Summary

**Code Versioning:**
- ✅ Git tracks all source code, configs, scripts
- ✅ Small repository size
- ✅ Full history and branching support

**Dataset Versioning:**
- ✅ DVC tracks large datasets (775MB)
- ✅ Only metadata in Git (101 bytes)
- ✅ Reproducible across machines
- ✅ Efficient storage and transfer

**Together:**
- ✅ Complete versioning solution
- ✅ Reproducible ML experiments
- ✅ Team collaboration ready
- ✅ CI/CD integration ready
