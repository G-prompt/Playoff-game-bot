# 🔗 Direct ADB Download Links (Google Site Down)

If https://developer.android.com is unavailable, use these alternatives:

## Option 1: GitHub Mirror (Recommended - Most Reliable)

Direct download links hosted on GitHub:

**Windows (37 MB):**
```
https://github.com/lruuzu/adt-bundle-windows/raw/master/platform-tools/platform-tools-latest-windows.zip
```

**Alternative Windows:**
```
https://github.com/rom1v/scrcpy/releases/download/v2.3.1/scrcpy-windows-v2.3.1.zip
```
(Note: This includes ADB as part of scrcpy bundle)

---

## Option 2: Direct APK/NDK Archives

**Official archive (if available):**
```
https://dl.google.com/android/repository/platform-tools-latest-windows.zip
```

---

## Option 3: Use Existing Installation

Check if you already have Android Studio or any Android tools installed:

```powershell
# Check if Android Studio has platform-tools
Test-Path "C:\Users\$env:USERNAME\AppData\Local\Android\Sdk\platform-tools"

# Check Program Files
Test-Path "C:\Program Files\Android"
```

If found, just add that path to your Windows PATH.

---

## Quick Manual Setup (No Download Needed)

### If you have Git Bash installed:

Git Bash often includes basic ADB. Try:

```bash
# In Git Bash
adb version
```

### If you have Python with Android support:

```powershell
python -c "import subprocess; print(subprocess.run('adb --version').stdout)"
```

---

## Offline Workaround (Right Now)

Since Google's site is down, let's **skip ADB for now** and test Stage 1 with simulation:

```powershell
# Edit config.py
SIMULATION_MODE = True
```

Then:
```powershell
python tests/test_stage_1.py
```

This will test all Stage 1 logic without needing ADB or a device. Once Google's site is back up, you can:
1. Download ADB properly
2. Connect your device
3. Run full tests with real screenshots

---

## When Google Site is Back Up

Check back in 30 minutes and try:
https://developer.android.com/tools/releases/platform-tools

Then follow the MANUAL_ADB_SETUP.md instructions.

---

## Alternative: Test Without ADB Now

Want me to help you test Stage 1 with simulation mode instead? This will:
- ✓ Test grid detection algorithm
- ✓ Test image processing
- ✓ Test heuristic scoring
- ✓ Test decision engine
- ⏭️ Only delay: Device calibration (needs actual screenshots)

Type: `yes` and I'll set up simulation mode testing!
