# Quick Commands Reference

All commands needed for the 5-minute MLOps demo, organized by module.

---

## Pre-Recording Setup

```bash
# Verify kind cluster
kind get clusters

# Check deployment
kubectl get pods -l app=cats-dogs-classifier

# Start port-forward
kubectl port-forward svc/cats-dogs-classifier-service 8080:80 &

# Verify service
curl http://localhost:8080/health

# Check git status
git status

# Verify test images
ls data/raw/cats/cat_000.jpg data/raw/dogs/dog_000.jpg
```

---

## Segment 1: Introduction (0:00 - 0:20)

```bash
# Show project structure
ls -la
tree -L 2 -I 'venv|__pycache__|mlruns|.git' | head -25
```

---

## Segment 2: M1 Showcase (0:20 - 0:50)

```bash
# Git versioning
git log --oneline -5
git status

# DVC versioning
cat data/raw.dvc
ls -lh data/raw/ | head -5

# Trained model
ls -lh models/best_model.pt

# MLflow tracking
ls mlruns/0/*/artifacts/ 2>/dev/null | head -5
```

---

## Segment 3: Code Change & M2 (0:50 - 1:30)

```bash
# Show FastAPI endpoints
grep -n "@app\." src/inference/app.py | head -5

# Show Dockerfile
head -15 Dockerfile

# Show requirements
grep -E "(torch|fastapi|uvicorn)" requirements.txt

# Commit and push
git add src/inference/app.py
git commit -m "Enhance logging for monitoring (M5 requirement)"
git push origin main
```

---

## Segment 4: M3 Showcase (1:30 - 2:30)

```bash
# Show CI config
cat .github/workflows/ci.yml

# Run tests
PYTHONPATH=. pytest tests/ -v --tb=short

# Check GitHub Actions (browser)
# Open: https://github.com/ps2program/MLOPS_ASSIGNMENT_2/actions
```

---

## Segment 5: M4 Showcase (2:30 - 3:30)

```bash
# Show CD config
head -20 .github/workflows/cd.yml

# Show K8s deployment
kubectl get deployment cats-dogs-classifier -o yaml | grep -A 5 "replicas\|image\|ports"

# Deploy new version
kubectl set image deployment/cats-dogs-classifier \
  classifier-api=cats-dogs-classifier:latest

# Watch rollout
kubectl rollout status deployment/cats-dogs-classifier --timeout=60s

# Check pods
kubectl get pods -l app=cats-dogs-classifier

# Run smoke tests
bash scripts/smoke_tests.sh http://localhost:8080
```

---

## Segment 6: M5 Showcase (3:30 - 4:30)

```bash
# Show metrics
curl -s http://localhost:8080/metrics | grep -E "(inference_requests_total|predictions_total|inference_request_duration)"

# Show logs
kubectl logs deployment/cats-dogs-classifier --tail=10

# Make predictions
curl -s -X POST -F "file=@data/raw/cats/cat_000.jpg" http://localhost:8080/predict | jq .

curl -s -X POST -F "file=@data/raw/dogs/dog_000.jpg" http://localhost:8080/predict | jq .

# Show updated metrics
curl -s http://localhost:8080/metrics | grep inference_requests_total
```

---

## Segment 7: Summary (4:30 - 4:50)

No commands needed - just narration and checklist display.

---

## Quick Health Checks

```bash
# Service health
curl http://localhost:8080/health

# Service metrics
curl http://localhost:8080/metrics | head -10

# Pod status
kubectl get pods -l app=cats-dogs-classifier

# Deployment status
kubectl get deployment cats-dogs-classifier

# Service status
kubectl get svc cats-dogs-classifier-service
```

---

## Troubleshooting Commands

```bash
# Restart port-forward
pkill -f "port-forward.*cats-dogs-classifier"
kubectl port-forward svc/cats-dogs-classifier-service 8080:80 &

# Check pod logs
kubectl logs deployment/cats-dogs-classifier --tail=20

# Describe pod (if issues)
kubectl describe pod -l app=cats-dogs-classifier

# Restart deployment
kubectl rollout restart deployment/cats-dogs-classifier

# Check cluster
kubectl cluster-info
kubectl get nodes
```

---

## One-Liner Verification

```bash
# Quick check everything is ready
kind get clusters && \
kubectl get pods -l app=cats-dogs-classifier && \
curl -s http://localhost:8080/health | grep -q "healthy" && \
git status --short | wc -l | grep -q "^0$" && \
[ -f data/raw/cats/cat_000.jpg ] && \
[ -f data/raw/dogs/dog_000.jpg ] && \
[ -f models/best_model.pt ] && \
echo "✅ All systems ready!"
```

---

## Command Cheat Sheet

| Purpose | Command |
|---------|---------|
| **Check cluster** | `kind get clusters` |
| **Check pods** | `kubectl get pods -l app=cats-dogs-classifier` |
| **Health check** | `curl http://localhost:8080/health` |
| **Run tests** | `PYTHONPATH=. pytest tests/ -v` |
| **Smoke tests** | `bash scripts/smoke_tests.sh http://localhost:8080` |
| **Make prediction** | `curl -X POST -F "file=@data/raw/cats/cat_000.jpg" http://localhost:8080/predict` |
| **View metrics** | `curl http://localhost:8080/metrics \| grep inference` |
| **View logs** | `kubectl logs deployment/cats-dogs-classifier --tail=10` |
| **Git status** | `git status` |
| **Git log** | `git log --oneline -5` |

---

## Timing Reference

| Segment | Commands | Time |
|---------|----------|------|
| Intro | `ls`, `tree` | 20s |
| M1 | `git log`, `cat data/raw.dvc`, `ls models/` | 30s |
| M2 | `grep`, `head Dockerfile`, `git commit` | 40s |
| M3 | `cat ci.yml`, `pytest` | 60s |
| M4 | `kubectl get`, `smoke_tests.sh` | 60s |
| M5 | `curl /metrics`, `curl /predict` | 60s |
| Summary | None | 20s |

---

## Pro Tips

1. **Pre-run slow commands:** Run `pytest` and `kubectl rollout` before recording
2. **Use aliases:** Create shortcuts for long commands
3. **Prepare outputs:** Have expected outputs ready to show
4. **Clear terminal:** Use `clear` between segments
5. **Zoom terminal:** Increase font for better visibility

---

## Common Command Variations

**If jq not available:**
```bash
# Instead of: curl ... | jq .
# Use: curl ... | python -m json.tool
```

**If tree not available:**
```bash
# Instead of: tree -L 2
# Use: find . -maxdepth 2 -type d | head -20
```

**Silent curl:**
```bash
# Add -s flag for silent output
curl -s http://localhost:8080/health
```

**Short pytest output:**
```bash
# Use --tb=short for shorter tracebacks
pytest tests/ -v --tb=short
```
