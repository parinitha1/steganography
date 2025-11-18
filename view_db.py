import sqlite3

# Connect to the same database used in your Flask app
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Show all tables
print("\n=== Tables in Database ===")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

# Show all users
print("\n=== Users Table Data ===")
cursor.execute("SELECT * FROM users;")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
