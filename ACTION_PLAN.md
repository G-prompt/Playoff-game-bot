# 🚀 ACTION PLAN - Fix Stage 1 & Continue Testing

## Current Status

❌ **Issue 1**: `adb: command not found` - Android SDK Tools not in PATH  
⚠️ **Issue 2**: NumPy/OpenCV compatibility - Can work around with simulation mode

---

## ✅ Solution Path (Choose One)

### Option A: Automated Setup (Recommended)

```powershell
cd c:\Users\darak\game-bot
python scripts/setup_adb.py
```

This script will:
1. ✓ Download Android SDK Platform Tools
2. ✓ Extract to `C:\platform-tools` 
3. ✓ Add to Windows PATH automatically
4. ✓ Verify ADB works

After it completes:
- Close PowerShell completely
- Reopen PowerShell  
- Run: `adb devices`

---

### Option B: Manual Setup

1. **Download**: https://developer.android.com/tools/releases/platform-tools
2. **Extract**: Unzip to `C:\platform-tools\`
3. **Add to PATH**:
   - Settings → System → About → Advanced system settings
   - Environment Variables → New
   - Variable: `PATH`
   - Value: `C:\platform-tools`
   - OK, OK, OK
4. **Restart PowerShell** (close & reopen)
5. **Verify**: `adb devices`

---

## Stage 1 Testing Order

### Step 1: Get ADB Working
```powershell
adb version
# Should show: Android Debug Bridge version info
```

### Step 2: Connect Your Device
```powershell
adb devices
# Should show: [device-id]    device
```

### Step 3: Take Screenshot (Calibration)
```powershell
adb exec-out screencap -p > screenshot.png
# Open screenshot.png to measure grid coordinates
```

### Step 4: Update config.py
Edit `game_ai_bot/config.py` with your measurements:
```python
GRID_TOP_LEFT = (x, y)    # Your measured top-left corner
GRID_CELL_SIZE = pixels   # Your measured cell width
```

### Step 5: Run Full Test Suite
```powershell
python tests/test_stage_1.py
```

---

## NumPy Compatibility Workaround (If Needed)

If you see: `numpy.core.multiarray failed to import`

**Option 1**: Use simulation mode (no device needed):
```python
# In game_ai_bot/config.py around line 185
SIMULATION_MODE = True
```

**Option 2**: Fix packages (when network is stable):
```powershell
pip uninstall numpy -y
pip install numpy==1.24.3
pip install opencv-python==4.8.1.78
```

---

## Quick Reference Commands

```powershell
# After ADB is set up in PATH:
adb version                          # Verify installation
adb devices                          # List connected devices
adb exec-out screencap -p > s.png   # Take screenshot

# Python testing:
python -c "import torch, numpy; print('OK')"  # Quick import test
python tests/test_stage_1.py         # Full Stage 1 test suite
python quick_test.py                 # 1-minute verification
```

---

## Timeline

- **ADB Setup**: 5-10 minutes
- **Device Calibration**: 10-15 minutes  
- **Full Stage 1 Test**: 5-10 minutes
- **Total**: ~30 minutes to completion ✓

---

## I Recommend:

**DO THIS NOW** (Pick one option):
1. Run: `python scripts/setup_adb.py` (automated)
2. OR follow "Option B: Manual Setup" above

Then reply and tell me:
- ✓ `adb version` works
- ✓ `adb devices` shows your device
- ✓ Screenshot captured successfully

Then I'll guide you through the grid calibration! 🎮
