# FloatCam

FloatCam is a minimal Windows floating-camera viewer designed to give a simple Loom-style camera overlay without the complexity of OBS.

It displays a webcam as an always-on-top floating window with selectable shape, digital zoom, mirroring, resizing and an optional green border.

## Current test camera

The initial development and testing camera is a generic **Mini DV / Thumb Camera**, which Windows identifies as:

- Device name: `Digital Microscope`
- USB VID: `1908`
- USB PID: `3283`
- USB interface: `VID_1908&PID_3283&MI_00`

The camera works as a standard Windows video capture device as well as exposing USB mass storage.

## Camera specifications

The following specifications are stated on the product packaging:

| Specification | Value |
|---|---|
| Sensor | 2 million pixels |
| Video resolution | 1920 × 1080p |
| Video format | AVI |
| Frame rate | 30 fps |
| View angle | 90° |
| Photo format | JPG |
| Photo resolution | 3760 × 2128 |
| Battery capacity | 350 mAh |
| Recording time | About 2–3 hours |
| Storage use | About 7 GB/hour |
| Charging time | 3–4 hours |
| Memory card | Micro SD |
| Maximum memory | Up to 128 GB |
| Supported OS | Windows XP / 7 / 10 / 11 |
| USB interface | USB 1.1 / 2.0 |
| Operating temperature | -10°C to 60°C |
| Operating humidity | 15–85% RH |

These are packaging specifications and have not all been independently verified.

## Current features

- Always-on-top floating camera
- Borderless window
- Rounded square
- Rounded rectangle
- Circular camera mode
- Transparent corners
- Resizable window
- Digital zoom: 1.0x, 1.25x, 1.5x and 2.0x
- Optional green live border
- Mirror mode
- Right-click control menu
- FFmpeg DirectShow capture
- Explicit selection of the `Digital Microscope` camera

## Requirements

- Windows 11
- Python 3
- Pillow
- FFmpeg

Install Python requirements:

    py -m pip install -r requirements.txt

FloatCam currently expects FFmpeg to be available on PATH.

## Run

    py floatcam.py

## Controls

- Drag the camera window to move it
- Drag from the bottom-right corner to resize
- Right-click for shape, zoom, border, mirror and camera controls
- Press `Esc` to exit

## Status

`v0.1-working` represents the first known-good Python implementation tested with the Mini DV camera described above.

Future work includes packaging FloatCam as a standalone Windows executable and improving camera-device selection.
