"""Contract checks. COURSE_IMPL=student selects the unfinished exercise modules."""
import hashlib
import importlib
import json
import os
from pathlib import Path
import sqlite3
import struct
import tempfile
import time
import unittest

IMPL = os.environ.get("COURSE_IMPL", "reference")
if IMPL not in {"reference", "student"}:
    raise RuntimeError("COURSE_IMPL must be reference or student")
def module(lesson):
    return importlib.import_module(f"python.{IMPL}.lab_{lesson}")

class Test171(unittest.TestCase):
    def setUp(self): self.m=module("17_1")
    def test_sum(self): self.assertEqual(self.m.run_child([2,3,5])["sum"],10)
    def test_pid(self): self.assertNotEqual(self.m.run_child([])["pid"],os.getpid())
    def test_empty(self): self.assertEqual(self.m.run_child([])["sum"],0)
    def test_range(self):
        for values in [[-1],[1001],[True],[2.0],["3"]]:
            with self.subTest(values=values), self.assertRaises(ValueError): self.m.run_child(values)
    def test_size(self):
        with self.assertRaises(ValueError): self.m.run_child([0]*257)
    def test_timeout_parameter(self):
        with self.assertRaises(ValueError): self.m.run_child([],0)
    def test_input_preserved(self):
        a=[1,2]; self.m.run_child(a); self.assertEqual(a,[1,2])

class Test172(unittest.TestCase):
    def setUp(self):
        self.m=module("17_2"); self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup); self.path=Path(self.tmp.name)/"asset.bin"
    def test_empty(self):
        self.path.write_bytes(b""); h=hashlib.sha256(b"").hexdigest(); self.assertEqual(self.m.file_digests(self.path),(h,h))
    def test_binary(self):
        data=bytes(range(256))*20;self.path.write_bytes(data);h=hashlib.sha256(data).hexdigest();self.assertEqual(self.m.file_digests(self.path),(h,h))
    def test_missing(self):
        with self.assertRaises(ValueError):self.m.file_digests(self.path)
    def test_directory(self):
        with self.assertRaises(ValueError):self.m.file_digests(self.path.parent)
    def test_large(self):
        self.path.write_bytes(b"x"*(1048576+1))
        with self.assertRaises(ValueError):self.m.file_digests(self.path)
    def test_unchanged(self):
        self.path.write_bytes(b"game");self.m.file_digests(self.path);self.assertEqual(self.path.read_bytes(),b"game")

class Test173(unittest.TestCase):
    def setUp(self):self.m=module("17_3")
    def test_empty(self):self.assertEqual(self.m.schedule_fcfs([]),[])
    def test_contention(self):
        r=self.m.schedule_fcfs([(0,12,100),(1,1,5)]);self.assertEqual(r[1],{"job":1,"start":12,"finish":13,"lateness":8})
    def test_idle_gap(self):self.assertEqual(self.m.schedule_fcfs([(7,2,9)])[0]["start"],7)
    def test_stable_ties(self):self.assertEqual([r["job"] for r in self.m.schedule_fcfs([(0,1,5)]*3)],[0,1,2])
    def test_order(self):self.assertEqual([r["job"] for r in self.m.schedule_fcfs([(5,1,9),(0,1,9)])],[1,0])
    def test_invalid(self):
        for jobs in [[(0,0,1)],[(0,1,-1)],[(0,True,5)],[(0,1)],[(0,1,5)]*129]:
            with self.subTest(jobs=jobs[:2]),self.assertRaises(ValueError):self.m.schedule_fcfs(jobs)

class Test174(unittest.TestCase):
    def setUp(self):
        self.m=module("17_4");self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.path=Path(self.tmp.name)/"save.json"
    def test_round_trip(self):
        self.m.write_save(self.path,{"version":1,"score":19});self.assertEqual(self.m.read_save(self.path),{"version":1,"score":19})
    def test_failure_before_commit(self):
        for point in ["before_write","partial_write","before_replace"]:
            with self.subTest(point=point):
                self.m.write_save(self.path,{"version":1,"score":7})
                with self.assertRaises(self.m.InjectedFailure):self.m.write_save(self.path,{"version":1,"score":99},point)
                self.assertEqual(self.m.read_save(self.path)["score"],7)
                self.assertEqual(len(list(self.path.parent.iterdir())),1)
    def test_failure_after_replace(self):
        with self.assertRaises(self.m.InjectedFailure):self.m.write_save(self.path,{"version":1,"score":99},"after_replace")
        self.assertEqual(self.m.read_save(self.path)["score"],99)
    def test_schema(self):
        for value in [{},{"version":2,"score":3},{"version":True,"score":3},{"version":1,"score":-1},{"version":1,"score":True},{"version":1,"score":2,"extra":0}]:
            with self.subTest(value=value),self.assertRaises(ValueError):self.m.validate_save(value)
    def test_truncated(self):
        self.path.write_bytes(b'{"version":1,')
        with self.assertRaises(ValueError):self.m.read_save(self.path)
    def test_oversize(self):
        self.path.write_bytes(b" "*1025)
        with self.assertRaises(ValueError):self.m.read_save(self.path)
    def test_invalid_does_not_replace(self):
        self.m.write_save(self.path,{"version":1,"score":3})
        with self.assertRaises(ValueError):self.m.write_save(self.path,{"version":1,"score":"bad"})
        self.assertEqual(self.m.read_save(self.path)["score"],3)

class FakeSocket:
    def __init__(self, chunks):self.chunks=list(chunks);self.timeouts=[]
    def settimeout(self,t):self.timeouts.append(t)
    def recv(self,n):
        if not self.chunks:return b""
        chunk=self.chunks.pop(0)
        if len(chunk)>n:self.chunks.insert(0,chunk[n:]);chunk=chunk[:n]
        return chunk

class Test191(unittest.TestCase):
    def setUp(self):self.m=module("19_1")
    def test_known_encoding(self):self.assertEqual(self.m.encode_frame(b"abc"),b"\0\0\0\3abc")
    def test_all_splits(self):
        wire=self.m.encode_frame(b"abc")+self.m.encode_frame(b"xyz")
        for k in range(len(wire)+1):
            decoder=self.m.FrameDecoder();self.assertEqual(decoder.feed(wire[:k])+decoder.feed(wire[k:]),[b"abc",b"xyz"]);decoder.finish()
    def test_byte_fragments(self):
        d=self.m.FrameDecoder();r=[]
        for b in self.m.encode_frame(b"hello"):r+=d.feed(bytes([b]))
        self.assertEqual(r,[b"hello"]);d.finish()
    def test_multiple_frames(self):
        d=self.m.FrameDecoder();self.assertEqual(d.feed(self.m.encode_frame(b"a")*10),[b"a"]*10)
    def test_boundary(self):
        d=self.m.FrameDecoder();body=b"a"*4096;self.assertEqual(d.feed(self.m.encode_frame(body)),[body])
    def test_bad_encode(self):
        for body in [b"",b"x"*4097,"text"]:
            with self.assertRaises(ValueError):self.m.encode_frame(body)
    def test_oversize_advertisement(self):
        d=self.m.FrameDecoder()
        with self.assertRaises(ValueError):d.feed(struct.pack("!I",0xffffffff))
        self.assertEqual(len(d.buffer),0)
        with self.assertRaises(ValueError):d.feed(b"a")
    def test_zero_size(self):
        with self.assertRaises(ValueError):self.m.FrameDecoder().feed(b"\0\0\0\0")
    def test_truncated(self):
        for wire in [b"\0",b"\0\0\0\3a"]:
            d=self.m.FrameDecoder();d.feed(wire)
            with self.assertRaises(ValueError):d.finish()
    def test_closed(self):
        d=self.m.FrameDecoder();d.finish()
        with self.assertRaises(ValueError):d.feed(b"x")
    def test_chunk_budget(self):
        with self.assertRaises(ValueError):self.m.FrameDecoder().feed(b"x"*8193)
    def test_exact_socket(self):
        s=FakeSocket([b"\0",b"\0\0\3ab",b"c"])
        self.assertEqual(self.m.recv_frame(s,time.monotonic()+1),b"abc")
        self.assertTrue(all(0<t<=1 for t in s.timeouts))
    def test_socket_eof(self):
        with self.assertRaises(EOFError):self.m.recv_frame(FakeSocket([b"\0"]),time.monotonic()+1)
    def test_deadline(self):
        with self.assertRaises(TimeoutError):self.m.recv_frame(FakeSocket([]),time.monotonic()-1)

class Test192(unittest.TestCase):
    def setUp(self):
        self.m=module("19_2");self.good={"version":1,"id":"job-1","operation":"sum_squares","values":[0,2,1000]}
    def raw(self,value=None):return json.dumps(self.good if value is None else value).encode()
    def test_good(self):self.assertEqual(self.m.parse_request(self.raw()),self.good)
    def test_canonical(self):
        other=dict(reversed(list(self.good.items())));self.assertEqual(self.m.canonical_request(other),self.m.canonical_request(self.good))
    def test_types(self):
        for v in [True,1.0,"1",None,-1,1001]:
            b=dict(self.good,values=[v])
            with self.subTest(v=v),self.assertRaises(ValueError):self.m.parse_request(self.raw(b))
    def test_version(self):
        for v in [True,2,1.0]:
            with self.assertRaises(ValueError):self.m.parse_request(self.raw(dict(self.good,version=v)))
    def test_fields(self):
        for b in [dict(self.good,other=1),{"version":1},[],None]:
            with self.assertRaises(ValueError):self.m.parse_request(json.dumps(b).encode())
    def test_duplicate(self):
        with self.assertRaises(ValueError):self.m.parse_request(b'{"version":1,"version":1}')
    def test_bad_encoding(self):
        for raw in [b"\xff",b"{",b"NaN",b"["*2000,b" "*4097,b""]:
            with self.subTest(raw=raw[:10]),self.assertRaises(ValueError):self.m.parse_request(raw)
    def test_id(self):
        for value in ["","x"*33,"../outside","a\nb","caf\u00e9",1]:
            with self.assertRaises(ValueError):self.m.parse_request(self.raw(dict(self.good,id=value)))
    def test_value_count(self):
        for values in [[],[0]*257,{}]:
            with self.assertRaises(ValueError):self.m.parse_request(self.raw(dict(self.good,values=values)))
    def test_max_values(self):self.assertEqual(len(self.m.parse_request(self.raw(dict(self.good,values=[1000]*256)))["values"]),256)
    def test_operation(self):
        with self.assertRaises(ValueError):self.m.parse_request(self.raw(dict(self.good,operation="exec")))

class Test193(unittest.TestCase):
    def setUp(self):self.m=module("19_3");self.db=self.m.connect_store();self.addCleanup(self.db.close)
    def test_seed(self):
        self.m.seed_inventory(self.db);self.assertEqual(self.db.execute("SELECT SUM(quantity) FROM inventory").fetchone()[0],23)
    def test_foreign_key_enabled(self):self.assertEqual(self.db.execute("PRAGMA foreign_keys").fetchone()[0],1)
    def test_invalid_reference(self):
        with self.assertRaises(sqlite3.IntegrityError):self.db.execute("INSERT INTO inventory VALUES (?,?,?)",("bad","ore",1))
    def test_negative(self):
        self.m.seed_inventory(self.db)
        with self.assertRaises(sqlite3.IntegrityError):self.db.execute("UPDATE inventory SET quantity=-1 WHERE player_id='A'")
    def test_unique(self):
        self.m.seed_inventory(self.db)
        with self.assertRaises(sqlite3.IntegrityError):self.db.execute("INSERT INTO inventory VALUES (?,?,?)",("A","ore",2))
    def test_text_as_data(self):
        name="x'); DROP TABLE players;--"
        self.db.execute("INSERT INTO players VALUES (?,?)",("C",name))
        self.assertEqual(self.db.execute("SELECT name FROM players WHERE id=?",("C",)).fetchone()[0],name)
    def test_atomic_seed_error(self):
        self.db.execute("INSERT INTO players VALUES (?,?)",("B","already there"))
        with self.assertRaises(sqlite3.IntegrityError):self.m.seed_inventory(self.db)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM players").fetchone()[0],1)

class Test194(unittest.TestCase):
    def setUp(self):
        self.m=module("19_4")
        from python.reference.lab_19_3 import connect_store,seed_inventory
        self.db=connect_store();self.addCleanup(self.db.close);seed_inventory(self.db)
    def qty(self):return self.db.execute("SELECT quantity FROM inventory ORDER BY player_id").fetchall()
    def call(self,**kw):return self.m.transfer(self.db,"op-1","A","B","ore",5,**kw)
    def test_transfer(self):self.assertEqual(self.call(),{"source_quantity":15,"destination_quantity":8});self.assertEqual(self.qty(),[(15,),(8,)])
    def test_replay(self):self.assertEqual(self.call(),self.call());self.assertEqual(self.qty(),[(15,),(8,)])
    def test_conflict(self):
        self.call()
        with self.assertRaises(ValueError):self.m.transfer(self.db,"op-1","A","B","ore",6)
        self.assertEqual(self.qty(),[(15,),(8,)])
    def test_rollback(self):
        for point in ["after_debit","before_commit"]:
            with self.assertRaises(RuntimeError):self.call(fail_at=point)
            self.assertEqual(self.qty(),[(20,),(3,)])
            self.assertEqual(self.db.execute("SELECT COUNT(*) FROM operations").fetchone()[0],0)
    def test_response_lost(self):
        with self.assertRaises(self.m.ResponseLost):self.call(fail_at="after_commit")
        self.assertEqual(self.call(),{"source_quantity":15,"destination_quantity":8})
        self.assertEqual(self.qty(),[(15,),(8,)])
    def test_invalid_quantity(self):
        for q in [0,-1,True,1.0,1000001]:
            with self.assertRaises(ValueError):self.m.transfer(self.db,"x","A","B","ore",q)
    def test_missing(self):
        with self.assertRaises(ValueError):self.m.transfer(self.db,"x","A","C","ore",1)
    def test_insufficient(self):
        with self.assertRaises(ValueError):self.m.transfer(self.db,"x","A","B","ore",21)
        self.assertEqual(self.qty(),[(20,),(3,)])
    def test_same_player(self):
        with self.assertRaises(ValueError):self.m.transfer(self.db,"x","A","A","ore",1)
    def test_creates_destination_item(self):
        self.db.execute("DELETE FROM inventory WHERE player_id='B'")
        self.assertEqual(self.call()["destination_quantity"],5)
    def test_history_limit(self):
        self.db.executemany("INSERT INTO operations VALUES (?,?,?)",[(str(i),"x","{}") for i in range(1024)])
        with self.assertRaises(ValueError):self.call()
        self.assertEqual(self.qty(),[(20,),(3,)])

if __name__=="__main__":unittest.main()
