#!/usr/bin/env python3
import os
import time
import pyfiglet
import shutil
import platform
import subprocess
import sys
import argparse
from pathlib import Path
from rich.console import Console

from modules.configuration.setup_rules import create_default_rules, interactive_add_rule
from modules.configuration.validate_conf import validate_configuration
from modules.acc_managt.creat_acc import create_account_cli
from modules.acc_managt.delete_acc import delete_account_cli
from modules.acc_managt.update_acc import update_account_cli
from modules.utilities.logger import get_logger

ROOT = Path(__file__).parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

console = Console()
OS_TYPE = platform.system().lower()
VERSION = "0.0.1"

logger = get_logger(__name__)

logger.info("SnortAMV started")
logger.debug("Detected OS: %s", OS_TYPE)
logger.warning("Snort not detected, skipping scan")
logger.error("Failed to parse rule file")

# ---------------- UI ----------------
def greeting_by_time():
    hour = int(time.strftime("%H"))
    if hour < 12:
        return "Good Morning"
    elif hour < 17:
        return "Good Afternoon"
    elif hour < 21:
        return "Good Evening"
    return "Good Night"


def banner():
    console.print(pyfiglet.figlet_format("SNORT AMV"), style="bold green")
    console.print(f"{greeting_by_time()} 👋", style="green")


# ---------------- Core ----------------
def check_snort():
    return shutil.which("snort") or shutil.which("snort3")


def setup_cmd(_):
    if not check_snort():
        console.print("[red]Snort not found[/red]")
        sys.exit(1)
    create_default_rules(ROOT)
    console.print("[green]Setup complete[/green]")


def run_cmd(_):
    if OS_TYPE == "linux":
        subprocess.run(["sudo", "bash", "snort_auto.bash"], check=True)
    elif OS_TYPE == "windows":
        subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", "snort.ps1"],
            check=True,
        )
    else:
        sys.exit("Unsupported OS")


def decrypt_cmd(_):
    if OS_TYPE == "linux":
        subprocess.run(["bash", "decrypt.bash"], check=True)
    elif OS_TYPE == "windows":
        subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", "decrypt.ps1"],
            check=True,
        )


def version_cmd(_):
    print(f"SnortAMV v{VERSION}")


# ---------------- CLI ----------------
def main():
    banner()

    parser = argparse.ArgumentParser(description="SnortAMV – Automated Snort Manager")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("setup", help="Run initial setup").set_defaults(func=setup_cmd)
    sub.add_parser("run", help="Runs the snort").set_defaults(func=run_cmd)
    sub.add_parser("decrypt", help="decrypt the snort to be readable").set_defaults(
        func=decrypt_cmd
    )
    sub.add_parser("validate", help="Validate the configuration").set_defaults(
        func=lambda _: validate_configuration(ROOT)
    )
    parser.add_argument(
    "--version",
    action="version",
    version=f"SnortAMV v{VERSION}",
)

    rule = sub.add_parser("rule", help="add an list out rules")
    rule_sub = rule.add_subparsers(dest="action", required=True)
    rule_sub.add_parser("add", help="Create a local rule interactively").set_defaults(
        func=lambda _: interactive_add_rule(ROOT)
    )
    rule_sub.add_parser("list", help="List local.rules").set_defaults(
        func=lambda _: print(open(ROOT / "rules/local.rules").read())
    )

    acc = sub.add_parser(
        "acc", help="Create, Delete and update project profile or users"
    )
    acc_sub = acc.add_subparsers(dest="action", required=True)
    acc_sub.add_parser("create", help="Create a project user").set_defaults(
        func=lambda _: create_account_cli(ROOT)
    )
    acc_sub.add_parser("delete", help="Delete a project user").set_defaults(
        func=lambda _: delete_account_cli(ROOT)
    )
    acc_sub.add_parser("update", help="Update a project user").set_defaults(
        func=lambda _: update_account_cli(ROOT)
    )

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
