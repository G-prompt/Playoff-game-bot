# ✅ Manual ADB Setup - 5 Minutes

## Step 1: Download (Right Now)

Go to this link in your browser:
**https://developer.android.com/tools/releases/platform-tools**

Scroll down to **"Downloads"** section and click the **Windows** download link.

This will download: `platform-tools-latest-windows.zip` (~100 MB)

---

## Step 2: Extract

1. Open File Explorer
2. Navigate to your Downloads folder
3. Right-click **platform-tools-latest-windows.zip**
4. Select **Extract All...**
5. Extract to: **`C:\platform-tools`**
   - (Or any location, but C:\ is easiest)
6. You should now have: `C:\platform-tools\adb.exe`

---

## Step 3: Add to Windows PATH (Permanent)

### Option A: PowerShell (Admin Required)

**Easiest** - Run PowerShell as Administrator:

```powershell
# Open PowerShell as Administrator (right-click → Run as Administrator)
$env:PATH += ";C:\platform-tools"

# Make it permanent (requires admin)
[Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";C:\platform-tools", "Machine")

# Verify
adb version
```

### Option B: Manual GUI (No Admin Needed)

1. Press **Win + X** → **Settings**
2. Type `environment` in search → **Edit environment variables**
3. Click **Environment Variables**
4. Under "User variables for [YourName]" → Click **New**
5. Variable name: `PATH`
6. Variable value: `C:\platform-tools`
7. Click OK → OK → OK

**Important**: Close PowerShell completely and reopen it for changes to take effect.

### Option C: Git Bash / Command Prompt

If you have Git Bash installed, the PATH change might already work there before needing to reopen PowerShell.

---

## Step 4: Verify (After Restarting PowerShell)

Close PowerShell completely, then reopen and run:

```powershell
adb version
```

If you see Android Debug Bridge version info, **ADB is ready!** ✓

---

## Step 5: Connect Your Device

```powershell
adb devices
```

Should show something like:
```
List of attached devices
xxxxxxxxxxxxxxxx       device
```

If you see "unauthorized", tap "Allow" on your device screen.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `adb: command not found` | PATH not updated. Close & reopen PowerShell, or use Option A (admin) |
| Device shows `unauthorized` | Tap "Allow" on device notification |
| Device not listed | Enable USB Debugging in Android settings |

---

## Quickest Path Forward

1. **Right now**: Download from https://developer.android.com/tools/releases/platform-tools
2. **Extract to**: `C:\platform-tools\`
3. **Option A** (quick): Open PowerShell as Admin and run both lines above
4. **Close PowerShell** completely
5. **Reopen PowerShell** and test: `adb version`

Then reply with the output and we'll continue! 🚀
