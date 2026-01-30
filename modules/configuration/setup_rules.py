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
    if not local_rules.exists():
        local_rules.write_text("".join(DEFAULT_RULES))
        print("Add a simple alert rule (demo)")
        proto = input("Protocol (tcp/udp/icmp): ")
        src = input("Source (e.g.192.168.0.2/any): ")
        src_port = input("Source port (e.g.192.168.0.2/any): ")
        dst = input("Destination (e.g.192.168.0.2/any): ")
        dst_port = input("Destination port (e.g.192.168.0.2/any): ")
        msg = input("Message: ")
        sid = input("SID (unique integer): ")
        rev = input("rev(integer): ")
        rule = f'alert {proto} {src} {src_port} -> {dst} {dst_port} (msg:"{msg}"; sid:{sid}; rev:{rev};)\n'
        with open(local_rules, "a") as f:
            f.write(rule)
        print(f"Rule added to {local_rules}")
    else:
        print("Available Status")
        console.print(local_rules.read_text(), style="green")
        print(
            "You will be add to the Availble Rule: \n  Follow the instructions below Thanks"
        )
        local_rules.write_text("".join(DEFAULT_RULES))
        print("Add a simple alert rule (demo)")
        proto = input("Protocol (tcp/udp/icmp): ")
        src = input("Source (e.g.192.168.0.2/any): ")
        src_port = input("Source port (e.g.192.168.0.2/any): ")
        dst = input("Destination (e.g.192.168.0.2/any): ")
        dst_port = input("Destination port (e.g.192.168.0.2/any): ")
        msg = input("Message: ")
        sid = input("SID (unique integer): ")
        rev = input("rev(integer): ")
        rule = f'alert {proto} {src} {src_port} -> {dst} {dst_port} (msg:"{msg}"; sid:{sid}; rev:{rev};)\n'
        with open(local_rules, "a") as f:
            f.write(rule)


def list_local_rules(root: Path):
    local_rules = root / "rules" / "local.rules"
    if not local_rules.exists():
        print("No local.rules found. Run `python main.py setup` to create defaults.")
        return
    print(local_rules.read_text())
