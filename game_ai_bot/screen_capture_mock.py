"""
Mock Screen Capture for Simulation Mode

When SIMULATION_MODE=True, generates synthetic game screenshots for testing
without needing ADB or an actual Android device.

This allows Stage 1 testing to proceed while waiting for device access.
"""

import numpy as np
from PIL import Image
import random
from pathlib import Path

def generate_mock_board(pattern="random"):
    """
    Generate a mock 8x8 game board.
    
    Args:
        pattern: 'random', 'sparse', 'dense', or 'empty'
    
    Returns:
        8x8 numpy array (0=empty, 1=filled)
    """
    board = np.zeros((8, 8), dtype=np.uint8)
    
    if pattern == "random":
        # Random 40% filled
        for i in range(8):
            for j in range(8):
                if random.random() < 0.4:
                    board[i, j] = 1
    
    elif pattern == "sparse":
        # 20% filled (mostly empty)
        for i in range(8):
            for j in range(8):
                if random.random() < 0.2:
                    board[i, j] = 1
    
    elif pattern == "dense":
        # 70% filled (mostly full)
        for i in range(8):
            for j in range(8):
                if random.random() < 0.7:
                    board[i, j] = 1
    
    elif pattern == "line":
        # Complete line (tests line clearing)
        board[5, :] = 1
    
    return board

def generate_mock_screenshot(board, width=512, height=912):
    """
    Generate a realistic mock screenshot with 8x8 grid.
    
    Args:
        board: 8x8 numpy array (0=empty, 1=filled)
        width: Screenshot width in pixels
        height: Screenshot height in pixels
    
    Returns:
        PIL Image of mock game screenshot
    """
    # Create image (white background)
    img = Image.new('RGB', (width, height), color=(240, 240, 240))
    pixels = img.load()
    
    # Add dark background frame for aesthetic
    for x in range(width):
        for y in range(height):
            if y < 100:  # Top area (UI space)
                pixels[x, y] = (50, 50, 50)
    
    # Calculate grid area
    grid_left = 75
    grid_top = 250
    cell_size = 45
    
    # Draw grid cells
    for i in range(8):
        for j in range(8):
            # Calculate cell position
            x_start = grid_left + j * cell_size
            y_start = grid_top + i * cell_size
            x_end = x_start + cell_size
            y_end = y_start + cell_size
            
            # Draw cell
            if board[i, j] == 1:
                # Filled cell - light blue
                fill_color = (100, 150, 200)
            else:
                # Empty cell - light gray
                fill_color = (240, 240, 240)
            
            # Fill cell
            for x in range(x_start, x_end):
                for y in range(y_start, y_end):
                    if x < width and y < height:
                        pixels[x, y] = fill_color
            
            # Draw cell border
            border_color = (100, 100, 100)
            for x in range(x_start, x_end + 1):
                if x < width:
                    pixels[x, y_start] = border_color
                    pixels[x, y_end] = border_color
            
            for y in range(y_start, y_end + 1):
                if y < height:
                    pixels[x_start, y] = border_color
                    pixels[x_end, y] = border_color
    
    return img

def capture_screenshot(device_id=None, save_path=None):
    """
    Capture screenshot (simulation mode).
    
    In SIMULATION_MODE, generates a mock screenshot instead of using ADB.
    
    Args:
        device_id: Ignored in simulation mode
        save_path: Optional path to save screenshot
    
    Returns:
        numpy array (OpenCV format) of screenshot
    """
    # Generate random board pattern
    patterns = ["random", "sparse", "dense", "line"]
    pattern = random.choice(patterns)
    board = generate_mock_board(pattern)
    
    # Generate screenshot image
    img = generate_mock_screenshot(board)
    
    # Save if requested
    if save_path:
        img.save(save_path)
        print(f"  Mock screenshot saved: {save_path}")
    
    # Convert PIL to OpenCV format (numpy array)
    img_array = np.array(img)
    # OpenCV uses BGR, PIL uses RGB
    img_array = img_array[:, :, ::-1]
    
    return img_array

# For backwards compatibility
def adb_screenshot():
    """Legacy function - calls capture_screenshot()"""
    return capture_screenshot()

