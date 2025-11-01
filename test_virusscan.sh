#!/bin/bash

# VirusTotal Local Testing Script
# Teste votre binaire avec ClamAV sans envoyer sur VirusTotal

echo "╔════════════════════════════════════════════════════════╗"
echo "║     VIRUS SCANNING - LOCAL ClamAV TESTING              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

EXE="/Users/kalilbelgoumri/Pupy_Outputs/dist/ChromeSetup_20251101_183240.exe"

# Vérifier si le fichier existe
if [ ! -f "$EXE" ]; then
    echo "[!] Fichier non trouvé: $EXE"
    exit 1
fi

echo "[1] CHECKING FILE"
echo "---"
echo "File: $EXE"
echo "Size: $(ls -lh "$EXE" | awk '{print $5}')"
echo "Type: $(file "$EXE" | cut -d: -f2-)"
echo ""

echo "[2] CHECKING ClamAV"
echo "---"
if command -v clamscan &> /dev/null; then
    echo "✅ ClamAV est installé"
    echo ""
    
    echo "[3] UPDATING VIRUS DEFINITIONS"
    echo "---"
    echo "Ceci peut prendre quelques minutes..."
    freshclam 2>&1 | tail -5
    echo ""
    
    echo "[4] SCANNING WITH ClamAV"
    echo "---"
    clamscan -r --scan-pe=yes --scan-mail=no "$EXE" 2>&1
    SCAN_RESULT=$?
    
    echo ""
    echo "[5] SCAN RESULTS"
    echo "---"
    if [ $SCAN_RESULT -eq 0 ]; then
        echo "✅ CLEAN - Aucun virus détecté par ClamAV"
    elif [ $SCAN_RESULT -eq 1 ]; then
        echo "⚠️  INFECTED - ClamAV a détecté quelque chose"
        echo "    (Vérifiez le résultat ci-dessus)"
    else
        echo "❓ Error running ClamAV (code: $SCAN_RESULT)"
    fi
    
else
    echo "❌ ClamAV n'est pas installé"
    echo ""
    echo "Installation:"
    echo "  brew install clamav"
    echo ""
    echo "Après installation, relancez ce script"
    echo ""
    echo "Ou testez directement sur VirusTotal:"
    echo "  https://www.virustotal.com"
fi

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║              SCAN COMPLETED                            ║"
echo "╚════════════════════════════════════════════════════════╝"
