# 🪟 Guide Officiel: Télécharger Windows ISO Gratuit

## ✅ Options Légales & Gratuites

### 📥 Option 1: Windows 10 ISO (Recommandé - Gratuit)

#### Étape 1: Aller sur le Site Officiel Microsoft

```
1. Ouvrir votre navigateur
2. Aller à: https://www.microsoft.com/en-us/software-download/windows10

3. Vous verrez: "Download Windows 10 Disc Image (ISO File)"
```

#### Étape 2: Télécharger l'ISO

```
Cliquer sur: "Download Now"
    ↓
Choisir la version:
├─ Langue: English (ou votre langue)
├─ Edition: Windows 10 (21H2) ← Recommandé
└─ Architecture: 64-bit ← Recommandé

Cliquer: "Confirm"
    ↓
Télécharger commence (défi: 4-6 GB)
```

#### Étape 3: Attendre le Téléchargement

```
Fichier: Windows.iso (environ 5.9 GB)
Vitesse: Dépend de votre connexion
Temps: 30 min - 2 heures

Vérifier le téléchargement:
macOS:
ls -lh ~/Downloads/Windows*
```

---

### 📥 Option 2: Windows 11 ISO (Plus Récent - Gratuit)

#### Étape 1: Aller sur le Site Officiel

```
1. Ouvrir votre navigateur
2. Aller à: https://www.microsoft.com/en-us/software-download/windows11

3. Vous verrez: "Download Windows 11"
```

#### Étape 2: Choisir la Méthode

```
Options disponibles:

A. "Create Windows 11 Installation Media"
   └─ Télécharge l'outil Media Creation Tool

B. "Download Windows 11 Disc Image (ISO File)"
   └─ Directement l'ISO (plus rapide)

Recommandation: Choisir Option B (ISO directe)
```

#### Étape 3: Sélectionner Version & Architecture

```
1. Cliquer sur "Download Windows 11 Disc Image (ISO File)"

2. Choisir:
   ├─ Langue: English (ou autre)
   ├─ Edition: Windows 11 (23H2)
   └─ Architecture: 64-bit

3. Cliquer: "Download"
    ↓
Téléchargement commence (6-7 GB)
```

---

### 🛠️ Méthode Alternative: Media Creation Tool

#### Pour Windows 10:

```
Étape 1: Télécharger l'outil
└─ https://www.microsoft.com/en-us/software-download/windows10

Chercher: "Create Windows 10 Installation Media"
└─ Cliquer "Download tool now"

Étape 2: Lancer l'outil
└─ Double-cliquer: MediaCreationTool.exe
└─ Cliquer: "Accept"

Étape 3: Créer Installation Media
└─ Choisir: "Create installation media"
└─ Sélectionner:
   ├─ Language: English
   ├─ Edition: Windows 10
   └─ Architecture: 64-bit

Étape 4: Sauvegarder l'ISO
└─ Choisir: "ISO file"
└─ Sauvegarder dans ~/Downloads/
```

#### Pour Windows 11:

```
Étape 1: Aller à
└─ https://www.microsoft.com/en-us/software-download/windows11

Étape 2: Cliquer "Download tool now"
└─ MediaCreationTool_w11.exe

Étape 3: Suivre le même processus que Windows 10
└─ (identique interface)
```

---

## 🎯 Liens Directs Officiels

| Système | Lien Officiel | Taille | Type |
|---------|--------------|--------|------|
| **Windows 10** | https://www.microsoft.com/en-us/software-download/windows10 | 5.9 GB | Gratuit ✅ |
| **Windows 11** | https://www.microsoft.com/en-us/software-download/windows11 | 6.7 GB | Gratuit ✅ |
| **Windows Server** | https://www.microsoft.com/en-us/evalcenter/download-windows-server-2022 | 12 GB | Gratuit 90j ✅ |

---

## 📊 Comparaison Windows 10 vs 11

### Windows 10 (21H2)

**Avantages**:
```
✅ Plus stable (sortie 2015, bien testé)
✅ Moins de ressources nécessaires
✅ Compatible avec plus de vieux PC
✅ Téléchargement plus rapide (5.9 GB)
✅ Gratuit indéfiniment
```

**Inconvénients**:
```
⚠️ Plus ancien (support fin 2025)
⚠️ Mises à jour moins fréquentes
```

**Recommandation pour test VM**: ✅ **Windows 10**

---

### Windows 11 (23H2)

**Avantages**:
```
✅ Plus récent (sortie 2021)
✅ Interface modernisée
✅ Meilleures performances
✅ Sécurité améliorée (TPM 2.0)
✅ Support jusqu'à 2026
```

**Inconvénients**:
```
⚠️ Nécessite plus de ressources
⚠️ Telecharger plus volumineux (6.7 GB)
⚠️ Compatible surtout processeurs récents
```

**Recommandation pour test VM**: ✅ **Windows 11** (si VM performante)

---

## ⚙️ Configuration Recommandée pour VM

### Pour Windows 10

```
Minimum:
├─ RAM: 2 GB (3 GB recommandé)
├─ Disque: 30 GB
├─ CPU: 1 core (2+ recommandé)
└─ Vram: 64 MB

Recommandé (pour votre test):
├─ RAM: 4 GB
├─ Disque: 50 GB (dynamique)
├─ CPU: 2-4 cores
└─ Vram: 128-256 MB
```

### Pour Windows 11

```
Minimum:
├─ RAM: 4 GB
├─ Disque: 64 GB
├─ CPU: 2 cores (1 GHz+)
└─ UEFI + Secure Boot

Recommandé (pour votre test):
├─ RAM: 6-8 GB
├─ Disque: 80 GB (dynamique)
├─ CPU: 4 cores
└─ Vram: 256 MB
```

---

## 📲 Commander le Téléchargement sur macOS

### Utiliser Terminal (Plus Rapide)

```bash
# Vérifier si vous avez wget ou curl
which wget
which curl

# Option 1: Utiliser curl (directement depuis macOS)
cd ~/Downloads
curl -L "https://www.microsoft.com/en-us/software-download/windows10" -o Windows10.iso

# MAIS: Microsoft bloquerait probablement...
# Meilleur: Utiliser navigateur directement (plus fiable)
```

### Utiliser le Navigateur (Recommandé)

```bash
# 1. Ouvrir Safari ou Chrome
# 2. Aller à: https://www.microsoft.com/en-us/software-download/windows10
# 3. Cliquer "Download Now"
# 4. Le fichier télécharge dans ~/Downloads/

# Vérifier le téléchargement:
ls -lh ~/Downloads/Windows*

# Sortie attendue:
# -rw-r--r-- 1 user staff 5.9G Nov 1 10:30 Windows10.iso
```

---

## ✅ Vérifier l'Intégrité du Téléchargement

### Obtenir le Hash SHA-256 (Microsoft)

Microsoft publie les hashes officiels. Vous pouvez les vérifier:

```bash
# Après téléchargement:
cd ~/Downloads

# Calculer le SHA-256 de votre ISO
shasum -a 256 Windows10.iso

# Sortie attendue:
# abc123def456... Windows10.iso

# Comparer avec la liste officielle Microsoft:
# https://www.microsoft.com/en-us/software-download/windows10
```

### Option: Vérifier la Taille

```bash
# Vérifier que la taille est proche de 5.9 GB
ls -lh Windows10.iso

# Résultat attendu:
# -rw-r--r-- 1 user staff 5.9G Nov 1 10:30 Windows10.iso

# Si taille < 5 GB: Le téléchargement s'est arrêté!
# → Relancer le téléchargement
```

---

## 🔧 Créer une Clé USB Bootable (Optionnel)

Si vous voulez installer Windows depuis une clé USB:

### Sur macOS avec l'ISO

```bash
# 1. Insérer une clé USB (minimum 8 GB)

# 2. Identifier la clé USB
diskutil list

# Vous verrez quelque chose comme:
# /dev/disk0 (internal, physical)
# /dev/disk1 (external, physical) ← VOTRE CLÉ

# 3. Convertir ISO en IMG (si nécessaire)
cd ~/Downloads
hdiutil convert Windows10.iso -format UDRW -o Windows10.img

# 4. Unmount la clé
diskutil unmountDisk /dev/disk1

# 5. Écrire l'ISO sur la clé (ATTENTION: Remplacer /dev/disk1!)
sudo dd if=Windows10.img.dmg of=/dev/rdisk1 bs=4m

# 6. Éjecter la clé
diskutil ejectDisk /dev/disk1

# 7. La clé est prête!
```

**Attention**: La commande `dd` est dangereuse. Assurez-vous que `/dev/disk1` est bien votre clé!

---

## 🎯 Résumé Rapide

### Les 3 Étapes Simples

```
1️⃣ Aller sur le site Microsoft
   https://www.microsoft.com/en-us/software-download/windows10

2️⃣ Cliquer "Download Now"
   (ou "Download Windows 11 Disc Image")

3️⃣ Sauvegarder l'ISO
   File: Windows10.iso (5.9 GB)
   Dossier: ~/Downloads/
```

### Temps Estimé

```
Téléchargement: 30 minutes - 2 heures
Vérification intégrité: 5 minutes
Installation VM: 15-30 minutes

Total: 1-3 heures
```

---

## 🔒 Sécurité: Vérifier l'Authenticité

### Certificat SSL/TLS

```
Avant de télécharger, vérifier:

1. URL commence par: https:// (cadenas 🔒)
2. Domaine: microsoft.com (pas microsft.com!)
3. Certificat valide (navigateur dit ✅)
```

### Source Officielle

```
Domaines OFFICIELS Microsoft:
✅ microsoft.com
✅ microsoft.en-us.com (régional)
✅ download.microsoft.com

Domaines SUSPECTS:
❌ microsft.com (typo!)
❌ microsoft-download.com (faux!)
❌ windows-iso.com (très faux!)
```

---

## ⚠️ Pièges à Éviter

### ❌ Ne PAS Télécharger Depuis:

```
❌ Sites torrent (sauf si vous savez ce que vous faites)
❌ Sites tiers inconnus
❌ "Windows ISO for Free" sur Google
❌ Liens Mediafire/Mega/Dropbox bizarres
❌ Sites en .ru, .tk, .xyz suspects

RAISON: Risque de malware/virus bundlé!
```

### ✅ Télécharger UNIQUEMENT Depuis:

```
✅ https://www.microsoft.com (OFFICIEL)
✅ microsoft.com/download
✅ Navigateur de votre PC Windows existant
```

---

## 📋 Checklist Avant Installation VM

```
☐ ISO téléchargée (5.9 GB minimum)
☐ VirtualBox installé sur votre Mac
☐ VM créée avec 4 GB RAM, 50 GB disque
☐ Fichier ISO assigné au lecteur CD de la VM
☐ Configuration réseau: NAT
☐ GPU/Display: 128-256 MB VRAM

→ Prêt à lancer l'installation!
```

---

## 🆘 Problèmes Courants

### Problème: "Invalid ISO"

```
Cause: Téléchargement corrompu
Solution:
1. Supprimer le fichier
2. Retélécharger depuis Microsoft
3. Vérifier la taille (5.9 GB)
```

### Problème: "Page Not Found"

```
Cause: Lien expiré ou votre région bloquée
Solution:
1. Utiliser un VPN (ExpressVPN, ProtonVPN)
2. Essayer Windows 11 au lieu de Windows 10
3. Utiliser Media Creation Tool à la place
```

### Problème: Téléchargement S'Arrête

```
Cause: Connexion internet instable
Solution:
1. Utiliser un gestionnaire de téléchargement:
   - Aria2 (terminal)
   - DownThemAll (Firefox)
   - IDM (Internet Download Manager)

2. Ou relancer le téléchargement
```

---

## 📞 Support Officiel

Si vous avez des problèmes:

```
Contact Microsoft:
├─ https://support.microsoft.com/en-us/windows
├─ https://www.microsoft.com/en-us/software-download/windows10
└─ Chat support disponible

Forum Communautaire:
├─ Reddit: r/Windows
├─ Microsoft Community: answers.microsoft.com
└─ TechNet Forums
```

---

## 🎉 Conclusion

**Pour tester votre .exe sur VM:**

```
1. Télécharger Windows 10 ou 11 ISO (GRATUIT & OFFICIEL)
   → https://www.microsoft.com/en-us/software-download/windows10

2. Créer une VM dans VirtualBox

3. Installer Windows depuis l'ISO

4. Copier votre .exe à la VM

5. Tester et valider!

Temps total: 1-3 heures
Coût: 0€ (100% gratuit!)
```

---

**Date**: 1 novembre 2025  
**Version**: 1.0  
**Source**: Liens officiels Microsoft  
**Statut**: ✅ À jour et vérifié
