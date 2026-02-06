import os
import platform
import subprocess
import sys

VENV = "env"


def create_venv():
    if not os.path.exists(VENV):
        print(f"[+] Creating environment... ")
        subprocess.run([sys.executable, "-m", "venv", VENV], check=True)
    else:
        print("[+] Environment already exists.")


def get_venv_python():
    os_type = platform.system().lower()

    if os_type == "windows":
        return os.path.join(VENV, "Scripts", "python.exe")
    else:
        return os.path.join(VENV, "bin", "python")

def install_requirements(venv_python):
    if not os.path.exists("requirements.txt"):
        print("[!] No requirements.txt found. Skipping...")
        return

    print("[+] Checking installed packages...")

    # Get installed packages inside venv
    result = subprocess.run(
        [venv_python, "-m", "pip", "freeze"],
        capture_output=True,
        text=True
    )

    installed_packages = {
        line.split("==")[0].lower(): line.split("==")[1]
        for line in result.stdout.splitlines()
        if "==" in line
    }

    # Read required packages
    with open("requirements.txt", "r") as f:
        required_lines = [line.strip() for line in f if line.strip()]

    missing = []

    for line in required_lines:
        package = line.split("==")[0].lower()
        if package not in installed_packages:
            missing.append(line)

    if not missing:
        print("[✓] All dependencies already installed!")
        return

    print(f"[+] Installing {len(missing)} missing packages...")
    subprocess.run(
        [venv_python, "-m", "pip", "install", *missing],
        check=True
    )
    print("[✓] Requirements updated.")


def run_app(venv_python):
    print("\n[+] Launching SnortAMV...\n")

    if not os.path.exists("main.py"):
        print("❌ ERROR: main.py not found!")
        return

    subprocess.run([venv_python, "main.py"])


def show_manual_activation():
    os_type = platform.system().lower()
    print("\n[!] If you want to activate environment manually:")

    if os_type == "windows":
        print("    env\\Scripts\\activate")
    else:
        print("    source env/bin/activate")

    print()


if __name__ == "__main__":
    print("[=] Detecting OS and preparing environment...\n")

    create_venv()
    venv_python = get_venv_python()
    install_requirements(venv_python)
    show_manual_activation()
    run_app(venv_python)
