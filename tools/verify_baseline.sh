#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APK="$ROOT/release/A28/Danmaku_Death_19.4_S25_A28_SAV_IMPORT_FIX.apk"
EXPECTED="4d4e7dcf91c5dbde1818edb66b3a22711bb8338578cb15d905c23b6496f5d050"
ACTUAL="$(sha256sum "$APK" | awk '{print $1}')"
[ "$ACTUAL" = "$EXPECTED" ] || { echo "FAIL: baseline APK hash mismatch"; exit 1; }
echo "OK: canonical A28 APK hash matches"
