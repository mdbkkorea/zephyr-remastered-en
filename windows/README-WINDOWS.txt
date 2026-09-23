ZEPHYR ENGLISH PATCHER — WINDOWS BUILD KIT

Use the prepared Windows build-kit ZIP for your game edition: Steam or PURPLE.
GitHub Code > Download ZIP contains source code, not the prepared payload.

1. Extract the entire kit to a short local path, such as C:\Zephyr.
   Open ZSteam or ZPurple inside it. Avoid nesting inside older kit folders.
2. Install Python 3.12 (64-bit), including Python Launcher and Tcl/Tk.
3. Run Build-Windows.cmd beside the payload folder.
4. The output is dist\ZephyrEnglishPatcher.exe.

Git, a .NET SDK and the ChatGPT app are not required. The first build needs
internet access to install PyInstaller. Building does not require administrator
privileges. Keep all extracted files together.

Close the game before applying a patch. For Program Files (x86), right-click
the finished EXE and choose Run as administrator. Choose the folder containing
ZephyrRemastered.exe, Check Files, then Install English. After an interrupted
installation, use Check Files and Recover before retrying. Test a separate game
copy first. Keep the patcher and backups for Restore Original.

Steam default:
C:\Program Files (x86)\Steam\steamapps\common\The Rhapsody of Zephyr Remastered
PURPLE default:
C:\Program Files (x86)\NC\Rhapsody of Zephyr Remastered

Steam kits detect supported ZephyrPassives 2.4.3 / ZephyrFullmap 1.8.0. Missing
or unsupported mods use standard translation; unsupported mod files stay intact.
PURPLE kits are separate and experimental, standard translation only; mod
compatibility is not verified there. Game-file hashes enforce edition/version.

Beta.2 includes Geysir, full battle names and Stab. Its Windows executable still
needs user build/testing. Earlier Windows release testing does not certify this
new kit. Installer resource checks on Mac are not Windows GUI/gameplay tests.

New build filenames: ZEnglishSteam_1.0.0_betaXX.exe or ZEnglishPurple_1.0.0_betaXX.exe, selected from the payload edition. Mac: ZEnglishMacos_1.0.0_betaXX.app. Linux: ZEnglishLinux_1.0.0_betaXX. The actual version/beta comes from english_version.py. Published older archives retain their original names.
