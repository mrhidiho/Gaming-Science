from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from python.reference.lab_19_3 import connect_store,seed_inventory
from python.reference.lab_19_4 import transfer,ResponseLost
db=connect_store()
try:
    seed_inventory(db)
    try:
        transfer(db,"op1","A","B","ore",5,"after_commit")
    except ResponseLost:
        print("reply lost; retry same request")
    print(transfer(db,"op1","A","B","ore",5))
    print("total=",db.execute("SELECT SUM(quantity) FROM inventory").fetchone()[0],sep="")
finally:
    db.close()
