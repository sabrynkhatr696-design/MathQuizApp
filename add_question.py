import sqlite3

# فتح الاتصال بقاعدة البيانات
conn = sqlite3.connect("global.db")
cursor = conn.cursor()

# قائمة الأسئلة
questions = [
    # Easy
    ("2 + 3 = ?", "5", "easy"),
    ("5 - 2 = ?", "3", "easy"),
    ("4 * 2 = ?", "8", "easy"),
    ("10 / 2 = ?", "5", "easy"),

    # Medium
    ("12 + 15 = ?", "27", "medium"),
    ("20 - 7 = ?", "13", "medium"),
    ("6 * 7 = ?", "42", "medium"),
    ("36 / 6 = ?", "6", "medium"),

    # Hard
    ("(5 + 3) * 2 = ?", "16", "hard"),
    ("(12 - 4) / 2 + 6 = ?", "10", "hard"),
    ("3^3 = ?", "27", "hard"),
    ("sqrt(49) + 5 = ?", "12", "hard")
]

# إضافة الأسئلة للجدول
for q in questions:
    cursor.execute("INSERT INTO questions (question, answer, level) VALUES (?, ?, ?)", q)

conn.commit()
cursor.close()
conn.close()

print("Questions added successfully ✅")