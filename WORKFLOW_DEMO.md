# MLOps Workflow Demonstration Guide

This guide shows how to demonstrate the complete MLOps workflow from code change to deployed model prediction.

## Complete Workflow Steps

### Step 1: Make a Code Change

```bash
# Edit a file (e.g., improve model architecture)
vim src/models/cnn_model.py

# Or add a new feature
vim src/inference/app.py
```

### Step 2: Commit and Push

```bash
# Stage changes
git add src/models/cnn_model.py

# Commit with descriptive message
git commit -m "Improve CNN architecture: add dropout layers"

# Push to trigger CI/CD
git push origin main
```

### Step 3: CI Pipeline (Automatic)

**What happens automatically:**
1. GitHub Actions detects push
2. Checks out code
3. Installs dependencies
4. Runs unit tests
5. Builds Docker image
6. Pushes to container registry

**View in GitHub:**
- Go to: https://github.com/ps2program/MLOPS_ASSIGNMENT_2/actions
- See CI pipeline running
- Check test results
- Verify image build

### Step 4: CD Pipeline (Automatic)

**What happens automatically:**
1. CD pipeline triggers on main branch
2. Pulls latest image from registry
3. Deploys to Kubernetes/Docker Compose
4. Runs smoke tests
5. Verifies deployment

### Step 5: Verify Deployment

```bash
# Check service health
curl http://localhost:8000/health

# Make a prediction
curl -X POST -F "file=@data/raw/cats/0.jpg" \
    http://localhost:8000/predict

# Check metrics
curl http://localhost:8000/metrics
```

## Screen Recording Script

For the 5-minute video demonstration:

### Timeline (5 minutes)

**0:00 - 0:30: Setup & Overview**
- Show project structure
- Explain components
- Show dataset (25,038 images)

**0:30 - 1:30: Code Change**
- Make a small code change (e.g., update model)
- Show Git status
- Commit and push

**1:30 - 2:30: CI Pipeline**
- Show GitHub Actions running
- Show tests passing
- Show Docker image building

**2:30 - 3:30: CD Pipeline**
- Show deployment happening
- Show smoke tests running
- Verify deployment success

**3:30 - 4:30: Testing**
- Test health endpoint
- Make predictions
- Show metrics

**4:30 - 5:00: Summary**
- Show MLflow UI
- Show monitoring dashboard
- Summarize workflow

## Quick Demo Commands

```bash
# 1. Make a code change
echo "# Model improvement" >> src/models/cnn_model.py
git add src/models/cnn_model.py
git commit -m "Demo: Improve model"
git push origin main

# 2. Watch CI/CD (in browser)
# https://github.com/ps2program/MLOPS_ASSIGNMENT_2/actions

# 3. Test deployed service
curl http://localhost:8000/health
curl -X POST -F "file=@data/raw/cats/0.jpg" \
    http://localhost:8000/predict

# 4. View MLflow
mlflow ui
# Open http://localhost:5000

# 5. View metrics
curl http://localhost:8000/metrics | grep inference
```

## Industry Workflow Comparison

### Assignment Workflow (Simplified)
```
Code → Git → CI → Build → Deploy → Test
```

### Industry Workflow (Full)
```
Code → Git → CI → Build → Test → Staging → 
Production → Monitor → Alert → Retrain → Deploy
```

## Key Differences

| Aspect | Assignment | Industry |
|--------|-----------|----------|
| **Environments** | Local/Dev | Dev → Staging → Prod |
| **Testing** | Unit + Smoke | Unit + Integration + E2E + Performance |
| **Deployment** | Manual/Auto | Fully automated with approvals |
| **Monitoring** | Basic metrics | Full observability stack |
| **Rollback** | Manual | Automated |
| **Scaling** | Fixed | Auto-scaling |
| **Security** | Basic | Comprehensive (auth, encryption, scanning) |

