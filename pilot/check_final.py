import sqlite3

con = sqlite3.connect("db.sqlite3")
print("papers total:", con.execute("select count(*) from papers").fetchone()[0])
print("by status:", con.execute(
    "select fetch_status, count(*) from papers group by fetch_status").fetchall())
others = con.execute(
    "select arxiv_id, fetch_status from papers "
    "where fetch_status is null or fetch_status=''").fetchall()
print("null status:", others)
