# Building FloatCam

## Build environment

FloatCam is currently built on Windows using Python and PyInstaller.

## Install dependencies

    py -m pip install -r requirements.txt
    py -m pip install pyinstaller

FFmpeg must currently also be installed and available on PATH.

## Build executable

From the repository root:

    py -m PyInstaller --onefile --windowed --name FloatCam floatcam.py

The executable is generated at:

    dist\FloatCam.exe

## Test

Close any application currently using the camera, then run:

    .\dist\FloatCam.exe

The current executable still depends on FFmpeg being installed on the machine.

A future build will bundle FFmpeg so FloatCam can run as a self-contained Windows application.
