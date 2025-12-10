"""Simple dependency checker (looks for `snort` executable)."""

import shutil


def check_snort():
    path = shutil.which("snort")
    if path:
        print(f"Found snort at: {path}")
        return True
    else:
        print("snort executable not found in PATH. Some features may not work.")
        return False
