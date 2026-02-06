"""Create and manage local.rules inside the project (simple rule format)."""

from pathlib import Path

DEFAULT_RULES = [
    "# Local rule format (demo)\n",
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
        src = input("Source (e.g. any): ")
        src_port = input("Source port (e.g. any): ")
        dst = input("Destination (e.g. any): ")
        dst_port = input("Destination port (e.g. any): ")
        msg = input("Message: ")
        sid = input("SID (unique integer): ")
        rule = f'alert {proto} {src} {src_port} -> {dst} {dst_port} (msg:"{msg}"; sid:{sid}; rev:1;)\n'
        with open(local_rules, "a") as f:
            f.write(rule)
        print(f"Rule added to {local_rules}")


def list_local_rules(root: Path):
    local_rules = root / "rules" / "local.rules"
    if not local_rules.exists():
        print("No local.rules found. Run `python main.py setup` to create defaults.")
        return
    print(local_rules.read_text())
