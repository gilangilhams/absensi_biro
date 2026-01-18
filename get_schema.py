import sqlite3

conn = sqlite3.connect('absensi_biro.db')
cursor = conn.cursor()

# Get all table schemas
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

for table in tables:
    print(table[0])
    print("---")

conn.close()
