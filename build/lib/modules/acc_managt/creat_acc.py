"""Simple demo account creation. Stores accounts in a JSON file inside project
root."""

import json
from pathlib import Path

ACCOUNTS_FILE = "accounts.json"


def _accounts_path(root: Path) -> Path:
    return root / ACCOUNTS_FILE


# def create_account(root: Path):
#     p = _accounts_path(root)
#     if not p.exists():
#         p.write_text("{}")
#     data = json.loads(p.read_text())
#     username = input("Enter username: ")
#     if username in data:
#         print("User already exists")
#         return

# data = {}
# username =input("User name")
# fullname = input("Full name: ")
# data[username] = {"fullname": fullname}
# p.write_text(json.dumps(data, indent=2))
# print(f"Created account: {username}")

data = {}


def create_account(root: Path):
    p = _accounts_path(root)
    if not p.exists():
        username = input(
            "Username (it is a one time creation ))",
        )
        Fullname = input(
            "Fullname ",
        )
        Password = input("Enter your pin or password: ")
        data[username] = {"Fullname": Fullname, "Password": Password}
        p.write_text(json.dumps(data, indent=2))
        print(f"Account Has Been created \n Welcome {username}")
    else:
        check = json.loads(p.read_text())
        CheckUser = input("Enter your Password to See your details: ")
        if CheckUser in check:
            print(f"welcome {check[username]["Fullname"]}")
            print(check)
