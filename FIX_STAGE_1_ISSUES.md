# 🔧 Fix Stage 1 Issues

## Issue 1: NumPy/OpenCV Compatibility ✅ WORKAROUND

The problem is torchvision installs NumPy 2.x, but OpenCV was compiled for NumPy 1.x.

**Temporary solution**: Use simulation mode for Stage 1 testing (no ADB/camera needed).

Edit `game_ai_bot/config.py` line ~185:
```python
SIMULATION_MODE = True  # Simulate without device
```

Then Stage 1 tests will work without OpenCV.

**Permanent solution** (when network is stable):
```powershell
pip uninstall numpy -y
pip install numpy==1.24.3
pip install opencv-python==4.8.1.78
```

---

## Issue 2: ADB Not Found in PATH ⚠️ CRITICAL

You need to download and configure Android SDK Platform Tools.

### Step 1: Download Android SDK Tools

1. Go to: https://developer.android.com/tools/releases/platform-tools
2. Click download for Windows (or your OS)
3. Extract the ZIP file to a folder, e.g., `C:\platform-tools\`

### Step 2: Add to PATH (Windows)

**Option A: Temporary (current session only)**
```powershell
$env:PATH += ";C:\platform-tools"
adb version  # Test
```

**Option B: Permanent (recommended)**

1. Open **Settings** → **System** → **About**
2. Click **Advanced system settings**
3. Click **Environment Variables**
4. Under "User variables", click **New**
   - Variable name: `PATH`
   - Variable value: `C:\platform-tools`
5. Click OK, OK, OK
6. **Close PowerShell and reopen it** (changes take effect)
7. Test: `adb version`

### Step 3: Verify ADB Works

```powershell
adb version
# Should output Android Debug Bridge version info

# Then connect your Android device and run:
adb devices
# Should show: [device-id]    device
```

---

## Recommended Testing Path

Since you have both issues, I recommend:

### Phase 1: Setup ADB (no Python needed)
1. ✅ Download and extract Android SDK Platform Tools
2. ✅ Add to PATH permanently
3. ✅ Verify: `adb devices` shows your connected device

### Phase 2: Fix Python Packages (with better network)
1. Use simulation mode in config.py for now
2. Test grid detection with mock data
3. Fix numpy/opencv compatibility when network improves

### Phase 3: Full Integration
1. Disable SIMULATION_MODE
2. Run full Stage 1 tests with device connected

---

## Quick Commands to Test Each Component

**Test ADB only:**
```powershell
# After adding to PATH and reopening PowerShell
adb devices
adb version
```

**Test Python packages (without OpenCV):**
```powershell
python -c "import torch, numpy; print('✓ Torch & NumPy OK')"
```

**Test with mock device (simulation mode):**
```powershell
# With SIMULATION_MODE = True in config.py
python tests/test_stage_1.py
```

---

## Priority Actions

**DO THIS FIRST:**
1. Download Android SDK Platform Tools: https://developer.android.com/tools/releases/platform-tools
2. Extract to `C:\platform-tools`
3. Add to Windows PATH (permanently)
4. Restart PowerShell
5. Verify: `adb devices`

**THEN:**
- Decide if you want to wait for network to fix packages, or use SIMULATION_MODE
- Run Stage 1 tests

---

## File Locations

After downloading, you should have:
```
C:\platform-tools\
├── adb.exe
├── fastboot.exe
├── platform-tools.jar
└── ... other files
```

Then PowerShell will recognize: `adb devices`, `adb version`, etc.

---

## Next Steps

Once ADB is working, reply and I'll help you continue Stage 1 testing!
