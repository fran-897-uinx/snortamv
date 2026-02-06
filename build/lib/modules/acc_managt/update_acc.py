import json
from pathlib import Path

ACCOUNTS_FILE = "accounts.json"


def _accounts_path(root: Path) -> Path:
    return root / ACCOUNTS_FILE


def update_account(root: Path):
    p = _accounts_path(root)
    if not p.exists():
        print("No accounts file found")
        return
    data = json.loads(p.read_text())
    username = input("Enter username to update: ")
    if username not in data:
        print("User not found")
        return
    new_full = input("New full name (leave blank to keep): ")
    if new_full:
        data[username]["Fullname"] = new_full
        p.write_text(json.dumps(data, indent=2))
        print(f"Updated account: {username}")
    else:
        print("No changes made")
