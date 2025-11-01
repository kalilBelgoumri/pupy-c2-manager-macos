# ❓ FAQ & Troubleshooting Guide

**Solutions to Common Issues**

---

## 📦 Installation & Setup Issues

### Q: "ModuleNotFoundError: No module named 'PyQt5'"

**Problem:** PyQt5 not installed

**Solutions:**
```bash
# Option 1: Install from requirements
pip3 install -r requirements.txt

# Option 2: Install directly
pip3 install PyQt5==5.15.9

# Option 3: Check Python version
python3 --version  # Should be 3.8+
```

**Verify:**
```bash
python3 -c "from PyQt5.QtWidgets import QApplication; print('✅ PyQt5 installed')"
```

---

### Q: "Python version 2.7 detected, need 3.8+"

**Problem:** Wrong Python version

**Solution:**
```bash
# Check version
python3 --version

# Verify pip is for Python 3
pip3 --version

# If needed, explicitly use python3
python3 src/main.py
```

---

### Q: "Command 'pip3' not found"

**Problem:** pip3 not installed or not in PATH

**Solutions:**
```bash
# macOS - Install via Homebrew
brew install python3

# Or download from python.org
# https://www.python.org/downloads/

# Verify installation
which python3
which pip3
```

---

### Q: "Permission denied when running build script"

**Problem:** Script not executable

**Solution:**
```bash
# Make executable
chmod +x build_macos.sh

# Run it
./build_macos.sh

# Or use bash directly
bash build_macos.sh
```

---

## 🚀 Application Launch Issues

### Q: "Application won't start, no error shown"

**Problem:** Silent failure (likely dependency issue)

**Solutions:**
```bash
# 1. Run with verbose output
python3 src/main.py 2>&1 | head -50

# 2. Check for import errors
python3 -c "
try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
    import subprocess
    import json
    print('✅ All imports OK')
except Exception as e:
    print(f'❌ Import error: {e}')
"

# 3. Test PyQt5 directly
python3 -c "
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
app = QApplication(sys.argv)
window = QMainWindow()
window.show()
print('✅ PyQt5 works')
"
```

---

### Q: "Application window appears then closes immediately"

**Problem:** Uncaught exception in main thread

**Solution:**
```bash
# Add error handling
python3 -c "
import sys
import traceback
try:
    exec(open('src/main.py').read())
except Exception as e:
    print('Error:', e)
    traceback.print_exc()
"
```

---

### Q: "Application window is blank/black"

**Problem:** UI not rendering properly

**Solutions:**
```bash
# 1. Try quitting and restarting
# Press Ctrl+C in terminal, then:
python3 src/main.py

# 2. Check if tabs are being created
# Edit src/main.py, add debug prints

# 3. Try running in different terminal
# macOS Terminal → try iTerm2 or different shell
```

---

## ⚙️ Settings & Configuration Issues

### Q: "Settings not saving"

**Problem:** Config file permission or path issue

**Solution:**
```bash
# 1. Check config directory exists
ls -la ~/.pupy_c2_manager/

# 2. Create if missing
mkdir -p ~/.pupy_c2_manager
chmod 700 ~/.pupy_c2_manager

# 3. Check file permissions
ls -la ~/.pupy_c2_manager/config.json

# 4. Test write access
touch ~/.pupy_c2_manager/test_write
rm ~/.pupy_c2_manager/test_write
```

---

### Q: "Pupy path not found"

**Problem:** Path doesn't exist or wrong path

**Solution:**
```bash
# 1. Verify Pupy installation
ls /Users/kalilbelgoumri/Desktop/Projet_dev/pupy/
# Should show: README.md, setup.py, client/, pupy/, etc.

# 2. Get full path
cd /Users/kalilbelgoumri/Desktop/Projet_dev/pupy
pwd

# 3. Enter in Settings
# Browse button or paste full path

# 4. Verify in config
cat ~/.pupy_c2_manager/config.json
```

---

### Q: "Can't browse directory"

**Problem:** File dialog issue (Qt issue)

**Solution:**
```bash
# 1. Try different approach
# Instead of Browse button, type path directly
# Click input field and paste path

# 2. Copy path from Finder
# In Finder, select folder
# Press Cmd+Option+C (Copy as pathname)
# Paste in application

# 3. Use Terminal to verify path first
ls /your/path
```

---

## 📦 Bundler Issues

### Q: "Bundling fails immediately"

**Problem:** deployment_orchestrator.py not found

**Solution:**
```bash
# 1. Verify orchestrator exists
ls /Users/kalilbelgoumri/Desktop/Projet_dev/pupy/client/legit_app/deployment_orchestrator.py

# 2. Set correct Pupy path in Settings
python3 src/main.py
# Settings tab → Browse Pupy path

# 3. Check logs
# Look in Logs tab for specific error message

# 4. Run orchestrator manually
cd /path/to/pupy/client/legit_app
python3 deployment_orchestrator.py --help
```

---

### Q: "Bundling takes too long (>10 minutes)"

**Problem:** Timeout or stuck process

**Solution:**
```bash
# 1. Check system resources
# macOS: Activity Monitor
# Look for high CPU or full disk

# 2. Try lower obfuscation level
# In Bundler tab, reduce to Level 1
# Obfuscation 5 can take 5+ minutes

# 3. Kill stuck process
ps aux | grep deployment_orchestrator
kill -9 <PID>

# 4. Free up disk space
# Check available disk: df -h
# Need at least 1 GB free
```

---

### Q: "Output files not created"

**Problem:** Orchestrator error or wrong output path

**Solution:**
```bash
# 1. Check output directory
# In Settings, verify output directory exists
mkdir -p ~/Desktop/pupy_output

# 2. Test directory write access
touch ~/Desktop/pupy_output/test.txt
rm ~/Desktop/pupy_output/test.txt

# 3. Change output to simple path
# Settings → Output Directory
# Try: /tmp/pupy_output

# 4. Check logs for specific error
# Logs tab should show error message
```

---

### Q: "Selected app not found / invalid"

**Problem:** File path issue

**Solution:**
```bash
# 1. File must exist
# Browse and select file
# Or manually type path and verify:
ls /path/to/your/app.py

# 2. File must be readable
ls -l /path/to/your/app.py
# Should show permissions like: -rw-r--r--

# 3. Try different app
# Create simple test file:
echo 'print("test")' > /tmp/test.py
# Try bundling this

# 4. Check file type
file /path/to/app.py
# Should show: Python script or executable
```

---

## 🦠 Anti-AV Testing Issues

### Q: "ClamAV test fails: command not found"

**Problem:** ClamAV not installed

**Solution:**
```bash
# Install ClamAV
brew install clamav

# Start daemon
brew services start clamav

# Or manually start
clamd

# Wait for it to start (takes ~30 seconds)
sleep 30

# Verify
clamdscan --version
```

---

### Q: "ClamAV shows threats (detection)"

**Problem:** Payload detected by antivirus

**Solutions:**

**Option 1: Increase obfuscation**
```
Settings → Obfuscation Level
Try: 4 or 5 (maximum)
```

**Option 2: Different obfuscation technique**
```bash
# Edit src/bundler_tab.py
# Add different obfuscation methods:
# - Compression
# - Packing (UPX)
# - Code rearrangement
```

**Option 3: Update ClamAV signatures**
```bash
# May help if signatures are old
freshclam

# Or disable ClamAV testing
Settings → Uncheck "Auto-test with ClamAV"
```

---

### Q: "ClamAV crashes or hangs"

**Problem:** Clamd daemon issue

**Solution:**
```bash
# Kill and restart daemon
brew services stop clamav
sleep 5
brew services start clamav

# Or manually:
killall clamd 2>/dev/null
sleep 2
clamd

# Update signatures
freshclam
```

---

## 👥 Victims Tab Issues

### Q: "No victims showing in Victims tab"

**Problem:** Not connected to listener or no connected victims

**Solutions:**

**Step 1: Start listener**
```bash
# Terminal 1
cd /Users/kalilbelgoumri/Desktop/Projet_dev/pupy
python3 -m pupy -l --port 4444
# Should show: [+] Listening on 0.0.0.0:4444
```

**Step 2: Verify connection settings**
```bash
# Settings tab
# Listener IP: Should match (127.0.0.1 or attacker IP)
# Listener Port: Should be 4444 (or your port)
```

**Step 3: Deploy a victim**
```bash
# Bundler tab → Bundle app
# Execute on target machine
# Wait for callback (5-10 seconds)
```

**Step 4: Check Victims tab**
```bash
# Should auto-refresh every 5 seconds
# Or manually refresh by going to another tab and back
```

---

### Q: "Victim shows but commands don't execute"

**Problem:** Victim connection or communication issue

**Solution:**
```bash
# 1. Verify victim is connected
# Right-click victim → Properties
# Should show "Status: Connected"

# 2. Try simple command first
# Type: whoami
# Click Execute

# 3. Check logs
# Logs tab should show command and result

# 4. Restart victim connection
# Bundler → Regenerate payload
# Redeploy on target
```

---

### Q: "Mock data not showing"

**Problem:** Mock data loading disabled or error

**Solution:**
```bash
# 1. Check if function is being called
# Edit src/victims_tab.py
# Uncomment: self.load_mock_data()

# 2. Verify function exists
grep -n "def load_mock_data" src/victims_tab.py

# 3. Restart application
python3 src/main.py
```

---

## 📋 Logging Issues

### Q: "Logs not appearing"

**Problem:** Logging not connected

**Solution:**
```bash
# 1. Verify logs are being generated
# Start app and watch terminal output:
python3 src/main.py 2>&1 | tee /tmp/app.log

# 2. Check Logs tab
# Click in Logs tab
# Should show timestamps
# If empty, something is not logging

# 3. Trigger some action
# Go to Bundler
# Click Browse (should log action)
```

---

### Q: "Logs tab shows old data"

**Problem:** Buffer not clearing or old config

**Solution:**
```bash
# 1. Click Clear Logs
# In Logs tab → Click "🗑️ Clear Logs"

# 2. Delete config
rm ~/.pupy_c2_manager/config.json

# 3. Restart app
python3 src/main.py
```

---

### Q: "Can't export logs"

**Problem:** File save dialog or permission issue

**Solution:**
```bash
# 1. Verify destination directory
# When prompted, browse to Desktop
# Make sure you have write permission

# 2. Try simpler path
# Save to: ~/Desktop/logs.txt

# 3. Manual export
# Copy logs manually:
python3 -c "
with open('/path/to/output/logs.txt', 'w') as f:
    f.write('Logs exported manually')
"
```

---

## 🏗️ Building & Deployment Issues

### Q: "Build script fails"

**Problem:** Various build issues

**Solution:**
```bash
# 1. Check prerequisites
python3 --version  # Need 3.8+
pip3 --version     # Need pip3

# 2. Install all dependencies
pip3 install -r requirements.txt

# 3. Run build with verbose output
bash -x build_macos.sh

# 4. Specific steps:
# Step 1: Install deps
pip3 install PyQt5==5.15.9 py2app==0.28

# Step 2: Build .app
python3 setup.py py2app -A

# Step 3: Build DMG
hdiutil create -volname "Pupy C2 Manager" \
    -srcfolder dist \
    -ov -format UDZO \
    dist/Pupy-C2-Manager-1.0.0.dmg
```

---

### Q: ".app bundle won't run"

**Problem:** Code signing or dependency issue

**Solution:**
```bash
# 1. Test if .app exists
ls -la dist/Pupy\ C2\ Manager.app

# 2. Try running directly
cd dist/Pupy\ C2\ Manager.app/Contents/MacOS
./Pupy\ C2\ Manager

# 3. Check code signature
codesign -v dist/Pupy\ C2\ Manager.app

# 4. Remove signature if blocked
sudo xattr -d com.apple.quarantine dist/Pupy\ C2\ Manager.app
```

---

### Q: "DMG won't mount"

**Problem:** DMG creation issue

**Solution:**
```bash
# 1. Verify DMG was created
ls -la dist/*.dmg

# 2. Check DMG integrity
hdiutil verify dist/Pupy-C2-Manager-1.0.0.dmg

# 3. Try mounting
hdiutil attach dist/Pupy-C2-Manager-1.0.0.dmg

# 4. Rebuild DMG
hdiutil detach /Volumes/Pupy\ C2\ Manager 2>/dev/null || true
rm dist/*.dmg
hdiutil create -volname "Pupy C2 Manager" \
    -srcfolder dist \
    -ov -format UDZO \
    dist/Pupy-C2-Manager-1.0.0.dmg
```

---

## 🔐 Security Issues

### Q: "Configuration contains sensitive data, where is it stored?"

**Answer:**
```
Location: ~/.pupy_c2_manager/config.json
Permissions: 0o700 (owner read/write only)
Contains: Pupy path, listener IP/port, settings
```

**Secure it:**
```bash
# Verify permissions
ls -la ~/.pupy_c2_manager/config.json
# Should show: -rw------- (700)

# Encrypt if needed
openssl enc -aes-256-cbc -in ~/.pupy_c2_manager/config.json \
    -out config.json.enc
```

---

### Q: "How do I remove all traces?"

**Answer:**
```bash
# Remove config
rm -rf ~/.pupy_c2_manager/

# Remove application
rm -rf dist/Pupy\ C2\ Manager.app
rm dist/*.dmg

# Remove source (if desired)
rm -rf /Users/kalilbelgoumri/Desktop/pupy-c2-manager-macos/

# Remove output payloads
rm -rf ~/Desktop/pupy_output/  # Or wherever you set output
```

---

## 🎯 Performance Issues

### Q: "Application is slow/laggy"

**Problem:** Too much processing on main thread

**Solution:**
```bash
# 1. Monitor resource usage
# Activity Monitor → CPU, Memory
# Check if app uses > 50% CPU

# 2. Check for stuck operations
# Kill and restart:
ps aux | grep "[p]ython3 src/main.py"
kill -9 <PID>
python3 src/main.py

# 3. Reduce victim list refresh rate
# Edit src/victims_tab.py
# Change: self.refresh_timer.setInterval(5000)  # 5 seconds
# To:     self.refresh_timer.setInterval(10000) # 10 seconds

# 4. Increase logging buffer
# Edit src/logs_tab.py
# Reduce MAX_BUFFER size if logs are huge
```

---

### Q: "Memory usage keeps growing"

**Problem:** Memory leak or unbounded buffer

**Solution:**
```bash
# 1. Monitor memory
# Activity Monitor → Memory tab
# Check "Real Memory" column

# 2. Restart application periodically
# Close and reopen to reset memory

# 3. Limit log buffer
# Edit src/logs_tab.py
# Add periodic clearing:
if len(self.display.toPlainText()) > 5000:
    self.display.clear()

# 4. Clear logs manually
# Logs tab → Click "Clear Logs"
```

---

## 🔗 Network Issues

### Q: "Can't connect to listener"

**Problem:** Listener not running or firewall blocking

**Solution:**
```bash
# 1. Verify listener running
netstat -an | grep 4444
# Should show: *.4444 (LISTEN)

# 2. Test connectivity
telnet 127.0.0.1 4444

# 3. Check firewall
# macOS System Settings → Security & Privacy → Firewall
# Or: sudo pfctl -s rules

# 4. Start listener manually
cd /path/to/pupy
python3 -m pupy -l --port 4444
```

---

### Q: "Payload not connecting from target"

**Problem:** Firewall, wrong IP, or connectivity issue

**Solution:**
```bash
# On target machine:
# 1. Test connectivity
ping attacker_ip
# Should get ping response

# 2. Test port
telnet attacker_ip 4444
# Should connect

# 3. Check bundled payload
# Contains correct listener IP?

# 4. Check target firewall
# Windows: netsh advfirewall show allprofiles
# Linux: sudo ufw status

# On attacker machine:
# 1. Verify listener is public
# netstat -an | grep 4444

# 2. Check if listening on correct IP
# If set to 127.0.0.1, only local connections work
# Use 0.0.0.0 for all interfaces
```

---

## 📊 Advanced Debugging

### Enable verbose logging

**Edit `src/main.py`:**
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(message)s'
)
```

### Check bundle at runtime

**Terminal:**
```bash
# While app is running
ps aux | grep python
# Look for deployment_orchestrator subprocess

# Monitor subprocess
ps -ef | head -1 && ps -ef | grep orchestrator

# Check file handles
lsof -p <PID>
```

### Debug file operations

**Check created files:**
```bash
# List all output files
ls -la ~/Desktop/pupy_output/

# Check file sizes
du -sh ~/Desktop/pupy_output/*

# Monitor file creation
# Terminal: 
watch 'ls -la ~/Desktop/pupy_output/'
```

---

## 📞 Still Having Issues?

### Collect diagnostic information:

```bash
# 1. Python version
python3 --version

# 2. Dependencies
pip3 list | grep -E "PyQt5|py2app"

# 3. Pupy version
cd /path/to/pupy
python3 -c "import pupy; print(pupy.__version__)" 2>/dev/null || echo "No version"

# 4. macOS version
sw_vers

# 5. App logs
cat ~/.pupy_c2_manager/config.json 2>/dev/null || echo "No config"

# 6. Run full diagnostic
python3 << 'EOF'
import sys
import platform
print(f"Python: {sys.version}")
print(f"macOS: {platform.mac_ver()}")
try:
    from PyQt5.QtWidgets import QApplication
    print("PyQt5: OK")
except:
    print("PyQt5: MISSING")
try:
    import subprocess
    print("subprocess: OK")
except:
    print("subprocess: MISSING")
EOF
```

---

**Version:** 1.0.0 FAQ  
**Last Updated:** November 2025  
**Status:** Comprehensive ✅

**Next:** Check INTEGRATION.md for deployment issues

