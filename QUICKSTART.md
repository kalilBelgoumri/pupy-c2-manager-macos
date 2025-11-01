# 🚀 Quick Start Guide - Pupy C2 Manager

**Get up and running in 5 minutes on macOS Tahoe**

---

## ⚡ 60-Second Setup

### 1. Install Dependencies (1 minute)
```bash
cd /Users/kalilbelgoumri/Desktop/pupy-c2-manager-macos
pip3 install -r requirements.txt
```

### 2. Run the Application (Instant)
```bash
python3 src/main.py
```

### 3. Configure Pupy Path (30 seconds)
- Go to **Settings** tab
- Click "Browse" next to "Pupy Path"
- Select: `/Users/kalilbelgoumri/Desktop/Projet_dev/pupy`
- Click "💾 Save Settings"

### ✅ Done! You're ready to bundle.

---

## 🎯 First Bundling (3 minutes)

### Step 1: Prepare an App
You need a Python or Windows executable to bundle. Example:
```python
# my_legit_app.py
print("I'm a legitimate app!")
```

### Step 2: Go to Bundler Tab
1. Click **"📦 Bundler"** tab
2. Click **"Browse"** button
3. Select your app file

### Step 3: Configure
- **Output Name**: MyApp
- **Listener IP**: 0.0.0.0 (or your attacking machine IP)
- **Listener Port**: 4444
- **Obfuscation**: Medium (for first test)

### Step 4: Bundle
1. Check "Auto-test with ClamAV" if you want AV testing
2. Click **"🚀 Bundle & Compile"**
3. Wait for completion (takes 2-3 minutes)
4. Check **Logs** tab for progress

### Step 5: Find Output
1. Click **"📁 Open Output"** button
2. Your bundled exe is in the output folder

---

## 👥 Testing with Mock Victims

The **Victims** tab has mock data preloaded. To see it:

1. Click **"👥 Victims"** tab
2. You should see 3 test clients
3. Click on a victim to see details
4. Try commands: `whoami`, `ls`, `getprivs`

---

## ⚙️ Essential Settings

### Required
| Setting | Value | Purpose |
|---------|-------|---------|
| Pupy Path | `/Users/kalilbelgoumri/Desktop/Projet_dev/pupy` | Framework location |
| Listener Port | 4444 | C2 communication port |

### Optional
| Setting | Value | Purpose |
|---------|-------|---------|
| Listener IP | 0.0.0.0 | Bind address (0.0.0.0 = all interfaces) |
| Output Directory | Auto | Where bundled files go |
| Obfuscation | 3 | Anti-AV level (0-5) |

---

## 📊 Understanding Tabs

### 📦 Bundler Tab
**What:** Bundle apps with Pupy payload
**How:** Select app → Configure → Click Bundle → Wait
**Output:** Malicious executable

### 👥 Victims Tab  
**What:** Manage connected machines
**How:** See list → Select victim → Execute commands
**Commands:** whoami, ls, shell, migrate, download, etc.

### ⚙️ Settings Tab
**What:** Configure everything
**How:** Set paths and options → Click Save
**Remember:** Changes apply immediately

### 📋 Logs Tab
**What:** See what's happening
**How:** Watch real-time output
**Export:** Save logs to file

---

## 🔧 Build .app Bundle (Optional)

### Create Standalone .app
```bash
chmod +x build_macos.sh
./build_macos.sh
```

**Creates:**
- `dist/Pupy C2 Manager.app` - Double-clickable app
- `dist/Pupy-C2-Manager-1.0.0.dmg` - DMG installer

### Run .app
```bash
open dist/Pupy\ C2\ Manager.app
```

---

## 🐛 Quick Troubleshooting

### App won't start
```bash
# Check Python
python3 --version  # Should be 3.8+

# Check PyQt5
python3 -c "from PyQt5.QtWidgets import QApplication; print('OK')"

# Try running with verbose output
python3 src/main.py 2>&1 | head -20
```

### Pupy path not found
```bash
# Verify Pupy exists
ls /Users/kalilbelgoumri/Desktop/Projet_dev/pupy
# Should show: README.md, setup.py, client/, etc.
```

### Bundling fails
1. Check Pupy path in Settings
2. Verify app file exists
3. Check output directory has write permissions
4. Check Logs tab for error messages

### ClamAV not available
```bash
# Install
brew install clamav

# Update signatures
freshclam
```

---

## 📱 Common Commands for Victims

Once connected, try these in the command field:

```bash
# Information gathering
whoami              # Current user
id                  # User ID and groups
hostname            # Computer name
uname -a            # System information

# File operations
ls                  # List files
ls -la              # List with details
cd /path            # Change directory
pwd                 # Current directory

# System commands
ps aux              # List processes
netstat -an         # Network connections
ifconfig            # Network interfaces

# Pupy commands
shell               # Interactive shell
screenshot          # Capture screen
download /path      # Download file
upload /path        # Upload file
getprivs            # Show privileges
migrate PID         # Inject into process
```

---

## 🎓 Example: Full Workflow

### Scenario: Bundle notepad.py and test

**Step 1: Create test app**
```bash
cat > /tmp/test_app.py << 'EOF'
print("This is a test application")
print("Running on", __import__('platform').platform())
EOF
```

**Step 2: Launch manager**
```bash
python3 src/main.py
```

**Step 3: Configure (Settings tab)**
1. Set Pupy path
2. Set listener to 0.0.0.0:4444
3. Save

**Step 4: Bundle (Bundler tab)**
1. Select `/tmp/test_app.py`
2. Set output name: `TestApp`
3. Set obfuscation: Medium
4. Click Bundle
5. Wait 3 minutes

**Step 5: Test anti-AV**
1. Check ClamAV box
2. Click Validate

**Step 6: Deploy**
1. Get bundled exe from output folder
2. Copy to target machine
3. Execute
4. Watch Victims tab for callback

**Step 7: Control**
1. Select victim in Victims tab
2. Type: `whoami`
3. Click Execute
4. See result

---

## 🚀 Next Steps

1. ✅ Run the app
2. ✅ Configure Pupy path
3. ✅ Bundle a test app
4. ✅ Test ClamAV
5. → Deploy to target (when authorized)

---

## 📞 Need Help?

| Issue | Solution |
|-------|----------|
| Can't find Pupy | Check path: `/Users/kalilbelgoumri/Desktop/Projet_dev/pupy` |
| PyQt5 error | Run: `pip3 install PyQt5==5.15.9` |
| Port in use | Change listener port in Settings |
| No output files | Check output directory permissions |
| Victim not connecting | Verify firewall and listener IP |

---

## ✨ Key Shortcuts

| Action | Keyboard |
|--------|----------|
| Clear logs | Right-click → Clear |
| Export logs | Click "💾 Export" |
| Refresh victims | Auto (5 sec) or click "🔄" |
| Open output folder | Click "📁 Open Output" |

---

## 🎯 Success Checklist

- [ ] Python 3.8+ installed
- [ ] PyQt5 installed
- [ ] Pupy path configured
- [ ] Can see Bundler tab
- [ ] Can see mock victims
- [ ] Can execute test bundle
- [ ] ClamAV testing works
- [ ] Logs display correctly

**All checked? You're ready for production! 🎉**

---

**Version:** 1.0.0 Quick Start  
**Last Updated:** November 2025  
**Status:** Ready to Deploy ✅

