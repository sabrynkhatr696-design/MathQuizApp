import sqlite3

# فتح الاتصال بقاعدة البيانات (global.db موجود في مجلد MathApp)
conn = sqlite3.connect("global.db")
cursor = conn.cursor()

# 1️⃣ جدول المستخدمين
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    pwd TEXT NOT NULL
)
""")

# 2️⃣ جدول الأسئلة
cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    level TEXT NOT NULL
)
""")

# 3️⃣ جدول النتائج
cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

# حفظ التغييرات وإغلاق الاتصال
conn.commit()
cursor.close()
conn.close()

print("All tables are ready in global.db ✅")