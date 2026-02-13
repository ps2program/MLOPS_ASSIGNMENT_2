# Module Showcase Guide

This guide explains how to demonstrate each of the 5 assignment modules (M1-M5) during the screen recording.

---

## M1: Model Development & Experiment Tracking

### Assignment Requirements:
1. ✅ Git for source code versioning
2. ✅ DVC (or Git-LFS) for dataset versioning
3. ✅ Implement at least one baseline model
4. ✅ Save trained model in standard format (.pkl, .pt, .h5)
5. ✅ Use MLflow/Neptune for experiment tracking
6. ✅ Log runs, parameters, metrics, and artifacts

### How to Showcase:

#### 1. Git Versioning (10 seconds)
**Command:**
```bash
git log --oneline -5
git status
```

**What to Highlight:**
- Show commit history with meaningful messages
- Show clean working directory
- Mention: "All source code tracked in Git"

**Files to Show:**
- `.gitignore` - Shows what's excluded
- `src/` directory - Shows versioned code

---

#### 2. DVC Versioning (10 seconds)
**Command:**
```bash
cat data/raw.dvc
ls -lh data/raw/ | head -5
```

**What to Highlight:**
- DVC metadata file (small, in Git)
- Actual dataset directory (large, not in Git)
- Mention: "25,000 images tracked with DVC - only metadata in Git"

**Files to Show:**
- `data/raw.dvc` - DVC metadata (101 bytes)
- `.dvc/config` - DVC configuration

**Key Point:** Show the contrast - small metadata file vs large dataset

---

#### 3. Trained Model (5 seconds)
**Command:**
```bash
ls -lh models/best_model.pt
```

**What to Highlight:**
- Model file exists
- File size (~100MB)
- Format (.pt = PyTorch)

**Files to Show:**
- `models/best_model.pt` - Trained model
- `models/confusion_matrix.png` - Model artifact

**Key Point:** Model ready for deployment

---

#### 4. MLflow Tracking (5 seconds)
**Option A - MLflow UI:**
- Open `http://localhost:5000`
- Show experiment: "cats_dogs_classification"
- Click on a run → Show parameters, metrics, artifacts

**Option B - Directory Structure:**
```bash
ls mlruns/0/*/artifacts/
cat mlruns/0/*/params/learning_rate
```

**What to Highlight:**
- Parameters logged (epochs, batch_size, learning_rate)
- Metrics logged (accuracy, loss, F1)
- Artifacts logged (confusion matrix, model)

**Files to Show:**
- `mlruns/` directory structure
- MLflow UI (if available)

**Key Point:** Complete experiment tracking

---

### M1 Summary Script:
> "M1 requirements: Git tracks source code, DVC tracks 25,000 image dataset, CNN model trained and saved as .pt file, MLflow tracks all experiments with parameters, metrics, and artifacts."

---

## M2: Model Packaging & Containerization

### Assignment Requirements:
1. ✅ Wrap model with REST API (FastAPI/Flask)
2. ✅ Implement health check endpoint
3. ✅ Implement prediction endpoint
4. ✅ Define dependencies using requirements.txt
5. ✅ Ensure version pinning for ML libraries
6. ✅ Create Dockerfile
7. ✅ Build and run Docker image locally

### How to Showcase:

#### 1. FastAPI Service (15 seconds)
**Command:**
```bash
grep -n "@app\." src/inference/app.py
```

**What to Highlight:**
- `/health` endpoint - Health check ✅
- `/predict` endpoint - Prediction ✅
- `/metrics` endpoint - Prometheus metrics (bonus)

**Files to Show:**
- `src/inference/app.py` - FastAPI service code
- Show endpoint definitions

**Key Point:** REST API with required endpoints

---

#### 2. Requirements.txt (10 seconds)
**Command:**
```bash
grep -E "(torch|fastapi|uvicorn|prometheus)" requirements.txt
```

**What to Highlight:**
- Version pinning (e.g., `torch==2.1.0`)
- All key ML libraries pinned
- Reproducibility ensured

**Files to Show:**
- `requirements.txt` - Show pinned versions

**Key Point:** Version pinning for reproducibility

---

#### 3. Dockerfile (10 seconds)
**Command:**
```bash
head -20 Dockerfile
```

**What to Highlight:**
- Multi-stage build (if used)
- Base image
- Dependencies installation
- Model copying
- Service startup

**Files to Show:**
- `Dockerfile` - Containerization config

**Key Point:** Complete containerization

---

#### 4. Docker Build & Run (5 seconds - mention only)
**Command (if showing):**
```bash
docker images | grep cats-dogs-classifier
```

**What to Highlight:**
- Image exists
- Size (~2.5GB with model)
- Ready for deployment

**Key Point:** Model packaged in container

---

### M2 Summary Script:
> "M2 requirements: FastAPI REST API with health check and prediction endpoints, requirements.txt with pinned versions for reproducibility, Dockerfile containerizes the entire service with model baked in."

---

## M3: CI Pipeline for Build, Test & Image Creation

### Assignment Requirements:
1. ✅ Write unit tests for preprocessing function
2. ✅ Write unit tests for inference function
3. ✅ Tests run via pytest
4. ✅ CI Setup (GitHub Actions/GitLab CI/Jenkins)
5. ✅ Pipeline on every push/merge request
6. ✅ Checkout, install dependencies, run tests, build image
7. ✅ Push Docker image to container registry

### How to Showcase:

#### 1. Unit Tests (20 seconds)
**Command:**
```bash
PYTHONPATH=. pytest tests/ -v --tb=short
```

**What to Highlight:**
- 14 tests total
- Tests for preprocessing (`test_preprocessing.py`)
- Tests for inference (`test_inference.py`)
- All tests passing

**Files to Show:**
- `tests/test_preprocessing.py` - Preprocessing tests
- `tests/test_inference.py` - Inference tests
- Test output showing "14 passed"

**Key Point:** Comprehensive test coverage

---

#### 2. CI Pipeline Configuration (15 seconds)
**Command:**
```bash
cat .github/workflows/ci.yml
```

**What to Highlight:**
- Triggers: push, pull_request
- Steps: checkout, install, test, build, push
- Registry: GitHub Container Registry

**Files to Show:**
- `.github/workflows/ci.yml` - CI configuration

**Key Point:** Automated CI on every push

---

#### 3. GitHub Actions (15 seconds)
**Option A - Live:**
- Open GitHub → Actions tab
- Show workflow running/completed
- Point out: Tests passed, Image built

**Option B - Mention:**
- Show CI config file
- Mention: "CI runs automatically on push"

**What to Highlight:**
- Workflow triggered
- Tests passed
- Image built and pushed

**Key Point:** Fully automated CI pipeline

---

### M3 Summary Script:
> "M3 requirements: Unit tests for preprocessing and inference functions - all 14 tests pass, GitHub Actions CI pipeline runs automatically on every push, tests code, builds Docker image, and publishes to GitHub Container Registry."

---

## M4: CD Pipeline & Deployment

### Assignment Requirements:
1. ✅ Choose deployment target (Kubernetes/Docker Compose)
2. ✅ Define infrastructure manifests (Deployment + Service YAML)
3. ✅ CD/GitOps flow
4. ✅ Pull new image from registry
5. ✅ Deploy/update service automatically on main branch
6. ✅ Smoke tests / health check
7. ✅ Fail pipeline if smoke tests fail

### How to Showcase:

#### 1. Kubernetes Manifests (10 seconds)
**Command:**
```bash
cat deployment/kubernetes/deployment.yaml | head -30
```

**What to Highlight:**
- Deployment with replicas
- Service definition
- Health probes (liveness, readiness)
- Resource limits

**Files to Show:**
- `deployment/kubernetes/deployment.yaml` - K8s manifests

**Key Point:** Infrastructure as code

---

#### 2. CD Pipeline Configuration (10 seconds)
**Command:**
```bash
head -20 .github/workflows/cd.yml
```

**What to Highlight:**
- Triggers on main branch
- Pulls image from registry
- Deploys to Kubernetes
- Runs smoke tests

**Files to Show:**
- `.github/workflows/cd.yml` - CD configuration

**Key Point:** Automated deployment

---

#### 3. Deployment (15 seconds)
**Command:**
```bash
kubectl get pods -l app=cats-dogs-classifier
kubectl rollout status deployment/cats-dogs-classifier
```

**What to Highlight:**
- Pods running (2/2)
- Rolling update (if updating)
- Zero downtime deployment

**Key Point:** Successful deployment

---

#### 4. Smoke Tests (15 seconds)
**Command:**
```bash
bash scripts/smoke_tests.sh http://localhost:8080
```

**What to Highlight:**
- Health check passes
- Metrics endpoint accessible
- Prediction endpoint works
- All tests pass

**Files to Show:**
- `scripts/smoke_tests.sh` - Smoke test script
- Test output

**Key Point:** Post-deployment verification

---

### M4 Summary Script:
> "M4 requirements: Kubernetes deployment manifests with 2 replicas and health probes, CD pipeline automatically deploys on main branch changes, smoke tests verify deployment and fail pipeline if tests fail."

---

## M5: Monitoring, Logs & Final Submission

### Assignment Requirements:
1. ✅ Enable request/response logging (excluding sensitive data)
2. ✅ Track basic metrics (request count, latency)
3. ✅ Via logs, Prometheus, or simple counters
4. ✅ Model performance tracking (post-deployment)
5. ✅ Collect batch of requests and true labels

### How to Showcase:

#### 1. Prometheus Metrics (15 seconds)
**Command:**
```bash
curl -s http://localhost:8080/metrics | grep -E "(inference_requests_total|predictions_total|inference_request_duration)"
```

**What to Highlight:**
- `inference_requests_total` - Request count
- `inference_request_duration_seconds` - Latency histogram
- `predictions_total{class="cat/dog"}` - Prediction distribution

**Key Point:** Comprehensive metrics tracking

---

#### 2. Application Logs (10 seconds)
**Command:**
```bash
kubectl logs deployment/cats-dogs-classifier --tail=10
```

**What to Highlight:**
- Structured logging
- Prediction results logged
- Confidence and latency logged
- No sensitive data (no image bytes)

**Key Point:** Request/response logging enabled

---

#### 3. Model Predictions (20 seconds)
**Command:**
```bash
curl -X POST -F "file=@data/raw/cats/cat_000.jpg" http://localhost:8080/predict
curl -X POST -F "file=@data/raw/dogs/dog_000.jpg" http://localhost:8080/predict
```

**What to Highlight:**
- Cat image → cat prediction ✅
- Dog image → dog prediction ✅
- High confidence scores
- JSON response format

**Key Point:** Model serving predictions successfully

---

#### 4. Updated Metrics (5 seconds)
**Command:**
```bash
curl -s http://localhost:8080/metrics | grep inference_requests_total
```

**What to Highlight:**
- Metrics updated after requests
- Request count increased
- Real-time monitoring

**Key Point:** Metrics tracking in real-time

---

### M5 Summary Script:
> "M5 requirements: Prometheus metrics track request count and latency, structured logging shows predictions without sensitive data, model successfully serving predictions with high accuracy, metrics update in real-time."

---

## Quick Reference: What to Show for Each Module

| Module | Key Files | Key Commands | Time |
|--------|-----------|--------------|------|
| **M1** | `data/raw.dvc`, `models/best_model.pt`, `mlruns/` | `git log`, `cat data/raw.dvc`, `ls models/` | 30s |
| **M2** | `src/inference/app.py`, `Dockerfile`, `requirements.txt` | `grep @app`, `head Dockerfile`, `grep torch requirements.txt` | 40s |
| **M3** | `.github/workflows/ci.yml`, `tests/` | `pytest tests/`, `cat .github/workflows/ci.yml` | 60s |
| **M4** | `deployment/kubernetes/deployment.yaml`, `.github/workflows/cd.yml` | `kubectl get pods`, `bash scripts/smoke_tests.sh` | 60s |
| **M5** | Metrics output, Logs, Predictions | `curl /metrics`, `kubectl logs`, `curl /predict` | 60s |

---

## Tips for Effective Showcase

1. **Be concise:** Don't explain everything, just show it works
2. **Use visuals:** Show actual files and outputs, not just talk
3. **Highlight key points:** Use cursor to point at important parts
4. **Practice timing:** Each module should take planned time
5. **Show, don't tell:** Let the code/outputs speak for themselves
6. **Smooth transitions:** Pause briefly between modules
7. **Clear narration:** Speak clearly and confidently

---

## Common Mistakes to Avoid

❌ **Don't:** Spend too much time on one module
✅ **Do:** Stick to timing for each segment

❌ **Don't:** Show error messages or failures
✅ **Do:** Pre-test everything, show only success

❌ **Don't:** Explain technical details deeply
✅ **Do:** Show that requirements are met

❌ **Don't:** Read from script verbatim
✅ **Do:** Use script as guide, speak naturally

❌ **Don't:** Show uncommitted changes
✅ **Do:** Ensure clean git status before recording
