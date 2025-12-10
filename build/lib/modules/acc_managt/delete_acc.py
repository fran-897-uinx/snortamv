import json
from pathlib import Path

ACCOUNTS_FILE = "accounts.json"


def _accounts_path(root: Path) -> Path:
    return root / ACCOUNTS_FILE


def delete_account(root: Path):
    p = _accounts_path(root)
    if not p.exists():
        print("No accounts file found")
        return
    data = json.loads(p.read_text())
    username = input("Enter username to delete: ")
    if username not in data:
        print("User not found")
        return
    del data[username]
    p.write_text(json.dumps(data, indent=2))
    print(f"Deleted account: {username}")
