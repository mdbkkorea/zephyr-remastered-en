# Project status - build 016

The Korean-authoritative English catalog contains 22,403 resource translations and 30 hard-coded text edits. Chinese is supporting context. Reviewed terminology includes Geyshir, Cyrups, Ruben, Gishne, Deimos, High Church, High God and Aura Slash. Dialogue spacing and compact UI labels have been corrected from playtest feedback.

The shared Windows/macOS/Linux installer automatically detects ZephyrPassives 2.4.3 and ZephyrFullmap 1.8.0. Supported mods receive matching translations. An unsupported version selects standard resource translation and preserves all mod files. Missing mods are not installed. Passives descriptions assume default settings. Backups, restoration and interrupted-operation recovery are implemented.

Windows x64, macOS Apple Silicon and Linux x64 installers have been built and tested separately from Steam installations. This repository update publishes source and review documents, not compiled installers or original game assets. See README.md, docs/RELEASE_016.md and TEST_LOG.md.

Pending: native Fedora 44/Proton gameplay, wider story coverage and translated map layout checks. Existing screenshots verify selected CrossOver gameplay screens, not a complete playthrough. Names without approval remain provisional. Tempest restoration remains separate.

## 1.0.0-beta.1 release preparation

Centralized version reporting and manifest version. Translation payload is unchanged from build 016. Source suite: 54 tests passed in 0.899 s. Platform rebuild validation is recorded in the release notes. Windows is the only fully tested release; macOS/Linux are experimental.

Windows beta.1 rebuild and direct GUI install/restore passed. All three beta.1 packages are ready, with Windows the only fully tested installer release and macOS/Linux experimental. Automatic export now refreshes packaged tests when combining older resource kits.

### Safari review suggestions - 2026-09-23

Added per-entry translation suggestions and explanations with separate pending Markdown records. A loopback-only Mac service saves into the mounted review folder. Browser drafts survive navigation; saved entries reload; revisions preserve previous Markdown files. Source/revision checks, idempotent retry and explicit save-failure states prevent silent data loss. No translation or game files are changed automatically. Private suggestion records and deployed service data are excluded from Git.

Validation: six persistence tests; JavaScript search/navigation, draft retention, successful saves/reload and offline failure tests; actual HTTP-to-mounted-storage Markdown save/readback with Unicode, idempotency and origin/token/source rejection. Safari rendering inspected; native Safari typing/save interaction was not established by automation. API and JavaScript paths were independently tested. No compiled release changes.

### Full battle-command names — 2026-09-23

Replaced compact battle labels with full names using nonbreaking spaces within attack suffixes. Updated 199 mirrored occurrences covering 51 Korean labels and ten Stab/stabs occurrences (209 total). Korean source, Chinese references and resource identities preserved. User confirmed both the Cyrano trial and expanded Mac CrossOver test work. Rebuilt bundles passed full-tree readback and unchanged-object checks; catalog CRC/size/hash checks passed. Local full-catalog audit: 22,403 entries, zero errors/warnings. Public catalogs and review sheets updated; distributed release packages have not been rebuilt. No Windows runtime verification of these labels is claimed.
