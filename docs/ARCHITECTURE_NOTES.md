# Architecture notes

## Bytecode

### `classes.dex`

- ~990 KB
- 725 class definitions total
- 416 classes in the `jakiganicsystems/danmakudeath` namespace
- 4,842 method references
- Contains the main game/menu/database/runtime code.

Notable strings show SQLite tables including:

- `my_score`
- `stage_history`

and stage/save related logic.

### `classes2.dex`

- ~5.5 KB
- 2 class definitions total
- Contains the small manual backup/import implementation introduced into the S25 build.
- Custom class: `jakiganicsystems.danmakudeath.menu.A14Launcher`
- Export/import logic packages the app-private `shared_prefs`, `databases`, `files`, and `no_backup` directories.

## Native code

`libdanmakudeath.so` exists for:

- arm64-v8a
- armeabi-v7a
- armeabi
- x86
- mips

Any game logic implemented inside these libraries will require native reverse engineering rather than DEX/smali editing.

## Resources

The APK contains extensive stage/avatar/boss art under `res/drawable*`. Binary resource XML has been decoded into `decoded/res/` for readable inspection.

The compiled resource table remains at `source/apk_raw/resources.arsc`; resource IDs in decoded XML are intentionally retained numerically where a symbolic mapping is not yet reconstructed.
