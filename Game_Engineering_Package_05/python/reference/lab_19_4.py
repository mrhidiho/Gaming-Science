"""Atomic transfer plus same-ID/same-payload replay inside one SQLite database."""
import json
import re
import sqlite3

class ResponseLost(RuntimeError):
    pass

def transfer(db: sqlite3.Connection, operation_id: str, source: str,
             destination: str, item: str, quantity: int,
             fail_at: str | None = None) -> dict:
    for value in (operation_id, source, destination, item):
        if type(value) is not str or not re.fullmatch(r"[A-Za-z0-9_-]{1,32}", value, re.ASCII):
            raise ValueError("invalid identifier")
    if source == destination or type(quantity) is not int or not 1 <= quantity <= 1000000:
        raise ValueError("distinct players and positive bounded quantity required")
    if fail_at not in {None, "after_debit", "before_commit", "after_commit"}:
        raise ValueError("unknown failure point")
    payload = json.dumps([source,destination,item,quantity],separators=(",",":"))
    db.execute("BEGIN IMMEDIATE")
    try:
        old = db.execute("SELECT payload,response FROM operations WHERE id=?",(operation_id,)).fetchone()
        if old:
            if old[0] != payload:
                raise ValueError("request ID was reused with different work")
            result = json.loads(old[1])
            db.execute("COMMIT")
            return result
        if db.execute("SELECT COUNT(*) FROM operations").fetchone()[0] >= 1024:
            raise ValueError("operation history full; do not silently evict replay protection")
        for player in (source,destination):
            if not db.execute("SELECT 1 FROM players WHERE id=?",(player,)).fetchone():
                raise ValueError("unknown player")
        row = db.execute("SELECT quantity FROM inventory WHERE player_id=? AND item_id=?",(source,item)).fetchone()
        source_before = row[0] if row else 0
        row = db.execute("SELECT quantity FROM inventory WHERE player_id=? AND item_id=?",(destination,item)).fetchone()
        destination_before = row[0] if row else 0
        if source_before < quantity or destination_before + quantity > 1000000:
            raise ValueError("insufficient source quantity or destination capacity")
        db.execute("UPDATE inventory SET quantity=quantity-? WHERE player_id=? AND item_id=?",(quantity,source,item))
        if fail_at == "after_debit":
            raise RuntimeError("injected failure after debit")
        db.execute("INSERT INTO inventory VALUES (?,?,?) ON CONFLICT(player_id,item_id) DO UPDATE SET quantity=excluded.quantity",
                   (destination,item,destination_before+quantity))
        result = {"source_quantity":source_before-quantity,"destination_quantity":destination_before+quantity}
        db.execute("INSERT INTO operations VALUES (?,?,?)",(operation_id,payload,json.dumps(result,sort_keys=True)))
        if fail_at == "before_commit":
            raise RuntimeError("injected failure before commit")
        db.execute("COMMIT")
    except BaseException:
        if db.in_transaction:
            db.execute("ROLLBACK")
        raise
    if fail_at == "after_commit":
        raise ResponseLost("commit succeeded but response was lost; retry same ID and payload")
    return result
