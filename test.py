import sqlite3
import re

def match(expr, item):
        return re.match(expr, item) is not None

conn = sqlite3.connect('films_info.db')
conn.create_function("MATCHES", 2, match)

cur = conn.cursor()

cursor.execute("SELECT MATCHES('^b', 'busy');")

print(cur.fetchall())
