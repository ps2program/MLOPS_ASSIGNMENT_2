# CI/CD Deployment Information

## Overview

This document explains where the CI and CD pipelines deploy artifacts and services.

---

## CI Pipeline (`.github/workflows/ci.yml`)

### What It Does:
1. **Runs Tests** - Executes pytest unit tests
2. **Builds Docker Image** - Creates containerized application
3. **Pushes to Container Registry** - Stores the image for deployment

### Where It Deploys:

**Container Registry:** GitHub Container Registry (GHCR)

**Image Location:**
```
ghcr.io/ps2program/mlops_assignment_2
```

**Full Image Path:**
```
ghcr.io/ps2program/mlops_assignment_2:<tag>
```

**Image Tags Created:**
- `main` or `develop` (branch name)
- `<commit-sha>` (Git commit SHA)
- Semantic version tags (if using version tags)

**Example Images:**
- `ghcr.io/ps2program/mlops_assignment_2:main`
- `ghcr.io/ps2program/mlops_assignment_2:abc123def` (SHA)
- `ghcr.io/ps2program/mlops_assignment_2:v1.0.0` (if tagged)

**When It Runs:**
- ✅ On every push to `main` or `develop` branches
- ✅ On pull requests to `main` or `develop`
- ❌ Does NOT push images on pull requests (only builds)

**Access:**
- View images at: `https://github.com/ps2program/MLOPS_ASSIGNMENT_2/pkgs/container/mlops_assignment_2`
- Pull image: `docker pull ghcr.io/ps2program/mlops_assignment_2:main`

---

## CD Pipeline (`.github/workflows/cd.yml`)

### What It Does:
1. **Pulls Image** from GHCR
2. **Deploys** to target environment
3. **Runs Smoke Tests** to verify deployment

### Where It Deploys:

The CD pipeline has **TWO deployment targets**:

---

### Target 1: Kubernetes (Primary)

**Deployment Location:** Kubernetes Cluster

**What Gets Deployed:**
- Kubernetes Deployment: `cats-dogs-classifier`
- Kubernetes Service: `cats-dogs-classifier-service`
- Namespace: `default`

**Image Used:**
```yaml
image: ghcr.io/ps2program/mlops_assignment_2:<commit-sha>
```

**Deployment Manifest:**
- File: `deployment/kubernetes/deployment.yaml`
- Replicas: 2 pods
- Service Type: NodePort

**Current Status:**
⚠️ **Note:** The CD pipeline has a placeholder for kubectl configuration. In practice:
- For **local kind cluster**: Would need to configure kubeconfig
- For **cloud Kubernetes** (GKE, EKS, AKS): Would need cluster credentials
- For **GitHub Actions**: Would run in the Actions runner (ephemeral)

**What Happens:**
1. Updates deployment.yaml with new image tag
2. Runs `kubectl apply -f deployment/kubernetes/deployment.yaml`
3. Waits for rollout: `kubectl rollout status`
4. Runs smoke tests against deployed service

**Access After Deployment:**
- Service endpoint via NodePort or LoadBalancer
- Port-forward: `kubectl port-forward svc/cats-dogs-classifier-service 8000:80`
- Then access: `http://localhost:8000`

---

### Target 2: Docker Compose (Alternative)

**Deployment Location:** GitHub Actions Runner (Ubuntu VM)

**What Gets Deployed:**
- Docker Compose stack
- Services: `classifier-api` and `prometheus`

**Image Used:**
```bash
docker pull ghcr.io/ps2program/mlops_assignment_2:<commit-sha>
# Tagged as: cats-dogs-classifier:latest
```

**Deployment Location:**
- Directory: `deployment/docker-compose/`
- Command: `docker-compose up -d`

**What Happens:**
1. Pulls image from GHCR
2. Tags it as `cats-dogs-classifier:latest`
3. Runs `docker-compose up -d`
4. Waits for health check: `http://localhost:8000/health`
5. Runs smoke tests

**Access After Deployment:**
- API: `http://localhost:8000`
- Prometheus: `http://localhost:9090`

**Note:** This deployment is **ephemeral** - it only exists during the GitHub Actions workflow run.

---

## Summary Table

| Pipeline | Artifact | Destination | Access |
|----------|----------|-------------|--------|
| **CI** | Docker Image | `ghcr.io/ps2program/mlops_assignment_2` | GitHub Container Registry |
| **CD (K8s)** | Kubernetes Deployment | Kubernetes Cluster | Via kubectl/Service |
| **CD (Docker Compose)** | Docker Containers | GitHub Actions Runner | `http://localhost:8000` |

---

## Current Deployment Status

### CI Pipeline:
✅ **Working** - Pushes images to GHCR on push to main/develop

### CD Pipeline:
⚠️ **Partially Configured** - Two deployment options:

1. **Kubernetes Deployment:**
   - ✅ Code is ready
   - ⚠️ Needs kubectl configuration for actual cluster
   - ⚠️ Currently has placeholder comments
   - **For local kind cluster:** Would need to export kubeconfig
   - **For cloud:** Would need cluster credentials/secrets

2. **Docker Compose Deployment:**
   - ✅ Fully configured
   - ✅ Works in GitHub Actions runner
   - ⚠️ Ephemeral (only during workflow run)

---

## How to View Deployed Images

### GitHub Container Registry:
1. Go to: `https://github.com/ps2program/MLOPS_ASSIGNMENT_2`
2. Click on **"Packages"** tab
3. Or directly: `https://github.com/ps2program/MLOPS_ASSIGNMENT_2/pkgs/container/mlops_assignment_2`

### Pull Image Locally:
```bash
# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Pull image
docker pull ghcr.io/ps2program/mlops_assignment_2:main
```

---

## Local vs CI/CD Deployment

### Local Development:
- Build: `docker build -t cats-dogs-classifier:latest .`
- Run: `docker run -p 8000:8000 cats-dogs-classifier:latest`
- Or: `docker-compose up` in `deployment/docker-compose/`

### CI/CD (Automated):
- **CI:** Builds and pushes to `ghcr.io/ps2program/mlops_assignment_2`
- **CD:** Pulls from GHCR and deploys to Kubernetes or Docker Compose

---

## Environment Variables Used

### CI Pipeline:
- `REGISTRY`: `ghcr.io`
- `IMAGE_NAME`: `${{ github.repository }}` (ps2program/MLOPS_ASSIGNMENT_2)
- `GITHUB_TOKEN`: Auto-provided by GitHub Actions

### CD Pipeline:
- `REGISTRY`: `ghcr.io`
- `IMAGE_NAME`: `${{ github.repository }}`
- `GITHUB_SHA`: Commit SHA for image tagging

---

## Next Steps for Production

To make CD pipeline fully functional:

1. **For Kubernetes:**
   - Set up kubectl credentials in GitHub Secrets
   - Configure kubeconfig for target cluster
   - Update CD workflow to use actual cluster

2. **For Cloud Deployment:**
   - Add cloud provider credentials (GCP, AWS, Azure)
   - Configure cluster connection
   - Set up LoadBalancer or Ingress

3. **For Local Testing:**
   - Use kind/minikube in GitHub Actions
   - Export kubeconfig from kind cluster
   - Deploy to ephemeral cluster
