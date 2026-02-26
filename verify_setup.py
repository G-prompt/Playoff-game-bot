#!/usr/bin/env python3
"""
Tech Stack Verification Script

Verifies that all required Python packages are installed and functional.
Run: python verify_setup.py
"""

import sys

def verify_packages():
    """Verify all required packages are installed."""
    print("\n" + "="*60)
    print("✓ Package Installation Verification")
    print("="*60 + "\n")
    
    packages = {
        "opencv-python": "cv2",
        "numpy": "numpy",
        "pillow": "PIL",
        "torch": "torch",
        "torchvision": "torchvision",
        "scikit-learn": "sklearn",
    }
    
    all_ok = True
    loaded_versions = {}
    
    for package_name, import_name in packages.items():
        try:
            module = __import__(import_name)
            version = getattr(module, "__version__", "unknown")
            loaded_versions[package_name] = version
            print(f"✓ {package_name:20} v{version}")
        except ImportError as e:
            print(f"❌ {package_name:20} NOT FOUND - {e}")
            all_ok = False
    
    print("\n" + "="*60)
    
    if all_ok:
        print("✅ All packages installed and functional!")
        print("="*60 + "\n")
        return True
    else:
        print("❌ Some packages are missing!")
        print("="*60 + "\n")
        print("Run:")
        print("  pip install -r requirements.txt")
        return False

def verify_python_version():
    """Verify Python version is 3.10+"""
    version = sys.version_info
    print(f"\nPython {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10+ required!")
        return False
    
    print("✓ Python version meets requirements (3.10+)")
    return True

def verify_directories():
    """Verify project directories exist."""
    from pathlib import Path
    
    print("\n" + "="*60)
    print("✓ Project Directory Structure")
    print("="*60 + "\n")
    
    dirs = [
        "game_ai_bot",
        "game_ai_bot/models",
        "game_ai_bot/logs",
        "tests",
        "debug_images",
    ]
    
    all_exist = True
    for dir_path in dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✓ {dir_path:30} exists")
        else:
            print(f"⚠️  {dir_path:30} missing (will be created)")
            all_exist = False
    
    return all_exist

def main():
    """Run all verifications."""
    print("\n" + "="*60)
    print("🤖 Android Game AI Bot - Tech Stack Verification")
    print("="*60)
    
    # Verify Python version
    py_ok = verify_python_version()
    
    # Verify packages
    pkg_ok = verify_packages()
    
    # Verify directories
    verify_directories()
    
    # Final status
    print("="*60)
    if py_ok and pkg_ok:
        print("✅ SETUP VERIFIED - Ready to begin development!")
    else:
        print("⚠️  Some issues detected - see above for details")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
