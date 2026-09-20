param(
 [Parameter(Mandatory=$true)][string]$Archive,
 [Parameter(Mandatory=$true)][string]$Version,
 [Parameter(Mandatory=$true)][string]$PrivateKeyPath,
 [Parameter(Mandatory=$true)][string]$OutputDirectory
)
$ErrorActionPreference = 'Stop'
$project = Split-Path $PSScriptRoot -Parent
$keyPath = [IO.Path]::GetFullPath($PrivateKeyPath)
if ($keyPath.StartsWith($project + [IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) { throw 'Private key must stay outside the repository.' }
$rsa = [Security.Cryptography.RSA]::Create()
$rsa.ImportFromPem([IO.File]::ReadAllText($keyPath))
if ($rsa.ExportSubjectPublicKeyInfoPem().Trim() -ne [IO.File]::ReadAllText("$project/release-public.pem").Trim()) { throw 'Signing key does not match release public key.' }
$file = Get-Item -LiteralPath $Archive
$metadata = [ordered]@{ version=$Version; filename=$file.Name; size=$file.Length; sha256=(Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant() }
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$manifest = Join-Path $OutputDirectory 'release.json'
[IO.File]::WriteAllText($manifest, ($metadata | ConvertTo-Json), [Text.UTF8Encoding]::new($false))
$signature = $rsa.SignData([IO.File]::ReadAllBytes($manifest),[Security.Cryptography.HashAlgorithmName]::SHA256,[Security.Cryptography.RSASignaturePadding]::Pss)
[IO.File]::WriteAllBytes((Join-Path $OutputDirectory 'release.sig'),$signature)
Write-Output 'Signed release metadata. Private key was not copied.'
