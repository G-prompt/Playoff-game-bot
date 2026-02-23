# Android 8x8 Block Game AI Bot - Installation Guide

## Prerequisites

### System Requirements
- **Python**: 3.10 or higher
- **OS**: Windows (with PowerShell), macOS, or Linux
- **Android Device**: Android 8.0+ with USB Debugging enabled
- **RAM**: Minimum 4GB (8GB+ recommended for ML training)
- **GPU** (Optional): NVIDIA GPU with CUDA support recommended for PyTorch acceleration

### Required System Dependencies

#### 1. Android SDK Platform Tools (ADB)

**Windows:**
```powershell
# Option A: Using Chocolatey
choco install android-sdk

# Option B: Manual Download
# Download from: https://developer.android.com/tools/releases/platform-tools
# Extract and add to System PATH
```

**macOS:**
```bash
brew install android-platform-tools
```

**Linux:**
```bash
sudo apt-get install android-tools-adb android-tools-fastboot
```

**Verify installation:**
```powershell
adb version
```

#### 2. Enable USB Debugging on Android Device
1. Go to **Settings → About Phone**
2. Tap **Build Number** 7 times to unlock Developer Options
3. Go to **Settings → Developer Options**
4. Enable **USB Debugging**
5. Connect device via USB
6. Accept the RSA fingerprint prompt on your device

**Verify connection:**
```powershell
adb devices
```

---

## Project Setup

### Step 1: Create Python Virtual Environment

**Windows (PowerShell):**
```powershell
cd c:\Users\darak\game-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux:**
```bash
cd ~/game-bot
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Python Dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

### Step 3: Verify Installation

```powershell
# Check Python version
python --version

# Check installed packages
pip list

# Verify OpenCV
python -c "import cv2; print(cv2.__version__)"

# Verify PyTorch
python -c "import torch; print(torch.__version__)"

# Verify ADB
adb version
```

---

## Project Structure

```
game-bot/
├── game_ai_bot/                 # Main application package
│   ├── main.py                  # Entry point / run loop
│   ├── config.py                # Grid coordinates & tuning constants
│   ├── screen_capture.py        # ADB screenshot module
│   ├── grid_detector.py         # 8x8 board detection
│   ├── block_detector.py        # Block shape detection
│   ├── decision_engine.py       # Heuristic + lookahead engine
│   ├── simulator.py             # Board simulation logic
│   ├── evaluation.py            # Scoring functions
│   ├── input_controller.py      # Tap/drag execution
│   ├── learning_engine.py       # Genetic optimization
│   ├── rl_model.py              # Reinforcement learning (future)
│   ├── logger.py                # Game logging system
│   ├── models/                  # Trained weights directory
│   └── logs/                    # Gameplay logs directory
├── tests/                       # Unit tests
├── requirements.txt             # Python dependencies
├── INSTALLATION.md              # This file
└── .gitignore                   # Git ignore rules
```

---

## Configuration

### Initial Setup (config.py)

You'll need to calibrate the game grid coordinates:

1. **Capture a screenshot** of the game board
2. **Identify the top-left corner** of the 8x8 grid (pixel coordinates)
3. **Measure the cell size** (pixel width/height of one grid cell)
4. **Set these in config.py**:

```python
# Example calibration (adjust to your device/game)
GRID_TOP_LEFT = (100, 400)      # (x, y) pixels
GRID_CELL_SIZE = 45              # pixels per cell
COLOR_THRESHOLDS = {
    'empty': (200, 200, 200),
    'filled': (100, 100, 100),
}
```

---

## Quick Start

### 1. Connect Android Device
```powershell
adb devices
```
Expected output:
```
List of attached devices
DEVICE_ID    device
```

### 2. Run the Bot
```powershell
cd c:\Users\darak\game-bot
.\venv\Scripts\Activate.ps1
python game_ai_bot/main.py
```

### 3. Monitor Logs
```powershell
tail -f game_ai_bot/logs/gameplay.log
```

---

## Troubleshooting

### ADB Connection Issues

**Problem**: `adb devices` shows "unauthorized"
```powershell
# Solution: Unplug device, uncheck USB Debugging, re-enable it
adb kill-server
adb start-server
adb devices
```

**Problem**: `adb: command not found` (Windows)
```powershell
# Solution: Add Android SDK to PATH manually
# 1. Download Platform Tools
# 2. Extract to a known location
# 3. Add to System Environment PATH
# Or use: $env:PATH += ";C:\path\to\platform-tools"
```

### Python/Virtual Environment

**Problem**: `ModuleNotFoundError: No module named 'cv2'`
```powershell
pip install opencv-python
```

**Problem**: Virtual environment won't activate
```powershell
# Try this:
python -m venv venv --clear
.\venv\Scripts\Activate.ps1
```

### GPU Support (Optional)

For NVIDIA GPU acceleration in PyTorch:
```powershell
# Uninstall default PyTorch
pip uninstall torch torchvision

# Install CUDA-enabled version
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## Additional Resources

- [ADB Documentation](https://developer.android.com/tools/adb)
- [OpenCV Setup](https://docs.opencv.org/master/d5/de5/tutorial_py_setup_in_windows.html)
- [PyTorch Installation](https://pytorch.org/get-started/locally/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

---

## Next Steps

1. ✅ Install dependencies
2. ⬜ Connect Android device
3. ⬜ Calibrate grid coordinates in `config.py`
4. ⬜ Run Stage 1: Screen capture & grid detection
5. ⬜ Test bot with heuristic engine
6. ⬜ Train with genetic algorithm
7. ⬜ Integrate reinforcement learning

---

**Last Updated**: February 2026
