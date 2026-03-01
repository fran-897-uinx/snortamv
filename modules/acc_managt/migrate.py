from pathlib import Path 
import database.db as db


def migrate_acc():
    print("account created ", db.migrate_from_json(Path.cwd())+1 )


migrate_acc()
if __name__ == "__main__":
    migrate_acc()
