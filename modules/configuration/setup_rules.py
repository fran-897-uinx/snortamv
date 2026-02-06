"""Create and manage local.rules inside the project (simple rule format)."""

from pathlib import Path
import rich
from rich.console import Console

console = Console()

DEFAULT_RULES = [
    'alert icmp any any -> any any (msg:"ICMP detected"; sid:1000001; rev:1;)\n',
]


def create_default_rules(root: Path):
    rules_dir = root / "rules"
    rules_dir.mkdir(exist_ok=True)
    local_rules = rules_dir / "local.rules"
    if not local_rules.exists():
        local_rules.write_text("".join(DEFAULT_RULES))
        print(f"Created default local.rules at {local_rules}")
    else:
        print("local.rules already exists")


def interactive_add_rule(root: Path):
    rules_dir = root / "rules"
    rules_dir.mkdir(exist_ok=True)

    local_rules = rules_dir / "local.rules"

    # Create file with default rules only once
    if not local_rules.exists():
        local_rules.write_text("".join(DEFAULT_RULES))
        print("local.rules created with default rules.")

    # Show existing rules
    print("\nCurrent rules:\n")
    console.print(local_rules.read_text(), style="green")

    print("\nAdd a simple alert rule (demo)")

    # --- User input ---
    proto = input("Protocol (tcp/udp/icmp/ip): ").strip().lower()
    if proto not in {"tcp", "udp", "icmp", "ip"}:
        print("Invalid protocol.")
        return

    src = input("Source (e.g. 192.168.0.2 or any): ").strip()
    src_port = input("Source port (e.g. 80 or any): ").strip()
    dst = input("Destination (e.g. 192.168.0.10 or any): ").strip()
    dst_port = input("Destination port (e.g. 443 or any): ").strip()
    msg = input("Message: ").strip()

    try:
        sid = int(input("SID (unique integer): "))
        rev = int(input("Rev (integer): "))
    except ValueError:
        print("SID and Rev must be integers.")
        return

    # --- Build rule ---
    rule = (
        f"alert {proto} {src} {src_port} -> {dst} {dst_port} "
        f'(msg:"{msg}"; sid:{sid}; rev:{rev};)\n'
    )

    # Append rule safely
    with open(local_rules, "a") as f:
        f.write(rule)

    print(f"\nRule successfully added to {local_rules}")


def list_local_rules(root: Path):
    local_rules = root / "rules" / "local.rules"
    if not local_rules.exists():
        print("No local.rules found. Run `python main.py setup` to create defaults.")
        return
    print(local_rules.read_text())
