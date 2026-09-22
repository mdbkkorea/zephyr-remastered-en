# Automatic mod detection — build 015

One installer supports the original game, ZephyrPassives 2.4.3, ZephyrFullmap 1.8.0, or both. Choose the game folder and click **Check Files**; the detected mods and selected translation are displayed. **Install English** checks again and applies the appropriate files.

- Without Passives: standard game descriptions.
- With Passives 2.4.3: descriptions for the mod's default settings. Customized gameplay settings are not interpreted.
- With Fullmap 1.8.0: English map labels, with the original plugin backed up for restoration.
- Missing mods are never installed. Already-English Fullmap is preserved if it was installed independently.
- Unknown/modified versions and duplicate or relocated named plugin DLLs stop installation. Detection covers these two supported mods, not arbitrary third-party patches.
- Adding/removing supported mods and rerunning this installer updates the selected translation. Removed plugins are not recreated.

Latest dialogue spacing, settings labels, Geyshir, Aura Slash and R675 corrections are included. Keep the same installer for restoration. Saves are unchanged.

macOS: unzip and open ZephyrEnglishPatcher.app (Apple Silicon, ad-hoc signed, not notarized). CrossOver mod launches still require the existing `--dll 'winhttp=n,b'` launcher option.

Linux: extract the archive, run `./ZephyrEnglishPatcher`. Built for x86-64 with Debian 12 / glibc 2.36. For the user mods, Steam/Proton launch options remain `WINEDLLOVERRIDES="winhttp=n,b" %command%`.

Validation: see TEST_LOG.md for exact build and test results. Fedora 44 native GUI/gameplay and the latest translated map layout still require user testing. Windows build is delegated to the user's Windows task.
