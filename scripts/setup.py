"""
Automated setup script for Android 8x8 Block Game AI Bot

This script:
1. Creates virtual environment
2. Installs dependencies
3. Verifies installation
4. Creates necessary directories
5. Checks ADB connectivity

Run: python scripts/setup.py
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(cmd, description=""):
    """Run a shell command and return success status."""
    print(f"\n{'='*60}")
    if description:
        print(f"📦 {description}")
    print(f"Running: {cmd}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_python_version():
    """Verify Python 3.10+"""
    version = sys.version_info
    print(f"\n✓ Python {version.major}.{version.minor}.{version.micro} detected")
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10+ required!")
        return False
    return True

def check_adb():
    """Check if ADB is installed and accessible."""
    try:
        result = subprocess.run("adb version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ ADB detected and accessible")
            return True
    except:
        pass
    
    print("\n⚠️  WARNING: ADB not found in PATH")
    print("   Android SDK Platform Tools required for production mode")
    print("   Download: https://developer.android.com/tools/releases/platform-tools")
    print("   You can still run in SIMULATION_MODE = True")
    return False

def check_venv():
    """Check if venv already exists."""
    venv_path = Path("venv")
    return venv_path.exists()

def create_directories():
    """Create necessary project directories."""
    dirs = [
        "game_ai_bot",
        "game_ai_bot/models",
        "game_ai_bot/logs",
        "tests",
        "debug_images",
        "scripts"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(exist_ok=True)
        print(f"✓ Directory: {dir_path}")

def main():
    """Main setup routine."""
    print("\n" + "="*60)
    print("🤖 Android 8x8 Block Game AI Bot - Setup")
    print("="*60)
    
    # Step 1: Check Python
    print("\n[1/5] Checking Python version...")
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Check existing venv
    print("\n[2/5] Checking virtual environment...")
    if check_venv():
        print("✓ Virtual environment already exists (venv/)")
    else:
        if run_command(f"{sys.executable} -m venv venv", "Creating virtual environment"):
            print("✓ Virtual environment created")
        else:
            print("❌ Failed to create virtual environment")
            sys.exit(1)
    
    # Step 3: Install dependencies
    print("\n[3/5] Installing dependencies...")
    pip_cmd = "pip --version"
    if not run_command(pip_cmd):
        print("❌ pip not found")
        sys.exit(1)
    
    packages = [
        "opencv-python",
        "numpy",
        "pillow",
        "torch",
        "torchvision",
        "scikit-learn"
    ]
    
    install_cmd = f"{sys.executable} -m pip install {' '.join(packages)}"
    if run_command(install_cmd, f"Installing {len(packages)} packages"):
        print(f"✓ {len(packages)} packages installed")
    else:
        print("❌ Failed to install packages")
        sys.exit(1)
    
    # Step 4: Create directories
    print("\n[4/5] Creating project directories...")
    create_directories()
    
    # Step 5: Check ADB
    print("\n[5/5] Checking Android SDK tools...")
    has_adb = check_adb()
    
    # Final summary
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE!")
    print("="*60)
    print("\n📚 Next Steps:")
    print("1. Read SETUP.md for detailed configuration")
    print("2. Calibrate game_ai_bot/config.py:")
    print("   - GRID_TOP_LEFT (measure from screenshot)")
    print("   - GRID_CELL_SIZE (cell size in pixels)")
    print("   - COLOR_THRESHOLDS (RGB values)")
    print("3. Enable USB Debugging on your Android device")
    print("4. Connect device via USB")
    if not has_adb:
        print("\n⚠️  Note: Install Android SDK Platform Tools first:")
        print("   Download from: https://developer.android.com/tools/releases/platform-tools")
        print("   Then configure PATH")
    
    print("\n🚀 Ready to develop! Good luck! 🎮\n")

if __name__ == "__main__":
    main()
