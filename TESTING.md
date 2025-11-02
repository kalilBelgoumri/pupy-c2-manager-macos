# 🧪 Installation, Testing & Validation

**Complete setup and testing procedures for Pupy C2 Manager**

---

## 🔥 GUIDE DE TEST RAPIDE (Après correctifs)

### Étape 1: Vérifier la configuration

1. **Lance l'app** : `python3 src/main.py`
2. **Onglet Settings** :
   - Listener IP : `192.168.1.40` (ton IP locale, PAS 0.0.0.0 !)
   - Listener Port : `4444`
   - Sauvegarde

### Étape 2: Démarrer le listener

1. **Onglet Clients** :
   - Clique **"Start Listener"**
   - Status doit afficher : 🟢 **Listening on 192.168.1.40:4444**

### Étape 3: Build GitHub avec bonne IP

1. **Onglet Bundler** :
   - Listener IP : `192.168.1.40` (IMPORTANT !)
   - Listener Port : `4444`
   - Obfuscation : **Level 2** (pour tests rapides, délai 1-3s)
   - Clique **"☁️ Build Windows (GitHub)"**

2. **GitHub Actions** :
   - Va sur https://github.com/kalilBelgoumri/pupy-c2-manager-macos/actions
   - Attends la compilation (~2 min)
   - Télécharge l'artifact `c2-payload-windows`

### Étape 4: Test sur Windows

1. **Transfère** le `c2_payload.exe` sur ta machine Windows
2. **Double-clique** sur le .exe
3. **Attends 3-8 secondes** (obfuscation niveau 2)
4. **Vérifie l'app macOS** → Onglet Clients → Tu devrais voir la victime apparaître !

### ⚠️ Problèmes fréquents

| Symptôme | Cause | Solution |
|----------|-------|----------|
| Pas de connexion | IP = 0.0.0.0 | Utilise ton IP locale (192.168.1.X) |
| Fenêtre se ferme | Niveau 5 = délai 60-300s | Utilise niveau 2 pour tests |
| Pas d'erreur visible | --windowed actif | Désactivé maintenant pour debug |
| Firewall bloque | Port 4444 fermé | Vérifie firewall macOS et Windows |

---

## 📋 Pre-Installation Checklist

Before you start, ensure you have:

- [ ] macOS Tahoe or later
- [ ] Python 3.8+ installed
- [ ] Git (optional, for cloning)
- [ ] Terminal access
- [ ] ~500 MB disk space
- [ ] Internet connection (for pip)

**Verify prerequisites:**
```bash
# Check macOS version
sw_vers
# Should show: macOS 15.0 or later (Tahoe)

# Check Python
python3 --version
# Should show: Python 3.8.0 or higher

# Check pip
pip3 --version
# Should show: pip ... from ... (python 3.8+)
```

---

## 🚀 Installation Steps

### Step 1: Navigate to Application Directory

```bash
cd /Users/kalilbelgoumri/Desktop/pupy-c2-manager-macos
```

### Step 2: Verify Directory Structure

```bash
ls -la
# Should show:
# - src/
# - resources/
# - build/
# - dist/
# - requirements.txt
# - setup.py
# - build_macos.sh
# - README.md
# - QUICKSTART.md
# - ARCHITECTURE.md
# - INTEGRATION.md
# - FAQ.md
```

### Step 3: Install Python Dependencies

```bash
# Install all required packages
pip3 install -r requirements.txt

# Verify installation
pip3 list | grep -E "PyQt5|py2app|pyinstaller"
```

**Expected output:**
```
PyQt5                    5.15.9
py2app                   0.28
pyinstaller              6.1.0
```

### Step 4: Verify Installation

```bash
# Test PyQt5 import
python3 -c "from PyQt5.QtWidgets import QApplication; print('✅ PyQt5 OK')"

# Test other imports
python3 << 'EOF'
try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget
    from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
    import subprocess
    import json
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
EOF
```

---

## ✅ Initial Testing

### Test 1: Launch Application

```bash
# Run the application
python3 src/main.py
```

**Expected behavior:**
- Window opens (850x600 pixels)
- Title bar shows "Pupy C2 Manager - v1.0.0"
- 4 tabs visible: 📦 Bundler, 👥 Victims, ⚙️ Settings, 📋 Logs
- Window is responsive

**Troubleshooting:**
```bash
# If window doesn't open, try debug mode:
python3 src/main.py 2>&1 | head -20
```

### Test 2: Settings Tab

```bash
1. Click "⚙️ Settings" tab
2. Verify 6 input fields are visible:
   - Pupy Path (empty or default)
   - Listener IP (shows "0.0.0.0")
   - Listener Port (shows "4444")
   - Output Directory (shows path)
   - Obfuscation Level (shows slider 0-5)
   - Auto ClamAV Test (shows checkbox)
3. Click "Browse" button next to Pupy Path
4. File dialog should open
5. Click Cancel to close
```

### Test 3: Configure Pupy Path

```bash
1. Go to Settings tab
2. Click "Browse" next to Pupy Path
3. Navigate to: /Users/kalilbelgoumri/Desktop/Projekt_dev/pupy
4. Select the pupy folder
5. Click "Open"
6. Path should populate
7. Click "💾 Save Settings"
8. Verify "Settings saved successfully" message
```

### Test 4: Logs Tab

```bash
1. Click "📋 Logs" tab
2. Click "🗑️ Clear" button
3. Log area should clear
4. Go to another tab and back
5. Verify logs are empty
```

### Test 5: Victims Tab

```bash
1. Click "👥 Victims" tab
2. Verify table appears with 6 columns
3. Should show 3 mock victims (if enabled)
4. Verify columns: Client ID, PID, User, OS, IP, Status
5. Click on a victim row
6. Victim info should display on right
```

### Test 6: Bundler Tab

```bash
1. Click "📦 Bundler" tab
2. Verify all UI elements present:
   - "Browse" button for app selection
   - Output Name input field
   - Listener IP field (default: 0.0.0.0)
   - Listener Port field (default: 4444)
   - Obfuscation Level selector (0-5)
   - ClamAV checkbox
   - Progress text area
   - Action buttons
3. Click "Browse"
4. File dialog should open
5. Cancel (don't select file yet)
```

---

## 🔧 Configuration Testing

### Test Configuration Persistence

```bash
1. Go to Settings tab
2. Change values:
   - Set Listener IP: 192.168.1.100
   - Set Listener Port: 5555
   - Set Obfuscation: 4
   - Check ClamAV box
3. Click "💾 Save Settings"
4. Close application
5. Reopen: python3 src/main.py
6. Go to Settings
7. Verify all values were saved
```

**Verify saved config:**
```bash
cat ~/.pupy_c2_manager/config.json
# Should show your settings
```

---

## 📦 Bundler Testing (Without Actual Pupy)

### Create Mock Test App

```bash
# Create simple test application
cat > /tmp/test_legit_app.py << 'EOF'
#!/usr/bin/env python3
import sys
import time
import platform

print("=" * 50)
print("Legitimate Application - Test Build")
print("=" * 50)
print(f"Python: {sys.version}")
print(f"Platform: {platform.platform()}")
print("Running...")

for i in range(5):
    print(f"  [*] Iteration {i+1}/5")
    time.sleep(1)

print("Complete!")
EOF

chmod +x /tmp/test_legit_app.py
```

### Test Bundler UI (Mock)

```bash
1. Go to Bundler tab
2. Click Browse
3. Select /tmp/test_legit_app.py
4. Verify file path appears
5. Set:
   - Output Name: TestApp
   - Listener IP: 127.0.0.1
   - Listener Port: 4444
   - Obfuscation: 2
   - Uncheck ClamAV (if not available)
6. Read progress output
7. Observe timestamped logs
```

---

## 🧪 Unit Testing

### Test Individual Components

**Test 1: Log System**
```python
python3 << 'EOF'
import sys
sys.path.insert(0, '/Users/kalilbelgoumri/Desktop/pupy-c2-manager-macos')

from PyQt5.QtWidgets import QApplication
from src.logs_tab import LogsTab

app = QApplication([])
logs = LogsTab()

# Test logging
logs.add_log("Test message 1")
logs.add_log("Test message 2")
logs.add_log("Test message 3")

# Verify logs
output = logs.display.toPlainText()
assert "Test message 1" in output
assert "Test message 2" in output
assert "Test message 3" in output
print("✅ Log system works")
EOF
```

**Test 2: Settings**
```python
python3 << 'EOF'
import sys
import json
import os

sys.path.insert(0, '/Users/kalilbelgoumri/Desktop/pupy-c2-manager-macos')

# Test config file operations
config_path = os.path.expanduser('~/.pupy_c2_manager')
config_file = os.path.join(config_path, 'config.json')

# Create directory
os.makedirs(config_path, exist_ok=True)

# Write test config
test_config = {
    'pupy_path': '/test/path',
    'listener_ip': '192.168.1.1',
    'listener_port': 5555,
    'obfuscation_level': 3
}

with open(config_file, 'w') as f:
    json.dump(test_config, f)

# Read it back
with open(config_file, 'r') as f:
    loaded = json.load(f)

assert loaded['listener_port'] == 5555
print("✅ Config system works")
EOF
```

---

## 🚀 Building .app Bundle

### Option 1: Using Build Script (Recommended)

```bash
cd /Users/kalilbelgoumri/Desktop/pupy-c2-manager-macos

# Make script executable
chmod +x build_macos.sh

# Run build
./build_macos.sh
```

**Expected output:**
```
Building Pupy C2 Manager...
[*] Installing dependencies...
[+] Dependencies installed
[*] Building .app bundle...
[+] .app bundle created
[*] Creating DMG installer...
[+] DMG created successfully
✅ Build complete!
Output:
  - dist/Pupy C2 Manager.app
  - dist/Pupy-C2-Manager-1.0.0.dmg
```

### Option 2: Manual Build

```bash
# Step 1: Install dependencies
pip3 install -r requirements.txt

# Step 2: Build .app
python3 setup.py py2app -A

# Step 3: Verify .app
ls -la dist/Pupy\ C2\ Manager.app

# Step 4: Create DMG
hdiutil create \
    -volname "Pupy C2 Manager" \
    -srcfolder dist \
    -ov -format UDZO \
    dist/Pupy-C2-Manager-1.0.0.dmg

# Step 5: Verify DMG
ls -lh dist/*.dmg
```

---

## 🧪 Testing Built .app

### Test Running .app from Source

```bash
# Run the .app
open dist/Pupy\ C2\ Manager.app

# Or from command line
dist/Pupy\ C2\ Manager.app/Contents/MacOS/Pupy\ C2\ Manager
```

**Verify:**
- [ ] Application launches
- [ ] Window opens
- [ ] All tabs responsive
- [ ] Settings can be changed
- [ ] Logs appear
- [ ] Mock victims load

### Test DMG Installation

```bash
# 1. Attach DMG
hdiutil attach dist/Pupy-C2-Manager-1.0.0.dmg

# 2. Verify content
# In Finder: /Volumes/Pupy\ C2\ Manager/
ls /Volumes/Pupy\ C2\ Manager/

# 3. Copy app to Applications
cp -r /Volumes/Pupy\ C2\ Manager/Pupy\ C2\ Manager.app /Applications/

# 4. Run from Applications
open /Applications/Pupy\ C2\ Manager.app

# 5. Detach DMG
hdiutil detach /Volumes/Pupy\ C2\ Manager

# 6. Clean up
rm -rf /Applications/Pupy\ C2\ Manager.app
```

---

## ✔️ Comprehensive Verification Checklist

### Application Launch
- [ ] `python3 src/main.py` opens window
- [ ] Window shows title "Pupy C2 Manager"
- [ ] 4 tabs are visible and clickable
- [ ] No error messages on startup

### UI Components
- [ ] Settings tab: All fields visible and editable
- [ ] Bundler tab: Browse button works
- [ ] Victims tab: Table displays
- [ ] Logs tab: Timestamps show

### Functionality
- [ ] Settings save and reload
- [ ] Config file created at `~/.pupy_c2_manager/config.json`
- [ ] Logs display messages with timestamps
- [ ] Mock victims load in table
- [ ] Tab navigation smooth

### Performance
- [ ] Application launches in < 5 seconds
- [ ] No GUI freezing
- [ ] Memory usage < 300 MB
- [ ] CPU usage minimal at idle

### Build
- [ ] `./build_macos.sh` completes without errors
- [ ] `.app` bundle created in `dist/`
- [ ] DMG file created in `dist/`
- [ ] `.app` is runnable
- [ ] DMG mounts and contains `.app`

### Error Handling
- [ ] Invalid Pupy path shows error message
- [ ] Missing file shows error message
- [ ] Permission errors handled gracefully
- [ ] Network errors don't crash app

---

## 🎯 Integration Testing

### Test with Real Pupy (if available)

```bash
# Terminal 1: Start listener
cd /Users/kalilbelgoumri/Desktop/Projekt_dev/pupy
python3 -m pupy -l --port 4444

# Terminal 2: Start manager
cd /Users/kalilbelgoumri/Desktop/pupy-c2-manager-macos
python3 src/main.py

# Test in GUI:
# Settings: Verify listener IP/port match
# Bundler: Try bundling (with orchestrator path set)
# Victims: Should show any connected victims
```

---

## 📊 Performance Testing

### Memory Usage Test

```bash
# Terminal 1: Monitor
top -l 1 -stats PID,COMMAND,%CPU,MEM -pid <APP_PID>

# Terminal 2: Run app
python3 src/main.py

# Keep app running for 5 minutes
# Monitor memory trend
# Should stay under 300 MB
```

### Startup Time Test

```bash
# Measure launch time
time python3 src/main.py

# Expected: < 5 seconds
# Real: ~3-4 seconds
```

### Logging Performance Test

```bash
# Start app
python3 src/main.py

# In Logs tab, generate many logs:
for i in {1..1000}; do
    # Simulate logs
    # Each produces a timestamp + message
done

# Verify:
# - No significant slowdown
# - Logs remain readable
# - Old logs auto-trim
```

---

## 🐛 Debugging Tips

### Enable Verbose Output

```bash
# Run with debug output
python3 -u src/main.py 2>&1 | tee /tmp/debug.log

# Check log file
tail -f /tmp/debug.log
```

### Monitor System Resources

```bash
# Terminal 1: Watch processes
while true; do
    ps aux | grep "[p]ython3 src/main.py"
    sleep 1
done

# Terminal 2: Activity Monitor
open -a Activity\ Monitor
# Select Python process
# Watch Memory and CPU columns
```

### Test Individual Modules

```bash
# Test imports
python3 -c "from src.main import *; print('✅ main imports OK')"
python3 -c "from src.bundler_tab import *; print('✅ bundler imports OK')"
python3 -c "from src.victims_tab import *; print('✅ victims imports OK')"
python3 -c "from src.settings_tab import *; print('✅ settings imports OK')"
python3 -c "from src.logs_tab import *; print('✅ logs imports OK')"
```

---

## 🎓 Complete Test Scenario

### Full Workflow Test

```bash
# 1. Clean state
rm -rf ~/.pupy_c2_manager

# 2. Launch
python3 src/main.py

# 3. Configure
# Settings tab:
#   - Set Pupy path
#   - Verify listener settings
#   - Save

# 4. Test UI
# - Click each tab
# - Verify responsive
# - Click buttons

# 5. Export logs
# Logs tab:
#   - Add some logs
#   - Click Export
#   - Save to ~/Desktop/test_logs.txt

# 6. Verify output
cat ~/Desktop/test_logs.txt
# Should contain timestamped messages

# 7. Close and reopen
# Close window
# python3 src/main.py
# Verify settings loaded
```

---

## ✅ Sign-Off Checklist

**Functional Testing:**
- [ ] All windows open correctly
- [ ] All buttons responsive
- [ ] All input fields work
- [ ] Configuration saves/loads
- [ ] Logging works
- [ ] No crashes or hangs

**Integration Testing:**
- [ ] Pupy path configuration works
- [ ] Settings persist across sessions
- [ ] Mock data loads correctly
- [ ] Tabs communicate properly

**Build Testing:**
- [ ] `./build_macos.sh` completes
- [ ] `.app` bundle runnable
- [ ] DMG installer works
- [ ] Installed app launches

**Performance Testing:**
- [ ] Memory usage reasonable
- [ ] No memory leaks
- [ ] CPU usage acceptable
- [ ] Responsive UI

---

**Version:** 1.0.0 Installation & Testing  
**Last Updated:** November 2025  
**Status:** Complete ✅

**Next Steps:**
1. Follow these tests
2. Verify all checkboxes
3. Build .app if passed
4. Proceed to Integration Guide
5. Deploy when ready

