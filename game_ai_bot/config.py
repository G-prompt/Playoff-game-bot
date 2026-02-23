"""
Android 8x8 Block Game AI Bot - Configuration Module

This module contains all configurable parameters for the game bot including:
- Grid detection coordinates and calibration
- Color thresholds for block detection
- AI decision parameters
- Human-like behavior settings
- Logging configuration
"""

# ============================================================================
# GRID CALIBRATION - CUSTOMIZE FOR YOUR DEVICE/GAME
# ============================================================================

# Top-left corner of the 8x8 grid in pixel coordinates
# Run screen capture, measure the top-left corner of the game board
GRID_TOP_LEFT = (100, 400)  # TODO: Calibrate via screenshot

# Size of each grid cell in pixels (width and height)
GRID_CELL_SIZE = 45  # TODO: Measure from your device

# Grid dimensions (fixed at 8x8 for this game)
GRID_ROWS = 8
GRID_COLS = 8

# ============================================================================
# COLOR THRESHOLDS - CUSTOMIZE FOR YOUR GAME
# ============================================================================

# RGB color thresholds for detecting filled vs empty cells
# Format: (R_min, G_min, B_min) to (R_max, G_max, B_max)
COLOR_THRESHOLDS = {
    'empty': {
        'lower': (180, 180, 180),  # TODO: Adjust from screenshots
        'upper': (255, 255, 255),
    },
    'block': {
        'lower': (50, 50, 50),     # TODO: Adjust from screenshots
        'upper': (200, 200, 200),
    },
}

# ============================================================================
# HEURISTIC WEIGHTS - TUNED VIA GENETIC ALGORITHM
# ============================================================================

HEURISTIC_WEIGHTS = {
    'lines_cleared': 100.0,
    'combo': 40.0,
    'holes': -15.0,
    'isolated_regions': -25.0,
    'compactness': 5.0,
}

# ============================================================================
# DECISION ENGINE PARAMETERS
# ============================================================================

# Depth of lookahead search (higher = slower but better moves)
LOOKAHEAD_DEPTH = 2

# Number of top moves to evaluate (prevents excessive simulation)
TOP_N_MOVES = 10

# Simulation timeout in seconds
SIMULATION_TIMEOUT = 2.0

# ============================================================================
# HUMAN-LIKE BEHAVIOR PARAMETERS
# ============================================================================

# Random delay before making a move (seconds)
DELAY_BEFORE_MOVE_MIN = 0.3
DELAY_BEFORE_MOVE_MAX = 1.2

# Random delay after completing a move (seconds)
DELAY_AFTER_MOVE_MIN = 0.2
DELAY_AFTER_MOVE_MAX = 0.8

# Jitter added to tap coordinates to look more human (pixels)
TAP_JITTER_PIXELS = 4

# Probability of intentionally making a suboptimal move
SUBOPTIMAL_MOVE_PROBABILITY = 0.05

# Add randomness to combo pause behavior
COMBO_PAUSE_RANDOMIZATION = True

# ============================================================================
# GENETIC ALGORITHM PARAMETERS
# ============================================================================

# Population size for genetic algorithms
POPULATION_SIZE = 20

# Number of top performers to keep each generation
SELECTION_TOP_K = 5

# Probability of mutating a weight
MUTATION_RATE = 0.1

# Strength of mutation (percentage change)
MUTATION_STRENGTH = 0.15

# Number of games to play per generation
GAMES_PER_GENERATION = 50

# Number of generations to train
NUM_GENERATIONS = 100  # TODO: Adjust based on convergence

# ============================================================================
# REINFORCEMENT LEARNING PARAMETERS
# ============================================================================

# Neural network architecture
RL_INPUT_SIZE = 64  # 8x8 flattened grid
RL_HIDDEN_LAYERS = [128, 128]
RL_LEARNING_RATE = 0.001

# DQN hyperparameters
RL_GAMMA = 0.99  # Discount factor
RL_EPSILON_START = 1.0
RL_EPSILON_DECAY = 0.995
RL_EPSILON_MIN = 0.05

# Experience replay
REPLAY_BUFFER_SIZE = 10000
BATCH_SIZE = 32
UPDATE_FREQUENCY = 4  # Update network every N steps

# Reward structure
REWARD_STRUCTURE = {
    'line_clear': 100.0,
    'combo_bonus': 40.0,
    'hole_penalty': -15.0,
    'isolation_penalty': -25.0,
    'game_over_penalty': -200.0,
}

# ============================================================================
# LOGGING AND OUTPUT
# ============================================================================

# Log file location
LOG_DIR = './game_ai_bot/logs'
LOG_FILE = 'gameplay.log'

# Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = 'INFO'

# Save game state snapshots every N moves
SNAPSHOT_INTERVAL = 50

# Save model weights every N games
MODEL_SAVE_INTERVAL = 10

# ============================================================================
# ADB AND ANDROID DEVICE
# ============================================================================

# Device ID (leave empty for single connected device)
ANDROID_DEVICE_ID = None  # TODO: Set if multiple devices connected

# Screenshot command
ADB_COMMAND = 'adb'

# Screenshot quality (1-100)
SCREENSHOT_QUALITY = 100

# Retry attempts for failed ADB commands
ADB_RETRY_ATTEMPTS = 3
ADB_RETRY_DELAY = 1.0  # seconds

# ============================================================================
# PERFORMANCE TUNING
# ============================================================================

# Maximum time allowed for decision making (seconds)
DECISION_TIMEOUT = 0.5

# Cache grid state between frames (reduces processing)
USE_GRID_CACHE = True
CACHE_INVALIDATE_FRAMES = 3

# Number of threads for parallel processing
NUM_THREADS = 4

# ============================================================================
# DEBUG AND TESTING
# ============================================================================

# Show computer vision detections (saves annotated images)
DEBUG_SHOW_DETECTIONS = False

# Direction to save debug images
DEBUG_DIR = './debug_images'

# Simulate game without ADB (for development)
SIMULATION_MODE = False

# Verbose output
VERBOSE = False
