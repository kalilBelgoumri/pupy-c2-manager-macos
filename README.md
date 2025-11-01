# 🚀 Pupy C2 Manager - macOS Application

**Complete Professional C2 Bundler, Anti-AV Manager, and Victim Controller for macOS Tahoe**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Platform](https://img.shields.io/badge/platform-macOS%20Tahoe-orange)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-Authorized%20Use%20Only-red)

---

## ✨ Features

### 📦 **Bundler Module**
- Bundle ANY third-party application (.py or .exe)
- Seamless Pupy payload injection
- Automatic compilation to native macOS executables
- Multi-level obfuscation (Low, Medium, High, Extreme)
- Integrated ClamAV anti-AV testing
- Real-time bundling progress

### 👥 **Victim Management**
- Real-time connected victim list
- Live victim information display
- Command execution interface
- Interactive shell support
- Process migration/injection
- Screenshot capture
- File upload/download capabilities
- Keylogger management

### ⚙️ **Advanced Configuration**
- Customizable listener IP/port
- Pupy path configuration
- Output directory management
- Obfuscation level control
- Auto-AV testing toggle
- Persistent settings

### 📋 **Logging & Diagnostics**
- Real-time operation logs
- Command execution history
- Error tracking and reporting
- Log export functionality
- Diagnostic information

---

## 🎯 Installation

### Prerequisites
- macOS Tahoe or later
- Python 3.8+
- Pupy framework installed

### Quick Setup

1. **Clone or download the repository**
```bash
# Navigate to app directory
cd /Users/kalilbelgoumri/Desktop/pupy-c2-manager-macos
```

2. **Install dependencies**
```bash
pip3 install -r requirements.txt
```

3. **Run the application**
```bash
python3 src/main.py
```

---

## 🔨 Building macOS .app Bundle

### Option 1: Using build script (Recommended)
```bash
chmod +x build_macos.sh
./build_macos.sh
```

This will create:
- `.app` bundle: `dist/Pupy C2 Manager.app`
- DMG installer: `dist/Pupy-C2-Manager-1.0.0.dmg`

### Option 2: Manual build with py2app
```bash
python3 setup.py py2app -A
```

### Option 3: Create DMG manually
```bash
hdiutil create -volname "Pupy C2 Manager" \
    -srcfolder dist \
    -ov -format UDZO \
    Pupy-C2-Manager-1.0.0.dmg
```

---

## 🚀 Usage

### Starting the Application

**From source:**
```bash
python3 src/main.py
```

**From .app bundle:**
```bash
open dist/Pupy\ C2\ Manager.app
```

**From Applications folder:**
Double-click "Pupy C2 Manager" in Applications

---

## 📱 Application Tabs

### Tab 1: 📦 Bundler
**Create weaponized applications**

1. Click "Browse" to select your application
2. Configure:
   - Output name
   - Listener IP (default: 0.0.0.0)
   - Listener port (default: 4444)
   - Obfuscation level (0-5)
3. Click "🚀 Bundle & Compile"
4. Wait for completion
5. Optional: Click "✅ Validate Anti-AV" to test with ClamAV

**Output files:**
- `MyApp_xyz.exe` - Final bundled executable
- `payload_xyz.dll` - Pupy payload
- `metadata_xyz.json` - Configuration metadata

### Tab 2: 👥 Victims
**Manage infected machines**

- **Connected Victims List**: Real-time victim display
- **Victim Info**: Selected victim details
- **Command Execution**: Run commands on victim
- **Actions**:
  - 🔄 Refresh: Update victim list
  - 🔌 Open Shell: Interactive shell
  - 💾 Migrate Process: Move payload to different process
  - ❌ Disconnect: Disconnect victim

**Available Commands:**
- `shell` - Interactive shell
- `screenshot` - Capture screen
- `whoami` - Current user
- `ls` - List files
- `cd` - Change directory
- `download` - Download files
- `upload` - Upload files
- `getprivs` - Show privileges

### Tab 3: 📋 Logs
**Monitor all operations**

- Real-time operation logging
- Command execution history
- Error messages and diagnostics
- 🗑️ Clear logs
- 💾 Export logs to file

### Tab 4: ⚙️ Settings
**Configure application**

**Pupy Configuration:**
- Pupy directory path
- Browse to Pupy installation

**Listener Configuration:**
- Listener IP address
- Listener port number

**Output Configuration:**
- Default output directory

**Bundler Configuration:**
- Obfuscation level (0-5)
- Auto-test with ClamAV

---

## 🎯 Complete Workflow Example

### 1. Setup Phase
```
1. Open Pupy C2 Manager
2. Go to Settings tab
3. Set Pupy path: /Users/user/Desktop/Projet_dev/pupy
4. Set listener IP: 192.168.1.1 (your attacking machine)
5. Set listener port: 4444
6. Click "💾 Save Settings"
```

### 2. Bundling Phase
```
1. Go to Bundler tab
2. Click "Browse" and select your app (e.g., mon_app.py)
3. Set output name: "MyApp"
4. Set obfuscation: "High"
5. Check "Auto-test with ClamAV"
6. Click "🚀 Bundle & Compile"
7. Wait for completion (3-5 minutes)
```

### 3. Testing Phase
```
1. Click "✅ Validate Anti-AV"
2. Wait for ClamAV results
3. Check Logs tab for results
4. Click "📁 Open Output" to see files
```

### 4. Deployment Phase
```
1. Copy MyApp_xyz.exe from output
2. Deploy to target machine
3. Execute on target
4. Go to Victims tab
5. See victim appear in list
```

### 5. Control Phase
```
1. Select victim in table
2. Type command in input field
3. Click "Execute"
4. See output in terminal
5. Use available commands to control machine
```

---

## 🛡️ Anti-AV Features Integrated

| Technique | Status |
|-----------|--------|
| XOR Encryption | ✅ Integrated |
| Base64 Encoding | ✅ Integrated |
| String Obfuscation | ✅ Integrated |
| Sandbox Detection | ✅ Integrated |
| Anti-Debugging | ✅ Integrated |
| Timing Jitter | ✅ Integrated |
| Process Injection | ✅ Integrated |
| Polymorphism | ✅ Integrated |

---

## 📊 System Requirements

| Component | Requirement |
|-----------|-------------|
| OS | macOS Tahoe or later |
| Python | 3.8+ |
| RAM | 4 GB minimum |
| Storage | 500 MB for dependencies |
| Network | Internet access for Pupy |

---

## 🔐 Security & Legal

### ✅ Requirements
- Authorized penetration testing ONLY
- Written permission from client
- Compliance with all applicable laws
- Proper documentation and cleanup

### ❌ Prohibited
- Unauthorized access
- Production system testing without approval
- Leaving backdoors after testing
- Violating any laws

---

## 📞 Troubleshooting

### Application won't start
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Verify PyQt5 installed
python3 -c "from PyQt5.QtWidgets import QApplication; print('OK')"

# Run with debug output
python3 src/main.py --debug
```

### Bundling fails
```bash
# Check Pupy path in Settings
# Verify app file exists
# Check output directory permissions

# Run manual bundler for details
cd /Users/kalilbelgoumri/Desktop/Projet_dev/pupy/client/legit_app
python3 deployment_orchestrator.py --app mon_app.py --name Test
```

### ClamAV test unavailable
```bash
# Install ClamAV on macOS
brew install clamav

# Update signatures
freshclam
```

---

## 🎓 File Structure

```
pupy-c2-manager-macos/
├── src/
│   ├── main.py              # Main application
│   ├── bundler_tab.py       # Bundling interface
│   ├── victims_tab.py       # Victim management
│   ├── settings_tab.py      # Configuration
│   └── logs_tab.py          # Logging
├── resources/               # App resources
├── build/                   # Build files
├── dist/                    # Distribution outputs
├── setup.py                 # Py2app configuration
├── build_macos.sh          # Build script
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 💻 Command Line Usage

### Run from source
```bash
python3 src/main.py
```

### Build .app bundle
```bash
python3 setup.py py2app -A
```

### Build with PyInstaller (alternative)
```bash
pyinstaller --onefile --windowed \
    --icon=resources/icon.png \
    --name="Pupy C2 Manager" \
    src/main.py
```

### Create DMG
```bash
hdiutil create -volname "Pupy C2 Manager" \
    -srcfolder dist \
    -ov -format UDZO \
    Pupy-C2-Manager-1.0.0.dmg
```

---

## 📈 Performance & Optimization

- **Victim list auto-refresh**: Every 5 seconds
- **Log size limit**: 10,000 characters (auto-trim)
- **Memory usage**: ~150-200 MB
- **CPU usage**: Minimal when idle

---

## 🚀 Future Enhancements

- [ ] Pupy WebSocket integration
- [ ] SSL/TLS support
- [ ] Encrypted communication
- [ ] Multi-listener support
- [ ] Advanced victim filtering
- [ ] Automated exploitation modules
- [ ] Real-time forensics
- [ ] Team collaboration features

---

## 📝 License

**Authorized Use Only**

This application is designed for authorized penetration testing and security research only. Unauthorized access or use is strictly prohibited and may violate applicable laws.

---

## 👤 Author

Security Research Project - macOS Edition

---

## 🔗 Links

- **Pupy Framework**: https://github.com/n1nj4sec/pupy
- **PyQt5 Documentation**: https://www.riverbankcomputing.com/software/pyqt
- **macOS Development**: https://developer.apple.com/macos

---

## ❓ FAQ

### Q: Can I use this on production systems?
**A:** NO. Only use on authorized test systems with written permission.

### Q: How do I update Pupy?
**A:** Update your Pupy installation separately, then point the app to the new path in Settings.

### Q: Can I distribute this app?
**A:** Only if you have proper authorization. Ensure all legal requirements are met.

### Q: Does it work on older macOS versions?
**A:** Optimized for Tahoe. May work on older versions but not officially supported.

### Q: How do I uninstall?
**A:** Delete from Applications folder or run:
```bash
rm -rf ~/Library/Application\ Support/Pupy\ C2\ Manager
```

---

**Version:** 1.0.0  
**Last Updated:** 1 November 2025  
**Status:** Production Ready ✅  
**Authorization:** Required ⚠️

---

**Ready to deploy? 🚀 Open the app and get started!**
