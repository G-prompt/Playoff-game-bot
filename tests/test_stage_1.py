#!/usr/bin/env python3
"""
Stage 1 Testing Suite - Screen Capture & Grid Detection

This script verifies all Stage 1 requirements are working:
1. ADB connectivity to Android device
2. Screen capture functionality
3. Image processing pipelines
4. Grid detection algorithm

Usage: python test_stage_1.py

Requirements:
- Android device connected via USB
- USB Debugging enabled
- ADB in PATH
"""

import subprocess
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def print_section(title):
    """Print formatted section header."""
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print(f"{'='*60}\n")

def run_command(cmd, description=""):
    """Run a shell command and return success status."""
    if description:
        print(f"  → {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.stdout:
            print(f"    {result.stdout.strip()}")
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        print(f"    ❌ Command timed out")
        return False, "", "Timeout"
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return False, "", str(e)

# ============================================================================
# TEST 1: Check Python Environment
# ============================================================================

def test_python_environment():
    """Verify Python 3.10+ and virtual environment."""
    print_section("Test 1: Python Environment")
    
    version = sys.version_info
    venv_active = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    print(f"Virtual Environment: {'✓ Active' if venv_active else '⚠️  Not active (use: .\\venv\\Scripts\\Activate.ps1)'}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10+ required!")
        return False
    
    print("✓ Python version OK\n")
    return True

# ============================================================================
# TEST 2: Check Required Packages
# ============================================================================

def test_imports():
    """Verify all required Python packages are installed."""
    print_section("Test 2: Python Package Imports")
    
    packages = {
        'opencv': 'cv2',
        'numpy': 'numpy',
        'pillow': 'PIL',
        'torch': 'torch',
        'torchvision': 'torchvision',
        'sklearn': 'sklearn',
    }
    
    all_ok = True
    for name, module_name in packages.items():
        try:
            module = __import__(module_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✓ {name:15} v{version}")
        except ImportError as e:
            print(f"❌ {name:15} NOT INSTALLED - {e}")
            all_ok = False
    
    print()
    return all_ok

# ============================================================================
# TEST 3: ADB Connectivity
# ============================================================================

def test_adb_connectivity():
    """Test ADB connection to Android device."""
    print_section("Test 3: ADB Connectivity")
    
    # Check if ADB is available
    ok, output, error = run_command("adb version", "Checking ADB installation")
    if not ok:
        print("❌ ADB not found in PATH")
        print("   Download: https://developer.android.com/tools/releases/platform-tools")
        print("   Add to PATH and try again\n")
        return False
    
    print("✓ ADB installed\n")
    
    # List connected devices
    ok, output, error = run_command("adb devices", "Listing connected devices")
    if not ok:
        print("❌ Failed to list devices\n")
        return False
    
    # Check if any device is connected
    if "device" not in output or "offline" in output.lower():
        print("❌ No device connected or offline")
        print("   Steps to fix:")
        print("   1. Enable USB Debugging on Android device")
        print("   2. Connect device via USB")
        print("   3. Tap 'Allow' when prompted on device\n")
        return False
    
    print("✓ Device connected\n")
    return True

# ============================================================================
# TEST 4: Screen Capture
# ============================================================================

def test_screen_capture():
    """Test capturing screenshot from Android device."""
    print_section("Test 4: Screen Capture via ADB")
    
    output_file = "test_screenshot.png"
    
    # Attempt to capture screenshot
    ok, output, error = run_command(
        f"adb exec-out screencap -p > {output_file}",
        "Capturing screenshot from device"
    )
    
    if not ok or not Path(output_file).exists():
        print(f"❌ Failed to capture screenshot")
        if error:
            print(f"   Error: {error}\n")
        return False
    
    # Check file size
    file_size = Path(output_file).stat().st_size
    print(f"✓ Screenshot captured: {output_file} ({file_size} bytes)\n")
    
    return True, output_file

# ============================================================================
# TEST 5: Image Processing
# ============================================================================

def test_image_processing():
    """Test image loading and processing with OpenCV."""
    print_section("Test 5: Image Processing Pipeline")
    
    import cv2
    import numpy as np
    
    screenshot_file = "test_screenshot.png"
    
    if not Path(screenshot_file).exists():
        print(f"❌ Screenshot file not found: {screenshot_file}")
        print("   Run test_screen_capture() first\n")
        return False
    
    try:
        # Load image
        img = cv2.imread(screenshot_file)
        if img is None:
            print(f"❌ Failed to load image: {screenshot_file}\n")
            return False
        
        height, width, channels = img.shape
        print(f"✓ Image loaded: {width}x{height} ({channels} channels)")
        
        # Convert to HSV (useful for color detection)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        print(f"✓ HSV conversion successful")
        
        # Test gray conversion
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print(f"✓ Grayscale conversion successful")
        
        # Test thresholding
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        print(f"✓ Thresholding successful")
        
        print()
        return True, img
        
    except Exception as e:
        print(f"❌ Image processing error: {e}\n")
        return False, None

# ============================================================================
# TEST 6: Grid Detection (Manual Calibration Test)
# ============================================================================

def test_grid_detection():
    """Test grid detection with current calibration."""
    print_section("Test 6: Grid Detection Calibration")
    
    try:
        from game_ai_bot.config import (
            GRID_TOP_LEFT, GRID_CELL_SIZE, 
            GRID_ROWS, GRID_COLS,
            COLOR_THRESHOLDS
        )
    except ImportError as e:
        print(f"❌ Cannot import config: {e}\n")
        return False
    
    # Validate configuration
    print("Current Grid Configuration:")
    print(f"  GRID_TOP_LEFT:     {GRID_TOP_LEFT}")
    print(f"  GRID_CELL_SIZE:    {GRID_CELL_SIZE}")
    print(f"  Grid dimension:    {GRID_ROWS}x{GRID_COLS}")
    
    if GRID_TOP_LEFT == (100, 400) or GRID_CELL_SIZE == 45:
        print("\n⚠️  WARNING: Using default calibration values!")
        print("   You MUST calibrate these for your device:")
        print("   1. Take a screenshot: adb exec-out screencap -p > screenshot.png")
        print("   2. Open screenshot in an image viewer")
        print("   3. Find top-left corner of 8x8 game grid")
        print("   4. Measure column width (one cell size in pixels)")
        print("   5. Update game_ai_bot/config.py:\n")
        print("      GRID_TOP_LEFT = (x, y)     # Coordinates you measured")
        print("      GRID_CELL_SIZE = pixels    # Size of each cell\n")
        return False
    
    # Calculate expected grid area
    bottom_right_x = GRID_TOP_LEFT[0] + (GRID_COLS * GRID_CELL_SIZE)
    bottom_right_y = GRID_TOP_LEFT[1] + (GRID_ROWS * GRID_CELL_SIZE)
    
    print(f"\nExpected Grid Area:")
    print(f"  Top-Left:     {GRID_TOP_LEFT}")
    print(f"  Bottom-Right: ({bottom_right_x}, {bottom_right_y})")
    print(f"  Width:  {GRID_COLS * GRID_CELL_SIZE}px")
    print(f"  Height: {GRID_ROWS * GRID_CELL_SIZE}px\n")
    
    print("Color Thresholds:")
    for color_name, thresholds in COLOR_THRESHOLDS.items():
        print(f"  {color_name}:")
        print(f"    Lower: {thresholds['lower']}")
        print(f"    Upper: {thresholds['upper']}")
    
    print("\n✓ Configuration loaded (verify coordinates match your device)\n")
    return True

# ============================================================================
# TEST 7: Extract Grid from Screenshot
# ============================================================================

def test_extract_grid(img):
    """Extract grid region from screenshot."""
    print_section("Test 7: Extract Grid Region from Screenshot")
    
    if img is None:
        print("❌ No image data (run image processing test first)\n")
        return False
    
    try:
        from game_ai_bot.config import GRID_TOP_LEFT, GRID_CELL_SIZE, GRID_ROWS, GRID_COLS
        import cv2
        
        x, y = GRID_TOP_LEFT
        size = GRID_CELL_SIZE
        
        # Extract grid region
        grid_region = img[y:y+GRID_ROWS*size, x:x+GRID_COLS*size]
        
        if grid_region.size == 0:
            print(f"❌ Grid region out of bounds")
            print(f"   Image size: {img.shape}")
            print(f"   Grid bounds: ({x}, {y}) to ({x+GRID_COLS*size}, {y+GRID_ROWS*size})\n")
            return False
        
        # Save extracted region for inspection
        output_file = "test_grid_region.png"
        cv2.imwrite(output_file, grid_region)
        
        region_height, region_width = grid_region.shape[:2]
        print(f"✓ Grid region extracted: {region_width}x{region_height}")
        print(f"  Saved to: {output_file}")
        print(f"  Open this file to verify grid detection is working\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error extracting grid: {e}\n")
        return False

# ============================================================================
# Main Test Suite
# ============================================================================

def run_all_tests():
    """Run complete Stage 1 test suite."""
    print("\n" + "="*60)
    print("🤖 Stage 1 Test Suite - Screen Capture & Grid Detection")
    print("="*60)
    
    results = {}
    
    # Test 1: Python Environment
    results['python'] = test_python_environment()
    
    # Test 2: Imports
    results['imports'] = test_imports()
    
    # Test 3: ADB Connectivity
    results['adb'] = test_adb_connectivity()
    
    # Test 4: Screen Capture
    if results['adb']:
        capture_result = test_screen_capture()
        results['capture'] = capture_result[0] if isinstance(capture_result, tuple) else capture_result
        screenshot_file = capture_result[1] if isinstance(capture_result, tuple) and capture_result[0] else None
    else:
        results['capture'] = False
        screenshot_file = None
    
    # Test 5: Image Processing
    img = None
    if results['capture'] and screenshot_file:
        process_result = test_image_processing()
        results['image'] = process_result[0] if isinstance(process_result, tuple) else process_result
        img = process_result[1] if isinstance(process_result, tuple) and process_result[0] else None
    else:
        results['image'] = False
    
    # Test 6: Grid Detection Calibration
    results['calibration'] = test_grid_detection()
    
    # Test 7: Extract Grid
    if results['image'] and img is not None and results['calibration']:
        results['extract'] = test_extract_grid(img)
    else:
        results['extract'] = False
    
    # Summary
    print_section("Test Summary")
    
    tests = [
        ('Python Environment', results['python']),
        ('Package Imports', results['imports']),
        ('ADB Connectivity', results['adb']),
        ('Screen Capture', results['capture']),
        ('Image Processing', results['image']),
        ('Grid Calibration', results['calibration']),
        ('Grid Extraction', results['extract']),
    ]
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, result in tests:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status:10} {test_name}")
    
    print(f"\nResult: {passed}/{total} tests passed\n")
    
    # Final recommendations
    print_section("Next Steps")
    
    if passed == total:
        print("✅ Stage 1 is READY!")
        print("   All systems operational. Move to Stage 2 (Heuristic Engine)\n")
    else:
        print("⚠️  Some tests failed. Address issues above before proceeding.\n")
        
        if not results['adb']:
            print("Action: Enable USB Debugging & connect Android device")
        if not results['calibration']:
            print("Action: Calibrate GRID_TOP_LEFT and GRID_CELL_SIZE in config.py")
        if not results['image']:
            print("Action: Verify screenshot was captured correctly")

if __name__ == "__main__":
    run_all_tests()
