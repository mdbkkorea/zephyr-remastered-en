# Installer and distribution filenames

User-approved convention for subsequent builds:

`ZEnglish[Steam|Purple|Macos|Linux]_Version_betaXX`

Use a three-part version and at least two digits for the beta number. Internal
Semantic Versioning and Git tags remain unchanged (`1.0.0-beta.5`,
`english-v1.0.0-beta.5`).

Examples:

- `ZEnglishSteam_1.0.0_beta05.exe` — Windows Steam installer
- `ZEnglishPurple_1.0.0_beta05.exe` — Windows PURPLE installer
- `ZEnglishMacos_1.0.0_beta05.app` — macOS patcher
- `ZEnglishLinux_1.0.0_beta05` — Linux executable

Archives use the same base name with `.zip` or `.tar.gz`. Windows build-kit
ZIPs contain the short `ZSteam`/`ZPurple` roots to limit extraction path length;
keep build kits and prebuilt EXE archives separately identified in release notes.
`windows/english_version.py` generates names from the release version. The Windows
build reads the edition from its payload manifest. The Mac launcher finds the
renamed app beside itself and rejects ambiguous folders with multiple patcher apps.
Application bundle identity and saved settings/backup locations stay stable.

Already published releases retain their filenames and checksums. Apply this scheme
when rebuilding or creating the next release. Older names in historical release
notes describe those downloads.
