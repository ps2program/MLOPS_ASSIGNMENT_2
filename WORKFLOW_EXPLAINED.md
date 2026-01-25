# MLOps Workflow: How It Works

## The Complete Journey: From Data to Production

### Phase 1: Data & Model Development (M1)

**What Happens:**
```
┌─────────────┐
│   Kaggle    │  Download dataset (25,038 images)
│   Dataset   │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  DVC Track  │  Version control for large files
│  data/raw/  │  Stores metadata, not actual data
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ Preprocess  │  Resize to 224x224, split 80/10/10
│   Images    │  Apply data augmentation
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Train     │  Train CNN model
│   Model     │  Optimize weights
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  MLflow     │  Track EVERYTHING:
│  Tracking   │  - Parameters (lr, batch_size)
│             │  - Metrics (accuracy, loss)
│             │  - Artifacts (model, confusion matrix)
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ Save Model  │  models/best_model.pt
└─────────────┘
```

**Why This Matters:**
- **DVC:** Reproducible datasets - anyone can get exact same data
- **MLflow:** Compare experiments - see which hyperparameters work best
- **Versioning:** Track what changed and when

### Phase 2: Packaging & Containerization (M2)

**What Happens:**
```
┌─────────────┐
│   Model     │  models/best_model.pt (100MB)
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  FastAPI    │  Wrap model in REST API
│   Service   │  /health, /predict endpoints
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ requirements│  Pin all versions for reproducibility
│    .txt     │  torch==2.10.0, fastapi==0.128.0, etc.
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ Dockerfile  │  Multi-stage build
│             │  - Stage 1: Install dependencies
│             │  - Stage 2: Copy code + model
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ Docker Image│  cats-dogs-classifier:latest
│             │  Self-contained, portable
└─────────────┘
```

**Why This Matters:**
- **Containerization:** "Works on my machine" → "Works everywhere"
- **Reproducibility:** Same environment every time
- **Scalability:** Run multiple instances easily

### Phase 3: CI Pipeline (M3)

**What Happens (Automatically on Git Push):**
```
┌─────────────┐
│ Git Push    │  Developer pushes code
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ GitHub      │  Detects push/PR
│ Actions     │  Triggers CI pipeline
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ Checkout    │  Get latest code
│ Code        │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ Install     │  pip install -r requirements.txt
│ Dependencies│
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ Run Tests   │  pytest tests/ -v
│             │  - Test preprocessing
│             │  - Test inference
└──────┬──────┘
       │
       ↓ (if tests pass)
┌─────────────┐
│ Build       │  docker build -t image:tag
│ Docker Image│
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ Push to     │  ghcr.io/ps2program/MLOPS_ASSIGNMENT_2
│ Registry    │  Tagged with: branch, SHA, version
└─────────────┘
```

**Why This Matters:**
- **Automation:** No manual steps = fewer errors
- **Quality Gates:** Bad code never reaches production
- **Speed:** Catch issues in minutes, not days

### Phase 4: CD Pipeline (M4)

**What Happens (Automatically on Main Branch):**
```
┌─────────────┐
│ Merge to    │  Code approved and merged
│   Main      │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ CD Pipeline │  GitHub Actions CD workflow
│  Triggered  │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ Pull Image  │  Get latest from registry
│ from Reg    │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ Deploy      │  kubectl apply OR docker-compose up
│ Service     │  Rolling update (zero downtime)
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ Smoke Tests │  Test health + prediction
│             │  Fail if broken
└──────┬──────┘
       │
       ↓ (if tests pass)
┌─────────────┐
│ Production  │  Service live and serving requests
│   Ready     │
└─────────────┘
```

**Why This Matters:**
- **Automated Deployment:** No manual steps = faster releases
- **Safety:** Smoke tests catch issues before users see them
- **Consistency:** Same deployment process every time

### Phase 5: Monitoring (M5)

**What Happens (Continuously):**
```
┌─────────────┐
│   User      │  Sends image for classification
│  Request    │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  API        │  FastAPI receives request
│  Endpoint   │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Log       │  Log request (timestamp, endpoint)
│  Request    │  Exclude sensitive data (image bytes)
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Predict    │  Run model inference
│             │  Measure latency
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Metrics    │  Update counters:
│  Update     │  - inference_requests_total++
│             │  - inference_latency.observe(time)
│             │  - predictions_total[class]++
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Response   │  Return prediction to user
└─────────────┘
```

**Why This Matters:**
- **Visibility:** Know what's happening in production
- **Debugging:** Logs help find issues quickly
- **Performance:** Metrics show bottlenecks
- **Quality:** Track model performance over time

## How It Works in Industry

### Industry-Scale Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Engineering Layer                    │
│  - Data pipelines (Airflow, Prefect)                        │
│  - Feature stores (Feast, Tecton)                           │
│  - Data quality checks (Great Expectations)                 │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                  Model Development Layer                      │
│  - Experimentation (Jupyter, VS Code)                        │
│  - Hyperparameter tuning (Optuna, Ray Tune)                  │
│  - Experiment tracking (MLflow, Weights & Biases)            │
│  - Model registry (MLflow Model Registry)                     │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                    CI/CD Automation Layer                     │
│  - Automated testing (pytest, unittest)                      │
│  - Code quality (linting, security scanning)                  │
│  - Container building (Docker, BuildKit)                     │
│  - Artifact management (Container registries)                │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                  Model Serving Layer                          │
│  - API gateways (Kong, AWS API Gateway)                       │
│  - Load balancers (NGINX, AWS ALB)                           │
│  - Inference services (FastAPI, TorchServe, TensorFlow Serving)│
│  - Auto-scaling (Kubernetes HPA, Cloud auto-scaling)         │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                Observability & Monitoring Layer               │
│  - Metrics (Prometheus, Datadog)                              │
│  - Logging (ELK Stack, CloudWatch)                           │
│  - Tracing (Jaeger, Zipkin)                                  │
│  - Dashboards (Grafana, custom)                              │
│  - Alerting (PagerDuty, Slack)                               │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│              Model Performance Monitoring                     │
│  - Prediction tracking                                       │
│  - Drift detection (Evidently AI, Fiddler)                   │
│  - Performance degradation alerts                            │
│  - Auto-retraining triggers                                  │
└─────────────────────────────────────────────────────────────┘
```

### Key Industry Differences

| Aspect | Assignment | Industry |
|--------|-----------|----------|
| **Scale** | Single model, local | Multiple models, distributed |
| **Environments** | Dev/Prod | Dev → Staging → Canary → Prod |
| **Testing** | Unit + Smoke | Unit + Integration + E2E + Performance + Load |
| **Deployment** | Manual/Auto | Fully automated with approvals |
| **Monitoring** | Basic metrics | Full observability (metrics, logs, traces) |
| **Security** | Basic | Comprehensive (auth, encryption, scanning, compliance) |
| **Cost** | Not tracked | Cost optimization, resource management |
| **Team** | Individual | Cross-functional teams (Data, ML, DevOps, SRE) |

### Industry Workflow Example: Netflix Recommendation System

```
1. Data Collection
   └─> User interactions, content metadata
   └─> Real-time streaming (Kafka)
   └─> Batch processing (Spark)

2. Feature Engineering
   └─> Feature store (Feast)
   └─> Real-time + batch features
   └─> Feature versioning

3. Model Training
   └─> Distributed training (PyTorch, TensorFlow)
   └─> Hyperparameter tuning (Ray Tune)
   └─> Experiment tracking (MLflow)
   └─> A/B testing framework

4. Model Serving
   └─> Multiple models (exploration vs exploitation)
   └─> Real-time inference (milliseconds)
   └─> Auto-scaling (thousands of requests/sec)
   └─> Model caching

5. Monitoring
   └─> Real-time dashboards
   └─> Anomaly detection
   └─> Performance tracking
   └─> Auto-retraining on drift
```

## Our Implementation: Step-by-Step

### 1. Data Collection & Versioning

**What we do:**
```bash
# Download dataset
kaggle datasets download -d bhavikjikadara/dog-and-cat-classification-dataset

# Track with DVC
dvc add data/raw
git add data/raw.dvc
git commit -m "Add dataset v1"
```

**Industry equivalent:**
- Data pipelines (Airflow)
- Data quality checks
- Automated data validation
- Cloud storage with versioning

### 2. Model Training & Experiment Tracking

**What we do:**
```python
with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.001)
    model = train_model(...)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.pytorch.log_model(model, "model")
```

**Industry equivalent:**
- Centralized MLflow server
- Model registry
- Automated hyperparameter tuning
- Distributed training

### 3. Containerization

**What we do:**
```dockerfile
FROM python:3.10-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
COPY models/ ./models/
CMD ["uvicorn", "src.inference.app:app"]
```

**Industry equivalent:**
- Multi-stage builds
- Security scanning
- Image optimization
- Base image management

### 4. CI/CD

**What we do:**
```yaml
# .github/workflows/ci.yml
- name: Run tests
  run: pytest tests/
- name: Build image
  run: docker build -t image:tag
- name: Push to registry
  run: docker push image:tag
```

**Industry equivalent:**
- Multi-stage pipelines
- Parallel execution
- Quality gates
- Automated rollback

### 5. Deployment

**What we do:**
```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: classifier
        image: cats-dogs-classifier:latest
```

**Industry equivalent:**
- Blue-green deployments
- Canary releases
- Auto-scaling
- Multi-region deployment

### 6. Monitoring

**What we do:**
```python
# Prometheus metrics
request_count = Counter('inference_requests_total')
request_latency = Histogram('inference_latency_seconds')

# Logging
logger.info(f"Prediction: {result}, Latency: {latency}s")
```

**Industry equivalent:**
- Full observability stack
- Real-time dashboards
- Automated alerting
- Anomaly detection

## Learning Outcomes

### What You've Learned

1. **Version Control for ML**
   - Git for code
   - DVC for data
   - MLflow for experiments

2. **Reproducibility**
   - Pinned dependencies
   - Containerization
   - Environment consistency

3. **Automation**
   - CI/CD pipelines
   - Automated testing
   - Automated deployment

4. **Observability**
   - Metrics collection
   - Logging
   - Monitoring

5. **Best Practices**
   - Code organization
   - Testing strategies
   - Deployment patterns

### Industry Skills Gained

- ✅ MLOps pipeline design
- ✅ Experiment tracking
- ✅ Container orchestration
- ✅ CI/CD for ML
- ✅ Model serving
- ✅ Monitoring & observability

## Next Steps for Industry

1. **Learn Kubernetes** in depth
2. **Explore cloud platforms** (AWS SageMaker, GCP Vertex AI, Azure ML)
3. **Study distributed training** (PyTorch DDP, Horovod)
4. **Learn feature stores** (Feast, Tecton)
5. **Practice with real datasets** at scale
6. **Understand cost optimization** for ML workloads

