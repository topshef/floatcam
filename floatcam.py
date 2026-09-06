import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import subprocess
import threading

CAMERA = "Digital Microscope"
WIDTH = 640
HEIGHT = 480

SHAPE = "square"
MIRROR = False
ZOOM = 1.0

BORDER = True
BORDER_WIDTH = 5
BORDER_COLOR = "#00e676"

CORNER_RADIUS = 24
MIN_SIZE = 120
RESIZE_ZONE = 20

# Deliberately weird colour used only as the Windows transparency key.
TRANSPARENT_COLOR = "#010203"

process = None
latest_frame = None
running = True

drag_x = 0
drag_y = 0

resizing = False
resize_start_x = 0
resize_start_y = 0
resize_start_w = 0
resize_start_h = 0


def start_camera():
    global process

    stop_camera()

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-f", "dshow",
        "-i", f"video={CAMERA}",
        "-an",
        "-vf", f"scale={WIDTH}:{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-f", "rawvideo",
        "pipe:1"
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    threading.Thread(
        target=read_frames,
        daemon=True
    ).start()


def stop_camera():
    global process

    if process:
        try:
            process.kill()
        except:
            pass

        process = None


def read_frames():
    global latest_frame

    frame_size = WIDTH * HEIGHT * 3

    while running and process:
        data = process.stdout.read(frame_size)

        if len(data) != frame_size:
            break

        latest_frame = Image.frombytes(
            "RGB",
            (WIDTH, HEIGHT),
            data
        )


root = tk.Tk()
root.title("FloatCam")
root.geometry("320x320")
root.attributes("-topmost", True)
root.overrideredirect(True)

root.configure(
    bg=TRANSPARENT_COLOR
)

# Make the transparency-key colour genuinely transparent in Windows.
root.wm_attributes(
    "-transparentcolor",
    TRANSPARENT_COLOR
)

label = tk.Label(
    root,
    bg=TRANSPARENT_COLOR,
    bd=0,
    highlightthickness=0
)

label.pack(
    fill="both",
    expand=True
)


def mouse_down(event):
    global drag_x
    global drag_y
    global resizing
    global resize_start_x
    global resize_start_y
    global resize_start_w
    global resize_start_h

    w = root.winfo_width()
    h = root.winfo_height()

    if (
        event.x >= w - RESIZE_ZONE
        and event.y >= h - RESIZE_ZONE
    ):
        resizing = True

        resize_start_x = event.x_root
        resize_start_y = event.y_root
        resize_start_w = w
        resize_start_h = h

    else:
        resizing = False

        drag_x = event.x_root - root.winfo_x()
        drag_y = event.y_root - root.winfo_y()


def mouse_move(event):
    if resizing:
        dx = event.x_root - resize_start_x
        dy = event.y_root - resize_start_y

        if SHAPE in ("square", "circle"):
            change = max(dx, dy)

            size = max(
                MIN_SIZE,
                resize_start_w + change
            )

            root.geometry(
                f"{size}x{size}"
            )

        else:
            new_w = max(
                MIN_SIZE,
                resize_start_w + dx
            )

            new_h = max(
                80,
                resize_start_h + dy
            )

            root.geometry(
                f"{new_w}x{new_h}"
            )

    else:
        x = event.x_root - drag_x
        y = event.y_root - drag_y

        root.geometry(
            f"+{x}+{y}"
        )


def mouse_up(event):
    global resizing
    resizing = False


def mouse_motion(event):
    w = root.winfo_width()
    h = root.winfo_height()

    if (
        event.x >= w - RESIZE_ZONE
        and event.y >= h - RESIZE_ZONE
    ):
        label.configure(
            cursor="size_nw_se"
        )
    else:
        label.configure(
            cursor="arrow"
        )


def set_circle():
    global SHAPE

    SHAPE = "circle"

    size = min(
        root.winfo_width(),
        root.winfo_height()
    )

    root.geometry(
        f"{size}x{size}"
    )


def set_square():
    global SHAPE

    SHAPE = "square"

    size = min(
        root.winfo_width(),
        root.winfo_height()
    )

    root.geometry(
        f"{size}x{size}"
    )


def set_rectangle():
    global SHAPE

    SHAPE = "rectangle"

    width = root.winfo_width()

    root.geometry(
        f"{width}x{int(width * 9 / 16)}"
    )


def toggle_mirror():
    global MIRROR
    MIRROR = not MIRROR


def set_zoom(value):
    global ZOOM
    ZOOM = value


def toggle_border():
    global BORDER
    BORDER = not BORDER


def quit_app():
    global running

    running = False
    stop_camera()
    root.destroy()


def popup(event):
    menu.tk_popup(
        event.x_root,
        event.y_root
    )


def make_shape_mask(w, h, inset=0):
    mask = Image.new(
        "L",
        (w, h),
        0
    )

    draw = ImageDraw.Draw(mask)

    box = (
        inset,
        inset,
        w - inset - 1,
        h - inset - 1
    )

    if SHAPE == "circle":
        draw.ellipse(
            box,
            fill=255
        )

    else:
        radius = min(
            CORNER_RADIUS,
            max(1, min(w, h) // 4)
        )

        radius = max(
            1,
            radius - inset
        )

        draw.rounded_rectangle(
            box,
            radius=radius,
            fill=255
        )

    return mask


def update():
    image = latest_frame

    if image:
        image = image.copy()

        if MIRROR:
            image = image.transpose(
                Image.Transpose.FLIP_LEFT_RIGHT
            )

        w = label.winfo_width()
        h = label.winfo_height()

        if w > 1 and h > 1:
            iw, ih = image.size

            # Digital centre zoom.
            if ZOOM > 1:
                crop_w = int(iw / ZOOM)
                crop_h = int(ih / ZOOM)

                left = (iw - crop_w) // 2
                top = (ih - crop_h) // 2

                image = image.crop(
                    (
                        left,
                        top,
                        left + crop_w,
                        top + crop_h
                    )
                )

                iw, ih = image.size

            # Cover the complete window while keeping camera aspect ratio.
            scale = max(
                w / iw,
                h / ih
            )

            nw = int(iw * scale)
            nh = int(ih * scale)

            image = image.resize(
                (nw, nh),
                Image.Resampling.LANCZOS
            )

            x = (nw - w) // 2
            y = (nh - h) // 2

            image = image.crop(
                (
                    x,
                    y,
                    x + w,
                    y + h
                )
            )

            # Start with a completely transparent-key coloured canvas.
            final = Image.new(
                "RGB",
                (w, h),
                TRANSPARENT_COLOR
            )

            if BORDER:
                # Outer shape is green and goes RIGHT to the window edge.
                outer_mask = make_shape_mask(
                    w,
                    h,
                    0
                )

                green = Image.new(
                    "RGB",
                    (w, h),
                    BORDER_COLOR
                )

                final.paste(
                    green,
                    (0, 0),
                    outer_mask
                )

                # Camera begins just inside the green edge.
                inner_mask = make_shape_mask(
                    w,
                    h,
                    BORDER_WIDTH
                )

                final.paste(
                    image,
                    (0, 0),
                    inner_mask
                )

            else:
                # Camera itself goes right to the shaped edge.
                outer_mask = make_shape_mask(
                    w,
                    h,
                    0
                )

                final.paste(
                    image,
                    (0, 0),
                    outer_mask
                )

            photo = ImageTk.PhotoImage(
                final
            )

            label.configure(
                image=photo
            )

            label.image = photo

    root.after(
        30,
        update
    )


menu = tk.Menu(
    root,
    tearoff=0
)

menu.add_command(
    label="Circle",
    command=set_circle
)

menu.add_command(
    label="Square",
    command=set_square
)

menu.add_command(
    label="Rectangle",
    command=set_rectangle
)

menu.add_separator()

zoom_menu = tk.Menu(
    menu,
    tearoff=0
)

zoom_menu.add_command(
    label="Wide - 1.0x",
    command=lambda: set_zoom(1.0)
)

zoom_menu.add_command(
    label="Normal - 1.25x",
    command=lambda: set_zoom(1.25)
)

zoom_menu.add_command(
    label="Close - 1.5x",
    command=lambda: set_zoom(1.5)
)

zoom_menu.add_command(
    label="Closer - 2.0x",
    command=lambda: set_zoom(2.0)
)

menu.add_cascade(
    label="Zoom",
    menu=zoom_menu
)

menu.add_command(
    label="Green border on/off",
    command=toggle_border
)

menu.add_command(
    label="Mirror",
    command=toggle_mirror
)

menu.add_command(
    label="Restart camera",
    command=start_camera
)

menu.add_separator()

menu.add_command(
    label="Exit",
    command=quit_app
)


label.bind(
    "<ButtonPress-1>",
    mouse_down
)

label.bind(
    "<B1-Motion>",
    mouse_move
)

label.bind(
    "<ButtonRelease-1>",
    mouse_up
)

label.bind(
    "<Motion>",
    mouse_motion
)

label.bind(
    "<Button-3>",
    popup
)

root.bind(
    "<Escape>",
    lambda event: quit_app()
)

root.protocol(
    "WM_DELETE_WINDOW",
    quit_app
)


start_camera()
update()
root.mainloop()