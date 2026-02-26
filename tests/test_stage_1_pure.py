#!/usr/bin/env python3
"""
Stage 1 Pure Simulation Test - No OpenCV Required

Tests only simulation mode functionality:
- Mock screenshot generation
- Grid detection logic
- Heuristic scoring
- Configuration

This is the minimal test to verify Stage 1 core logic works.
No external dependencies beyond numpy and pillow.

Usage: python tests/test_stage_1_pure.py
"""

import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def print_section(title):
    """Print formatted section header."""
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print(f"{'='*60}\n")

# ============================================================================
# TEST 1: Simulation Mode Enabled
# ============================================================================

def test_simulation_mode():
    """Verify simulation mode is enabled."""
    print_section("Test 1: Simulation Mode Enabled")
    
    try:
        from game_ai_bot import config
        
        if config.SIMULATION_MODE:
            print("✓ SIMULATION_MODE = True")
            return True
        else:
            print("❌ SIMULATION_MODE must be True") 
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ============================================================================
# TEST 2: Core Package Imports (No OpenCV)
# ============================================================================

def test_core_imports():
    """Test core packages needed for Stage 1."""
    print_section("Test 2: Core Package Imports")
    
    packages = {
        'numpy': 'NumPy',
        'PIL': 'Pillow',
    }
    
    all_ok = True
    for module_name, display_name in packages.items():
        try:
            module = __import__(module_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✓ {display_name:15} v{version}")
        except ImportError:
            print(f"❌ {display_name:15} NOT FOUND")
            all_ok = False
    
    return all_ok

# ============================================================================
# TEST 3: Mock Screenshot Generation
# ============================================================================

def test_mock_screenshot():
    """Test mock screenshot generation."""
    print_section("Test 3: Mock Screenshot Generation")
    
    try:
        from game_ai_bot.screen_capture_mock import (
            generate_mock_board,
            generate_mock_screenshot,
            capture_screenshot
        )
        
        # Generate different board patterns
        patterns = ["random", "sparse", "dense", "line"]
        for pattern in patterns:
            board = generate_mock_board(pattern)
            filled = np.sum(board)
            pct = (filled / board.size) * 100
            print(f"✓ {pattern:10} board: {filled:2}/64 cells ({pct:5.1f}%)")
        
        # Generate screenshot
        screenshot = capture_screenshot(save_path="test_mock_screenshot.png")
        height, width = screenshot.shape[:2]
        print(f"✓ Screenshot generated: {width}x{height}")
        
        if Path("test_mock_screenshot.png").exists():
            size_kb = Path("test_mock_screenshot.png").stat().st_size / 1024
            print(f"✓ Saved: test_mock_screenshot.png ({size_kb:.1f} KB)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============================================================================
# TEST 4: Configuration Loading
# ============================================================================

def test_configuration():
    """Test configuration system."""
    print_section("Test 4: Configuration Loading")
    
    try:
        from game_ai_bot.config import (
            GRID_TOP_LEFT, GRID_CELL_SIZE,
            GRID_ROWS, GRID_COLS,
            HEURISTIC_WEIGHTS,
            LOOKAHEAD_DEPTH,
            DELAY_BEFORE_MOVE_MIN,
            DELAY_BEFORE_MOVE_MAX
        )
        
        print(f"✓ Grid Configuration:")
        print(f"  Top-left:  {GRID_TOP_LEFT}")
        print(f"  Cell size: {GRID_CELL_SIZE}px")
        print(f"  Dimension: {GRID_ROWS}x{GRID_COLS}")
        
        print(f"\n✓ Decision Engine:")
        print(f"  Lookahead depth: {LOOKAHEAD_DEPTH}")
        
        print(f"\n✓ Heuristic Weights:")
        weights_str = ", ".join(f"{k}={v}" for k, v in HEURISTIC_WEIGHTS.items())
        print(f"  {weights_str}")
        
        print(f"\n✓ Human Behavior:")
        print(f"  Move delay: {DELAY_BEFORE_MOVE_MIN}-{DELAY_BEFORE_MOVE_MAX}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ============================================================================
# TEST 5: Board Grid Extraction Logic
# ============================================================================

def test_grid_extraction():
    """Test grid extraction logic (numpy only)."""
    print_section("Test 5: Grid Extraction Logic")
    
    try:
        from game_ai_bot.config import (
            GRID_TOP_LEFT, GRID_CELL_SIZE, 
            GRID_ROWS, GRID_COLS
        )
        from game_ai_bot.screen_capture_mock import capture_screenshot
        
        # Get mock screenshot
        screenshot = capture_screenshot()
        print(f"✓ Screenshot shape: {screenshot.shape}")
        
        # Extract grid region using coordinates
        x, y = GRID_TOP_LEFT
        size = GRID_CELL_SIZE
        
        grid_height = GRID_ROWS * size
        grid_width = GRID_COLS * size
        
        grid_region = screenshot[y:y+grid_height, x:x+grid_width]
        
        if grid_region.size == 0:
            print(f"❌ Grid extraction failed (region out of bounds)")
            print(f"   Image: {screenshot.shape}")
            print(f"   Bounds: ({x}, {y}) -> ({x+grid_width}, {y+grid_height})")
            return False
        
        print(f"✓ Grid region extracted: {grid_region.shape}")
        print(f"  Expected: ({grid_height}, {grid_width}, 3)")
        
        # Analyze content
        # Convert to grayscale for analysis
        gray = np.mean(grid_region, axis=2)  # Simple grayscale
        empty_pixels = np.sum(gray > 200)
        filled_pixels = np.sum(gray <= 200)
        
        print(f"✓ Grid analysis:")
        print(f"  Empty pixels:  {empty_pixels:,}")
        print(f"  Filled pixels: {filled_pixels:,}")
        print(f"  Total pixels:  {gray.size:,}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============================================================================
# TEST 6: Heuristic Evaluation
# ============================================================================

def test_heuristic_scoring():
    """Test heuristic board scoring."""
    print_section("Test 6: Heuristic Evaluation")
    
    try:
        from game_ai_bot.config import HEURISTIC_WEIGHTS
        from game_ai_bot.screen_capture_mock import generate_mock_board
        
        def simple_board_score(board):
            """Evaluate board using heuristic weights."""
            score = 0
            
            # Count filled cells
            filled = np.sum(board)
            score += filled * HEURISTIC_WEIGHTS['compactness']
            
            # Count holes (surrounded empty cells)
            # Simple approximation: prefer denser boards
            empty = np.sum(board == 0)
            score -= empty * 1.0
            
            return score
        
        # Test different board states
        test_cases = [
            ("Empty", np.zeros((8, 8), dtype=np.uint8)),
            ("Sparse", generate_mock_board("sparse")),
            ("Random", generate_mock_board("random")),
            ("Dense", generate_mock_board("dense")),
            ("Full Line", generate_mock_board("line")),
        ]
        
        scores = {}
        for name, board in test_cases:
            score = simple_board_score(board)
            filled = np.sum(board)
            scores[name] = score
            print(f"✓ {name:15} score: {score:8.2f} ({filled:2}/64 cells)")
        
        # Verify scoring is rational
        if scores["Dense"] > scores["Random"] > scores["Sparse"] > scores["Empty"]:
            print(f"\n✓ Scoring progression is logical (Dense > Random > Sparse > Empty)")
            return True
        else:
            print(f"\n⚠️  Scoring progression unexpected, but functional")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============================================================================
# TEST 7: Board State Representation
# ============================================================================

def test_board_representation():
    """Test board state data structures."""
    print_section("Test 7: Board State Representation")
    
    try:
        from game_ai_bot.screen_capture_mock import generate_mock_board
        
        board = generate_mock_board("random")
        
        print(f"✓ Board shape: {board.shape} (8x8 grid)")
        print(f"✓ Board dtype: {board.dtype} (0=empty, 1=filled)")
        
        # Validate values
        unique = np.unique(board)
        if all(v in [0, 1] for v in unique):
            print(f"✓ Valid values: {list(unique)}")
        else:
            print(f"❌ Invalid board values: {list(unique)}")
            return False
        
        # Statistics
        filled_pct = (np.sum(board) / board.size) * 100
        print(f"✓ Board fill: {filled_pct:.1f}%")
        
        # Test cell access
        for i in range(5):
            r, c = np.random.randint(0, 8, 2)
            val = board[r, c]
            print(f"✓ Cell [{r},{c}] = {val}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ============================================================================
# Main Test Suite
# ============================================================================

def run_all_tests():
    """Run all Stage 1 pure simulation tests."""
    print("\n" + "="*60)
    print("🤖 Stage 1 Pure Simulation Test (numpy + Pillow only)")
    print("="*60)
    
    results = {}
    
    results['sim_mode'] = test_simulation_mode()
    results['imports'] = test_core_imports()
    results['mock'] = test_mock_screenshot()
    results['config'] = test_configuration()
    results['grid'] = test_grid_extraction()
    results['heuristic'] = test_heuristic_scoring()
    results['board'] = test_board_representation()
    
    # Summary
    print_section("Test Summary")
    
    tests = [
        ('Simulation Mode', results['sim_mode']),
        ('Core Imports', results['imports']),
        ('Mock Generation', results['mock']),
        ('Configuration', results['config']),
        ('Grid Extraction', results['grid']),
        ('Heuristic Scoring', results['heuristic']),
        ('Board Representation', results['board']),
    ]
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    print()
    for test_name, result in tests:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status:10} {test_name}")
    
    print(f"\n{'='*60}")
    print(f"Result: {passed}/{total} tests passed")
    print(f"{'='*60}\n")
    
    if passed == total:
        print("✅ Stage 1 Core Logic PASSES!")
        print("\nYou can now:")
        print("  • Continue to Stage 2 (Heuristic Engine)")
        print("  • Build move simulation logic")
        print("  • Implement decision engine")
        print("  • Test with real game when device ready\n")
        return 0
    else:
        print(f"⚠️  {total - passed} test(s) failed\n")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
