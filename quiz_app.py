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

    # تحقق من طول كلمة المرور
    if len(password) < 6:
        print("Password must be at least 6 characters!")
        return None

    # تحقق من وجود المستخدم
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
        return result[0]  # user_id
    else:
        print("Incorrect username or password!")
        return None


# ==========================
# 2️⃣ إضافة أسئلة (للمعلم أو المطور)
# ==========================
def add_question():
    question = input("Enter the question: ").strip()
    answer = input("Enter the correct answer: ").strip()

    # التحقق من مستوى الصعوبة
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

    # حفظ النتيجة في جدول scores
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
    #  نفس الكود بس عليه شرح بالعربي
    # import sqlite3  # استيراد مكتبة للتعامل مع قواعد بيانات SQLite
    # from datetime import datetime  # استيراد مكتبة للتعامل مع التاريخ والوقت
    # import random  # استيراد مكتبة لتوليد أرقام عشوائية (لخلط الأسئلة)
    #
    # # فتح الاتصال بقاعدة البيانات (أو إنشاؤها إذا مش موجودة)
    # conn = sqlite3.connect("global.db")
    # cursor = conn.cursor()  # إنشاء مؤشر للتعامل مع قاعدة البيانات
    #
    #
    # # ==========================
    # # 1️⃣ تسجيل المستخدم / تسجيل الدخول
    # # ==========================
    # def register_user():
    #     username = input("Enter your username: ").strip().lower()  # إدخال اسم المستخدم وتحويله لحروف صغيرة
    #     password = input("Enter your password: ").strip()  # إدخال كلمة المرور
    #
    #     # تحقق من وجود المستخدم مسبقًا
    #     cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
    #     if cursor.fetchone()[0] >= 1:  # إذا موجود بالفعل
    #         print("This username is already taken! Try another one.")
    #         return None
    #     else:
    #         # إدخال المستخدم الجديد في جدول users
    #         cursor.execute("INSERT INTO users (username, pwd) VALUES (?, ?)", (username, password))
    #         conn.commit()  # حفظ التغييرات في قاعدة البيانات
    #         print(f"User '{username}' registered successfully ✅")
    #         return cursor.lastrowid  # إرجاع رقم المستخدم الجديد (id)

    #
    # def login_user():
    #     username = input("Enter your username: ").strip().lower()  # إدخال اسم المستخدم
    #     password = input("Enter your password: ").strip()  # إدخال كلمة المرور
    #     # البحث عن المستخدم في قاعدة البيانات
    #     cursor.execute("SELECT id FROM users WHERE username = ? AND pwd = ?", (username, password))
    #     result = cursor.fetchone()
    #     if result:  # إذا وجد المستخدم
    #         print(f"Welcome back, {username}!")
    #         return result[0]  # إرجاع رقم المستخدم (user_id)
    #     else:
    #         print("Incorrect username or password!") #سم المستخدم أو كلمة المرور غير صحيحة!"
    #         return None
    #
    #
    # # ==========================
    # # 2️⃣ إضافة أسئلة (للمعلم أو المطور)
    # # ==========================
    # def add_question():
    #     question = input("Enter the question: ")  # إدخال نص السؤال
    #     answer = input("Enter the correct answer: ")  # إدخال الإجابة الصحيحة
    #     level = input("Enter difficulty level (easy/medium/hard): ").lower()  # إدخال مستوى الصعوبة
    #     # إدخال السؤال في جدول questions
    #     cursor.execute("INSERT INTO questions (question, answer, level) VALUES (?, ?, ?)", (question, answer, level))
    #     conn.commit()  # حفظ التغييرات
    #     print("Question added successfully ✅")
    #
    #
    # # ==========================
    # # 3️⃣ بدء الاختبار
    # # ==========================
    # def start_quiz(user_id):
    #     level = input("Choose difficulty level (easy/medium/hard): ").lower()  # اختيار مستوى الصعوبة
    #     # جلب الأسئلة من قاعدة البيانات حسب المستوى
    #     cursor.execute("SELECT id, question, answer FROM questions WHERE level = ?", (level,)) #تنفيذ استعلام (Query) على قاعدة البيانات باستخدام المؤشر cursor
    #     questions = cursor.fetchall()
    #     if not questions:  # إذا ما في أسئلة
    #         print(f"No questions available for level '{level}'")
    #         return
    #
    #     random.shuffle(questions)  # خلط ترتيب الأسئلة عشوائيًا
    #     score = 0  # بدء العداد للنقاط
    #     for q in questions:  # المرور على كل سؤال
    #         print("\nQuestion:", q[1])  # عرض نص السؤال
    #         ans = input("Your answer: ").strip()  # أخذ إجابة المستخدم
    #         if ans.lower() == q[2].lower():  # مقارنة الإجابة مع الصحيحة
    #             print("✅ Correct!")
    #             score += 1  # زيادة النقاط
    #         else:
    #             print(f"❌ Wrong! Correct answer: {q[2]}")
    #
    #     # عرض النتيجة النهائية
    #     print(f"\nQuiz finished! Your score: {score}/{len(questions)}")
    #
    #     # حفظ النتيجة في جدول scores
    #     today = datetime.now().strftime("%Y-%m-%d")  # الحصول على تاريخ اليوم
    #     cursor.execute("INSERT INTO scores (user_id, score, date) VALUES (?, ?, ?)", (user_id, score, today))
    #     conn.commit()  # حفظ التغييرات
    #     print("Your score has been saved in the database ✅")
    #
    #
    # # ==========================
    # # 4️⃣ القائمة الرئيسية
    # # ==========================
    # def main():
    #     print("Welcome to Math Quiz App 🎯")  # رسالة ترحيب
    #     while True:  # حلقة مستمرة حتى يختار المستخدم الخروج
    #         print("\nMenu:")
    #         print("1. Register")
    #         print("2. Login")
    #         print("3. Add Question (Admin)")
    #         print("4. Exit")
    #         choice = input("Enter your choice: ")  # أخذ خيار المستخدم
    #         if choice == "1":
    #             register_user()  # تسجيل مستخدم جديد
    #         elif choice == "2":
    #             user_id = login_user()  # تسجيل الدخول
    #             if user_id:  # إذا نجح تسجيل الدخول
    #                 start_quiz(user_id)  # بدء الاختبار
    #         elif choice == "3":
    #             add_question()  # إضافة سؤال جديد
    #         elif choice == "4":
    #             print("Goodbye!")  # إنهاء البرنامج
    #             break
    #         else:
    #             print("Invalid choice!")  # إذا أدخل خيار غير صحيح
    #
    #
    # # نقطة البداية للبرنامج
    # if __name__ == "__main__":
    #     main()  # تشغيل القائمة الرئيسية
    #     cursor.close()  # إغلاق المؤشر
    #     conn.close()  # إغلاق الاتصال بقاعدة البيانات