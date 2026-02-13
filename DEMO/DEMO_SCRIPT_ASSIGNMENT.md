# Assignment-Aligned MLOps Demo Script

**Purpose:** Screen recording script demonstrating all 5 assignment modules (M1-M5) in under 5 minutes.

**Target:** Complete MLOps workflow from code change to deployed model prediction

---

## Pre-Recording Checklist

**CRITICAL:** Complete ALL items before starting recording:

- [ ] Kind cluster running: `kind get clusters` → should show `mlops-cluster`
- [ ] Current deployment healthy: `kubectl get pods -l app=cats-dogs-classifier` → 2/2 Running
- [ ] Port-forward active: `kubectl port-forward svc/cats-dogs-classifier-service 8080:80 &`
- [ ] MLflow UI running (optional): `mlflow ui --port 5000 &`
- [ ] GitHub repository open in browser tab
- [ ] Terminal ready in project directory: `cd /path/to/ML_Ops_A2`
- [ ] Test images available: `ls data/raw/cats/cat_000.jpg data/raw/dogs/dog_000.jpg`
- [ ] Git repo clean: `git status` → no uncommitted changes
- [ ] Smoke test script executable: `chmod +x scripts/smoke_tests.sh`
- [ ] IDE ready with `src/inference/app.py` open

---

## Demo Script (4:50 Total)

### Segment 1: Introduction & Module Overview (0:00 - 0:20)

**Screen:** Terminal showing project structure

**Commands:**
```bash
# Show project structure
ls -la
echo "=== Project Structure ==="
tree -L 2 -I 'venv|__pycache__|mlruns|.git' | head -25
```

**Narration:**
> "This is our complete MLOps pipeline implementing all 5 assignment modules. We have:
> - M1: Model Development with Git/DVC versioning, CNN model, and MLflow tracking
> - M2: Model Packaging with FastAPI REST API and Docker containerization
> - M3: CI Pipeline with automated tests and Docker image publishing
> - M4: CD Pipeline with Kubernetes deployment and smoke tests
> - M5: Monitoring with Prometheus metrics and logging
> 
> Now let's see the complete workflow from code change to deployed prediction."

**Visual Focus:**
- Project directory structure
- Key folders: `src/`, `deployment/`, `.github/workflows/`, `tests/`

---

### Segment 2: M1 Showcase - Versioning & Model (0:20 - 0:50)

**Screen:** Terminal showing M1 components

**Commands:**
```bash
# 1. Show Git versioning
echo "=== M1: Git Versioning ==="
git log --oneline -5
echo ""
git status

# 2. Show DVC versioning
echo ""
echo "=== M1: DVC Versioning ==="
cat data/raw.dvc
echo ""
ls -lh data/raw/ | head -5

# 3. Show trained model
echo ""
echo "=== M1: Trained Model ==="
ls -lh models/best_model.pt

# 4. Show MLflow (quick)
echo ""
echo "=== M1: MLflow Tracking ==="
ls mlruns/0/*/artifacts/ 2>/dev/null | head -5 || echo "MLflow runs available in mlruns/"
```

**Narration:**
> "M1 requirements demonstrated:
> - Git tracks all source code with full commit history
> - DVC tracks our 25,000 image dataset - only 101 bytes of metadata in Git, actual data in DVC storage
> - Trained CNN model saved as .pt file, ready for deployment
> - MLflow tracks all experiment parameters, metrics like accuracy and F1 score, and artifacts like confusion matrices"

**Visual Focus:**
- Git log showing commits
- DVC metadata file showing dataset hash
- Model file size
- MLflow directory structure

---

### Segment 3: Code Change & M2 Showcase (0:50 - 1:30)

**Screen:** IDE showing code change, then terminal

**Actions:**

1. **Make code change in IDE:**
   - Open `src/inference/app.py`
   - Navigate to prediction endpoint function
   - Add logging line (see prepared change below)
   - Save file

2. **Show M2 - FastAPI endpoints:**
   ```bash
   echo "=== M2: FastAPI Service ==="
   grep -n "@app\." src/inference/app.py | head -5
   ```

3. **Show M2 - Docker:**
   ```bash
   echo ""
   echo "=== M2: Dockerfile ==="
   head -15 Dockerfile
   echo ""
   echo "=== M2: Requirements (Pinned Versions) ==="
   grep -E "(torch|fastapi|uvicorn)" requirements.txt
   ```

4. **Commit and push:**
   ```bash
   echo ""
   echo "=== Committing Code Change ==="
   git add src/inference/app.py
   git commit -m "Enhance logging for monitoring (M5 requirement)"
   git push origin main
   ```

**Narration:**
> "I'm making a code change to enhance logging for better monitoring - this demonstrates M5 requirement. 
> 
> M2 requirements shown:
> - FastAPI REST API with health check endpoint and prediction endpoint
> - Dockerfile containerizes the entire inference service
> - requirements.txt pins all ML library versions for reproducibility
> 
> Code change committed and pushed. This automatically triggers our CI/CD pipeline."

**Visual Focus:**
- Code change in IDE
- FastAPI endpoints
- Dockerfile structure
- Git commit and push

---

### Segment 4: M3 Showcase - CI Pipeline (1:30 - 2:30)

**Screen:** IDE showing CI config, then terminal with tests

**Actions:**

1. **Show CI workflow:**
   ```bash
   echo "=== M3: CI Pipeline Configuration ==="
   cat .github/workflows/ci.yml
   ```
   (Or show in IDE for better readability)

2. **Run tests (simulate CI):**
   ```bash
   echo ""
   echo "=== M3: Running Unit Tests (CI Step) ==="
   PYTHONPATH=. pytest tests/ -v --tb=short
   ```

3. **Show GitHub Actions (if available):**
   - Switch to browser → GitHub Actions tab
   - Show workflow running/completed
   - Point out: Tests passed, Image built

**Alternative if GitHub Actions slow:**
```bash
echo ""
echo "=== M3: CI Pipeline Status ==="
echo "GitHub Actions automatically runs on push:"
echo "1. Checkout code"
echo "2. Install dependencies"
echo "3. Run pytest (14 tests)"
echo "4. Build Docker image"
echo "5. Push to GitHub Container Registry"
```

**Narration:**
> "M3 requirements demonstrated:
> - CI pipeline configured in GitHub Actions - runs on every push
> - Unit tests for preprocessing functions and inference functions - all 14 tests pass
> - Docker image automatically built and pushed to GitHub Container Registry
> 
> The CI pipeline ensures code quality before deployment."

**Visual Focus:**
- CI workflow YAML file
- Test results showing 14 passed
- GitHub Actions UI (if available)

---

### Segment 5: M4 Showcase - CD Pipeline & Deployment (2:30 - 3:30)

**Screen:** Terminal showing deployment

**Actions:**

1. **Show CD workflow:**
   ```bash
   echo "=== M4: CD Pipeline Configuration ==="
   head -20 .github/workflows/cd.yml
   ```

2. **Show Kubernetes manifests:**
   ```bash
   echo ""
   echo "=== M4: Kubernetes Deployment ==="
   kubectl get deployment cats-dogs-classifier -o yaml | grep -A 5 "replicas\|image\|ports"
   ```

3. **Simulate deployment:**
   ```bash
   echo ""
   echo "=== M4: Deploying New Version ==="
   kubectl set image deployment/cats-dogs-classifier \
     classifier-api=cats-dogs-classifier:latest
   
   echo "Waiting for rollout..."
   kubectl rollout status deployment/cats-dogs-classifier --timeout=60s
   
   echo ""
   echo "=== Deployment Status ==="
   kubectl get pods -l app=cats-dogs-classifier
   ```

4. **Run smoke tests:**
   ```bash
   echo ""
   echo "=== M4: Running Smoke Tests ==="
   bash scripts/smoke_tests.sh http://localhost:8080
   ```

**Narration:**
> "M4 requirements demonstrated:
> - CD pipeline configured to deploy on main branch changes
> - Kubernetes deployment manifests define 2 replicas with health probes
> - CD automatically pulls new image and deploys to Kubernetes
> - Smoke tests verify deployment - health check passes, prediction endpoint works
> 
> Deployment successful with zero downtime rolling update."

**Visual Focus:**
- CD workflow file
- Kubernetes deployment status
- Pods updating
- Smoke test results

---

### Segment 6: M5 Showcase - Monitoring & Prediction (3:30 - 4:30)

**Screen:** Terminal showing monitoring and predictions

**Actions:**

1. **Show Prometheus metrics:**
   ```bash
   echo "=== M5: Prometheus Metrics ==="
   curl -s http://localhost:8080/metrics | grep -E "(inference_requests_total|predictions_total|inference_request_duration)"
   ```

2. **Show logs:**
   ```bash
   echo ""
   echo "=== M5: Application Logs ==="
   kubectl logs deployment/cats-dogs-classifier --tail=10
   ```

3. **Make predictions (KEY DEMO):**
   ```bash
   echo ""
   echo "=== M5: Making Predictions ==="
   echo "Cat image prediction:"
   curl -s -X POST -F "file=@data/raw/cats/cat_000.jpg" http://localhost:8080/predict | jq .
   
   echo ""
   echo "Dog image prediction:"
   curl -s -X POST -F "file=@data/raw/dogs/dog_000.jpg" http://localhost:8080/predict | jq .
   ```

4. **Show updated metrics:**
   ```bash
   echo ""
   echo "=== M5: Updated Metrics ==="
   curl -s http://localhost:8080/metrics | grep inference_requests_total
   ```

**Narration:**
> "M5 requirements demonstrated:
> - Prometheus metrics track request count, latency, and prediction distribution
> - Structured logging shows each prediction with confidence and latency
> - Model successfully making predictions - cat image correctly classified as cat with high confidence, dog image correctly classified as dog
> - Metrics automatically updated after each request
> 
> Complete MLOps workflow working end-to-end!"

**Visual Focus:**
- Metrics output
- Logs showing predictions
- JSON prediction responses
- Updated metric counts

---

### Segment 7: Summary & Module Checklist (4:30 - 4:50)

**Screen:** Terminal or overlay showing checklist

**Visual:**
Create a simple checklist display or narrate:

```
╔══════════════════════════════════════════════════════════╗
║         MLOps Assignment - All Modules Complete         ║
╠══════════════════════════════════════════════════════════╣
║ M1: Model Development & Experiment Tracking              ║
║   ✅ Git versioning (source code)                        ║
║   ✅ DVC versioning (dataset)                           ║
║   ✅ CNN model trained (.pt format)                      ║
║   ✅ MLflow tracking (parameters, metrics, artifacts)   ║
║                                                          ║
║ M2: Model Packaging & Containerization                   ║
║   ✅ FastAPI REST API (health, predict endpoints)        ║
║   ✅ requirements.txt with pinned versions              ║
║   ✅ Dockerfile containerization                         ║
║                                                          ║
║ M3: CI Pipeline                                          ║
║   ✅ Unit tests (preprocessing, inference)              ║
║   ✅ GitHub Actions CI workflow                         ║
║   ✅ Docker image published to registry                 ║
║                                                          ║
║ M4: CD Pipeline & Deployment                            ║
║   ✅ Kubernetes deployment manifests                    ║
║   ✅ CD workflow (auto-deploy on main)                  ║
║   ✅ Smoke tests (health, prediction)                   ║
║                                                          ║
║ M5: Monitoring & Logging                                 ║
║   ✅ Prometheus metrics (requests, latency)             ║
║   ✅ Request/response logging                           ║
║   ✅ Model serving predictions successfully             ║
╚══════════════════════════════════════════════════════════╝
```

**Narration:**
> "Complete MLOps workflow demonstrated in under 5 minutes:
> 
> Code change → CI pipeline tests and builds → CD pipeline deploys → Monitoring tracks → Model predicts successfully
> 
> All 5 assignment modules showcased:
> - M1: Versioning, model building, experiment tracking
> - M2: API packaging and containerization
> - M3: Automated testing and CI
> - M4: Automated deployment with smoke tests
> - M5: Monitoring, logging, and model serving
> 
> Thank you!"

---

## Timing Rehearsal Tips

**Practice each segment separately:**
1. Time Segment 1 (Intro) - Target: 20 seconds
2. Time Segment 2 (M1) - Target: 30 seconds
3. Time Segment 3 (Code Change & M2) - Target: 40 seconds
4. Time Segment 4 (M3) - Target: 60 seconds
5. Time Segment 5 (M4) - Target: 60 seconds
6. Time Segment 6 (M5) - Target: 60 seconds
7. Time Segment 7 (Summary) - Target: 20 seconds

**If running over time:**
- Segment 2: Skip MLflow UI, just show directory
- Segment 4: Skip GitHub Actions UI, just show config
- Segment 5: Pre-deploy before recording, just show status
- Segment 6: Make only one prediction instead of two

**Speed up commands:**
- Use `-s` flag for curl (silent)
- Use `--tb=short` for pytest (shorter traceback)
- Use `head -N` to limit output
- Pre-run slow commands and show results

---

## Troubleshooting

**If port-forward not working:**
```bash
# Kill existing port-forward
pkill -f "port-forward.*cats-dogs-classifier"
# Restart
kubectl port-forward svc/cats-dogs-classifier-service 8080:80 &
```

**If deployment not ready:**
```bash
# Check status
kubectl get pods -l app=cats-dogs-classifier
# Wait for ready
kubectl wait --for=condition=ready pod -l app=cats-dogs-classifier --timeout=60s
```

**If tests fail:**
- Ensure PYTHONPATH is set: `export PYTHONPATH=.`
- Check dependencies: `pip install -r requirements.txt`

**If predictions fail:**
- Check service health: `curl http://localhost:8080/health`
- Check logs: `kubectl logs deployment/cats-dogs-classifier --tail=20`
- Verify image exists: `ls data/raw/cats/cat_000.jpg`

---

## Recording Tips

1. **Use a script:** Read narration from this document
2. **Practice first:** Run through entire demo once before recording
3. **Clear terminal:** Use `clear` between segments for clean visuals
4. **Zoom terminal:** Increase font size for better visibility
5. **Smooth transitions:** Pause briefly between segments
6. **Highlight key points:** Use cursor to point at important outputs
7. **Keep it simple:** Don't explain everything, just show it works

---

## Success Criteria

✅ All 5 modules (M1-M5) clearly demonstrated
✅ Complete workflow: Code change → Deployment → Prediction
✅ Under 5 minutes total
✅ No errors or failures shown
✅ Professional presentation
✅ Clear narration throughout
