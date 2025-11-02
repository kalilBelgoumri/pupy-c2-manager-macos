# 🚀 Pupy C2 Manager - macOS Application

**Complete Professional C2 Framework with Payload Bundler & Victim Controller**

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Platform](https://img.shields.io/badge/platform-macOS%20arm64-orange)
![Python](https://img.shields.io/badge/python-3.12%2B-green)
![License](https://img.shields.io/badge/license-Authorized%20Use%20Only-red)

---

## ✨ Features

### 📦 **Bundler Module**
- **Standalone Payloads** : Génération d'exécutables C2 autonomes
- **🆕 Patch Mode** : Injection dans des applications existantes (ChromeSetup.exe, etc.)
- **5 niveaux d'obfuscation** : De basique à EXTREME (anti-analysis)
- **Cross-platform** : Support Windows/macOS/Linux
- **PyInstaller integration** : Compilation automatique en natif
- **GitHub Actions** : Build Windows PE automatisé

### 👥 **Victim Management**
- **Listener TCP** : Port configurable, multi-clients
- **Alertes temps réel** : Popup automatique lors de nouvelles connexions
- **Actions rapides** : Boutons whoami, hostname, ipconfig, systeminfo, etc.
- **Screenshots** : Capture d'écran distante avec sauvegarde auto
- **Keylogger** : Enregistrement des frappes (durée configurable)
- **Transferts de fichiers** : Download/Upload avec chemins personnalisés
- **Shell interactif** : Exécution de commandes système
- **Artifacts auto** : Stockage dans `~/pupy_artifacts/` (downloads, screenshots, keylogs)

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

## 🚀 Utilisation

### Démarrage

**Depuis les sources :**
```bash
cd /Users/kalilbelgoumri/Desktop/pupy-c2-manager-macos
python3 src/main.py
```

**Avec l'environnement virtuel :**
```bash
source /Users/kalilbelgoumri/Desktop/pupy_env/bin/activate
python src/main.py
```

---

## 📱 Onglets de l'Application

### 🔨 Onglet 1 : Bundler
**Créer des payloads C2**

#### Mode Standalone
1. Configurer Listener IP/Port
2. Choisir le niveau d'obfuscation (1-5)
3. Cliquer sur **Build Payload**

#### 🆕 Mode Patch
1. Configurer Listener IP/Port
2. Choisir le niveau d'obfuscation (1-5)
3. ✅ **Cocher "Patch Mode"**
4. Cliquer sur **Browse** → Sélectionner l'app à patcher (ex: `ChromeSetup.exe`)
5. Cliquer sur **Build Payload**

**Fichiers de sortie :**
- `dist/c2_payload` ou `dist/c2_payload.exe` (standalone)
- `dist/[NomOriginal].exe` (patch mode)

📚 **Documentation complète** : Voir [PATCH_MODE.md](PATCH_MODE.md)

### 👥 Onglet 2 : Client (Victims)
**Contrôler les machines infectées**

#### Démarrer le Listener
1. Configurer le port (défaut: 4444)
2. Cliquer sur **▶️ Start Listener**
3. Attendre les connexions (popup automatique)

#### Actions Disponibles

**🧰 Quick Actions (boutons):**
- Whoami
- Hostname
- IP Config
- System Info
- List Processes
- Client Info

**⚙️ Commands:**
- **📷 Screenshot** : Capture d'écran (sauvegardé dans `~/pupy_artifacts/screenshots/`)
- **⬇️ Download** : Télécharger un fichier depuis la victime
- **⬆️ Upload** : Envoyer un fichier vers la victime
- **⌨️ Keylogger** : Enregistrer les frappes (durée configurable)
- **▶️ Execute** : Commande shell personnalisée

### 📋 Onglet 3 : Logs
**Surveiller toutes les opérations**

- Logs temps réel de toutes les actions
- Historique des commandes exécutées
- Messages d'erreur et diagnostics
- 🗑️ Effacer les logs
- 💾 Exporter vers fichier

### ⚙️ Onglet 4 : Settings
**Configurer l'application**

- **GitHub Workflow** : Informations sur la compilation Windows PE
- **Build automatique** : Via GitHub Actions pour obtenir un `.exe` Windows
- Paramètres de configuration persistants

---

## 🎯 Workflow Complet

### 1️⃣ Phase Listener
```
1. Ouvrir l'onglet Client
2. Configurer le port (défaut: 4444)
3. Cliquer sur "▶️ Start Listener"
4. Listener actif → prêt à recevoir les connexions
```

### 2️⃣ Phase Bundler (Mode Standalone)
```
1. Onglet Bundler
2. IP Listener: 192.168.1.40 (votre IP)
3. Port: 4444
4. Obfuscation: Niveau 5 (MAX)
5. Cliquer sur "Build Payload"
6. Attendre 30-60 secondes
7. Récupérer dist/c2_payload ou dist/c2_payload.exe
```

### 3️⃣ Phase Bundler (Mode Patch)
```
1. Onglet Bundler
2. IP Listener: 192.168.1.40
3. Port: 4444
4. Obfuscation: Niveau 5
5. ✅ Cocher "Patch Mode"
6. Browse → Sélectionner ChromeSetup.exe
7. Cliquer sur "Build Payload"
8. Attendre 30-60 secondes
9. Récupérer dist/ChromeSetup.exe (patché)
```

### 4️⃣ Phase Déploiement
```
1. Transférer l'exécutable vers la machine cible (avec autorisation)
2. Exécuter sur la cible
3. Retour automatique vers le listener
```

### 5️⃣ Phase Contrôle
```
1. Onglet Client → Popup de connexion automatique
2. Sélectionner la victime dans la liste
3. Utiliser les boutons Quick Actions ou commandes manuelles
4. Screenshots → ~/pupy_artifacts/screenshots/
5. Keylogger → ~/pupy_artifacts/keylogs/
6. Downloads → ~/pupy_artifacts/downloads/
```

---

## 🛡️ Techniques d'Obfuscation

| Niveau | Techniques | Délai |
|--------|-----------|-------|
| 1 | Base64 | Aucun |
| 2 | XOR + Base64 | 1-3s |
| 3 | XOR + Base64 + Sandbox Detection | 5-15s |
| 4 | Dynamic Imports + XOR | 5-15s |
| 5 | **EXTREME** : Anti-debugging + Analysis Detection + Long delay | 60-300s |

**Niveau 5 détecte** : IDA, Ghidra, OllyDbg, WinDbg, x64dbg, Wireshark, Burp, Fiddler, VirtualBox, VMware, QEMU

---

## 📊 Configuration Système

| Composant | Requis |
|-----------|--------|
| OS | macOS (arm64) ou Windows |
| Python | 3.12+ |
| PyInstaller | 6.16.0+ |
| RAM | 4 GB minimum |
| Storage | 500 MB pour dépendances |
| Environnement | `/Users/kalilbelgoumri/Desktop/pupy_env` |

---

## 🔄 Compilation Cross-Platform

### macOS → macOS ✅
```bash
python src/c2_bundler_simple.py
# Résultat: dist/c2_payload (Mach-O arm64)
```

### macOS → Windows ❌ (Local)
PyInstaller ne peut pas cross-compiler. Utiliser GitHub Actions :

1. Push vers le repo
2. Workflow `.github/workflows/build-windows-pe.yml` démarre automatiquement
3. Télécharger l'artifact `c2-payload-windows.exe`

### Windows → Windows ✅
```cmd
python src\c2_bundler_simple.py
# Résultat: dist\c2_payload.exe (PE)
```

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

## 📈 Performances

- **Listener** : Multi-clients simultanés
- **Payload** : 8-15 MB (standalone), +10-15 MB (patch mode)
- **Artifacts** : Sauvegarde automatique organisée par catégorie
- **Logs** : Auto-trim à 10 000 caractères

---

## ✅ Statut Actuel

| Fonctionnalité | Statut |
|----------------|--------|
| Standalone Payload | ✅ Opérationnel |
| Patch Mode | ✅ Opérationnel |
| Obfuscation Niv. 1-5 | ✅ Opérationnel |
| Listener TCP | ✅ Opérationnel |
| Screenshot | ✅ Opérationnel |
| Keylogger | ✅ Opérationnel |
| Download/Upload | ✅ Opérationnel |
| Quick Actions | ✅ Opérationnel |
| Artifact Management | ✅ Opérationnel |
| GitHub Actions (Windows PE) | ✅ Opérationnel |

---

## 🚀 Améliorations Futures

- [ ] Support SSL/TLS pour communication chiffrée
- [ ] Multi-listener simultanés
- [ ] Filtrage avancé des victimes
- [ ] Persistence automatique
- [ ] Module de lateral movement
- [ ] Interface web optionnelle

---

## ⚖️ Avertissement Légal

**UTILISATION AUTORISÉE UNIQUEMENT**

Cette application est conçue EXCLUSIVEMENT pour :
- ✅ Tests de sécurité autorisés (pentest avec accord écrit)
- ✅ Recherche en cybersécurité dans un environnement contrôlé
- ✅ Formation en sécurité informatique

**INTERDICTIONS STRICTES :**
- ❌ Utilisation sans autorisation écrite
- ❌ Déploiement sur systèmes tiers
- ❌ Distribution malveillante
- ❌ Violation de la vie privée

**L'utilisation non autorisée constitue un DÉLIT PÉNAL** dans la plupart des juridictions.

---

## 👤 Auteur

Projet C2 Framework - Edition macOS  
Version 2.0.0 - Novembre 2025

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
