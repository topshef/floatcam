import os
import sys

if getattr(sys, "frozen", False):
    bundle_dir = getattr(
        sys,
        "_MEIPASS",
        os.path.dirname(sys.executable)
    )

    os.environ["PATH"] = (
        bundle_dir
        + os.pathsep
        + os.environ.get("PATH", "")
    )
