# MLOps Workflow: From Data to Deployment

## Understanding the Complete MLOps Pipeline

This document explains how the MLOps pipeline works according to the assignment requirements and how it scales in industry.

## Assignment Workflow Overview

Based on [MLOPS_Assignment2.pdf](MLOPS_Assignment2.pdf), the complete workflow consists of 5 modules:

```
Data → Training → Packaging → CI/CD → Deployment → Monitoring
  ↓        ↓          ↓         ↓          ↓            ↓
 M1       M1        M2        M3         M4          M5
```

## Module-by-Module Workflow

### M1: Model Development & Experiment Tracking

**Workflow:**
```
1. Data Collection
   └─> Download from Kaggle
   └─> Track with DVC (data/raw.dvc)

2. Data Preprocessing
   └─> Resize to 224x224 RGB
   └─> Split: 80% train / 10% val / 10% test
   └─> Apply data augmentation
   └─> Track processed data with DVC

3. Model Training
   └─> Build baseline CNN model
   └─> Train with hyperparameters
   └─> MLflow tracks:
       - Parameters (epochs, batch_size, lr)
       - Metrics (loss, accuracy, precision, recall, F1)
       - Artifacts (model, confusion matrix)

4. Model Versioning
   └─> Save model as .pt file
   └─> MLflow Model Registry
   └─> Git tracks code changes
```

**Industry Practice:**
- **Experiment Tracking:** MLflow/Weights & Biases/Neptune
- **Data Versioning:** DVC, Pachyderm, or cloud storage with versioning
- **Model Registry:** Centralized storage for model versions
- **Reproducibility:** Pin all dependencies, use containers

### M2: Model Packaging & Containerization

**Workflow:**
```
1. Model Serialization
   └─> Save trained model (.pt, .pkl, .h5)
   └─> Include preprocessing logic

2. API Development
   └─> FastAPI/Flask wrapper
   └─> Health check endpoint
   └─> Prediction endpoint
   └─> Input validation

3. Environment Specification
   └─> requirements.txt with pinned versions
   └─> Ensures reproducibility

4. Containerization
   └─> Dockerfile (multi-stage build)
   └─> Build Docker image
   └─> Test locally
   └─> Push to registry
```

**Industry Practice:**
- **API Standards:** RESTful APIs, OpenAPI/Swagger docs
- **Containerization:** Docker, optimized base images
- **Model Serving:** TensorFlow Serving, TorchServe, or custom APIs
- **Versioning:** Semantic versioning for models and APIs

### M3: CI Pipeline (Continuous Integration)

**Workflow:**
```
1. Code Push/PR
   └─> GitHub Actions triggered

2. Automated Testing
   └─> Install dependencies
   └─> Run unit tests (pytest)
   └─> Test data preprocessing
   └─> Test inference functions
   └─> Code coverage checks

3. Build & Package
   └─> Build Docker image
   └─> Run integration tests
   └─> Security scanning

4. Artifact Publishing
   └─> Push Docker image to registry
   └─> Tag with version/branch/SHA
   └─> Store build artifacts
```

**Industry Practice:**
- **Testing:** Unit, integration, performance tests
- **Quality Gates:** Code coverage, linting, security scans
- **Artifact Management:** Container registries (Docker Hub, ECR, GCR)
- **Build Optimization:** Caching, parallel builds

### M4: CD Pipeline (Continuous Deployment)

**Workflow:**
```
1. Deployment Trigger
   └─> Push to main branch
   └─> CD pipeline starts

2. Image Pull
   └─> Pull latest image from registry
   └─> Verify image integrity

3. Deployment
   └─> Kubernetes: Apply manifests
   └─> Docker Compose: docker-compose up
   └─> Rolling update strategy
   └─> Health checks

4. Smoke Tests
   └─> Test health endpoint
   └─> Test prediction endpoint
   └─> Verify metrics
   └─> Fail pipeline if tests fail
```

**Industry Practice:**
- **Deployment Strategies:** Blue-green, canary, rolling updates
- **Infrastructure as Code:** Terraform, CloudFormation
- **GitOps:** ArgoCD, Flux for declarative deployments
- **Feature Flags:** Gradual rollout, A/B testing

### M5: Monitoring & Logging

**Workflow:**
```
1. Request Logging
   └─> Log all requests (excluding sensitive data)
   └─> Structured logging (JSON)
   └─> Log aggregation (ELK, Splunk)

2. Metrics Collection
   └─> Request count
   └─> Latency (p50, p95, p99)
   └─> Error rates
   └─> Prediction distribution

3. Model Performance Tracking
   └─> Collect predictions + true labels
   └─> Calculate accuracy over time
   └─> Detect model drift
   └─> Trigger retraining if needed
```

**Industry Practice:**
- **Observability:** Prometheus + Grafana, Datadog, New Relic
- **Logging:** Centralized logging (ELK stack, CloudWatch)
- **Alerting:** PagerDuty, Slack notifications
- **Model Monitoring:** Evidently AI, Fiddler, custom dashboards

## Complete End-to-End Workflow

### Development Phase
```
Developer → Code Change → Git Commit → Push to Branch
                                    ↓
                            Create Pull Request
                                    ↓
                            CI Pipeline Runs
                                    ↓
                            Tests Pass → Merge to Main
```

### Deployment Phase
```
Main Branch Updated → CD Pipeline Triggered
                              ↓
                    Pull Latest Image
                              ↓
                    Deploy to Staging
                              ↓
                    Run Smoke Tests
                              ↓
                    Deploy to Production
                              ↓
                    Monitor & Alert
```

### Production Phase
```
User Request → API Gateway → Inference Service
                                    ↓
                            Model Prediction
                                    ↓
                            Log Request/Response
                                    ↓
                            Update Metrics
                                    ↓
                            Return Prediction
```

---

## How Teams Use These Five Phases in Industry

In practice, the same five modules (M1–M5) are used continuously and together. Here’s how teams typically use them.

### Who Uses What (Roles)

| Phase | Primary users | What they do |
|-------|----------------|---------------|
| **M1** (Data + training + tracking) | Data scientists, ML engineers | Pull versioned data (DVC), run experiments, log to MLflow/W&B, register best model |
| **M2** (Packaging + API + Docker) | ML engineers, backend engineers | Wrap model in API, write `requirements.txt`, maintain Dockerfile and image |
| **M3** (CI) | Everyone; owned by platform/DevOps | Every push/PR runs tests and builds image; engineers fix failing tests |
| **M4** (CD) | DevOps / platform / ML platform | Deploy new images (K8s, ECS, etc.), manage staging/prod, run smoke tests |
| **M5** (Monitoring + logs) | ML engineers, SRE, data scientists | Watch dashboards, set alerts, run post-deploy evaluation, decide when to retrain |

So: **M1–M2** are where most “model work” happens; **M3–M4** run on every change; **M5** runs all the time in production.

### Day-to-Day Flow: One Change Through All Five Phases

A typical cycle looks like this:

1. **M1**  
   - Data scientist/engineer gets new data or changes preprocessing/training code.  
   - They run training, compare runs in MLflow, promote the best model (e.g. to “Production” in Model Registry).  
   - **Output:** New model artifact + experiment record.

2. **M2**  
   - Same or another engineer ensures the inference service (FastAPI) and Docker image can load and serve this model.  
   - They update code/config if needed (e.g. new preprocessing), rebuild image.  
   - **Output:** New Docker image (and optionally new API version).

3. **M3**  
   - They push code (and sometimes trigger “use new model” config).  
   - CI runs automatically: unit tests, integration tests, build image, push to registry.  
   - **Output:** Test results + new image in registry (if tests pass).

4. **M4**  
   - On merge to main (or release tag), CD runs: deploy new image to staging, run smoke tests, then promote to production (rolling/canary).  
   - **Output:** New version of the service running in production.

5. **M5**  
   - Logs and metrics (Prometheus, Grafana, etc.) show traffic, latency, errors.  
   - Team runs post-deploy evaluation (batch of requests + labels, like our `evaluate_deployed_model.py`) to check accuracy.  
   - If metrics drift or accuracy drops, they go back to **M1** (retrain or fix data) and the cycle repeats.

So in industry, **all five phases are used as one loop**: M1 → M2 → M3 → M4 → M5 → (back to M1 when needed).

### How Often Each Phase Runs

| Phase | Frequency | Trigger |
|-------|-----------|--------|
| **M1** | On demand + scheduled | New data, retraining schedule, or performance drift (from M5) |
| **M2** | When API/model interface or env changes | Code/config change in inference or dependencies |
| **M3** | Every push / every PR | Git push, PR opened/updated |
| **M4** | On merge to main (or release) | Merge, tag, or manual “deploy” button |
| **M5** | Continuous | Every request is logged; metrics scraped every few seconds; evaluations run after deploy or on schedule |

So **M3 and M4** are the “heartbeat” (every code change); **M1 and M2** are used when model or serving code changes; **M5** is always on in production.

### Handoffs Between Phases

- **M1 → M2:** “This model version is approved; please make sure the API and Docker image can serve it.”  
  - In small teams, the same person does both. In larger orgs, a Model Registry (e.g. MLflow) holds the artifact; M2 pulls by version.

- **M2 → M3:** “This image is built from this repo and this Dockerfile.”  
  - CI (M3) builds that image on every push; no manual handoff.

- **M3 → M4:** “This image passed tests; deploy it.”  
  - CD (M4) pulls the image from the registry and deploys; often triggered automatically on merge.

- **M4 → M5:** “New version is live; start monitoring it.”  
  - Monitoring (M5) is always on; after deploy, teams watch dashboards and run evaluation scripts.

- **M5 → M1:** “Accuracy dropped or drift detected; we need to retrain.”  
  - This is the feedback loop: production signals (M5) drive the next round of data/training work (M1).

### How This Compares to Our Project

Our assignment has the same five modules:

- **M1:** We use Git + DVC + MLflow (data versioning, training, tracking).  
- **M2:** FastAPI + `requirements.txt` + Dockerfile (packaging and containerization).  
- **M3:** GitHub Actions runs tests and builds the image (CI).  
- **M4:** CD workflow + Kubernetes/Docker Compose + smoke tests (deployment).  
- **M5:** Logging + Prometheus + `evaluate_deployed_model.py` (monitoring and post-deploy evaluation).

In industry, the **ideas are the same**; the differences are usually:

- **Scale:** More data, more experiments, more services, more frequent deploys.  
- **Tooling:** Dedicated model registries, feature stores, orchestration (Airflow/Prefect), managed K8s.  
- **Governance:** Approval steps (e.g. “promote to production” in registry), compliance, access control.  
- **Automation:** Scheduled retraining, auto-deploy on metric thresholds, canary releases.

So: **teams use MLOps by running M1–M2 when the model or API changes, M3–M4 on every code change, and M5 all the time—with M5 feeding back into M1 for retraining.** Our five modules map directly to this loop.

---

## Industry-Scale MLOps Architecture

### Typical Industry Setup

```
┌─────────────────────────────────────────────────────────┐
│                    Data Sources                          │
│  (Databases, APIs, Files, Streaming)                     │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│              Data Pipeline (Airflow/Prefect)            │
│  - Data ingestion                                       │
│  - Data validation                                      │
│  - Feature engineering                                  │
│  - Data versioning (DVC/Delta Lake)                     │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│          Model Development (Jupyter/VS Code)            │
│  - Experimentation                                      │
│  - Hyperparameter tuning (Optuna, Ray Tune)             │
│  - Model training (distributed if needed)               │
│  - Experiment tracking (MLflow/W&B)                     │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│              Model Registry (MLflow/Weights & Biases)   │
│  - Model versioning                                     │
│  - Model metadata                                       │
│  - Model lineage                                        │
│  - Approval workflows                                   │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│              CI/CD Pipeline (GitHub Actions/Jenkins)     │
│  - Automated testing                                    │
│  - Model validation                                     │
│  - Container building                                   │
│  - Security scanning                                    │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│         Container Registry (Docker Hub/ECR/GCR)          │
│  - Versioned images                                     │
│  - Image scanning                                       │
│  - Access control                                       │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│         Deployment (Kubernetes/Cloud Services)          │
│  - Auto-scaling                                         │
│  - Load balancing                                       │
│  - Health checks                                        │
│  - Rolling updates                                      │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│              Monitoring & Observability                  │
│  - Prometheus (metrics)                                 │
│  - Grafana (dashboards)                                 │
│  - ELK Stack (logging)                                  │
│  - Alerting (PagerDuty/Slack)                           │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│              Model Performance Monitoring                │
│  - Prediction tracking                                  │
│  - Drift detection                                      │
│  - Performance degradation alerts                       │
│  - Auto-retraining triggers                            │
└─────────────────────────────────────────────────────────┘
```

## Key Industry Practices

### 1. Experiment Tracking (MLflow)

**Why it matters:**
- Track what works and what doesn't
- Reproduce experiments
- Compare model versions
- Share results with team

**How it works:**
```python
with mlflow.start_run():
    # Log parameters
    mlflow.log_param("learning_rate", 0.001)
    mlflow.log_param("batch_size", 32)
    
    # Train model
    model = train_model(...)
    
    # Log metrics
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("f1_score", 0.93)
    
    # Log artifacts
    mlflow.log_artifact("confusion_matrix.png")
    mlflow.pytorch.log_model(model, "model")
```

**Industry Scale:**
- Centralized MLflow server
- Model registry for production models
- Automated experiment tracking
- Integration with CI/CD

### 2. Data Versioning (DVC)

**Why it matters:**
- Reproduce exact dataset used for training
- Track data lineage
- Manage large datasets efficiently
- Collaborate on data changes

**How it works:**
```bash
# Track dataset
dvc add data/raw

# Commit DVC metadata (not actual data)
git add data/raw.dvc .gitignore
git commit -m "Add dataset v1"

# Pull dataset on another machine
dvc pull
```

**Industry Scale:**
- Cloud storage backends (S3, GCS, Azure)
- Data pipelines with versioning
- Data quality checks
- Automated data validation

### 3. CI/CD for ML

**Why it matters:**
- Catch issues early
- Automate testing
- Ensure reproducibility
- Fast deployment cycles

**How it works:**
```yaml
# .github/workflows/ci.yml
on: [push, pull_request]
jobs:
  test:
    - Install dependencies
    - Run unit tests
    - Run integration tests
  build:
    - Build Docker image
    - Push to registry
  deploy:
    - Deploy to staging
    - Run smoke tests
    - Deploy to production
```

**Industry Scale:**
- Multi-stage pipelines
- Parallel test execution
- Automated rollback on failure
- Feature flags for gradual rollout

### 4. Model Serving

**Why it matters:**
- Scalable inference
- Low latency
- High availability
- Resource efficiency

**How it works:**
```
Request → API Gateway → Load Balancer → Inference Pods
                                              ↓
                                        Model Cache
                                              ↓
                                        Prediction
                                              ↓
                                        Response
```

**Industry Scale:**
- Auto-scaling based on load
- Model caching
- Batch inference for efficiency
- GPU acceleration
- Multi-model serving

### 5. Monitoring & Observability

**Why it matters:**
- Detect issues early
- Track model performance
- Understand system behavior
- Make data-driven decisions

**What to monitor:**
- **System Metrics:** CPU, memory, latency
- **Business Metrics:** Request rate, error rate
- **Model Metrics:** Prediction distribution, accuracy
- **Data Metrics:** Input distribution, drift

**Industry Scale:**
- Real-time dashboards
- Automated alerting
- Anomaly detection
- Performance SLAs
- Cost tracking

## Our Implementation vs Industry

### What We Have (Assignment Requirements)

✅ **Experiment Tracking:** MLflow
✅ **Data Versioning:** DVC
✅ **CI/CD:** GitHub Actions
✅ **Containerization:** Docker
✅ **Deployment:** Kubernetes + Docker Compose
✅ **Monitoring:** Prometheus metrics
✅ **Testing:** Unit tests + smoke tests

### Industry Additions (Beyond Assignment)

**Additional Components:**
- **Feature Stores:** Feast, Tecton (for feature management)
- **Model Serving Platforms:** Seldon, KServe, BentoML
- **Workflow Orchestration:** Airflow, Prefect, Kubeflow
- **Hyperparameter Tuning:** Optuna, Ray Tune, Hyperopt
- **A/B Testing:** Split.io, LaunchDarkly
- **Model Explainability:** SHAP, LIME integration
- **Data Quality:** Great Expectations, Pandera
- **Security:** Model encryption, access control

## Best Practices Summary

### 1. **Reproducibility**
- Version everything: code, data, models, environment
- Use containers for consistent environments
- Pin all dependencies

### 2. **Automation**
- Automate testing, building, deployment
- Reduce manual steps
- Fail fast, recover quickly

### 3. **Observability**
- Log everything (safely)
- Monitor metrics
- Set up alerts
- Create dashboards

### 4. **Scalability**
- Design for scale from start
- Use cloud-native tools
- Plan for growth

### 5. **Security**
- Secure API endpoints
- Encrypt sensitive data
- Manage secrets properly
- Regular security audits

## Learning Resources

- **MLflow:** https://mlflow.org/docs/latest/index.html
- **DVC:** https://dvc.org/doc
- **Kubernetes:** https://kubernetes.io/docs/home/
- **Prometheus:** https://prometheus.io/docs/
- **MLOps Best Practices:** Google's MLOps Guide, AWS MLOps Framework

## Next Steps for Industry Readiness

1. **Add Feature Store** for production features
2. **Implement Model Registry** for model lifecycle management
3. **Add A/B Testing** framework
4. **Implement Auto-scaling** for inference service
5. **Add Model Explainability** endpoints
6. **Set up Alerting** for production issues
7. **Implement Canary Deployments** for safe rollouts
8. **Add Cost Tracking** for resource optimization

