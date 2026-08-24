# Future reverse-engineering map

The repository is intentionally prepared for progressively deeper reconstruction.

Recommended next layers:

1. Disassemble `classes.dex` and `classes2.dex` to smali and commit the smali tree.
2. Generate Java-like decompiler output for navigation only; treat smali/DEX as authoritative.
3. Map resource IDs in `resources.arsc` back to symbolic names.
4. Build a stage-system map: stage IDs, stage-selection entries, enemy/boss classes, backgrounds, music and completion records.
5. Determine which stage logic is DEX-side versus `libdanmakudeath.so` native-side.
6. Add deterministic rebuild scripts and compare rebuilt APK payloads against known-good checkpoints.

For adding new levels, step 4 is the critical investigation. Once the stage registry/loading path is mapped, future level work becomes incremental rather than rediscovered from scratch.
