# Windows build kits 1.0.0-beta.2

Two separate prepared ZIPs are required; each produces `dist/ZephyrEnglishPatcher.exe`:

- `Zephyr-English-1.0.0-beta.2-steam-windows-build-kit.zip`: Steam; automatic supported Passives 2.4.3 and Fullmap 1.8.0 detection.
- `Zephyr-English-1.0.0-beta.2-purple-windows-build-kit.zip`: verified PURPLE build; standard translation, experimental mod/platform support.

Both include current Geysir terminology, full battle-command names using nonbreaking spaces, and Stab. Extract the entire matching kit and run its `Build-Windows.cmd`. Install Python 3.12 x64 with the launcher and Tk. Git is not required. **GitHub Code → Download ZIP and source archives are not prepared build kits:** they omit generated English payloads. Build-kit ZIPs are separate distribution artifacts, not committed game assets.

The version identifies translation/installer changes; the platform filename and manifest identify edition. Do not interchange editions. Old downloaded ZIPs do not update when the repository changes.

Build without elevation. Run the finished EXE as administrator when patching under Program Files (x86). Use Check Files/Recover after an interrupted install. Default PURPLE path: `C:\Program Files (x86)\NC\Rhapsody of Zephyr Remastered`.

Validation: all three stages (Steam standard, Steam Passives, PURPLE standard) rebuilt 22,403 entries with zero errors/warnings and original/readback checks. Full battle names were user-tested in Mac CrossOver. The new Windows executables must be built/tested by the user; no Windows PC was controlled. This is not a claim of newly tested Windows binaries. Existing published beta.1 executables remain unchanged.

## SHA256

- `Zephyr-English-1.0.0-beta.2-steam-windows-build-kit.zip` (49190133 bytes): `f3b02fd60dea3f7d2b493a7a84cd1d6b9a6d80ff0fb81a23cc37b93cf23c35f7`
- `Zephyr-English-1.0.0-beta.2-purple-windows-build-kit.zip` (24936411 bytes): `28a27c96e566f6e7ef9c13bd4b556f1fcf6e95827ad88c74ad6e870ac37171f4`

Integration checks on separate resource copies passed for install, repeat install and exact restoration: Steam standard, Passives, Fullmap, both supported mods, unsupported mods, and PURPLE standard. Wrong editions were rejected. Global running-game detection was overridden only in the private test harness because a separate user game was running; the distributed check is unchanged. Public test suite: 60 passed.
