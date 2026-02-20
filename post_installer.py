import os
import platform
import subprocess
import sys
import shutil
import activenv
from pathlib import Path

VENV = "env"


# ================Distro Detection================
def get_linux_distro():
    os_release = Path("/etc/os-release")
    if not os_release.exists():
        return None

    data = {}
    for line in os_release.read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            data[k] = v.strip('"')

    return {
        "id": data.get("ID"),
        "name": data.get("NAME"),
        "version": data.get("VERSION_ID"),
    }


distro = get_linux_distro()


if not distro:
    print(" Cannot detect Linux distro")
    sys.exit(1)

print(f"Running on {distro['name']} {distro['version']}")


def get_pkg_manager(distro):
    distro_id = distro["id"]

    if distro_id in ("ubuntu", "debian"):
        return "apt"
    if distro_id in ("fedora", "rhel", "centos"):
        return "dnf"
    if distro_id in ("arch", "manjaro"):
        return "pacman"

    return None


# ---------------------------------------
#   CHECK if Snort is installed
# ---------------------------------------
def snort_installed():
    return shutil.which("snort") is not None or shutil.which("snort3") is not None


# ---------------------------------------
#   INSTALL SNORT 3 BY OS
# ---------------------------------------
def install_snort():
    os_type = platform.system().lower()

    print(f"\n[=] Checking if Snort is installed...")

    if snort_installed():
        print(f" Snort already installed. Skipping installation.\n")
        return

    print(f"[+] Snort not found. Installing Snort 3...\n")

    # -------------------------------
    # WINDOWS
    # -------------------------------
    if os_type == "windows":
        if shutil.which("choco") is None:
            print("[!] Chocolatey not installed. Installing Chocolatey...")
            subprocess.run(
                [
                    "powershell",
                    "Set-ExecutionPolicy Bypass -Scope Process -Force; "
                    "iwr https://community.chocolatey.org/install.ps1 -UseBasicParsing | iex",
                ],
                check=True,
            )

        print("[+] Installing Snort 3 using Chocolatey...")
        subprocess.run(["choco", "install", "snort3", "-y"], check=True)

    # -------------------------------
    # LINUX
    # -------------------------------
    elif os_type == "linux":
        print("[+] Installing Snort for Linux...")

        distro = get_linux_distro()
        if not distro:
            print(" Cannot detect Linux distro")
            return

        pm = get_pkg_manager(distro)

        if pm == "apt":
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "snort"], check=True)

        elif pm == "dnf":
            subprocess.run(["sudo", "dnf", "install", "-y", "snort"], check=True)

        elif pm == "pacman":
            subprocess.run(
                ["sudo", "pacman", "-Sy", "--noconfirm", "snort"],
                check=True,
            )

        else:
            print(" Unsupported Linux distro")

    # -------------------------------
    # MACOS
    # -------------------------------
    elif os_type == "darwin":
        print("[+] Checking homebrew...")
        if shutil.which("brew") is None:
            print("[+] Installing Homebrew...")
            subprocess.run(
                [
                    "/bin/bash",
                    "-c",
                    "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)",
                ],
                check=True,
            )

        print("[+] Installing Snort 3 on macOS...")
        subprocess.run(["brew", "install", "snort"], check=True)

    else:
        print("❌ Unsupported OS for Snort installation.")
        return

    print(f"\n[✓] Snort 3 installation completed.\n")


# ---------------------------------------
#   CREATE VIRTUAL ENVIRONMENT
# ---------------------------------------
def create_venv():
    if not os.path.exists(VENV):
        print("[+] Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", VENV], check=True)
    else:
        print(" Virtual environment already exists.")


# ---------------------------------------
#   GET PYTHON INSIDE VENV
# ---------------------------------------
def get_venv_python():
    os_type = platform.system().lower()
    if os_type == "windows":
        return os.path.join(VENV, "Scripts", "python.exe")
    elif os_type == "linux" or os_type == "darwin":
        return os.path.join(VENV, "bin", "python")


# ---------------------------------------
#   INSTALL REQUIREMENTS INSIDE VENV
# ---------------------------------------
def install_requirements(venv_python):
    if not os.path.exists("requirements.txt"):
        print("[!] requirements.txt not found. Skipping.")
        return

    print("[+] Checking installed packages inside venv...")

    result = subprocess.run(
        [venv_python, "-m", "pip", "freeze"], capture_output=True, text=True
    )

    installed = {
        line.split("==")[0].lower(): line.split("==")[1]
        for line in result.stdout.splitlines()
        if "==" in line
    }

    with open("requirements.txt", "r") as f:
        required = [l.strip() for l in f if l.strip()]

    missing = []

    for pkg in required:
        pkg_name = pkg.split("==")[0].lower()
        if pkg_name not in installed:
            missing.append(pkg)

    if not missing:
        print(" All requirements already installed.")
        return

    print(f"[+] Installing missing packages: {missing}")
    subprocess.run([venv_python, "-m", "pip", "install", *missing], check=True)
    print(f" Done installing requirements.\n")


# -------------------------------------
#         ACTIVATING THE VENV
# ----------------------------------------
def actvenv(venv_python):
    if not os.path.exists("activenv.py"):
        print(
            f"Please go to the README.MD the see \n how to activate the Virtual environment"
        )
        return
    print("[+] Activating virtual Environment")
    subprocess.run([venv_python, "activenv.py"])


# ---------------------------------------
#   RUN APPLICATION INSIDE VENV
# ---------------------------------------
def run_app(venv_python):
    if not os.path.exists("cli.py"):
        print("❌ ERROR: cli.py not found.")
        return

    print(f"[+] Launching SnortAMV inside activated venv...\n")
    subprocess.run([venv_python, "cli.py"])


# ---------------------------------------
#               MAIN
# ---------------------------------------
if __name__ == "__main__":
    print(f"[=] Starting post installation...\n")

    install_snort()  # FIRST → install snort
    create_venv()  # THEN create env
    venv_python = get_venv_python()  # get python inside env
    actvenv(venv_python)  # activate venv
    install_requirements(venv_python)  # install packages
    run_app(venv_python)  # run your tool
