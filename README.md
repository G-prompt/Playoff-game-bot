# Android 8x8 Block Game AI Bot

An advanced external automation AI agent that connects to a native Android 8x8 block puzzle game via USB debugging (ADB), captures screen frames, detects grid and blocks using computer vision, simulates moves using heuristic + lookahead search, learns using genetic optimization, and later upgrades to reinforcement learning.

## 🎮 Project Overview

This bot is designed to:
- 📱 Connect to an Android device via ADB (USB Debugging)
- 🖼️ Capture and analyze game screenshots
- 🔍 Detect 8x8 grid and block placements using OpenCV
- 🧠 Make intelligent moves using heuristic evaluation + lookahead search
- 🤖 Behave like a human player (with natural delays and occasional suboptimal moves)
- 📈 Learn and improve through genetic algorithm optimization
- 🔮 Eventually upgrade to reinforcement learning (Deep Q-Network)

## 📋 Quick Setup

### Prerequisites
- Python 3.10+
- Android device with USB Debugging enabled
- Android SDK Platform Tools (ADB)

### Installation
```powershell
# Clone/navigate to project
cd c:\Users\darak\game-bot

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

For detailed installation instructions, see [INSTALLATION.md](INSTALLATION.md)

## 🏗️ Project Structure

```
game_ai_bot/
├── main.py              # Main run loop
├── config.py            # Configuration (grid coords, thresholds, etc)
├── screen_capture.py    # ADB screenshot capture
├── grid_detector.py     # 8x8 grid detection
├── block_detector.py    # Block shape detection
├── decision_engine.py   # Heuristic + lookahead AI
├── simulator.py         # Board state simulation
├── evaluation.py        # Scoring functions
├── input_controller.py  # Human-like input/tap execution
├── learning_engine.py   # Genetic weight optimization
├── rl_model.py          # Reinforcement learning (future)
├── logger.py            # Logging system
├── models/              # Saved trained weights
└── logs/                # Gameplay logs
```

## 🚀 Development Stages

| Stage | Goal | Status |
|-------|------|--------|
| 1 | Stable screen capture + grid detection | ⏳ |
| 2 | Heuristic placement engine | ⏳ |
| 3 | Depth-2 lookahead search | ⏳ |
| 4 | Genetic weight tuning | ⏳ |
| 5 | Reinforcement learning integration | ⏳ |
| 6 | Performance optimization & testing | ⏳ |

## ⚙️ Key Features

### Screen Capture
- Captures frames via ADB: `adb exec-out screencap -p`
- Converts to OpenCV-compatible format
- Handles connection retries

### Grid Detection
- Manually calibrated top-left coordinate + cell size
- Outputs binary 8x8 matrix (0=empty, 1=filled)
- Color-based threshold segmentation

### Decision Engine
- Simulates all valid block placements
- Scores using weighted heuristic function
- Implements depth-2 lookahead search
- Selects best move

### Human-Like Behavior
- Random delays: 0.3-1.2 seconds before move
- Tap jitter: ±4 pixels
- Suboptimal moves: 5% probability
- Randomized combo pauses

### Learning System
- **Phase 1**: Genetic algorithm optimization of heuristic weights
- **Phase 2**: Deep Q-Learning with PyTorch

## 📊 Heuristic Scoring

```python
Score = sum([
    lines_cleared * 100,
    combo * 40,
    holes * -15,
    isolated_regions * -25,
    compactness * 5
])
```

## 🧬 Genetic Algorithm Config

- Population: 20
- Selection: Top 5 per generation
- Mutation rate: 10%
- Mutation strength: 15%
- Games per generation: 50

## 🔮 Reinforcement Learning (Deep Q-Network)

- **Input**: 64 neurons (flattened 8x8 grid)
- **Hidden layers**: [128, 128]
- **Optimizer**: Adam
- **Learning rate**: 0.001
- **Gamma**: 0.99 (discount factor)
- **Epsilon decay**: 0.995 (exploration → exploitation)

## 🎯 Success Metrics

- ✅ Average score increasing over generations
- ✅ Survival time increasing
- ✅ Grid density management improves
- ✅ Stable performance over 100+ games

## 📝 Configuration

All project settings are in `game_ai_bot/config.py`:

```python
# Grid calibration (adjust for your device)
GRID_TOP_LEFT = (100, 400)
GRID_CELL_SIZE = 45

# Heuristic weights (tuned by genetic algorithm)
HEURISTIC_WEIGHTS = {...}

# Human behavior
DELAY_BEFORE_MOVE_MIN = 0.3
DELAY_BEFORE_MOVE_MAX = 1.2
```

## 🔧 Usage

```powershell
# Activate environment
.\venv\Scripts\Activate.ps1

# Run the bot
python game_ai_bot/main.py

# Monitor logs
tail -f game_ai_bot/logs/gameplay.log
```

## 🐛 Troubleshooting

**ADB connection issues?**
```powershell
adb kill-server
adb start-server
adb devices
```

**Module not found error?**
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

See [INSTALLATION.md](INSTALLATION.md) for detailed troubleshooting.

## 📚 Resources

- [ADB Documentation](https://developer.android.com/tools/adb)
- [OpenCV Tutorials](https://docs.opencv.org/)
- [PyTorch Docs](https://pytorch.org/docs/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## 📄 License

Internal use only

---

**Created**: February 2026  
**Status**: Tech stack setup ✅ | Core implementation ⏳
