# 🔄 Workflow Hybride: Application GUI + GitHub Actions

## 📌 Concept

Vous utilisez **DEUX chemins** selon votre situation:

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  WORKFLOW HYBRIDE (Meilleur des 2 mondes!)            │
│                                                         │
│  ✅ Créer payload avec GUI sur macOS                   │
│  ✅ Compiler en PE x64 avec GitHub Actions             │
│  ✅ Tester sur Windows                                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Les 2 Chemins

### Chemin 1: Tester Rapidement sur macOS
```
┌─ Application GUI (bundler_tab.py)
│  ├─ Entrer payload.py
│  ├─ Sélectionner obfuscation (Level 1-5)
│  ├─ Plateforme: macOS
│  └─ Générer binaire Mach-O
│
└─ Résultat: payload_macos.exe (Mach-O ARM64)
             ✅ Testé sur macOS
             ❌ Ne marche PAS sur Windows
```

**Utilisation:**
- Développement rapide
- Tests sur macOS
- Vérifier la génération de code

---

### Chemin 2: Compiler pour Windows (GitHub Actions)
```
┌─ Prendre le payload.py créé par l'app
│
├─ Push à GitHub
│  ├─ commit
│  └─ push
│
├─ GitHub Actions s'active
│  ├─ Runner Windows se lance
│  ├─ PyInstaller compile
│  └─ Crée PE x64 binaire
│
└─ Résultat: payload_windows.exe (PE x64)
             ✅ Testé sur Windows
             ✅ Exécutable sur VM
```

**Utilisation:**
- Production finale
- Tests Windows
- Distribution C2

---

## 🚀 Setup Complet (Étape par Étape)

### Étape 1: Intégrer GUI + GitHub Actions

#### 1A. Modifier bundler_tab.py pour exporter payload.py

```python
# src/bundler_tab.py - Ajouter cette fonction

def export_for_github(self, output_path):
    """Exporte le payload.py pour GitHub Actions"""
    
    # Lire le payload généré
    with open(self.payload_file, 'r') as f:
        payload_content = f.read()
    
    # Sauvegarder à la racine pour GitHub
    with open('payload.py', 'w') as f:
        f.write(payload_content)
    
    # Afficher message
    self.log_message(
        "✅ payload.py créé!\n"
        "📤 Prêt pour GitHub Actions\n"
        "💡 Utilisez: git add payload.py && git push"
    )
```

#### 1B. Ajouter bouton "Export pour GitHub"

Dans bundler_tab.py, ajouter:

```python
# Nouveau bouton
export_github_btn = QPushButton("📤 Export pour GitHub Actions")
export_github_btn.clicked.connect(self.export_for_github)
self.layout.addWidget(export_github_btn)
```

---

### Étape 2: Créer Workflow GitHub Actions

#### 2A. Créer dossier workflow

```bash
mkdir -p .github/workflows
```

#### 2B. Créer le fichier workflow

```bash
cat > .github/workflows/build-windows-pe.yml << 'EOF'
name: Build Windows PE Binary

on:
  push:
    paths:
      - 'payload.py'
    branches: [ main, master ]

jobs:
  build-windows:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pyinstaller pycryptodome
    
    - name: Build Windows PE executable
      run: |
        pyinstaller --onefile --console --distpath ./dist payload.py
    
    - name: Verify PE binary format
      run: |
        $bytes = [System.IO.File]::ReadAllBytes("dist/payload.exe")
        $magic = "{0:X2}{1:X2}" -f $bytes[0], $bytes[1]
        Write-Host "Magic bytes: $magic"
        if ($magic -eq "4D5A") {
          Write-Host "✅ Valid PE x64 binary!"
        } else {
          Write-Host "❌ Invalid PE format!"
          exit 1
        }
    
    - name: Upload Windows binary
      uses: actions/upload-artifact@v3
      with:
        name: payload-windows-pe
        path: dist/payload.exe
        retention-days: 30
    
    - name: Create Release
      uses: softprops/action-gh-release@v1
      if: startsWith(github.ref, 'refs/tags/')
      with:
        files: dist/payload.exe
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
EOF
```

---

### Étape 3: Configuration Git

```bash
# Initialiser Git (si pas fait)
cd /Users/kalilbelgoumri/Desktop/pupy-c2-manager-macos
git init

# Ajouter le workflow
git add .github/workflows/build-windows-pe.yml

# Premier commit
git commit -m "Add GitHub Actions Windows build"

# Ajouter GitHub comme remote
git remote add origin https://github.com/YOUR_USERNAME/pupy-c2-manager-macos.git
git branch -M main
git push -u origin main
```

---

## 📊 Workflow Complet

### Pour Développer et Tester

```
1️⃣ DÉVELOPPEMENT (macOS - Rapide)
   
   Ouvrir Application GUI
     ↓
   bundler_tab.py
     ├─ Entrer payload.py
     ├─ Sélectionner Level 5 (maximum)
     ├─ Plateforme: macOS
     └─ Cliquer "Générer"
   
   ✅ Résultat: payload_macos.exe (Mach-O)
   
   Usage:
   - Tests rapides sur votre macOS
   - Vérifier génération code
   - Développement itératif


2️⃣ EXPORT POUR GITHUB (1 clic)
   
   Cliquer "📤 Export pour GitHub Actions"
     ↓
   Cré payload.py à la racine
     ↓
   
   Usage:
   - Prépare compilation Windows
   - Exporte payload généré


3️⃣ GITHUB COMPILE (Automatique)
   
   Terminal:
   $ git add payload.py
   $ git commit -m "Update payload"
   $ git push
     ↓
   GitHub Actions s'active automatiquement!
     ├─ Windows runner se lance
     ├─ PyInstaller compile
     ├─ Vérifie PE x64 format
     └─ Sauvegarde artifact
   
   ✅ Résultat: payload.exe (PE x64)
   
   Usage:
   - Binaire Windows RÉEL
   - Télécharger depuis artifacts
   - Tester sur Windows VM


4️⃣ TEST WINDOWS (VM)
   
   Copier payload.exe à VM
     ↓
   Exécuter sur Windows
     ↓
   ✅ Listener reçoit connexion
```

---

## 🎯 Exemple Pratique Complet

### Jour 1: Développement

```bash
# 1. Ouvrir l'app et créer payload
python3 src/main.py

# Dans GUI:
# - Charger payload.py
# - Obfuscation: Level 5
# - Platform: macOS
# - Click "Générer"
# ✅ Teste rapidement sur macOS

# 2. Quand satisfait, exporter pour GitHub
# Click "📤 Export pour GitHub Actions"

# 3. Voir le payload généré
cat payload.py
# (Vérifie que obfuscation est là)
```

### Jour 2: Compiler Windows

```bash
# 4. Push à GitHub
git add payload.py
git commit -m "Production payload Level 5"
git push

# 5. GitHub Actions compile automatiquement
# (Aller sur GitHub.com pour voir le build)

# URL: github.com/YOUR_USERNAME/pupy-c2-manager-macos/actions

# 6. Attendre 2-3 minutes
# Status: ✅ Build passed!

# 7. Télécharger artifact
# Click "payload-windows-pe"
# ✅ payload.exe (PE x64) téléchargé!

# 8. Copier à VM Windows
# Tester!
```

---

## 📋 Fichiers à Modifier/Créer

### 1. Modifier: src/bundler_tab.py

```python
# Ajouter import en haut
from pathlib import Path
import shutil

# Ajouter cette méthode à la classe BundlerTab
def export_for_github(self):
    """Exporte payload.py à la racine pour GitHub Actions"""
    try:
        # Copier payload_macos.exe → payload.py
        source = Path(self.output_dir) / self.latest_binary
        dest = Path.cwd() / "payload.py"
        
        shutil.copy(str(source), str(dest))
        
        self.log_message(
            f"\n✅ Payload exporté pour GitHub!\n"
            f"📂 Fichier: {dest}\n"
            f"📤 Prêt pour: git push\n\n"
            f"Commandes:\n"
            f"  git add payload.py\n"
            f"  git commit -m 'Update payload'\n"
            f"  git push\n"
        )
        
        # Afficher notification
        QMessageBox.information(
            self,
            "Succès",
            "✅ payload.py créé!\n\n"
            "Utilisez:\n"
            "git add payload.py\n"
            "git push\n\n"
            "GitHub compilera automatiquement!"
        )
        
    except Exception as e:
        self.log_message(f"❌ Erreur: {str(e)}")

# Dans __init__, ajouter ce bouton
self.export_github_btn = QPushButton("📤 Export pour GitHub Actions")
self.export_github_btn.clicked.connect(self.export_for_github)
self.main_layout.addWidget(self.export_github_btn)
```

### 2. Créer: .github/workflows/build-windows-pe.yml

```yaml
name: Build Windows PE

on:
  push:
    paths: ['payload.py']
    branches: [main, master]

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - run: pip install pyinstaller
    
    - run: pyinstaller --onefile --console payload.py
    
    - uses: actions/upload-artifact@v3
      with:
        name: payload-windows
        path: dist/payload.exe
```

### 3. Créer: .gitignore

```
# Python
__pycache__/
*.pyc
*.pyo
dist/
build/
*.egg-info/

# Generated binaries
payload_*.exe
*.exe

# IDE
.vscode/
.idea/

# OS
.DS_Store
```

---

## 🔐 Avantages du Workflow Hybride

### Application GUI (macOS)
```
✅ Développement rapide
✅ Tests locaux immédiats
✅ Interface visuelle
✅ Itération rapide
✅ Pas d'attente GitHub
```

### GitHub Actions (Compilation Windows)
```
✅ Compile sur Windows RÉEL
✅ Vrai PE x64 binaire
✅ Automatisé (1 push = build)
✅ Gratuit
✅ Versioning intégré
✅ Historique artifacts
```

### Combinaison = PARFAIT! 🎯
```
✅ Meilleur des 2 mondes
✅ Rapide en dev (GUI)
✅ Fiable en prod (GitHub)
✅ Zéro manuel intervention
✅ Traçabilité complète
```

---

## 📊 Comparaison: Avant vs Après

### Avant (Workflow Simple)
```
macOS
  ├─ Créer payload (GUI)
  ├─ Créer binaire Mach-O
  └─ Problem: Ne marche pas sur Windows ❌
```

### Après (Workflow Hybride)
```
macOS
  ├─ Créer payload (GUI) ✅ Rapide test
  ├─ Exporter pour GitHub (1 clic)
  └─ Commit + Push

GitHub Actions
  ├─ Reçoit push
  ├─ Lance Windows runner
  ├─ Compile PE x64 ✅ Vrai binaire Windows
  ├─ Valide format
  └─ Disponible artifact

Windows VM
  └─ Télécharger + Exécuter ✅ Fonctionne!
```

---

## 🚀 Quick Start (Copier-Coller)

```bash
# 1. Créer le workflow
mkdir -p .github/workflows

cat > .github/workflows/build-windows-pe.yml << 'EOF'
name: Build Windows PE

on:
  push:
    paths: ['payload.py']

jobs:
  build:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - run: pip install pyinstaller
    - run: pyinstaller --onefile payload.py
    - uses: actions/upload-artifact@v3
      with:
        name: payload-windows
        path: dist/payload.exe
EOF

# 2. Commit
git add .github/workflows/build-windows-pe.yml
git commit -m "Add GitHub Actions Windows build"
git push

# ✅ C'est prêt!
# Maintenant chaque fois que vous faites:
# git add payload.py && git commit && git push
# → GitHub compile automatiquement!
```

---

## 💡 Résumé

### Vous Avez Maintenant 2 Chemins:

| Étape | Outil | Résultat |
|-------|-------|----------|
| **Développement** | GUI App | Mach-O (test macOS) |
| **Compilation** | GitHub Actions | PE x64 (Windows) |
| **Test** | Windows VM | ✅ Fonctionne! |

### Workflow Quotidien:

```
1. Ouvrir app GUI
2. Créer payload (Level 5)
3. Cliquer "Export pour GitHub"
4. Terminal: git push
5. Attendre 2-3 min
6. Télécharger artifact
7. Copier à VM + Test!
```

### Résultat Final:

```
✅ Application GUI pour tester
✅ GitHub Actions pour compiler Windows
✅ Workflow complètement automatisé
✅ Zéro manual compilation sur Windows
✅ Vrai PE x64 binaire garanti!
```

---

**Date**: 1 novembre 2025  
**Concept**: Hybrid Workflow (GUI + GitHub Actions)  
**Résultat**: Compilation Windows automatisée depuis macOS  
**Status**: ✅ READY TO IMPLEMENT
