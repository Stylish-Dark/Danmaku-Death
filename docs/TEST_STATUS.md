# Runtime test status

## Current baseline

A28 is the user-selected canonical baseline and the best current build.

## Proven immediately before A28

The A27 manual game-data control flow was physically tested and reported working almost flawlessly. The only reported defect was that the import document picker did not accept the `.tar` extension produced by export.

## A28 delta

A28 changes the backup filename extension from `.tar` to `.sav` while leaving the underlying archive format unchanged.

A detailed physical regression matrix for A28 should be recorded here after testing rather than inferred from static APK validation.

## Future checkpoint rule

A revision is not called "verified" from ZIP integrity, DEX checksums, resource alignment or signatures alone. Runtime claims require physical-device confirmation.
