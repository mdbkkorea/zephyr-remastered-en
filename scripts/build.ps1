param([Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference = 'Stop'
$project = Split-Path $PSScriptRoot -Parent
$out = [IO.Path]::GetFullPath($OutputDirectory)
if ($out.StartsWith($project + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw 'Build outside the public source directory.' }
if (Test-Path -LiteralPath $out) { throw 'Choose a new output directory.' }
New-Item -ItemType Directory -Path $out | Out-Null
$work = Join-Path $out 'build-work'
$release = Join-Path $out 'Zephyr-Chinese-Patcher'
python -m PyInstaller --noconfirm --clean --onedir --name ZephyrPatchEngine --collect-all UnityPy --distpath "$release/tools" --workpath "$work/pyinstaller" --specpath $work "$project/engine/main.py"
if ($LASTEXITCODE -ne 0) { throw 'Engine build failed' }
dotnet publish "$project/app/ZephyrPatcher.csproj" -c Release -r win-x64 --self-contained true -o $release --nologo
if ($LASTEXITCODE -ne 0) { throw 'Application build failed' }
Copy-Item -LiteralPath "$project/payload", "$project/licenses", "$project/docs" -Destination $release -Recurse
Get-ChildItem -LiteralPath $project -Filter '*.md' | Copy-Item -Destination $release
Copy-Item -LiteralPath "$project/LICENSE", "$project/release-public.pem", "$project/dependency-versions.json" -Destination $release
Write-Output "Built: $release"
