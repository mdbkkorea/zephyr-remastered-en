ZEPHYR ENGLISH PATCHER — WINDOWS BUILD KIT

1. Extract this entire ZIP to a writable folder (not inside the game).
2. Install 64-bit Python 3.12 from https://www.python.org/downloads/windows/
   Include the Python launcher and Tcl/Tk (default installer options).
3. Double-click Build-Windows.cmd. Internet is needed to download PyInstaller.
4. The result is dist/ZephyrEnglishPatcher.exe.

No .NET SDK or ChatGPT app is required. The finished EXE contains its runtime
and patch data. End users do not need Python or an internet connection.
The build wrapper uses a process-only PowerShell execution-policy override;
it does not change the machine's saved policy.

FIRST WINDOWS TEST
- Close the game. Make a separate copy of the original Korean game folder.
- Run the EXE, browse to that copy, and choose Check Files.
- Choose Install English. Unsupported/modified files are rejected.
- Start the patched copy with Steam running and inspect gameplay.
- Close the game and choose Restore Original. Check Files should say original.
- Test installation again. Keep the EXE for restoration.

FINDING YOUR GAME FOLDER
The usual Steam installation folder is:
C:\Program Files (x86)\Steam\steamapps\common\The Rhapsody of Zephyr Remastered

If you installed Steam or the game on another drive, your folder will differ.
In Steam, right-click the game in your Library, choose Manage, then Browse
local files. Copy the folder address from File Explorer and paste it into
the patcher, or click Browse and select that folder. Select the folder that
contains ZephyrRemastered.exe, not the EXE itself or ZephyrRemastered_Data.
Close the game, click Check Files, then Install English and confirm the folder.
The patcher shows the usual folder and opens Browse there when it exists;
you still choose which game folder or test copy to patch.

Original backups are under %LOCALAPPDATA%\ZephyrEnglishPatcher, grouped by
installation path. Keep the game folder at the same path for restoration.
Recover handles an interrupted operation. Changed files after interruption
are not silently overwritten. Do not run the Chinese upstream patcher.

Optional save-name conversion produces separate copies only. It changes
DialogueName, FullName and JobName using reviewed translations, preserving
unknown names. Back up active saves and close the game before manually
replacing the matching .dat files. Do not overwrite newer progress with an
older converted copy. Game-resource installation does not modify saves.

STATUS
The payload is English playtest 3: 22,403 resource entries and 30 hard-coded
text edits. Local reconstruction and transaction tests are recorded in the
project TEST_LOG.md. This kit is not a compiled or Windows-tested EXE yet.
Some layout/name issues may remain. It supports the exact original resource
hashes in payload/manifest.json, not arbitrary Steam updates or Chinese mods.

The patch data consists of compressed XOR differences against owned original
files, not a full playable game. This local kit has not been published.
There is no updater, telemetry, or external download in the patcher itself.

WINDOWS TEST FOLLOW-UP
The Windows handoff for build kit 003 reports Python 3.12.10 x64/Tk 8.6.15,
a successful EXE build, 10 passing tests, and install/restore of copied game
files through a frozen diagnostic. It found and fixed long backup paths
(WinError 3) and backslashes in recovery journals. These fixes are now merged
with the newer Mac/Linux code. This newly merged kit needs a fresh Windows
EXE build/test. The tested earlier Windows EXE is not included here.
Old failed journals containing backslashes are not automatically migrated.
Real UNC/network-share behavior and full Windows gameplay remain untested.
