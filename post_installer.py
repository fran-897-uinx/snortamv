import os
import platform
import subprocess
import sys
import shutil
import activenv
from pathlib import Path

os_type = platform.system().lower()
from modules.utilities.logger import get_logger

logger = get_logger(__name__)
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


def distro_detector():
    distro = get_linux_distro()
    if os_type == "linux":
        if not distro:
            print(" Cannot detect Linux distro")
            sys.exit(1)
        print(f"Running on {distro['name']} {distro['version']}")
    else:
        return


distro_detector()


def get_pkg_manager(distro):
    distro_id = distro["id"]

    if distro_id in ("ubuntu", "debian"):
        return "apt"
    if distro_id in ("fedora", "rhel", "centos"):
        return "dnf"
    if distro_id in ("arch", "manjaro"):
        return "pacman"

    return None


def get_aur_helper():
    for helper in ("yay", "paru"):
        if shutil.which(helper):
            return helper
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
        logger.info("Snort already installed.")
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
            sys.exit(1)

        elif pm == "dnf":
            subprocess.run(["sudo", "dnf", "install", "-y", "snort"], check=True)

        elif pm == "pacman":
            aur = get_aur_helper()

            if not aur:
                print("❌ Arch detected but no AUR helper found.")
                print("👉 Install one of these first:")
                print("   sudo pacman -S --needed base-devel git")
                print("   git clone https://aur.archlinux.org/yay.git")
                print("   cd yay && makepkg -si")
                return

            print(f"[+] Installing Snort using AUR helper ({aur})...")
            try:
                subprocess.run(
                    [aur, "-S", "--noconfirm", "snort"],
                    check=True,
                )
            except subprocess.CalledProcessError as e:
                print("[!] snort not found, trying snort3-git...")
                subprocess.run([aur, "-S", "--noconfirm", "snort3-git"], check=True)
                return

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


if __name__ == "__main__":
    print(f"[=] Starting post installation...\n")

    install_snort()
