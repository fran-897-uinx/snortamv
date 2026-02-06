from pathlib import Path 
import database.db as db 

print("miragted", db.migrate_from_json(Path.cwd()))