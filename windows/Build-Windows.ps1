$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
if (-not (Test-Path 'payload/manifest.json')) { throw 'Translation payload is missing. GitHub Code > Download ZIP contains source only and cannot build the patcher directly. Download the prepared Windows build-kit ZIP for your edition (Steam or PURPLE), extract the entire ZIP, and run its Build-Windows.cmd. The payload folder must be beside this script.' }
py -3.12 -c "import struct; assert struct.calcsize('P') == 8, 'Install 64-bit Python'"
if ($LASTEXITCODE -ne 0) { throw 'Install Python 3.12 (64-bit) with the Python launcher, then retry.' }
if (-not (Test-Path '.build-venv/Scripts/python.exe')) {
    py -3.12 -m venv .build-venv
    if ($LASTEXITCODE -ne 0) { throw 'Could not create build environment.' }
}
$python = Join-Path $PSScriptRoot '.build-venv/Scripts/python.exe'
& $python -m pip install 'pyinstaller==6.22.3'
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
& $python -m unittest discover -s tests
if ($LASTEXITCODE -ne 0) { throw 'Patcher tests failed. EXE was not built.' }
& $python -m PyInstaller --noconfirm --clean --onefile --windowed --name ZephyrEnglishPatcher --add-data 'payload;payload' --add-data 'licenses;licenses' --add-data 'LICENSE;.' english_gui.py
if ($LASTEXITCODE -ne 0) { throw 'EXE build failed.' }
Write-Host "Built: $PSScriptRoot/dist/ZephyrEnglishPatcher.exe"
Write-Host 'Test Check Files, Install English, and Restore Original on a separate game copy before distributing.'
