# ⚡ QUICK START: Commandes Essentielles

## 🚀 5 Étapes pour Commencer Immédiatement

### ✅ Étape 1: Initialiser Git (5 min)

```bash
cd /Users/kalilbelgoumri/Desktop/pupy-c2-manager-macos

git init
git add .
git commit -m "Initial commit: Pupy C2 Manager with Hybrid Workflow"
```

### ✅ Étape 2: Créer Repository GitHub (2 min)

1. Aller sur **https://github.com/new**
2. **Repository name**: `pupy-c2-manager-macos`
3. **Description**: Pupy C2 Manager with GitHub Actions
4. **Public** ✓
5. Cliquer **Create repository**

### ✅ Étape 3: Connecter à GitHub (2 min)

```bash
# Remplacer YOUR_USERNAME par votre username GitHub
git remote add origin https://github.com/YOUR_USERNAME/pupy-c2-manager-macos.git

git branch -M main

git push -u origin main
```

### ✅ Étape 4: Lancer l'Application (1 min)

```bash
python3 src/main.py
```

### ✅ Étape 5: Créer Premier Payload (2 min)

**Dans l'Application GUI:**
```
1. Cliquer "Browse" → Sélectionner payload.py
2. Listener IP: 192.168.1.100
3. Listener Port: 4444
4. Level: Level 2 - Medium ⭐
5. Cliquer "🚀 Bundle & Compile"
6. Attendre ~60s
```

---

## 🔄 Cycle Quotidien (Après Setup)

### À chaque fois que vous voulez compiler pour Windows:

```bash
# 1. Dans l'app GUI
# Cliquer "📤 Export pour GitHub Actions"

# 2. Dans Terminal
cd /Users/kalilbelgoumri/Desktop/pupy-c2-manager-macos

# 3. Push à GitHub
git add payload.py
git commit -m "New payload - Level 2"
git push

# 4. Attendre 2-3 minutes
# GitHub Actions compile automatiquement!

# 5. Télécharger le binaire
# Aller sur github.com → Actions → payload-windows-pe

# 6. Tester sur Windows VM
# ✅ C'est tout!
```

---

## 📊 Vérification Rapide

### Vérifier que tout est configuré:

```bash
# Vérifier Git
git status

# Vérifier remote GitHub
git remote -v

# Vérifier workflow GitHub Actions
ls -la .github/workflows/

# Vérifier .gitignore
cat .gitignore | head -10

# Vérifier l'app
python3 src/main.py --version
```

---

## 🎯 Raccourcis Essentiels

### Créer payload rapidement:

```bash
# Dans l'app:
Bouton "🚀 Bundle & Compile"
```

### Exporter pour Windows:

```bash
# Dans l'app:
Bouton "📤 Export pour GitHub Actions"
```

### Compiler sur GitHub:

```bash
git add payload.py && git commit -m "Payload" && git push
```

### Vérifier status GitHub:

```bash
# Aller sur:
github.com/YOUR_USERNAME/pupy-c2-manager-macos/actions
```

### Télécharger binaire Windows:

```
GitHub → Actions → Dernier workflow
↓
Cliquer "Run build-windows"
↓
Scroller en bas
↓
Cliquer "payload-windows-pe"
↓
Télécharger payload.exe
```

---

## 🔐 Niveaux d'Obfuscation

### Choisir le bon niveau:

| Niveau | Vitesse | Sécurité | Délai | Cas d'Usage |
|--------|---------|----------|-------|------------|
| **Level 1** | ⚡⚡⚡ | ⭐ | 0s | Dev/Test |
| **Level 2** | ⚡⚡ | ⭐⭐ | 1-3s | **RECOMMANDÉ** |
| **Level 3** | ⚡ | ⭐⭐⭐ | 5-15s | Production |
| **Level 4** | 🐢 | ⭐⭐⭐⭐ | 30-60s | Haute menace |
| **Level 5** | 🐢🐢 | ⭐⭐⭐⭐⭐ | 60-300s | Maximum |

**👉 Recommandation:** Commencer avec Level 2, augmenter si nécessaire.

---

## ⚠️ Problèmes Courants

### "GitHub Actions ne démarre pas"

```bash
# Solution:
git push
# Vérifier sur github.com/...../actions après 30s
```

### "Pas de payload.py"

```bash
# Solution:
# Cliquer "📤 Export pour GitHub Actions" dans l'app
```

### "Build échoue sur GitHub"

```bash
# Vérifier la syntaxe:
python3 -m py_compile payload.py

# Si erreur, corriger et re-push
git add payload.py
git commit -m "Fix payload"
git push
```

### "Cannot find artifact"

```bash
# Attendre 3-5 minutes après push
# GitHub Actions compile en arrière-plan
# Vérifier status sur github.com → Actions
```

---

## 📋 Checklist Avant de Démarrer

- [ ] Git initialisé (`git init` fait)
- [ ] Repository créé sur GitHub
- [ ] Remote ajouté (`git remote add origin`)
- [ ] Workflow `.github/workflows/build-windows-pe.yml` créé
- [ ] `.gitignore` créé
- [ ] `bundler_tab.py` mis à jour avec bouton Export
- [ ] Première push faite (`git push -u origin main`)
- [ ] Application GUI testée (`python3 src/main.py`)

---

## 🎊 Résumé

```
✅ Setup: 15 minutes (1 fois)
✅ Utilisation: 2-3 minutes par payload
✅ Résultat: Vrai binaire Windows PE x64
✅ Automatisation: 100%
```

### Prochaine étape:

```bash
# Faire les 5 étapes ci-dessus!
```

---

**Date**: 1 novembre 2025  
**Temps de Setup**: 15 minutes  
**Status**: ✅ PRÊT  
🚀 **GO!**
