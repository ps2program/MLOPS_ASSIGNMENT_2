# Timing Rehearsal Guide

Practice guide to ensure the demo stays under 5 minutes while showcasing all modules effectively.

---

## Target Timing Breakdown

| Segment | Target Time | Module | Key Actions |
|---------|-------------|--------|-------------|
| **1. Intro** | 0:20 | All | Project structure, overview |
| **2. M1** | 0:30 | M1 | Git/DVC, Model, MLflow |
| **3. Code Change & M2** | 0:40 | M2 | FastAPI, Docker, commit |
| **4. M3** | 1:00 | M3 | Tests, CI config |
| **5. M4** | 1:00 | M4 | K8s, CD, smoke tests |
| **6. M5** | 1:00 | M5 | Metrics, logs, predictions |
| **7. Summary** | 0:20 | All | Checklist recap |
| **TOTAL** | **4:50** | **All** | **Under 5 min** |

---

## Segment-by-Segment Rehearsal

### Segment 1: Introduction (20 seconds)

**Practice:**
1. Say: "This is our complete MLOps pipeline..." (5s)
2. Run: `ls -la` and `tree` command (5s)
3. Narrate module checklist (10s)

**Timing Tips:**
- Don't wait for tree output - start narrating immediately
- Keep narration concise
- Move quickly to next segment

**If over time:**
- Skip detailed tree output
- Just show `ls` and narrate structure

---

### Segment 2: M1 Showcase (30 seconds)

**Practice:**
1. Git log: `git log --oneline -5` (5s)
2. DVC: `cat data/raw.dvc` (5s)
3. Model: `ls -lh models/best_model.pt` (5s)
4. MLflow: `ls mlruns/` (5s)
5. Narration (10s)

**Timing Tips:**
- Pre-run commands to see output length
- Don't read full DVC file - just show it exists
- Skip MLflow UI if slow - just show directory

**If over time:**
- Skip MLflow entirely, just mention it
- Combine Git and DVC into one command block

---

### Segment 3: Code Change & M2 (40 seconds)

**Practice:**
1. Open IDE, make change (10s)
2. Show FastAPI endpoints: `grep` (5s)
3. Show Dockerfile: `head` (5s)
4. Show requirements: `grep` (5s)
5. Commit and push: `git add/commit/push` (10s)
6. Narration (5s)

**Timing Tips:**
- Have code change prepared - just add one line
- Don't explain code in detail - just show it
- Git push may take time - mention it triggers CI

**If over time:**
- Skip showing Dockerfile/requirements in detail
- Just mention they exist
- Focus on code change and commit

---

### Segment 4: M3 Showcase (60 seconds)

**Practice:**
1. Show CI config: `cat ci.yml` (10s)
2. Run tests: `pytest` (30s)
3. Show GitHub Actions (20s)

**Timing Tips:**
- Pre-run pytest before recording
- Show test results quickly - don't read all output
- If GitHub Actions slow, just show config and mention it runs

**If over time:**
- Skip GitHub Actions UI entirely
- Just show CI config and test results
- Mention: "CI runs automatically on push"

---

### Segment 5: M4 Showcase (60 seconds)

**Practice:**
1. Show CD config: `head cd.yml` (5s)
2. Show K8s manifest: `kubectl get` (5s)
3. Deploy: `kubectl set image` (10s)
4. Watch rollout: `kubectl rollout status` (20s)
5. Smoke tests: `bash smoke_tests.sh` (15s)
6. Narration (5s)

**Timing Tips:**
- Pre-deploy before recording if possible
- Show deployment status instead of waiting
- Smoke tests should be fast - they're simple

**If over time:**
- Skip watching rollout - just show final status
- Pre-run smoke tests, just show results
- Focus on showing deployment succeeded

---

### Segment 6: M5 Showcase (60 seconds)

**Practice:**
1. Show metrics: `curl /metrics` (10s)
2. Show logs: `kubectl logs` (10s)
3. Cat prediction: `curl /predict` (15s)
4. Dog prediction: `curl /predict` (15s)
5. Updated metrics: `curl /metrics` (5s)
6. Narration (5s)

**Timing Tips:**
- Predictions are the KEY demo - don't rush these
- Show JSON output clearly
- Metrics should be quick - just grep for key metrics

**If over time:**
- Make only one prediction instead of two
- Skip showing updated metrics
- Focus on one good prediction example

---

### Segment 7: Summary (20 seconds)

**Practice:**
1. Show checklist (10s)
2. Final narration (10s)

**Timing Tips:**
- Have checklist prepared visually
- Keep narration brief and confident
- End strong with "All 5 modules showcased"

**If over time:**
- Skip detailed checklist
- Just narrate: "All 5 modules complete"
- End quickly

---

## Full Rehearsal Schedule

### First Rehearsal: Timing Check
- Run through entire demo
- Time each segment
- Note which segments run over
- Adjust for next rehearsal

### Second Rehearsal: Flow Check
- Focus on smooth transitions
- Practice narration
- Ensure commands work
- Fix any issues

### Third Rehearsal: Final Polish
- Run at target pace
- Practice key phrases
- Ensure under 5 minutes
- Ready to record

---

## Time-Saving Strategies

### Pre-Recording Preparation
- [ ] Pre-run slow commands (pytest, kubectl rollout)
- [ ] Have outputs ready to show
- [ ] Pre-deploy if possible
- [ ] Have checklist visual ready

### During Recording
- [ ] Don't wait for slow outputs - narrate while running
- [ ] Use `head` and `grep` to limit output
- [ ] Skip detailed explanations
- [ ] Keep narration concise

### Command Optimizations
```bash
# Instead of waiting for full output:
kubectl rollout status deployment/cats-dogs-classifier --timeout=60s

# Show status immediately:
kubectl get pods -l app=cats-dogs-classifier

# Instead of full file:
cat .github/workflows/ci.yml

# Show key parts:
head -20 .github/workflows/ci.yml
```

---

## Common Timing Issues

### Issue: Segment 2 (M1) takes too long
**Solution:**
- Skip MLflow UI
- Just show directory structure
- Combine commands

### Issue: Segment 4 (M3) takes too long
**Solution:**
- Pre-run pytest
- Skip GitHub Actions UI
- Just show config and mention it runs

### Issue: Segment 5 (M4) takes too long
**Solution:**
- Pre-deploy before recording
- Skip rollout watching
- Just show final status

### Issue: Segment 6 (M5) takes too long
**Solution:**
- Make only one prediction
- Skip updated metrics
- Focus on one good example

---

## Practice Checklist

Before recording, practice:

- [ ] Segment 1: Can complete in 20 seconds
- [ ] Segment 2: Can complete in 30 seconds
- [ ] Segment 3: Can complete in 40 seconds
- [ ] Segment 4: Can complete in 60 seconds
- [ ] Segment 5: Can complete in 60 seconds
- [ ] Segment 6: Can complete in 60 seconds
- [ ] Segment 7: Can complete in 20 seconds
- [ ] Full demo: Under 5 minutes total

---

## Rehearsal Script

**Practice this narration:**

> "This is our complete MLOps pipeline implementing all 5 assignment modules. M1: Git/DVC versioning, CNN model, MLflow tracking. M2: FastAPI REST API and Docker containerization. M3: CI pipeline with tests and image publishing. M4: CD pipeline with Kubernetes deployment. M5: Monitoring with Prometheus metrics. Now let's see the complete workflow from code change to deployed prediction."

> "M1 requirements: Git tracks source code, DVC tracks 25,000 image dataset, CNN model trained and saved, MLflow tracks experiments."

> "Making a code change to enhance logging. M2 requirements: FastAPI REST API with health and prediction endpoints, Dockerfile containerizes service, requirements.txt pins versions. Committing and pushing triggers CI/CD."

> "M3 requirements: Unit tests for preprocessing and inference - all pass, GitHub Actions CI pipeline runs automatically, builds and publishes Docker image."

> "M4 requirements: Kubernetes deployment manifests, CD pipeline deploys automatically, smoke tests verify deployment."

> "M5 requirements: Prometheus metrics track requests and latency, structured logging shows predictions, model successfully making predictions with high accuracy."

> "Complete MLOps workflow demonstrated: Code change → CI tests and builds → CD deploys → Monitoring tracks → Model predicts. All 5 assignment modules showcased in under 5 minutes."

---

## Timing Tools

**Use a timer:**
```bash
# Start timer
date +%s > /tmp/demo_start

# Check elapsed time
echo "Elapsed: $(($(date +%s) - $(cat /tmp/demo_start))) seconds"
```

**Or use stopwatch:**
- Phone stopwatch
- Online timer
- Recording software timer

---

## Final Tips

1. **Practice makes perfect:** Run through 2-3 times before recording
2. **Stay calm:** If you go over, don't panic - you can edit or retake
3. **Focus on key points:** Don't explain everything, just show it works
4. **Keep moving:** Don't pause too long between segments
5. **Be confident:** You know your project - trust yourself

---

## Success Metrics

✅ Each segment within target time
✅ Total time under 5 minutes
✅ All modules clearly shown
✅ Smooth transitions
✅ Clear narration
✅ No errors or failures

**You're ready when you can complete the demo in 4:50 or less!**
