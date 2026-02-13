# MLOps Demo Documentation

Complete guide for creating the 5-minute screen recording demonstrating all 5 assignment modules.

---

## Quick Start

1. **Read:** [DEMO_CHECKLIST.md](DEMO_CHECKLIST.md) - Complete pre-recording setup
2. **Review:** [DEMO_SCRIPT_ASSIGNMENT.md](DEMO_SCRIPT_ASSIGNMENT.md) - Detailed demo script
3. **Practice:** [TIMING_REHEARSAL.md](TIMING_REHEARSAL.md) - Rehearse timing
4. **Reference:** [QUICK_COMMANDS.md](QUICK_COMMANDS.md) - All commands in one place
5. **Guide:** [MODULE_SHOWCASE_GUIDE.md](MODULE_SHOWCASE_GUIDE.md) - How to showcase each module

---

## Files Created

### 1. DEMO_SCRIPT_ASSIGNMENT.md
**Purpose:** Complete step-by-step demo script aligned with assignment requirements

**Contents:**
- Pre-recording checklist
- 7 segments with exact timing
- Commands for each segment
- Narration script
- Troubleshooting tips

**Use:** Primary script to follow during recording

---

### 2. MODULE_SHOWCASE_GUIDE.md
**Purpose:** Detailed guide on how to demonstrate each module (M1-M5)

**Contents:**
- Requirements for each module
- How to showcase each requirement
- Key files to show
- Key commands to run
- What to highlight

**Use:** Reference when preparing each module segment

---

### 3. DEMO_CHECKLIST.md
**Purpose:** Comprehensive pre-recording setup checklist

**Contents:**
- System prerequisites
- Project setup verification
- Dependencies check
- Testing verification
- Recording setup

**Use:** Complete before starting recording

---

### 4. QUICK_COMMANDS.md
**Purpose:** All commands organized by segment for quick reference

**Contents:**
- Commands for each segment
- Quick health checks
- Troubleshooting commands
- Command cheat sheet
- Timing reference

**Use:** Quick reference during recording

---

### 5. TIMING_REHEARSAL.md
**Purpose:** Practice guide to ensure timing stays under 5 minutes

**Contents:**
- Target timing for each segment
- Practice tips
- Time-saving strategies
- Common timing issues and solutions
- Rehearsal schedule

**Use:** Practice before recording

---

## Code Change Prepared

**File:** `src/inference/app.py`

**Change:** Added enhanced logging line for M5 requirement demonstration

**Location:** Line 196-197 in `predict_image()` function

**What it does:**
- Logs timestamp when processing prediction request
- Visible in Kubernetes logs after deployment
- Demonstrates M5 monitoring requirement

**To use in demo:**
1. This change is already in the file
2. Commit and push during Segment 3
3. After deployment, logs will show this new logging line

---

## Demo Flow

```
1. Introduction (0:20)
   └─> Show project structure, overview all modules

2. M1 Showcase (0:30)
   └─> Git/DVC versioning, Model, MLflow

3. Code Change & M2 (0:40)
   └─> Make change, show FastAPI/Docker, commit

4. M3 Showcase (1:00)
   └─> Tests, CI pipeline, image publishing

5. M4 Showcase (1:00)
   └─> Kubernetes, CD pipeline, smoke tests

6. M5 Showcase (1:00)
   └─> Metrics, logs, predictions

7. Summary (0:20)
   └─> Recap all modules

Total: 4:50 (under 5 minutes)
```

---

## Assignment Requirements Coverage

### M1: Model Development & Experiment Tracking ✅
- Git versioning shown
- DVC versioning shown
- Trained model shown
- MLflow tracking shown

### M2: Model Packaging & Containerization ✅
- FastAPI REST API shown
- requirements.txt with pinned versions shown
- Dockerfile shown
- Containerization demonstrated

### M3: CI Pipeline ✅
- Unit tests run and shown
- CI workflow configuration shown
- GitHub Actions demonstrated
- Image publishing mentioned

### M4: CD Pipeline & Deployment ✅
- Kubernetes manifests shown
- CD workflow shown
- Deployment demonstrated
- Smoke tests run and shown

### M5: Monitoring & Logging ✅
- Prometheus metrics shown
- Application logs shown
- Model predictions demonstrated
- Metrics tracking shown

---

## Next Steps

1. **Complete Pre-Recording Checklist**
   - Follow [DEMO_CHECKLIST.md](DEMO_CHECKLIST.md)
   - Verify all systems ready
   - Test all commands

2. **Practice Demo**
   - Use [TIMING_REHEARSAL.md](TIMING_REHEARSAL.md)
   - Run through demo 2-3 times
   - Ensure timing under 5 minutes

3. **Record Demo**
   - Follow [DEMO_SCRIPT_ASSIGNMENT.md](DEMO_SCRIPT_ASSIGNMENT.md)
   - Use [QUICK_COMMANDS.md](QUICK_COMMANDS.md) for reference
   - Keep [MODULE_SHOWCASE_GUIDE.md](MODULE_SHOWCASE_GUIDE.md) handy

4. **Review Recording**
   - Check timing (under 5 minutes)
   - Verify all modules shown
   - Ensure no errors
   - Check audio quality

---

## Tips for Success

1. **Prepare thoroughly:** Complete all checklist items
2. **Practice timing:** Rehearse multiple times
3. **Stay calm:** If something goes wrong, pause and continue
4. **Focus on key points:** Don't explain everything, just show it works
5. **Be confident:** You know your project well

---

## Support Files

- **Assignment PDF:** `MLOPS_Assignment2.pdf`
- **Assignment Checklist:** `ASSIGNMENT_CHECKLIST.md`
- **Workflow Demo:** `WORKFLOW_DEMO.md` (comprehensive, but longer)
- **Setup Guide:** `SETUP.md`

---

## Quick Reference

**Main Script:** [DEMO_SCRIPT_ASSIGNMENT.md](DEMO_SCRIPT_ASSIGNMENT.md)
**Commands:** [QUICK_COMMANDS.md](QUICK_COMMANDS.md)
**Checklist:** [DEMO_CHECKLIST.md](DEMO_CHECKLIST.md)
**Timing:** [TIMING_REHEARSAL.md](TIMING_REHEARSAL.md)
**Modules:** [MODULE_SHOWCASE_GUIDE.md](MODULE_SHOWCASE_GUIDE.md)

---

**Ready to record? Start with the checklist!**
