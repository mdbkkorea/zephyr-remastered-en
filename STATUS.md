# Project status - build 016

The Korean-authoritative English catalog contains 22,403 resource translations and 30 hard-coded text edits. Chinese is supporting context. Reviewed terminology includes Geyshir, Cyrups, Ruben, Gishne, Deimos, High Church, High God and Aura Slash. Dialogue spacing and compact UI labels have been corrected from playtest feedback.

The shared Windows/macOS/Linux installer automatically detects ZephyrPassives 2.4.3 and ZephyrFullmap 1.8.0. Supported mods receive matching translations. An unsupported version selects standard resource translation and preserves all mod files. Missing mods are not installed. Passives descriptions assume default settings. Backups, restoration and interrupted-operation recovery are implemented.

Windows x64, macOS Apple Silicon and Linux x64 installers have been built and tested separately from Steam installations. This repository update publishes source and review documents, not compiled installers or original game assets. See README.md, docs/RELEASE_016.md and TEST_LOG.md.

Pending: native Fedora 44/Proton gameplay, wider story coverage and translated map layout checks. Existing screenshots verify selected CrossOver gameplay screens, not a complete playthrough. Names without approval remain provisional. Tempest restoration remains separate.

## 1.0.0-beta.1 release preparation

Centralized version reporting and manifest version. Translation payload is unchanged from build 016. Source suite: 54 tests passed in 0.899 s. Platform rebuild validation is recorded in the release notes. Windows is the only fully tested release; macOS/Linux are experimental.
