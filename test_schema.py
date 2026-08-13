from database.db import fetch_all

rows = fetch_all("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""")

for row in rows:
    print(row["name"])

rows = fetch_all("""
SELECT name
FROM sqlite_master
WHERE type='index'
ORDER BY name
""")

for row in rows:
    print(row["name"])