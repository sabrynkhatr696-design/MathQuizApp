import sqlite3
from datetime import datetime
import random

# فتح الاتصال بقاعدة البيانات
conn = sqlite3.connect("global.db")
cursor = conn.cursor()

# ==========================
# 1️⃣ تسجيل المستخدم / تسجيل الدخول
# ==========================
def register_user():
    username = input("Enter your username: ").strip().lower()
    password = input("Enter your password (min 6 chars): ").strip()

    if len(password) < 6:
        print("Password must be at least 6 characters!")
        return None

    cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
    if cursor.fetchone()[0] >= 1:
        print("This username is already taken! Try another one.")
        return None
    else:
        cursor.execute("INSERT INTO users (username, pwd) VALUES (?, ?)", (username, password))
        conn.commit()
        print(f"User '{username}' registered successfully ✅")
        return cursor.lastrowid

def login_user():
    username = input("Enter your username: ").strip().lower()
    password = input("Enter your password: ").strip()
    cursor.execute("SELECT id FROM users WHERE username = ? AND pwd = ?", (username, password))
    result = cursor.fetchone()
    if result:
        print(f"Welcome back, {username}!")
        return result[0]
    else:
        print("Incorrect username or password!")
        return None

# ==========================
# 2️⃣ إضافة أسئلة (للمعلم أو المطور)
# ==========================
def add_question():
    question = input("Enter the question: ").strip()
    answer = input("Enter the correct answer: ").strip()
    level = input("Enter difficulty level (easy/medium/hard): ").lower().strip()
    if level not in ["easy", "medium", "hard"]:
        print("Invalid level! Please enter: easy, medium, or hard.")
        return

    cursor.execute("INSERT INTO questions (question, answer, level) VALUES (?, ?, ?)", (question, answer, level))
    conn.commit()
    print("Question added successfully ✅")

# ==========================
# 3️⃣ بدء الاختبار
# ==========================
def start_quiz(user_id):
    level = input("Choose difficulty level (easy/medium/hard): ").lower().strip()
    if level not in ["easy", "medium", "hard"]:
        print("Invalid level! Please choose easy, medium, or hard.")
        return

    cursor.execute("SELECT id, question, answer FROM questions WHERE level = ?", (level,))
    questions = cursor.fetchall()
    if not questions:
        print(f"No questions available for level '{level}'")
        return

    random.shuffle(questions)
    score = 0
    for q in questions:
        print("\nQuestion:", q[1])
        ans = input("Your answer: ").strip()
        if ans.lower() == q[2].lower():
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Wrong! Correct answer: {q[2]}")

    print(f"\nQuiz finished! Your score: {score}/{len(questions)}")

    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO scores (user_id, score, date) VALUES (?, ?, ?)", (user_id, score, today))
    conn.commit()
    print("Your score has been saved in the database ✅")

# ==========================
# 4️⃣ القائمة الرئيسية
# ==========================
def main():
    print("Welcome to Math Quiz App 🎯")
    while True:
        print("\nMenu:")
        print("1. Register")
        print("2. Login")
        print("3. Add Question (Admin)")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            register_user()
        elif choice == "2":
            user_id = login_user()
            if user_id:
                start_quiz(user_id)
        elif choice == "3":
            add_question()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please select 1-4 only.")

if __name__ == "__main__":
    try:
        main()
    finally:
        cursor.close()
        conn.close()
