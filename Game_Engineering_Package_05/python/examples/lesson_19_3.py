from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from python.reference.lab_19_3 import connect_store,seed_inventory
import sqlite3

db=connect_store()
try:
    seed_inventory(db)
    print(db.execute("SELECT player_id,quantity FROM inventory ORDER BY player_id").fetchall())
    try:
        db.execute("INSERT INTO inventory VALUES (?,?,?)",("missing","ore",1))
    except sqlite3.IntegrityError:
        print("foreign key rejected")
finally:
    db.close()
