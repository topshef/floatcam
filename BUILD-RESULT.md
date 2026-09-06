# FloatCam Portable Build Record

## Artifact

- File: FloatCam.exe
- Size: 111.4 MB
- SHA-256: 43B2DD87C453D714CA43FA0AB6E41A6379B278043F4ECF418790B78D73D2CD2A
- Built: 2026-09-06 15:08:16 +01:00
- Source commit: 3665ad91cbc9112cd8734321b4e26edb70d92b28

## Build environment

- Python: Python 3.14.2
- PyInstaller: 6.22.2
- FFmpeg: ffmpeg version 9.0.1-full_build-www.gyan.dev Copyright (c) 2000-2026 the FFmpeg developers
- Windows: Microsoft Windows 11 Home
- Windows version: 10.0.26200
- Windows build: 26200

## Build method

The executable was built using:

    .\build.ps1

The build uses FloatCam.spec and bundles ffmpeg.exe into the PyInstaller one-file executable.

## Portability test

The executable was launched after reducing PATH to Windows system directories only:

    $oldPath = $env:Path
    $env:Path = "$env:SystemRoot\System32;$env:SystemRoot"
    Start-Process (Resolve-Path ".\dist\FloatCam.exe")
    $env:Path = $oldPath

The Digital Microscope live camera feed operated successfully during this test.

This demonstrates that this tested executable uses its bundled FFmpeg and does not depend on the separately installed FFmpeg being present on PATH.

## Hash note

The SHA-256 above identifies the exact executable tested in this build.

A future rebuild is not expected to produce the same SHA-256 unless the entire build process and environment are made reproducible. A differing hash therefore does not by itself indicate a bad build.
