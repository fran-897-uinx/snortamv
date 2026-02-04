# modules/acc_managt/create_acc.py
from pathlib import Path
from database.db import create_account, get_account

def create_account_cli(root: Path):
    username = input("Enter username: ").strip()
    if get_account(username):
        print("User already exists")
        return
    fullname = input("Full name: ").strip()
    password = input("Password: ").strip()
    ok = create_account(username, fullname, password)
    if ok:
        print(f"Created account: {username}")
    else:
        print("Failed to create account (maybe user exists).")
    return ok
