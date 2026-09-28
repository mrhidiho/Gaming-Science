-- Optional PostgreSQL companion. Run only in your own disposable local database.
-- NOT executed in the package validation environment. No SQLite PRAGMAs here.
BEGIN;
CREATE TEMP TABLE course_players (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL
);
CREATE TEMP TABLE course_inventory (
  player_id TEXT REFERENCES course_players(id),
  item_id TEXT NOT NULL,
  quantity BIGINT NOT NULL CHECK (quantity BETWEEN 0 AND 1000000),
  PRIMARY KEY (player_id,item_id)
);
INSERT INTO course_players VALUES ('A','Ada'),('B','Bo');
INSERT INTO course_inventory VALUES ('A','ore',20),('B','ore',3);
SAVEPOINT before_transfer;
UPDATE course_inventory SET quantity=quantity-5 WHERE player_id='A' AND item_id='ore';
UPDATE course_inventory SET quantity=quantity+5 WHERE player_id='B' AND item_id='ore';
SELECT SUM(quantity) AS conserved_total FROM course_inventory;
ROLLBACK TO SAVEPOINT before_transfer;
SELECT * FROM course_inventory ORDER BY player_id;
EXPLAIN SELECT quantity FROM course_inventory WHERE player_id='A' AND item_id='ore';
ROLLBACK;
-- Use parameterized statements through the selected client driver in an application.
-- Inspect the server's isolation/constraint behavior; do not infer it from SQLite tests.
