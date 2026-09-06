$ErrorActionPreference = "Stop"

$ffmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue

if (-not $ffmpeg) {
    throw "ffmpeg.exe not found on PATH"
}

Write-Host "Bundling FFmpeg from:"
Write-Host $ffmpeg.Source
Write-Host ""

py -m PyInstaller --clean --noconfirm .\FloatCam.spec

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Build complete:"
Get-Item .\dist\FloatCam.exe |
    Select-Object FullName,
        @{Name="SizeMB";Expression={
            [math]::Round($_.Length / 1MB, 1)
        }}

Write-Host ""
Get-FileHash .\dist\FloatCam.exe -Algorithm SHA256
