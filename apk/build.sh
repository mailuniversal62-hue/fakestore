#!/bin/bash
# Build dropper APK from source.
# Requires: Android Studio or cmdline-tools + JDK 17

set -e
cd "$(dirname "$0")/dropper"

echo "[*] Building dropper APK..."
./gradlew assembleRelease

echo "[*] Copying to static/"
cp app/build/outputs/apk/release/app-release.apk ../../static/app.apk

echo "[+] Done. APK at static/app.apk"
