# Danmaku Death 19.4 — S25 reverse-engineering workspace

This repository is an archival and editing workspace built from the **A28 S25 baseline APK**.

It deliberately keeps two separate views of the game:

- `release/A28/` — the untouched reference APK supplied as the current canonical build.
- `source/apk_raw/` — the APK payload extracted byte-for-byte for inspection and future patching.
- `decoded/` — human-readable AndroidManifest and binary-XML resources decoded from the APK.
- `index/` — generated DEX/resource inventories to make code archaeology repeatable.
- `tools/` — small local analysis tools used to generate the decoded/indexed views.
- `docs/` — baseline, architecture and test notes.

## Important

This is **not the original Java/Android Studio source project**. The original source is not present in the APK. The DEX files and native libraries are compiled artifacts and will require smali/decompilation or native reverse engineering for deeper edits.

The purpose of this repository is to stop reverse-engineering knowledge from being lost between APK revisions and to give future changes a stable, version-controlled base.

## Canonical baseline

`release/A28/Danmaku_Death_19.4_S25_A28_SAV_IMPORT_FIX.apk`

SHA-256: `4d4e7dcf91c5dbde1818edb66b3a22711bb8338578cb15d905c23b6496f5d050`

## Safety rule for future changes

Never overwrite the canonical release artifact. Make code/resource changes in a branch or new revision, build a new APK, test it physically, then tag the physically confirmed checkpoint.
