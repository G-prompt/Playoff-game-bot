#!/usr/bin/env python3
"""
ADB Setup Helper - Download and Configure Android SDK Platform Tools

This script helps you:
1. Download Android SDK Platform Tools
2. Extract to a standard location
3. Add to Windows PATH automatically

Usage: python scripts/setup_adb.py
"""

import os
import sys
import urllib.request
import zipfile
import subprocess
from pathlib import Path
import shutil

def print_header(text):
    print(f"\n{'='*60}")
    print(f"📱 {text}")
    print(f"{'='*60}\n")

def print_step(step_num, text):
    print(f"[{step_num}] {text}")

def check_adb_installed():
    """Check if ADB is already in PATH."""
    print_step("1", "Checking if ADB is already installed...")
    try:
        result = subprocess.run("adb version", shell=True, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("  ✓ ADB already installed and in PATH!")
            print(f"  Version: {result.stdout.split(chr(10))[0]}")
            return True
    except:
        pass
    
    print("  ❌ ADB not found in PATH")
    return False

def download_platform_tools():
    """Download Android SDK Platform Tools."""
    print_step("2", "Downloading Android SDK Platform Tools...")
    
    # Determine OS
    if sys.platform == "win32":
        url = "https://developer.android.com/studio/releases/platform-tools/platform-tools-latest-windows.zip"
        filename = "platform-tools-windows.zip"
    elif sys.platform == "darwin":
        url = "https://developer.android.com/studio/releases/platform-tools/platform-tools-latest-darwin.zip"
        filename = "platform-tools-darwin.zip"
    else:
        url = "https://developer.android.com/studio/releases/platform-tools/platform-tools-latest-linux.zip"
        filename = "platform-tools-linux.zip"
    
    print(f"  URL: {url}")
    print(f"  Saving to: {filename}")
    
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"  ✓ Downloaded successfully ({os.path.getsize(filename)} bytes)")
        return filename
    except Exception as e:
        print(f"  ❌ Download failed: {e}")
        return None

def extract_platform_tools(zip_file):
    """Extract platform tools to standard location."""
    print_step("3", "Extracting platform tools...")
    
    # Standard installation location
    if sys.platform == "win32":
        install_dir = os.path.expandvars(r"C:\platform-tools")
    else:
        install_dir = os.path.expanduser("~/platform-tools")
    
    print(f"  Target directory: {install_dir}")
    
    # Create directory if needed
    Path(install_dir).parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(Path(install_dir).parent)
        
        print(f"  ✓ Extracted successfully")
        
        # Verify adb.exe exists
        adb_path = Path(install_dir) / "adb.exe" if sys.platform == "win32" else Path(install_dir) / "adb"
        if adb_path.exists():
            print(f"  ✓ ADB executable found: {adb_path}")
            return str(install_dir)
        
    except Exception as e:
        print(f"  ❌ Extraction failed: {e}")
    
    return None

def add_to_windows_path(platform_tools_path):
    """Add platform-tools to Windows PATH via registry."""
    print_step("4", "Adding to Windows PATH...")
    
    try:
        import winreg
        
        # Open registry
        reg_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as reg:
            with winreg.OpenKeyEx(reg, reg_path, 0, winreg.KEY_ALL_ACCESS) as key:
                current_path = winreg.QueryValueEx(key, "Path")[0]
                
                # Check if already in PATH
                if platform_tools_path.lower() in current_path.lower():
                    print(f"  ✓ Already in PATH")
                    return True
                
                # Add to PATH
                new_path = f"{current_path};{platform_tools_path}"
                winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                
                print(f"  ✓ Added to system PATH")
                print(f"  ⚠️  Close and reopen PowerShell for changes to take effect")
                return True
                
    except PermissionError:
        print(f"  ❌ Requires Administrator privileges")
        print(f"  Solution: Run PowerShell as Administrator and rerun this script")
        return False
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return False

def verify_adb():
    """Verify ADB works after setup."""
    print_step("5", "Verifying ADB installation...")
    
    # Force PATH refresh
    if sys.platform == "win32":
        import ctypes
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x1A
        SMTO_ABORTIFHUNG = 0x0002
        result = ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, ctypes.c_wchar_p("Environment"), SMTO_ABORTIFHUNG, 5000, ctypes.pointer(ctypes.c_long()))
    
    try:
        result = subprocess.run("adb version", shell=True, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("  ✓ ADB is working!")
            print(f"  {result.stdout.split(chr(10))[0]}")
            return True
    except:
        pass
    
    print(f"  ⚠️  Could not verify yet")
    print(f"  Please close PowerShell and reopen it, then run: adb version")
    return False

def cleanup(zip_file):
    """Remove downloaded zip file."""
    try:
        os.remove(zip_file)
        print(f"\n✓ Cleaned up {zip_file}")
    except:
        pass

def main():
    print_header("Android SDK Platform Tools Setup")
    
    # Check if already installed
    if check_adb_installed():
        print("\n✅ ADB is already ready!\n")
        return 0
    
    # Download
    zip_file = download_platform_tools()
    if not zip_file:
        print("\n❌ Failed to download platform tools\n")
        print("Manual download: https://developer.android.com/tools/releases/platform-tools")
        return 1
    
    # Extract
    platform_tools_path = extract_platform_tools(zip_file)
    if not platform_tools_path:
        print("\n❌ Failed to extract platform tools\n")
        return 1
    
    # Add to PATH
    if not add_to_windows_path(platform_tools_path) and sys.platform == "win32":
        print("\n⚠️  Could not automatically add to PATH (requires admin)")
        print(f"Manual instructions:")
        print(f"1. Open Settings → System → About")
        print(f"2. Advanced system settings → Environment Variables")
        print(f"3. Add PATH variable: {platform_tools_path}")
        print(f"4. Restart PowerShell\n")
    
    # Verify
    verify_adb()
    
    # Cleanup
    cleanup(zip_file)
    
    print(f"\n{'='*60}")
    print("✅ Setup Complete!")
    print(f"{'='*60}\n")
    print("Next steps:")
    print("1. Close PowerShell completely")
    print("2. Reopen PowerShell")
    print("3. Run: adb devices")
    print("4. Connect your Android device via USB")
    print("5. Tap 'Allow' on device when prompted\n")

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nAborted by user")
        sys.exit(1)
