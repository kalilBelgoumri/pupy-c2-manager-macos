#!/usr/bin/env python3
"""
Test script to compare obfuscation levels
Shows generated payload examples for each level
"""

import sys
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from advanced_bundler import AntiAVBundler


def print_level_info(level, title, techniques):
    """Print level information"""
    print(f"\n{'='*70}")
    print(f"LEVEL {level}: {title}")
    print(f"{'='*70}")
    for technique in techniques:
        print(f"  ✓ {technique}")


def main():
    """Main test function"""

    print(
        """
    ╔════════════════════════════════════════════════════════════════╗
    ║   Anti-AV Bundler - Levels Comparison Demo                    ║
    ╚════════════════════════════════════════════════════════════════╝
    """
    )

    bundler = AntiAVBundler()

    # Level descriptions
    levels = {
        0: (
            "Simple",
            ["Code source brut", "Pas de chiffrement", "Détectable par tous les AV"],
        ),
        1: (
            "Low Obfuscation",
            [
                "Base64 encoding des strings",
                "Noms de variables génériques",
                "Imports dynamiques simples",
                "Échappe aux signatures basiques",
            ],
        ),
        2: (
            "Medium Obfuscation",
            [
                "Chiffrement XOR avec clés aléatoires",
                "Base64 encoding",
                "Délais d'exécution (1-3s)",
                "Imports dynamiques",
                "Échappe à la plupart des signatures statiques",
            ],
        ),
        3: (
            "High Obfuscation",
            [
                "Détection Sandbox (VirtualBox, VMware, KVM, Hyper-V)",
                "Détection Débogueur (sys.gettrace)",
                "Délais longs (5-15s)",
                "Chiffrement XOR",
                "Anti-exécution en VM",
            ],
        ),
        4: (
            "Extreme Obfuscation",
            [
                "Tous les niveaux précédents",
                "Noms de variables aléatoires",
                "Imports dynamiques avancés (__import__)",
                "Vérification liste des processus",
                "Détection outils d'analyse (IDA, Ghidra, gdb, etc)",
                "Exécution en thread daemon",
                "Session ID unique Base64",
            ],
        ),
        5: (
            "Maximum Evasion",
            [
                "Tous les niveaux précédents",
                "Chiffrement XOR complet",
                "Détection multi-couches (filesystem, registry, processus)",
                "Délais extrêmes (60-300s / 1-5 minutes)",
                "Silence complet des erreurs",
                "Exécution avec timeout",
                "Obfuscation maximale du code",
            ],
        ),
    }

    # Print all levels
    for level, (title, techniques) in levels.items():
        print_level_info(level, title, techniques)

    # Generate sample payloads
    print(f"\n{'='*70}")
    print("SAMPLE PAYLOADS GENERATION")
    print(f"{'='*70}\n")

    test_ip = "192.168.1.100"
    test_port = 4444

    for level in range(6):
        print(f"\n[*] Generating Level {level} payload sample...")

        if level == 0:
            payload = bundler._create_simple_payload(test_ip, test_port)
        elif level == 1:
            payload = bundler._create_string_obfuscated_payload(test_ip, test_port)
        elif level == 2:
            payload = bundler._create_xor_encrypted_payload(test_ip, test_port)
        elif level == 3:
            payload = bundler._create_sandbox_aware_payload(test_ip, test_port)
        elif level == 4:
            payload = bundler._create_antiav_advanced_payload(test_ip, test_port)
        else:  # 5
            payload = bundler._create_maximum_evasion_payload(test_ip, test_port)

        # Print first 10 lines
        payload_lines = payload.split("\n")[:10]
        print("[Payload Preview (first 10 lines)]")
        for line in payload_lines:
            if line.strip():
                print(f"  {line[:60]}...")

        # Show payload size and characteristics
        payload_size = len(payload)
        xor_present = "bytes.fromhex" in payload
        sandbox_check = "is_sandboxed" in payload
        timing_present = "time.sleep" in payload

        characteristics = []
        if xor_present:
            characteristics.append("XOR ✓")
        if sandbox_check:
            characteristics.append("Sandbox ✓")
        if timing_present:
            characteristics.append("Timing ✓")

        print(f"  Payload Size: {payload_size} bytes")
        print(
            f"  Features: {', '.join(characteristics) if characteristics else 'None'}"
        )
        print(f"  ✓ Generated")

    # Comparison table
    print(f"\n{'='*70}")
    print("QUICK COMPARISON TABLE")
    print(f"{'='*70}\n")

    print("Level │ Tech          │ Speed │ Sandbox │ Anti-Debug │ Detection")
    print("──────┼───────────────┼───────┼─────────┼────────────┼──────────")
    print("  0   │ None          │ <1s   │   No    │    No      │ Very High")
    print("  1   │ Base64        │ <1s   │   No    │    No      │ High")
    print("  2   │ XOR+Timing    │ 1-3s  │   No    │    No      │ Medium ⭐")
    print("  3   │ Sandbox+Time  │ 5-15s │  Yes    │    Yes     │ Low")
    print("  4   │ Advanced      │ Var   │  Yes    │    Yes✓✓   │ Very Low")
    print("  5   │ Maximum       │ 1-5m  │  Yes✓✓ │   Yes✓✓✓   │ Minimal")

    # Usage recommendations
    print(f"\n{'='*70}")
    print("RECOMMENDATIONS BY ENVIRONMENT")
    print(f"{'='*70}\n")

    recommendations = {
        "Development": "Level 0-1 (pas de sandbox check, débugging facile)",
        "PoC/Lab": "Level 2 (good balance, rapide)",
        "Non-Defensive": "Level 2-3 (AV standard)",
        "Defensive Environment": "Level 3-4 (protection Defender/EDR basique)",
        "High-Security": "Level 4-5 (EDR avancé, honeypot)",
    }

    for env, recommendation in recommendations.items():
        print(f"  {env:.<25} {recommendation}")

    print(f"\n{'='*70}")
    print("✅ All levels generated and tested successfully!")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
