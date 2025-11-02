# 📍 WHERE TO FIND LOGS - Guide Complet

## 🎯 IMPORTANT: Les logs sont maintenant GARANTIS

Chaque niveau d'obfuscation écrit les logs **AVANT** d'essayer d'exécuter le payload.

---

## 📁 Localisations des Logs

### Sur Windows

#### Option 1: Via PowerShell
```powershell
# Chemin TEMP
$env:TEMP

# Résultat: Généralement C:\Users\[UserName]\AppData\Local\Temp

# Afficher le contenu
cat "$env:TEMP\c2_payload.log"
cat "$env:TEMP\c2_wrapper.log"
```

#### Option 2: Via Explorateur
1. Appuyer sur **Win + R**
2. Taper: `%TEMP%`
3. Appuyer sur Entrée
4. Chercher les fichiers: `c2_payload.log` ou `c2_wrapper.log`

#### Option 3: Chemin complet (Généralement)
```
C:\Users\[YourUsername]\AppData\Local\Temp\c2_payload.log
C:\Users\[YourUsername]\AppData\Local\Temp\c2_wrapper.log
```

### Sur macOS / Linux

```bash
# TEMP dir
$TMPDIR      # Usually /var/folders/xx/xxxxx/T/

# Or fallback
/tmp/c2_payload.log
/tmp/c2_wrapper.log

# Afficher le contenu
cat /tmp/c2_payload.log
tail -f /tmp/c2_payload.log   # Follow in real-time
```

---

## 📝 Contenu des Logs

### c2_payload.log (NOUVEAU!)
Créé par le payload lui-même au démarrage

**Contenu attendu:**
```
[STARTUP] Level 1 obfuscation starting
[STARTUP] Python version: 3.11.0 (main, Oct 10 2025)
[STARTUP] Platform: win32
[STARTUP] Delay complete, decoding payload...
[STARTUP] Successfully decoded payload
[STARTUP] Executing payload...
[STARTUP] C2 Client initialized
[STARTUP] Attempting connection to 192.168.1.40:4444
```

### c2_wrapper.log (Patch mode uniquement)
Créé si tu utilises le mode "patch" (wrapper + original app)

**Contenu attendu:**
```
[2025-11-02 14:23:45] Launching original
[2025-11-02 14:23:46] Starting original app
[2025-11-02 14:23:47] C2 starting
[2025-11-02 14:23:48] C2 error: Connection refused
```

---

## 🔴 Si les logs ne s'affichent pas

### Vérifier 1: Le dossier TEMP existe
```powershell
Test-Path $env:TEMP
# Output: True
```

### Vérifier 2: Permissions d'écriture
```powershell
# Créer un fichier test
"test" | Out-File "$env:TEMP\test.txt"
cat "$env:TEMP\test.txt"
# Si c'est affiché, les permissions OK
```

### Vérifier 3: L'exe s'est vraiment lancé
```powershell
# Lancer avec output visible
.\c2_payload.exe

# Si une fenêtre s'ouvre/se ferme très vite, l'exe s'est lancé
# Si RIEN ne se passe, c'est peut-être un problème PyInstaller
```

### Vérifier 4: Chercher partout
```powershell
# Chercher tous les fichiers c2_payload.log du système
Get-ChildItem -Path C:\ -Filter "c2_payload.log" -Recurse -ErrorAction SilentlyContinue

# Ou chercher fichiers modifiés récemment
Get-ChildItem -Path $env:TEMP -Filter "*.log" | Sort-Object LastWriteTime -Descending
```

---

## 🧪 TEST RAPIDE: Vérifier que la logging fonctionne

### Créer un fichier de test
```powershell
# Sur Windows
$testFile = "$env:TEMP\test_write.txt"
"Hello from PowerShell" | Out-File $testFile
cat $testFile
Remove-Item $testFile
```

Si ce test fonctionne, le TEMP dir est accessible.

---

## 📊 Flux de Logs Attendus

### Scénario 1: Success ✅
```
[STARTUP] Level 2 obfuscation starting
[STARTUP] Delay complete, decoding payload...
[STARTUP] Successfully decoded payload
[STARTUP] Executing payload...
[STARTUP] C2 Client initialized
[STARTUP] Attempting connection to 192.168.1.40:4444
[SUCCESS] Connection successful!
```

### Scénario 2: Connection Refused ❌
```
[STARTUP] Level 2 obfuscation starting
[STARTUP] Successfully decoded payload
[STARTUP] Executing payload...
[STARTUP] C2 Client initialized
[STARTUP] Attempting connection to 192.168.1.40:4444
[ERROR] Connection failed: [WinError 10061] No connection possible
```

### Scénario 3: Module Import Error ❌ (Ancien bug)
```
[STARTUP] Level 1 obfuscation starting
[STARTUP] Successfully decoded payload
[STARTUP] Executing payload...
[ERROR] Execution failed: name 'platform' is not defined
[ERROR] Traceback: Traceback (most recent call last):
  File "<string>", line 15, in <module>
NameError: name 'platform' is not defined
```

---

## 💻 Automatiser la Recherche (PowerShell Script)

Crée un script `find_logs.ps1` :

```powershell
# find_logs.ps1
$tempDir = $env:TEMP
$logFiles = Get-ChildItem -Path $tempDir -Filter "c2_*.log" -ErrorAction SilentlyContinue

if ($logFiles) {
    Write-Host "Found logs:" -ForegroundColor Green
    foreach ($file in $logFiles) {
        Write-Host "  - $($file.FullName)" -ForegroundColor Cyan
        Write-Host "    Last modified: $($file.LastWriteTime)" -ForegroundColor Gray
        Write-Host "    Size: $($file.Length) bytes" -ForegroundColor Gray
        Write-Host "    ---" -ForegroundColor Gray
        Get-Content $file.FullName | Select-Object -Last 10
        Write-Host ""
    }
} else {
    Write-Host "No c2_*.log files found in $tempDir" -ForegroundColor Red
}
```

Utilisation:
```powershell
powershell -ExecutionPolicy Bypass -File find_logs.ps1
```

---

## 🔗 Integration avec la GUI

Une fois les logs trouvés:

1. Copie le contenu de `c2_payload.log`
2. Envoie-le moi avec le rapport
3. Je vais identifier le problème exactement

---

## ✅ Checklist de Diagnostic

- [ ] Vérifier que `%TEMP%` est accessible
- [ ] Lancer `c2_payload.exe`
- [ ] Attendre 5 secondes
- [ ] Chercher `c2_payload.log` dans `%TEMP%`
- [ ] Si trouvé → copier le contenu
- [ ] Si non trouvé → vérifier permissions
- [ ] Envoyer le log

---

## 📞 Si Problème

1. Copie le exact path du fichier trouvé
2. Copie les 10 dernières lignes du log
3. Note: 
   - Version Windows (7/10/11)
   - Obfuscation level utilisé
   - IP du listener
4. Envoie-moi tout ça

On trouvera le problème! 🚀
