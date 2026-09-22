# Release versioning

The canonical version is `VERSION` in `windows/english_version.py`. The installer engine and GUI import it; exported automatic manifests record it as `release_version`. All platform packages must use the same frozen kit.

Release progression: `1.0.0-beta.1`, `1.0.0-beta.2`, `1.0.0-rc.1`, `1.0.0`. Afterwards, patch versions cover compatible translation/UI/installer fixes, minor versions add compatible features/mod support, and major versions indicate incompatible installer or backup changes.

Tags use `english-v<version>` to distinguish inherited Chinese tags. Assets use `Zephyr-English-<version>-<platform>-<architecture>`. Do not replace published assets with different bytes: distribute a new version. Record SHA256 checksums. Game build and mod compatibility are separate fields, not parts of the release number. Build 016 remains a legacy identifier; beta.1 contains the same translation payload with centralized version reporting.

A release must identify its tested platforms. Only Windows is fully tested for the first beta; macOS and Linux are experimental. Translation coverage is separate from installer validation.
