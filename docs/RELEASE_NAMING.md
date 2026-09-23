# Distribution filenames

User-approved convention, effective from the next build after beta.4:

`zephyr_english_[platform]_[version number]_betaXX`

Use lowercase names, underscore separators and a two-digit beta number. Keep
Semantic Versioning internally (for example, `1.0.0-beta.5`) and the existing tag
pattern `english-v1.0.0-beta.5`. These rules name the download archives; do not
rename executable/app internals without updating their launch/build scripts.

Examples for beta.5:

- `zephyr_english_macos_1.0.0_beta05.zip` (Apple Silicon; document architecture)
- `zephyr_english_linux_1.0.0_beta05.tar.gz` (x64; document architecture)
- `zephyr_english_windows_steam_1.0.0_beta05.zip` (Steam build kit)
- `zephyr_english_windows_purple_1.0.0_beta05.zip` (PURPLE build kit)

Steam and PURPLE Windows packages must remain distinct. Keep short internal ZIP
roots (`ZSteam`, `ZPurple`) and existing Windows path-length checks. If additional
architectures are shipped, add an architecture component to avoid collisions.
Beta.4 and earlier published asset filenames remain unchanged.
