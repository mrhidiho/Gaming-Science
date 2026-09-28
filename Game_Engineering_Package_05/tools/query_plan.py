"""Bounded in-memory SQLite query-plan experiment; generated data only."""
import json
import sqlite3

def experiment():
    db=sqlite3.connect(":memory:")
    try:
        db.execute("CREATE TABLE sample (player_id INTEGER NOT NULL,item_id TEXT NOT NULL,quantity INTEGER NOT NULL,PRIMARY KEY(player_id,item_id))")
        db.executemany("INSERT INTO sample VALUES (?,?,?)",[(i,"rare" if i%97==0 else "common",i%20) for i in range(5000)])
        query="SELECT player_id,quantity FROM sample WHERE item_id=? ORDER BY player_id"
        before=db.execute("EXPLAIN QUERY PLAN "+query,("rare",)).fetchall()
        rows_before=db.execute(query,("rare",)).fetchall()
        db.execute("CREATE INDEX sample_item ON sample(item_id)")
        after=db.execute("EXPLAIN QUERY PLAN "+query,("rare",)).fetchall()
        rows_after=db.execute(query,("rare",)).fetchall()
        if rows_before!=rows_after:raise RuntimeError("index changed query result")
        return {"sqlite_runtime":sqlite3.sqlite_version,"fixture_rows":5000,"returned_rows":len(rows_after),"before":before,"after":after,
                "note":"Generated fixture; plans are observed for this SQLite version, not PostgreSQL or every dataset."}
    finally:db.close()
if __name__=="__main__":print(json.dumps(experiment(),indent=2))
