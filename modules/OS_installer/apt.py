from pathlib import Path
import subprocess, platform, sys, os, time, shutil,socket
from modules.utilities.logger import get_logger
from rich.console import Console
logger = get_logger(__name__)
console = Console()



def network_available(host="archive.ubuntu.com", port=80, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.create_connection((host, port))
        return True
    except OSError:
        return False

def snort_installed():
    return shutil.which("snort") is not None or shutil.which("snort3") is not None


def sudo_warm(dry_run=False):
    cmd = ["sudo", "-V"]
    if dry_run:
        console.print(f"[DRY-RUN] would run {' '.join(cmd)}", style="purple")
        logger.info("DRY-RUN %s", cmd)
        return
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info(f"{cmd} completed")
    except subprocess.CalledProcessError as e:
        logger.info(cmd, "result %s", e.stdout)
        logger.info(cmd, "error %s", e.stderr)
        logger.debug("Snort installation failed %s", e.stderr)
        logger.debug("Snort installation failed %s", e.stdout)


def sudo_cmd(cmd):
    """
    Prefix command with sudo if not already root
    """
    if os.geteuid() != 0:
        return ["sudo"] + cmd
    return cmd


### This function will update the ubuntu or debian
def apt_update(dry_run=False):
    console.print("Updating package index... .......", style="green")
    time.sleep(0.2)
    cmd = sudo_cmd(["apt", "update"])
    if dry_run:
        console.print(f"[DRY-RUN] would run  {' '.join(cmd)}", style="yellow")
        logger.info("DRY-RUN: %s", cmd)
        return

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info(f"{cmd} completed")
    except subprocess.CalledProcessError as e:
        logger.error("error occured with the updating of linux %s", e)
        logger.error("Error: %s", e.stderr, "\n")
        logger.debug("Snort installation failed %s", e.stderr)
        logger.debug("Snort installation failed %s", e.stdout)
        sys.exit(1)
        return
    time.sleep(0.3)


### This function will upgrade the ubuntu or debian
def apt_upgrade(dry_run=False):
    console.print(" Upgrading installed packages (apt upgrade) .......", style="green")
    time.sleep(0.2)
    cmd = sudo_cmd(["apt", "upgrade", "-y"])
    if dry_run:
        console.print(f"[DRY-RUN] Would run: {' '.join(cmd)}", style="yellow")
        logger.info("DRY-RUN: %s", cmd)
        return
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info("Apt Upgrade completed ")
    except subprocess.CalledProcessError as e:
        logger.error(" Apt error just  occured  %s", e)
        logger.error("Error: %s", e.stderr, "\n")
        logger.debug("Snort installation failed %s", e.stderr)
        logger.debug("Snort installation failed %s", e.stdout)
        sys.exit(1)
        return
    time.sleep(0.3)


# This function will install dependeces to run to install snort
def install_dependences(dry_run=False):
    deps = [
        "build-essential",
        "libpcap-dev",
        "libpcre3-dev",
        "libdumbnet-dev",
        "zlib1g-dev",
        "wget",
        "curl",
    ]
    cmd = sudo_cmd(["apt", "install", "-y"] + deps)
    if dry_run:
        console.print(f"[DRY-RUN] Would run: {' '.join(cmd)}", style="yellow")
        logger.info("[DRY-RUN]: %s", cmd)
        return
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info("Dependeces installation has been compeleted")
    except subprocess.CalledProcessError as e:
        logger.error(
            "installtion failed please you have enough network and Data %s", e.stderr
        )
        logger.debug("Snort installation failed %s", e.stderr)
        logger.debug("Snort installation failed %s", e.stdout)
        sys.exit(1)
        return


### This function will install snort
def install_snort(dry_run=False):
    console.print(f"\n[Process] Checking if Snort is installed...", style="yellow")
    time.sleep(0.5)
    if snort_installed():
        logger.info("Snort already installed.")
        return
    console.print(
        f"[Not Found] Snort not found. Installing Snort now...\n", style="red"
    )
    cmd = sudo_cmd(["apt", "install", "-y", "snort"])
    if dry_run:
        console.print(f"[DRY-RUN] would run: {' '.join(cmd)}", style="yellow")
        logger.info("[DRY-RUN]: %s", cmd)
        return
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info("Snort installation completed")
    except subprocess.CalledProcessError as e:
        logger.info("Snort installation failed %s", e.stderr)
        logger.debug("Snort installation failed %s", e.stderr)
        logger.debug("Snort installation failed %s", e.stdout)
        sys.exit(1)
        return


def install_ubuntu_debian(dry_run=False):
    sudo_warm(dry_run=dry_run)
    if not network_available():
        console.print(
        "[bold red]❌ Network check failed.[/bold red]\n"
        "Please ensure you have a working internet connection.",
        style="red",
    )
        return

    console.print(
        "[yellow]⚠️ Network detected. Ensure stable connectivity before proceeding.[/yellow]"
    )

    time.sleep(0.8)

    confirm = input("Type confirm to continue or quit: ").strip().lower()
    if confirm != "confirm":
        console.print("Installation aborted.")
        return
    else:
        console.print(
            "[bold cyan]Starting SnortAMV installation for Ubuntu/Debian[/bold cyan]"
        )
        console.print("📦 updating packages...", style="green")
        apt_update(dry_run=dry_run)

        console.print("📦 upgrading packages...", style="green")
        apt_upgrade(dry_run=dry_run)

        console.print("📦 Installing dependencies...", style="green")
        install_dependences(dry_run=dry_run)

        console.print("🔗 Installing Snort...", style="green")
        install_snort(dry_run=dry_run)

        console.print("[bold green]✅ Installation completed successfully[/bold green]")


if __name__ == "__main__":
    print(f"[=] Starting apt installation...\n")
    install_ubuntu_debian()
