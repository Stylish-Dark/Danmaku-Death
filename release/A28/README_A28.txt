Danmaku Death 19.4 S25 — A28 SAV IMPORT FIX

Base: physically-tested A27 manual data control build.

Single functional change:
- Backup filename changed from Danmaku_Death_Data.tar to Danmaku_Death_Data.sav.
- Import picker behavior/code is otherwise unchanged. Because it already accepts generic application/octet-stream data, the .sav extension is selectable while .tar was classified by Android as application/x-tar and filtered out.

No other app behavior was intentionally changed.

Static verification completed:
- classes2.dex contains Danmaku_Death_Data.sav and no Danmaku_Death_Data.tar.
- DEX SHA-1 header signature valid.
- DEX Adler-32 checksum valid.
- All non-signature APK payload entries other than classes2.dex are byte-identical to A27.
- JAR/v1 signature verifies.
- APK Signature Scheme v2 content digest verifies.
- APK Signature Scheme v2 RSA signature verifies.
- resources.arsc is stored and 4-byte aligned.
- ZIP local-header offsets validate.
- ZIP integrity passes.

Runtime status:
- A27 manual export/import was physically confirmed by user, except .tar selection bug.
- A28 .sav behavior requires physical device confirmation.
