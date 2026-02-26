# Android 8x8 Block Game AI Bot - Setup Guide

## Prerequisites

- **Python 3.10+** (verified: 3.13.7 ✓)
- **Windows/Mac/Linux** with USB debugging support
- **Android Device** with USB Debugging enabled
- **USB Cable** for device connection

## System Dependencies

### Windows
1. **Android SDK Platform Tools (ADB)**
   - Download: https://developer.android.com/tools/releases/platform-tools
   - Extract to: `C:\platform-tools`
   - Add to PATH: Open System Properties → Environment Variables → Add `C:\platform-tools`
   - Verify: Open PowerShell and run `adb version`

2. **USB Driver** (if needed)
   - Install manufacturer's USB driver
   - Go to Settings → About → Build Number (tap 7 times to enable Developer Mode)
   - Enable USB Debugging in Developer Options

### macOS
```bash
brew install android-platform-tools
adb version  # Verify
```

### Linux
```bash
sudo apt-get install android-tools-adb
adb version  # Verify
```

## Python Environment Setup

### Step 1: Create Virtual Environment ✓ COMPLETED
```powershell
cd c:\Users\darak\game-bot
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies ✓ COMPLETED
```powershell
pip install --upgrade pip setuptools wheel
pip install opencv-python numpy pillow torch torchvision scikit-learn
```

**Installed Packages:**
- ✅ opencv-python (4.8.1.78) - Computer vision
- ✅ numpy (2.4.2) - Numerical computing
- ✅ pillow (12.1.1) - Image processing
- ✅ torch (2.10.0) - Deep learning
- ✅ torchvision (0.25.0) - Vision models
- ✅ scikit-learn - Machine learning utilities

### Step 3: Verify Installation
```powershell
python -c "import cv2, torch, numpy; print('All packages installed!')"
```

## Device Setup

### 1. Enable USB Debugging on Android Device

**Android 10+:**
1. Settings → About Phone → Build Number (tap 7 times)
2. Settings → System → Developer Options → USB Debugging (enable)
3. Connect device via USB
4. On device, tap "Allow" when prompted

**Android 9 and earlier:**
1. Settings → About Phone → Build Number (tap 7 times)
2. Settings → Developer Options → USB Debugging (enable)
3. Connect device via USB
4. On device, tap "Allow" when prompted

### 2. Verify ADB Connection
```powershell
adb devices
# Should show: [device-id] device
```

### 3. Test Screen Capture
```powershell
adb exec-out screencap -p > test_screenshot.png
```
If successful, you'll have `test_screenshot.png` in your directory.

## Project Structure

```
game-bot/
├── venv/                          # Virtual environment
├── game_ai_bot/                   # Main package
│   ├── __init__.py
│   ├── main.py                    # Entry point
│   ├── config.py                  # Configuration (⚠️ Needs calibration)
│   ├── screen_capture.py          # ADB screenshot module
│   ├── grid_detector.py           # 8x8 grid detection
│   ├── block_detector.py          # Block shape detection
│   ├── decision_engine.py         # Heuristic + lookahead
│   ├── simulator.py               # Board simulation
│   ├── evaluation.py              # Scoring functions
│   ├── input_controller.py        # Touch input executor
│   ├── learning_engine.py         # Genetic algorithm
│   ├── rl_model.py                # Deep Q-Learning (future)
│   ├── logger.py                  # Game logging
│   ├── models/                    # Saved model weights
│   └── logs/                      # Gameplay logs
├── tests/                         # Unit tests
├── requirements.txt               # Python dependencies
├── SETUP.md                       # This file
└── README.md                      # Project overview
```

## Critical Calibration Steps

### ⚠️ BEFORE FIRST RUN:

Edit `game_ai_bot/config.py` and calibrate:

1. **Grid Coordinates** (Lines 16-17)
   - Run: `python -c "from game_ai_bot.screen_capture import capture_screenshot; img = capture_screenshot(); print(img.shape)"`
   - Measure top-left corner of game board from screenshot
   - Update: `GRID_TOP_LEFT = (x, y)`
   - Measure cell size: `GRID_CELL_SIZE = pixels`

2. **Color Thresholds** (Lines 31-41)
   - Take a screenshot of an empty cell and filled cell
   - Use a color picker tool to get RGB values
   - Update `COLOR_THRESHOLDS` accordingly

3. **Device ID** (Line 170)
   - If multiple devices connected, run `adb devices`
   - Update: `ANDROID_DEVICE_ID = 'DEVICE_ID'`

## Running the Bot

### Development Mode (No ADB)
```powershell
cd game-bot
.\venv\Scripts\Activate.ps1
# Set SIMULATION_MODE = True in config.py
python -m game_ai_bot.main
```

### Production Mode (With Device)
```powershell
cd game-bot
.\venv\Scripts\Activate.ps1
python -m game_ai_bot.main
```

## Troubleshooting

### "ADB: device not found"
- Verify USB cable connection
- Check device has USB Debugging enabled
- Try: `adb kill-server && adb devices`

### "Python module not found"
- Verify venv is activated: `(venv)` should appear in terminal
- Reinstall: `pip install -r requirements.txt`

### "Grid detection fails"
- Calibrate `GRID_TOP_LEFT` and `GRID_CELL_SIZE`
- Check `COLOR_THRESHOLDS` match your device's color scheme
- Enable `DEBUG_SHOW_DETECTIONS = True` to see detection images

### Slow performance
- Reduce `LOOKAHEAD_DEPTH` (default: 2)
- Reduce `TOP_N_MOVES` (default: 10)
- Enable `USE_GRID_CACHE = True` (already enabled)

## Next Steps

1. ✅ Virtual environment created
2. ✅ Dependencies installed
3. ⏭️ **Device calibration** (grid coordinates, colors)
4. ⏭️ Create core modules (Stage 1-2)
5. ⏭️ Test screen capture and grid detection
6. ⏭️ Implement heuristic engine
7. ⏭️ Add lookahead search
8. ⏭️ Genetic algorithm training
9. ⏭️ Reinforcement learning upgrade

## Questions?

See `README.md` for architecture overview and feature descriptions.
