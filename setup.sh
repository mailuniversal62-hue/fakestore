#!/bin/bash
set -e
echo "[*] Installing Python deps..."
pip3 install -r requirements.txt

echo "[*] Creating directories..."
mkdir -p apk logs static templates

echo "[*] Checking for Android build tools..."
which apktool || echo "  [!] apktool not found - install with: sudo apt install apktool"
which zipalign || echo "  [!] zipalign not found - install with: sudo apt install zipalign"

echo "[+] Setup done."
