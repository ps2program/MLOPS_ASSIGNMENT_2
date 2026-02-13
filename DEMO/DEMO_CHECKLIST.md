# Pre-Recording Checklist

Complete ALL items before starting the screen recording. This ensures a smooth, error-free demo.

---

## System Prerequisites

### 1. Kubernetes Cluster
- [ ] Kind cluster created and running
  ```bash
  kind get clusters
  # Expected output: mlops-cluster
  ```

- [ ] Cluster is healthy
  ```bash
  kubectl get nodes
  # Expected: Ready status
  ```

### 2. Current Deployment
- [ ] Deployment exists and is healthy
  ```bash
  kubectl get deployment cats-dogs-classifier
  # Expected: READY 2/2
  ```

- [ ] Pods are running
  ```bash
  kubectl get pods -l app=cats-dogs-classifier
  # Expected: 2 pods, STATUS Running
  ```

- [ ] Service is available
  ```bash
  kubectl get svc cats-dogs-classifier-service
  # Expected: Service exists
  ```

### 3. Port Forwarding
- [ ] Port-forward is active
  ```bash
  kubectl port-forward svc/cats-dogs-classifier-service 8080:80 &
  # Check if running:
  ps aux | grep "port-forward.*8080"
  ```

- [ ] Service is accessible
  ```bash
  curl http://localhost:8080/health
  # Expected: {"status":"healthy","model_loaded":true}
  ```

### 4. MLflow (Optional for M1)
- [ ] MLflow UI is running (optional)
  ```bash
  mlflow ui --port 5000 &
  # Check: curl http://localhost:5000
  ```

---

## Project Setup

### 5. Git Repository
- [ ] Repository is clean
  ```bash
  git status
  # Expected: "nothing to commit, working tree clean"
  ```

- [ ] On main branch
  ```bash
  git branch
  # Expected: * main
  ```

- [ ] Remote is configured
  ```bash
  git remote -v
  # Expected: origin pointing to GitHub repo
  ```

### 6. Project Files
- [ ] Test images exist
  ```bash
  ls data/raw/cats/cat_000.jpg
  ls data/raw/dogs/dog_000.jpg
  # Expected: Files exist
  ```

- [ ] Model file exists
  ```bash
  ls -lh models/best_model.pt
  # Expected: File exists, ~100MB
  ```

- [ ] DVC metadata exists
  ```bash
  cat data/raw.dvc
  # Expected: DVC metadata file content
  ```

### 7. Scripts and Tools
- [ ] Smoke test script is executable
  ```bash
  chmod +x scripts/smoke_tests.sh
  ls -l scripts/smoke_tests.sh
  # Expected: -rwxr-xr-x (executable)
  ```

- [ ] Python environment is set
  ```bash
  which python
  python --version
  # Expected: Python 3.10+
  ```

- [ ] PYTHONPATH is set (for tests)
  ```bash
  echo $PYTHONPATH
  # Should be: . (current directory)
  # If not: export PYTHONPATH=.
  ```

---

## Dependencies

### 8. Python Packages
- [ ] All dependencies installed
  ```bash
  pip list | grep -E "(torch|fastapi|pytest|mlflow|dvc)"
  # Expected: All packages listed
  ```

- [ ] Requirements match
  ```bash
  pip check
  # Expected: No conflicts
  ```

### 9. Docker
- [ ] Docker is running
  ```bash
  docker ps
  # Expected: Docker daemon running
  ```

- [ ] Docker image exists (optional)
  ```bash
  docker images | grep cats-dogs-classifier
  # Expected: Image exists (optional, CI builds it)
  ```

### 10. Kubernetes Tools
- [ ] kubectl is configured
  ```bash
  kubectl version --client
  # Expected: kubectl version info
  ```

- [ ] kubectl can access cluster
  ```bash
  kubectl cluster-info
  # Expected: Cluster information
  ```

---

## Testing

### 11. Unit Tests
- [ ] Tests pass locally
  ```bash
  PYTHONPATH=. pytest tests/ -v
  # Expected: 14 passed
  ```

### 12. Smoke Tests
- [ ] Smoke tests pass
  ```bash
  bash scripts/smoke_tests.sh http://localhost:8080
  # Expected: All smoke tests passed
  ```

### 13. Predictions Work
- [ ] Health endpoint works
  ```bash
  curl http://localhost:8080/health
  # Expected: {"status":"healthy","model_loaded":true}
  ```

- [ ] Prediction endpoint works
  ```bash
  curl -X POST -F "file=@data/raw/cats/cat_000.jpg" http://localhost:8080/predict
  # Expected: JSON with prediction
  ```

- [ ] Metrics endpoint works
  ```bash
  curl http://localhost:8080/metrics | head -5
  # Expected: Prometheus metrics
  ```

---

## Browser & Tools

### 14. Browser Setup
- [ ] GitHub repository open in browser
  - URL: `https://github.com/ps2program/MLOPS_ASSIGNMENT_2`
  - Tab ready for Actions view

- [ ] MLflow UI open (optional)
  - URL: `http://localhost:5000`
  - Experiment visible

### 15. IDE Setup
- [ ] IDE ready with project open
- [ ] `src/inference/app.py` file open
- [ ] Terminal integrated or separate terminal ready

---

## Code Change Preparation

### 16. Code Change Ready
- [ ] Know what change to make
  - Location: `src/inference/app.py`
  - Type: Add logging line (see prepared change)
  - Safe: Won't break functionality

- [ ] Change is visible
  - Will show in logs after deployment
  - Demonstrates M5 requirement

---

## Recording Setup

### 17. Screen Recording
- [ ] Recording software ready
  - OBS, QuickTime, or preferred tool
  - Audio input configured
  - Screen area selected

- [ ] Audio check
  - Microphone working
  - Audio levels good
  - No background noise

- [ ] Screen resolution
  - Terminal font size readable
  - IDE font size readable
  - Browser zoom appropriate

### 18. Environment
- [ ] Quiet environment
  - No distractions
  - Phone silenced
  - Notifications disabled

- [ ] Time available
  - 5 minutes for recording
  - Extra time for retakes if needed

---

## Final Verification

### 19. Quick Run-Through
- [ ] Run through demo script once
  - Don't record, just practice
  - Check timing
  - Verify all commands work

- [ ] Check timing
  - Segment 1: 20 seconds
  - Segment 2: 30 seconds
  - Segment 3: 40 seconds
  - Segment 4: 60 seconds
  - Segment 5: 60 seconds
  - Segment 6: 60 seconds
  - Segment 7: 20 seconds
  - Total: ~4:50

### 20. Backup Plans
- [ ] Know fallback if GitHub Actions slow
  - Show config file instead
  - Mention it runs automatically

- [ ] Know fallback if deployment slow
  - Pre-deploy before recording
  - Show status instead of waiting

- [ ] Know fallback if MLflow slow
  - Show directory structure
  - Skip UI, just mention it

---

## Quick Verification Script

Run this script to verify everything:

```bash
#!/bin/bash
echo "=== Pre-Recording Verification ==="

echo "1. Kubernetes cluster:"
kind get clusters || echo "❌ Kind cluster not running"

echo "2. Deployment status:"
kubectl get pods -l app=cats-dogs-classifier || echo "❌ Pods not running"

echo "3. Port-forward:"
curl -s http://localhost:8080/health | grep -q "healthy" && echo "✅ Service accessible" || echo "❌ Service not accessible"

echo "4. Git status:"
git status --short || echo "❌ Git issues"

echo "5. Test images:"
[ -f data/raw/cats/cat_000.jpg ] && echo "✅ Cat image exists" || echo "❌ Cat image missing"
[ -f data/raw/dogs/dog_000.jpg ] && echo "✅ Dog image exists" || echo "❌ Dog image missing"

echo "6. Model file:"
[ -f models/best_model.pt ] && echo "✅ Model exists" || echo "❌ Model missing"

echo "7. Tests:"
PYTHONPATH=. pytest tests/ -q --tb=no 2>/dev/null | grep -q "passed" && echo "✅ Tests pass" || echo "❌ Tests fail"

echo "8. Smoke tests:"
bash scripts/smoke_tests.sh http://localhost:8080 > /dev/null 2>&1 && echo "✅ Smoke tests pass" || echo "❌ Smoke tests fail"

echo "=== Verification Complete ==="
```

Save as `verify_demo_setup.sh`, make executable, and run before recording.

---

## Troubleshooting

**If port-forward not working:**
```bash
pkill -f "port-forward.*cats-dogs-classifier"
kubectl port-forward svc/cats-dogs-classifier-service 8080:80 &
sleep 2
curl http://localhost:8080/health
```

**If pods not ready:**
```bash
kubectl get pods -l app=cats-dogs-classifier
kubectl describe pod <pod-name> | tail -20
kubectl logs <pod-name> --tail=20
```

**If tests fail:**
```bash
export PYTHONPATH=.
pip install -r requirements.txt
pytest tests/ -v
```

**If smoke tests fail:**
```bash
curl http://localhost:8080/health
curl http://localhost:8080/metrics | head -5
```

---

## Ready to Record!

Once all items are checked:
1. ✅ All systems running
2. ✅ All tests passing
3. ✅ All files in place
4. ✅ Recording setup ready

**You're ready to record!**

Start with Segment 1 and follow the demo script.
