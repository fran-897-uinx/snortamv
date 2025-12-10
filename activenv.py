import os
import platform
import subprocess
import shutil
import sys

VENV = "env"   # Change if your venv folder has a different name


def get_shell():
    """Detect current shell."""
    if os.name == "nt":  # Windows
        parent = os.environ.get("COMSPEC", "")
        if "powershell.exe" in parent.lower():
            return "powershell"
        if "cmd.exe" in parent.lower():
            return "cmd"
        return "cmd"

    # Linux / macOS
    return os.environ.get("SHELL", "").split("/")[-1].lower()


def get_venv_paths():
    """Return activation script paths for all OS/shell types."""
    return {
        "windows": {
            "powershell": os.path.join(VENV, "Scripts", "Activate.ps1"),
            "cmd": os.path.join(VENV, "Scripts", "activate.bat"),
            "python": os.path.join(VENV, "Scripts", "python.exe")
        },
        "unix": {
            "bash": os.path.join(VENV, "bin", "activate"),
            "zsh": os.path.join(VENV, "bin", "activate"),
            "python": os.path.join(VENV, "bin", "python")
        }
    }


def activate_and_run():
    os_type = platform.system().lower()
    shell = get_shell()
    paths = get_venv_paths()

    print(f"Detected OS: {os_type}")
    print(f"Detected shell: {shell}")

    # 1. WINDOWS
    if os_type == "windows":
        p = paths["windows"]["python"]
        if os.path.exists(p):
            print(f"Using venv Python: {p}")
            subprocess.run([p, "--version"])
            return
        
        else:
            print("Venv Python not found. Is the environment created?")
            return

    # 2. LINUX / MAC
    if os_type in ["linux", "darwin"]:
        p = paths["unix"]["python"]
        if os.path.exists(p):
            print(f"Using venv Python: {p}")
            subprocess.run([p, "--version"])
            return
        else:
            print("Venv Python not found. Create venv first.")
            return

    print("Unsupported OS")


if __name__ == "__main__":
    activate_and_run()
