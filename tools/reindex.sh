#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/tools/dex_index.py" "$ROOT/source/apk_raw/classes.dex" "$ROOT/index/classes.dex"
python3 "$ROOT/tools/dex_index.py" "$ROOT/source/apk_raw/classes2.dex" "$ROOT/index/classes2.dex"
python3 "$ROOT/tools/axml_dump.py" "$ROOT/source/apk_raw/AndroidManifest.xml" "$ROOT/decoded/AndroidManifest.xml"
find "$ROOT/source/apk_raw/res" -type f -name '*.xml' -print0 | while IFS= read -r -d '' f; do
    rel="${f#"$ROOT/source/apk_raw/res/"}"
    python3 "$ROOT/tools/axml_dump.py" "$f" "$ROOT/decoded/res/$rel"
done
