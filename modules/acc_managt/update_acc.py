# modules/acc_managt/update_acc.py
from pathlib import Path
from database.db import update_account, get_account, verify_password

def update_account_cli(root: Path):
    username = input("Enter username to update: ").strip()
    acc = get_account(username)
    if not acc:
        print("User not found")
        return
    password = input("Enter your password to confirm: ").strip()
    if not verify_password(username, password):
        print("Incorrect password.")
        return

    new_full = input("New full name (leave blank to keep): ").strip()
    new_pass = input("New password (leave blank to keep): ").strip()

    if not new_full and not new_pass:
        print("No changes made")
        return

    ok = update_account(username, new_fullname=new_full or None, new_password=new_pass or None)
    if ok:
        print(f"Updated account: {username}")
    else:
        print("Failed to update account")
