#!/usr/bin/env python3

## Entry point of the project

import os
import sys
import time
import pyfiglet
import shutil
from pathlib import Path
from rich.console import Console
import platform
import subprocess

ROOT = Path(__file__).parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from modules.configuration.setup_rules import create_default_rules
from modules.configuration.validate_conf import validate_configuration
from modules.acc_managt.creat_acc import create_account_cli
from modules.acc_managt.delete_acc import delete_account_cli
from modules.acc_managt.update_acc import update_account_cli

from activate import get_venv_python

console = Console()
os_type = platform.system().lower()


def Time():
    hour = int(time.strftime("%H"))
    if 12 <= hour < 17:
        print("Good Afternoon")
    elif 1 <= hour < 12:
        print("Good Morning")
    elif 17 <= hour < 21:
        print("Good Evening")
    else:
        print("Good Night")


def Greating():
    text = pyfiglet.figlet_format("SNORT { AMV }")
    for line in text.split("\n"):
        console.print(line, style="bold white")
        time.sleep(0.05)
    width = shutil.get_terminal_size().columns
    great = f"WE Welcome You To SNORT AUTOMATED VERSION".ljust(width, " ")
    for t in great:
        console.print(t, end=" ", style="blue")
        time.sleep(0.01)
    print("\n")


def check_snort():
    snort_path = shutil.which("snort") or shutil.which("snort3")
    if snort_path:
        print(f"[✓] Snort found at {snort_path}")
        return True
    print("[!] Snort not found. Please run post_installer.py first.")
    return False


def help():
    match os_type.lower():
        case "windows":
            print(
                """\n
        SnortAMV - Automated Snort Manager
        Usage:
            python main.py                    Show this help
            python main.py --version           Show version
            python main.py setup               Run initial setup
            python main.py rules add           Create a local rule interactively
            python main.py rules list          List local.rules
            python main.py config validate     Validate the configuration
            python main.py acc create          Create a project user
            python main.py acc delete          Delete a project user
            python main.py acc update          Update a project user
            python main.py run                 Runs the snort 
        """
            )
        case "linux":
            print(
                """\n
        SnortAMV - Automated Snort Manager
        Usage:
            python3 main.py                    Show this help
            python3 main.py --version           Show version
            python3 main.py setup               Run initial setup
            python3 main.py rules add           Create a local rule interactively
            python3 main.py rules list          List local.rules
            python3 main.py config validate     Validate the configuration
            python3 main.py acc create          Create a project user
            python3 main.py acc delete          Delete a project user
            python3 main.py acc update          Update a project user
            python3 main.py run                 Runs the snort 
        """
            )


def main():
    Time()

    if "--version" in sys.argv:
        print("snortAMV v1.0.0")
        return

    if len(sys.argv) < 2:
        Greating()
        help()
        return

    cmd = sys.argv[1]

    if cmd == "setup":
        print("Running setup checks...")
        if not check_snort():
            return
        create_default_rules(ROOT)
        print("Setup complete.")
    elif cmd == "run":
        os_type = platform.system().lower()

        if os_type == "windows":
            console.print(
                "Operating system has been detected as Windows", style="green"
            )
        subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", "snort.ps1"],
            check=True,
        )

        if os_type == "linux":
            console.print("Operating system has been detected as Linux", style="green")
            subprocess.run(["bash", "snort_auto.bash"], check=True)

        else:
            console.print(f"Unsupported operating system: {os_type}", style="red")

    elif cmd == "rules":
        if len(sys.argv) < 3:
            print("rules subcommands: add, list")
            return
        sub = sys.argv[2]
        if sub == "add":
            from modules.configuration.setup_rules import interactive_add_rule

            interactive_add_rule(ROOT)
        elif sub == "list":
            from modules.configuration.setup_rules import list_local_rules

            list_local_rules(ROOT)
        else:
            print("Unknown rules subcommand")

    elif cmd == "config":
        if len(sys.argv) < 3 or sys.argv[2] != "validate":
            print("config subcommands: validate")
            return
        validate_configuration(ROOT)

    elif cmd == "acc":
        if len(sys.argv) < 3:
            print("acc subcommands: create, delete, update")
            return
        sub = sys.argv[2]
        if sub == "create":
            create_account_cli(ROOT)
        elif sub == "delete":
            delete_account_cli(ROOT)
        elif sub == "update":
            update_account_cli(ROOT)
        else:
            print("Unknown acc subcommand")

    else:
        help()


if __name__ == "__main__":
    main()
