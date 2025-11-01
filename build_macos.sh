#!/bin/bash
# Build macOS .app Bundle for Pupy C2 Manager
# Tahoe compatible

echo "🚀 Building Pupy C2 Manager for macOS..."

# Install dependencies
echo "[*] Installing dependencies..."
pip3 install -r requirements.txt

# Create app bundle using py2app
echo "[*] Creating app bundle..."
python3 setup.py py2app -A

# Create DMG
echo "[*] Creating DMG installer..."
mkdir -p dist_dmg
cp -r dist/Pupy\ C2\ Manager.app dist_dmg/

# Create DMG
hdiutil create -volname "Pupy C2 Manager" \
    -srcfolder dist_dmg \
    -ov -format UDZO \
    dist/Pupy-C2-Manager-1.0.0.dmg

# Cleanup
rm -rf dist_dmg

echo "[+] Build complete!"
echo "[+] App bundle: dist/Pupy C2 Manager.app"
echo "[+] DMG installer: dist/Pupy-C2-Manager-1.0.0.dmg"
echo ""
echo "To run:"
echo "  open 'dist/Pupy C2 Manager.app'"
echo ""
echo "To install from DMG:"
echo "  open 'dist/Pupy-C2-Manager-1.0.0.dmg'"
echo "  Drag Pupy C2 Manager.app to Applications"
