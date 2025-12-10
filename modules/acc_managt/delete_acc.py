# modules/acc_managt/delete_acc.py
from pathlib import Path
from database.db import delete_account, get_account, verify_password

def delete_account_cli(root: Path):
    username = input("Enter username to delete: ").strip()
    acc = get_account(username)
    if not acc:
        print("User not found")
        return
    password = input("Enter your password to confirm deletion: ").strip()
    if not verify_password(username, password):
        print("Incorrect password")
        return
    ok = delete_account(username)
    if ok:
        print(f"Deleted account: {username}")
    else:
        print("Failed to delete account")
    return ok