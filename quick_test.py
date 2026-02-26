#!/usr/bin/env python3
"""
Quick Stage 1 Verification - 1 Minute Check

Run this anytime to verify Stage 1 is functioning.
Usage: python quick_test.py
"""

import subprocess
import sys
from pathlib import Path

def check(condition, label):
    """Print check result."""
    if condition:
        print(f"  ✓ {label}")
        return True
    else:
        print(f"  ❌ {label}")
        return False

print("\n📋 Quick Stage 1 Verification\n")

passed = 0
total = 0

# 1. Python
print("1️⃣  Python & Packages:")
total += 1
try:
    import cv2, torch, numpy
    if passed := check(True, "All packages imported"):
        passed += 1
except:
    check(False, "Package import failed")

# 2. ADB
print("\n2️⃣  Android Connection:")
total += 1
result = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
if passed := check(result.returncode == 0 and "device" in result.stdout, "ADB device connected"):
    passed += 1

# 3. Screenshot
print("\n3️⃣  Screen Capture:")
total += 1
result = subprocess.run("adb exec-out screencap -p > /tmp/test.png", shell=True, capture_output=True)
if passed := check(result.returncode == 0, "Screenshot captured"):
    passed += 1

# 4. Config
print("\n4️⃣  Configuration:")
total += 1
try:
    from game_ai_bot.config import GRID_TOP_LEFT, GRID_CELL_SIZE
    is_calibrated = GRID_TOP_LEFT != (100, 400) or GRID_CELL_SIZE != 45
    if passed := check(is_calibrated, "Grid calibrated"):
        passed += 1
    else:
        print("     ⚠️  Using default calibration - update config.py")
except:
    check(False, "Config loaded")

# Summary
print(f"\n{'='*40}")
print(f"✅ Ready!" if passed == total else f"⚠️  {total-passed} issue(s) found")
print(f"{'='*40}\n")

sys.exit(0 if passed == total else 1)
