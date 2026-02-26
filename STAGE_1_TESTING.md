# 🧪 Stage 1 Testing Guide

## Quick Test (5 minutes)

### Step 1: Verify Virtual Environment Active
```powershell
# PowerShell should show (venv) prefix before prompt
(venv) PS C:\Users\darak\game-bot>

# If not active, run:
.\venv\Scripts\Activate.ps1
```

### Step 2: Verify Package Imports
```powershell
python -c "import cv2, torch, numpy; print('✓ All packages OK')"
```

Should output: `✓ All packages OK`

### Step 3: Verify ADB Connection
```powershell
adb devices
```

Should show your device as `device` (not offline):
```
List of attached devices
xxxxxxxxxxxxxxxx       device
```

### Step 4: Verify Screen Capture
```powershell
adb exec-out screencap -p > test.png
```

Should create `test.png` file. Open it to verify it looks like your game.

---

## Full Test Suite (10-15 minutes)

Run comprehensive Stage 1 tests:

```powershell
python tests/test_stage_1.py
```

This will test:
- ✓ Python version & venv
- ✓ Package imports (OpenCV, PyTorch, etc)
- ✓ ADB connectivity
- ✓ Screen capture functionality
- ✓ Image processing (load, convert, threshold)
- ✓ Grid detection calibration
- ✓ Grid region extraction

**Expected output:**
```
=============================================================
🤖 Stage 1 Test Suite - Screen Capture & Grid Detection
=============================================================

[Test results will show ✓ or ❌ for each subsystem]

Result: 7/7 tests passed
```

---

## Manual Testing Workflow

### 1️⃣ Connect Device

**Windows:**
1. Enable USB Debugging:
   - Settings → About Phone → Build Number (tap 7 times)
   - Settings → Developer Options → USB Debugging (toggle ON)
2. Connect via USB
3. Tap "Allow" on device when prompted

**Verify connection:**
```powershell
adb devices
# Should show: [device-id] device
```

### 2️⃣ Capture Screenshot

```powershell
adb exec-out screencap -p > screenshot.png
```

Open `screenshot.png` in an image viewer/editor.

### 3️⃣ Measure Grid Coordinates

**Using Windows Paint or any image editor:**

1. Open `screenshot.png`
2. Use **Color Picker** tool and hover over grid corners
3. Measure **top-left corner (x, y)** of the 8x8 game board
4. Measure **cell width** (one square in pixels)

Example measurements:
```
Top-left corner: (100, 400)
Cell width: 45 pixels
Grid area: 360x360 pixels (8×45=360)
```

### 4️⃣ Configure Calibration

Edit `game_ai_bot/config.py`:

```python
# Around line 16-17
GRID_TOP_LEFT = (100, 400)  # YOUR measured values
GRID_CELL_SIZE = 45          # YOUR measured cell size
```

### 5️⃣ Measure Color Thresholds

**For empty cells:**
1. Pick an empty grid square in the screenshot
2. Use Color Picker → note RGB values
3. Record Min/Max ranges (usually ±10 from center values)

**For filled cells:**
1. Pick a filled block in the screenshot
2. Color Picker → note RGB values
3. Record Min/Max ranges

Edit `game_ai_bot/config.py` around line 31-41:

```python
COLOR_THRESHOLDS = {
    'empty': {
        'lower': (245, 245, 245),  # Adjust based on your screenshot
        'upper': (255, 255, 255),
    },
    'block': {
        'lower': (100, 100, 100),  # Adjust based on your screenshot
        'upper': (180, 180, 180),
    },
}
```

### 6️⃣ Test Grid Extraction

Run the test to see if grid is extracted correctly:

```powershell
python tests/test_stage_1.py
```

This will create `test_grid_region.png` showing the extracted grid area.

**Check `test_grid_region.png`:**
- Should show just the 8x8 game grid
- No UI chrome around edges
- All 64 cells visible
- If not, adjust `GRID_TOP_LEFT` and `GRID_CELL_SIZE`

---

## Troubleshooting

### ❌ "adb: command not found"
- **Fix**: Download Android SDK Platform Tools
  - https://developer.android.com/tools/releases/platform-tools
  - Extract to `C:\platform-tools`
  - Add to PATH: `$env:PATH += ";C:\platform-tools"`

### ❌ "no devices found"
- Check USB cable connection
- Enable USB Debugging on device
- Tap "Allow" on device permission prompt
- Try: `adb kill-server` then `adb devices`

### ❌ Grid region extracted incorrectly
- Open `test_grid_region.png` to see what was captured
- Adjust `GRID_TOP_LEFT` (x,y coordinates)
- Adjust `GRID_CELL_SIZE` (cell width in pixels)
- Test again

### ❌ "Python module not found"
- Verify venv is active: `(venv)` in prompt
- Reinstall: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.10+)

---

## What Stage 1 Tests

| Test | Purpose | Pass Criteria |
|------|---------|---------------|
| Python Env | Verify 3.10+ in venv | Python 3.10+ active |
| Imports | Load all packages | All 6 packages import successfully |
| ADB | Connect to device | Device shows in `adb devices` |
| Capture | Screenshot from device | PNG file created >100KB |
| Image Load | OpenCV can read PNG | Image loads, dimensions correct |
| Conversions | Color space transforms | HSV/Gray conversions work |
| Calibration | Config values exist | GRID_TOP_LEFT & GRID_CELL_SIZE set |
| Extraction | Extract grid from image | Grid region PNG created |

---

## Performance Targets

- Screenshot capture: <2 seconds
- Image processing: <100ms
- Grid extraction: <50ms
- Total Stage 1 pipeline: <3 seconds per frame

---

## Files Generated During Testing

```
test_screenshot.png       # Raw screenshot from device
test_grid_region.png      # Extracted 8x8 grid region
```

Delete these after testing:
```powershell
Remove-Item test_screenshot.png
Remove-Item test_grid_region.png
```

---

## Success Criteria for Stage 1 ✅

All tests pass when:
- ✓ Device connects via adb
- ✓ Screenshots capture successfully
- ✓ Grid coordinates are calibrated correctly
- ✓ Grid region extracts properly
- ✓ `test_grid_region.png` shows only the 8x8 grid

**Then you're ready for → Stage 2 (Heuristic Engine)**

---

**Estimated Time**: 15-30 minutes for full calibration  
**Difficulty**: Medium (requires manual measurement)  
**Next Stage**: Decision engine & move simulation
