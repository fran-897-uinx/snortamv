# database/db.py
import sqlite3
from pathlib import Path
import os
import hashlib
from typing import Optional, Dict, Any
import platform

OS_TYPE = platform.system().lower()
# Windows AppData path
if OS_TYPE == "windows":
    USERDIR = os.getlogin()
    LOCAL_APPDATA = f"C:\\Users\\{USERDIR}\\Desktop"
    APP_DIR = Path(LOCAL_APPDATA) / "SnortAMV"
    APP_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH = APP_DIR / "sqlite.db"
if OS_TYPE == "linux":
    LINUX_DIR = os.getcwd()
    LINUX_DB = f"{LINUX_DIR}/sqlite.db"

# ### Debug Message
# if OS_TYPE == "windows":
#     if os.path.exists(DB_PATH) == False:
#         open(DB_PATH, "x")
# else:
#     print("fILE ALREADY EXISTS")
# if OS_TYPE == "linux":
#     if os.path.exists(LINUX_DB) == False:
#         print("Creating DB")
#         open(LINUX_DB, "x")
# else:
#     print("fILE ALREADY EXISTS")
# ### end of Debug Message


# SQLite connection (use row factory for dict-like access)
def get_connection():
    if OS_TYPE == "windows":
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    if OS_TYPE == "linux":
        conn = sqlite3.connect(LINUX_DB)
        conn.row_factory = sqlite3.Row
        return conn


# Simple password hashing
def hash_password(plaintext: str) -> str:
    return hashlib.sha256(plaintext.encode("utf-8")).hexdigest()


# Initialize database and tables
def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            firstname TEXT,
            fullname TEXT,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );
        """
    )
    conn.commit()
    conn.close()


# Account CRUD operations
def create_account(
    username: str, firstname: str, fullname: str, password_hash: str
) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO accounts (username, firstname, fullname, password_hash) VALUES (?, ?, ?, ?)",
            (username, firstname, fullname, password_hash(password_hash)),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_account(username: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username,firstname, fullname, created_at FROM accounts WHERE username = ?",
        (username,),
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def verify_password(username: str, password: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM accounts WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return False
    return row["password_hash"] == hash_password(password_hash)


def update_account(
    username: str,
    new_fullname: Optional[str] = None,
    new_password: Optional[str] = None,
) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    # ensure user exists
    cur.execute("SELECT id FROM accounts WHERE username = ?", (username,))
    if not cur.fetchone():
        conn.close()
        return False
    if new_fullname and new_password:
        cur.execute(
            "UPDATE accounts SET fullname = ?, password_hash = ? WHERE username = ?",
            (new_fullname, hash_password(new_password), username),
        )
    elif new_fullname:
        cur.execute(
            "UPDATE accounts SET fullname = ? WHERE username = ?",
            (new_fullname, username),
        )
    elif new_password:
        cur.execute(
            "UPDATE accounts SET password_hash = ? WHERE username = ?",
            (hash_password(new_password), username),
        )
    else:
        conn.close()
        return False
    conn.commit()
    conn.close()
    return True


def delete_account(username: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM accounts WHERE username = ?", (username,))
    changed = cur.rowcount
    conn.commit()
    conn.close()
    return changed > 0


def list_accounts() -> list:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username,firstname, fullname, created_at FROM accounts ORDER BY id"
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# Migrate from legacy accounts.json (if exists in project root)
def migrate_from_json(project_root: Path) -> int:
    json_path = project_root / "accounts.json"
    if not json_path.exists():
        return 0
    import json

    count = 0
    with json_path.open() as f:
        data = json.load(f)
    for username, info in data.items():
        firstname = info.get("Firstname") or info.get("firstname") or ""
        fullname = info.get("Fullname") or info.get("fullname") or ""
        password = info.get("Password") or info.get("password") or ""
        if not username or not password:
            continue
        created = create_account(username, firstname, fullname, password)
        if created:
            count += 1
    # Optionally rename the old file so migration doesn't re-run
    try:
        json_path.rename(project_root / "accounts.json.migrated")
    except Exception:
        pass
    return count


# Initialize DB automatically on import
init_db()
