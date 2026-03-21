import sqlite3

conn = sqlite3.connect("global.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    pwd TEXT NOT NULL
)
""")

name = input("What is your name: ").lower().strip()
password = input("What is your password: ")

cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (name,))
count = cursor.fetchone()[0]

if count >= 1:
    print("this username is already taken")
else:
    cursor.execute("INSERT INTO users(username, pwd) VALUES(?, ?)", (name, password))
    conn.commit()
    print("Inserted successfully")

cursor.close()
conn.close()