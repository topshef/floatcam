# -*- mode: python ; coding: utf-8 -*-

import shutil

ffmpeg_path = shutil.which("ffmpeg")

if not ffmpeg_path:
    raise SystemExit(
        "ffmpeg.exe was not found on PATH. Install FFmpeg before building."
    )

a = Analysis(
    ["floatcam.py"],
    pathex=[],
    binaries=[
        (ffmpeg_path, ".")
    ],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[
        "pyi_rth_ffmpeg.py"
    ],
    excludes=[],
    noarchive=False,
    optimize=0
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="FloatCam",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)
