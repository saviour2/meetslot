import sqlite3
import json

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
res = {}
for (t,) in cur.fetchall():
    if t.startswith('sqlite_'): continue
    data = cur.execute(f"SELECT * FROM {t}").fetchall()
    if data:
        res[t] = data

print(json.dumps(res, indent=2))
