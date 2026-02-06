import os
import platform
import subprocess
import sys
import shutil
import activenv


VENV = "env"


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

    print("\n[=] Checking if Snort is installed...")

    if snort_installed():
        print("[✓] Snort already installed. Skipping installation.\n")
        return

    print("[+] Snort not found. Installing Snort 3...\n")

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
        print("[+] Installing Snort 3 for Linux...")
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "snort"], check=True)

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

    print("\n[✓] Snort 3 installation completed.\n")


# ---------------------------------------
#   CREATE VIRTUAL ENVIRONMENT
# ---------------------------------------
def create_venv():
    if not os.path.exists(VENV):
        print("[+] Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", VENV], check=True)
    else:
        print("[✓] Virtual environment already exists.")


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
        print("[✓] All requirements already installed.")
        return

    print(f"[+] Installing missing packages: {missing}")
    subprocess.run([venv_python, "-m", "pip", "install", *missing], check=True)
    print("[✓] Done installing requirements.\n")


# -------------------------------------
#         ACTIVATING THE VENV
# ----------------------------------------
def actvenv(venv_python):
    if not os.path.exists("activenv.py"):
        print(
            "Please go to the README.MD the see \n how to activate the Virtual environment"
        )
        return
    print("[+] Activating virtual Environment")
    subprocess.run([venv_python, "activenv.py"])


# ---------------------------------------
#   RUN APPLICATION INSIDE VENV
# ---------------------------------------
def run_app(venv_python):
    if not os.path.exists("main.py"):
        print("❌ ERROR: main.py not found.")
        return

    print("[+] Launching SnortAMV inside activated venv...\n")
    subprocess.run([venv_python, "main.py"])


# ---------------------------------------
#               MAIN
# ---------------------------------------
if __name__ == "__main__":
    print("[=] Starting post installation...\n")

    install_snort()  # FIRST → install snort
    create_venv()  # THEN create env
    venv_python = get_venv_python()  # get python inside env
    actvenv(venv_python) # activate venv 
    install_requirements(venv_python)  # install packages
    run_app(venv_python)  # run your tool
