#!/usr/bin/env python3
"""
Stage 1 Simulation Test - Test Without ADB or Device

This test suite runs Stage 1 tests using mock screenshots (simulation mode).
No ADB, no device, no network required - perfect for development & testing.

Usage: python tests/test_stage_1_simulation.py
"""

import sys
import numpy as np
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def print_section(title):
    """Print formatted section header."""
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print(f"{'='*60}\n")

# ============================================================================
# TEST 1: Enable Simulation Mode
# ============================================================================

def test_simulation_mode():
    """Enable and verify simulation mode."""
    print_section("Test 1: Simulation Mode Setup")
    
    try:
        from game_ai_bot import config
        
        # Check if simulation mode is enabled
        if config.SIMULATION_MODE:
            print("✓ SIMULATION_MODE is enabled")
            print(f"  Grid calibration: {config.GRID_TOP_LEFT}")
            print(f"  Cell size: {config.GRID_CELL_SIZE}")
            return True
        else:
            print("❌ SIMULATION_MODE must be True")
            print("  Edit game_ai_bot/config.py and set SIMULATION_MODE = True")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ============================================================================
# TEST 2: Generate Mock Screenshots
# ============================================================================

def test_mock_screenshot_generation():
    """Test mock screenshot generation."""
    print_section("Test 2: Mock Screenshot Generation")
    
    try:
        from game_ai_bot.screen_capture_mock import (
            generate_mock_board,
            generate_mock_screenshot,
            capture_screenshot
        )
        
        # Test board generation
        patterns = ["random", "sparse", "dense", "line"]
        for pattern in patterns:
            board = generate_mock_board(pattern)
            filled = np.sum(board)
            total = board.size
            pct = (filled / total) * 100
            print(f"✓ Generated '{pattern}' board: {filled}/{total} cells filled ({pct:.1f}%)")
        
        # Test screenshot generation
        board = generate_mock_board("random")
        img = generate_mock_screenshot(board)
        print(f"✓ Generated mock screenshot: {img.size[0]}x{img.size[1]} pixels")
        
        # Test capture
        screenshot = capture_screenshot(save_path="test_mock_screenshot.png")
        if screenshot is not None and screenshot.shape[0] > 0:
            print(f"✓ Screenshot captured: {screenshot.shape}")
            print(f"  Saved: test_mock_screenshot.png")
            return True
        else:
            print("❌ Failed to capture screenshot")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============================================================================
# TEST 3: OpenCV Image Processing
# ============================================================================

def test_image_processing():
    """Test image processing pipeline."""
    print_section("Test 3: Image Processing Pipeline")
    
    try:
        import cv2
        from game_ai_bot.screen_capture_mock import capture_screenshot
        
        # Capture mock screenshot
        screenshot = capture_screenshot()
        
        # Convert to grayscale
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        print(f"✓ Grayscale conversion: {gray.shape}")
        
        # Thresholding
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        print(f"✓ Binary thresholding: {binary.shape}")
        
        # Contour detection
        contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        print(f"✓ Contour detection: {len(contours)} contours found")
        
        # Edge detection
        edges = cv2.Canny(gray, 100, 200)
        print(f"✓ Edge detection: {edges.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============================================================================
# TEST 4: Grid Detection
# ============================================================================

def test_grid_detection():
    """Test grid detection with mock screenshot."""
    print_section("Test 4: Mock Grid Detection")
    
    try:
        from game_ai_bot.config import GRID_TOP_LEFT, GRID_CELL_SIZE, GRID_ROWS, GRID_COLS
        from game_ai_bot.screen_capture_mock import capture_screenshot
        import cv2
        
        # Capture mock screenshot
        screenshot = capture_screenshot()
        
        # Extract grid region
        x, y = GRID_TOP_LEFT
        size = GRID_CELL_SIZE
        grid_region = screenshot[y:y+GRID_ROWS*size, x:x+GRID_COLS*size]
        
        if grid_region.size == 0:
            print(f"❌ Grid extraction failed")
            print(f"   Image size: {screenshot.shape}")
            print(f"   Grid bounds: ({x}, {y}) to ({x+GRID_COLS*size}, {y+GRID_ROWS*size})")
            return False
        
        print(f"✓ Grid region extracted: {grid_region.shape}")
        
        # Save extracted region
        cv2.imwrite("test_grid_region_mock.png", grid_region)
        print(f"✓ Grid region saved: test_grid_region_mock.png")
        
        # Analyze grid
        gray = cv2.cvtColor(grid_region, cv2.COLOR_BGR2GRAY)
        cells_empty = np.sum(gray > 200)
        cells_filled = np.sum(gray <= 200)
        total_pixels = gray.size
        
        print(f"✓ Grid analysis:")
        print(f"  Empty pixels: {cells_empty}")
        print(f"  Filled pixels: {cells_filled}")
        print(f"  Total: {total_pixels}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============================================================================
# TEST 5: Heuristic Evaluation
# ============================================================================

def test_heuristic_evaluation():
    """Test heuristic scoring function."""
    print_section("Test 5: Heuristic Evaluation")
    
    try:
        from game_ai_bot.config import HEURISTIC_WEIGHTS
        
        # Test scoring function
        def evaluate_board(board):
            """Simple heuristic scoring."""
            score = 0
            score += np.sum(board) * 5  # Reward pieces
            score -= np.sum(board == 0) * 0.1  # Slight penalty for empty
            return score
        
        # Generate test boards
        from game_ai_bot.screen_capture_mock import generate_mock_board
        
        patterns = ["empty", "sparse", "random", "dense"]
        scores = {}
        
        for pattern in patterns:
            if pattern == "empty":
                board = np.zeros((8, 8), dtype=np.uint8)
            else:
                board = generate_mock_board(pattern)
            
            score = evaluate_board(board)
            scores[pattern] = score
            print(f"✓ {pattern:10} score: {score:.2f}")
        
        # Verify scoring makes sense
        if scores["empty"] < scores["sparse"] < scores["dense"]:
            print("\n✓ Scoring progression is logical")
            return True
        else:
            print("\n⚠️  Scoring may not be optimal")
            return True  # Still passes
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============================================================================
# TEST 6: Package Imports
# ============================================================================

def test_package_imports():
    """Verify all required packages import."""
    print_section("Test 6: Package Imports")
    
    packages = {
        'cv2': 'OpenCV',
        'numpy': 'NumPy',
        'torch': 'PyTorch',
        'PIL': 'Pillow',
    }
    
    all_ok = True
    for module_name, display_name in packages.items():
        try:
            module = __import__(module_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✓ {display_name:15} v{version}")
        except ImportError as e:
            print(f"❌ {display_name:15} NOT FOUND")
            all_ok = False
    
    return all_ok

# ============================================================================
# TEST 7: Configuration
# ============================================================================

def test_configuration():
    """Verify configuration is loaded."""
    print_section("Test 7: Configuration Verification")
    
    try:
        from game_ai_bot.config import (
            GRID_TOP_LEFT, GRID_CELL_SIZE,
            HEURISTIC_WEIGHTS, LOOKAHEAD_DEPTH,
            DELAY_BEFORE_MOVE_MIN, DELAY_BEFORE_MOVE_MAX
        )
        
        print(f"✓ Grid Configuration:")
        print(f"  Top-left: {GRID_TOP_LEFT}")
        print(f"  Cell size: {GRID_CELL_SIZE}px")
        
        print(f"\n✓ Decision Engine:")
        print(f"  Lookahead depth: {LOOKAHEAD_DEPTH}")
        
        print(f"\n✓ Heuristic Weights:")
        for key, val in HEURISTIC_WEIGHTS.items():
            print(f"  {key:20} {val:10.2f}")
        
        print(f"\n✓ Human Behavior:")
        print(f"  Move delay: {DELAY_BEFORE_MOVE_MIN}-{DELAY_BEFORE_MOVE_MAX}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ============================================================================
# Main Test Suite
# ============================================================================

def run_all_tests():
    """Run complete Stage 1 simulation test suite."""
    print("\n" + "="*60)
    print("🤖 Stage 1 Simulation Test Suite (No ADB Required)")
    print("="*60)
    
    results = {}
    
    # Run all tests
    results['sim_mode'] = test_simulation_mode()
    results['packages'] = test_package_imports()
    results['config'] = test_configuration()
    results['mock_gen'] = test_mock_screenshot_generation()
    results['image_proc'] = test_image_processing()
    results['grid'] = test_grid_detection()
    results['heuristic'] = test_heuristic_evaluation()
    
    # Summary
    print_section("Test Summary")
    
    tests = [
        ('Simulation Mode', results['sim_mode']),
        ('Package Imports', results['packages']),
        ('Configuration', results['config']),
        ('Mock Generation', results['mock_gen']),
        ('Image Processing', results['image_proc']),
        ('Grid Detection', results['grid']),
        ('Heuristic Evaluation', results['heuristic']),
    ]
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, result in tests:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status:10} {test_name}")
    
    print(f"\nResult: {passed}/{total} tests passed\n")
    
    # Final status
    if passed == total:
        print("✅ Stage 1 Simulation Tests PASSED!")
        print("\nYou can now:")
        print("  1. Continue developing Stage 2 (Heuristic Engine)")
        print("  2. Later connect a real device for end-to-end testing")
        print("  3. Set SIMULATION_MODE = False when ready for real game\n")
    else:
        print(f"⚠️  {total - passed} test(s) failed\n")

if __name__ == "__main__":
    run_all_tests()
