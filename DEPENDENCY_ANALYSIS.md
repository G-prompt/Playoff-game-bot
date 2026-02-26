# 📊 Dependency Analysis - Stage 1 Stable Setup

## Current State

**Python Version**: 3.13.7 ✓ (exceeds 3.10 requirement)

**Currently Installed**:
```
✓ numpy           2.4.2      (Stable, we have it)
✓ pillow         12.1.1      (Stable, we have it)
✓ Django          6.0.1      (Not needed, leftover)
✓ Various utils   (Django dependencies, not needed)
```

**Removed Due to Conflicts**:
```
❌ opencv-python        (Compiled for NumPy 1.x, conflicts with 2.4.2)
❌ torch               (Pulled in NumPy 2.4.2, but we don't need it yet)
❌ torchvision        (Pulled in with torch)
```

---

## What Each Stage Actually Needs

### Stage 1: Screen Capture & Grid Detection (CURRENT)
**Purpose**: Test ADB, capture screenshots, extract grid

**Actual Imports in Code**:
- `numpy` ✓ (we have 2.4.2)
- `PIL/Pillow` ✓ (we have 12.1.1)
- `random` (stdlib - free)
- `subprocess` (stdlib - free)
- `pathlib` (stdlib - free)

**Real Requirement**: Only `numpy` + `Pillow` = **2 packages**

**OpenCV Status**: NOT NEEDED FOR SIMULATION MODE
- Only used for real device screenshots (Stage 1 Part B)
- Can skip until device is connected
- Version conflicts are resolved when we have a stable environment

---

### Stage 2: Heuristic Engine (Next)
**Purpose**: Move simulation, board evaluation, scoring

**New Imports Needed**: None (uses what Stage 1 has)

**Requirement**: Still just `numpy` + `Pillow`

---

### Stage 3: Lookahead Search
**Purpose**: Simulate multiple moves, search trees

**New Imports Needed**: None

**Requirement**: Still just `numpy` + `Pillow`

---

### Stage 4: Genetic Algorithm
**Purpose**: Optimize heuristic weights across generations

**New Imports Needed**: 
- `numpy` (already have)
- Optional: `scikit-learn` (for statistical analysis)

**Requirement**: `numpy` + `Pillow` + (optional `scikit-learn`)

---

### Stage 5: Reinforcement Learning (Future)
**Purpose**: Deep Q-Network, neural network training

**New Imports Needed**:
- `torch` (PyTorch)
- `torchvision`

**Requirement**: Everything above + `torch` + `torchvision`

---

## Stable Dependency Matrix

| Package | Version | Stage 1-4 | Stage 5+ | Status |
|---------|---------|-----------|----------|--------|
| numpy | 2.4.2 | ✓ Need | ✓ Need | **STABLE** |
| pillow | 12.1.1 | ✓ Need | ✓ Need | **STABLE** |
| opencv | TBD | ⏳ Optional*| ✓ Need | **CONFLICT** |
| torch | Latest | ✗ Don't need | ✓ Need | **NOT NOW** |
| scikit-learn | Latest | ⏳ Optional | ✓ Need | **LATER** |

*OpenCV only needed when connecting real device for screenshot processing

---

## Problem: OpenCV Conflict

**Root Cause**: 
- OpenCV 4.8.x compiled with NumPy 1.x API
- NumPy 2.4.2 changed the internal API (_ARRAY_API removed)
- Python 3.13 doesn't have pre-built wheels for older numpy+opencv combo

**Solutions**:

### Solution A: Skip OpenCV for Now (RECOMMENDED)
```python
# game_ai_bot/config.py
SIMULATION_MODE = True  # Use mock screenshots
```
- ✓ Test everything without device
- ✓ No version conflicts
- ✓ Can add real device later when environment is stable
- ⏳ Defer OpenCV to when we connect device

### Solution B: Use Different Python Version
```
Python 3.11 or 3.12 (more compatible wheels available)
```
- ✓ More pre-built wheels available
- ⏳ Requires new venv

### Solution C: Build OpenCV from Source
```
Requires C++ compiler + build tools
```
- ✗ Complex, time-consuming
- ✗ Not recommended

---

## Stable Minimal Install (Recommended Now)

### Clean Start:
```powershell
# Keep what we have (already good)
pip list
# numpy       2.4.2  ✓
# pillow     12.1.1  ✓

# Remove Django (not needed)
pip uninstall Django asgiref sqlparse -y

# Verify
python -c "import numpy, PIL; print('✓ Core dependencies OK')"
```

### Result: Clean, Conflict-Free Environment
```
✓ numpy       2.4.2
✓ pillow     12.1.1
✓ Python      3.13.7
```

This is **ALL YOU NEED** for Stages 1-4!

---

## When to Add More Packages

| Event | Action | Command |
|-------|--------|---------|
| Ready for device screenshots | Add OpenCV properly | `pip install opencv-python-headless` (test compatibility) |
| Building AI model (Stage 5) | Add PyTorch | `pip install torch torchvision` |
| Statistical analysis | Add scikit-learn | `pip install scikit-learn` |

---

## Recommended Next Steps

### Option 1: Clean Environment NOW (5 minutes)
```powershell
# Remove unused packages
pip uninstall Django asgiref sqlparse -y
pip list  # Verify clean

# Run Stage 1 simulation tests
python tests/test_stage_1_simulation.py

# Result: 7/7 tests passing (no OpenCV conflicts)
```

### Option 2: Test with Minimal Code
```powershell
# Skip all installations, just test what we have
python -c "
import numpy as np
from PIL import Image
print('✓ numpy', np.__version__)
print('✓ PIL ready')
print('✓ Ready for Stage 1!')
"
```

### Option 3: Wait for Stable venv Fresh Start
```powershell
# When you're ready for fresh install
deactivate  # Exit current venv
rmdir venv /s  # Delete old venv
python -m venv venv_clean
.\venv_clean\Scripts\Activate.ps1

# Install only what Stage 1-4 needs:
pip install numpy==2.4.2 pillow>=12.0
```

---

## My Recommendation

**Do this now**:

1. **Clean up** - Remove Django packages (not needed):
```powershell
pip uninstall Django asgiref sqlparse -y
```

2. **Verify** - Test Stage 1 works with what we have:
```powershell
python -c "import numpy, PIL; print('Ready')"
python tests/test_stage_1_simulation.py
```

3. **Continue** - Build Stages 1-4 with just `numpy` + `PIL`

4. **Later** - When you need real device or ML:
   - Connect device → add OpenCV properly
   - Build neural network → add torch

---

## Why This Works

✓ **numpy 2.4.2** - Latest, stable, no conflicts with PIL  
✓ **pillow 12.1.1** - Latest, stable, pure Python mostly  
✓ **Python 3.13.7** - Latest, what you have  
✓ **No OpenCV** - Can add cleanly when needed  
✓ **No torch** - Don't need until Stage 5  

**Total**: 2 production dependencies. Clean. Simple. Stable.

---

**Summary**: You have a **perfectly good environment** already. Just remove the Django deps and you're set for Stages 1-4!
