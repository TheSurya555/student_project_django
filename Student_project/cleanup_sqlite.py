import sqlite3

conn = sqlite3.connect('db.sqlite3')
conn.execute("VACUUM")
conn.close()
