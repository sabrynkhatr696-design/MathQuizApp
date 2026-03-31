import streamlit as st
import sqlite3
import random
from datetime import datetime

conn = sqlite3.connect("global.db", check_same_thread=False)
cursor = conn.cursor()

st.title("🎯 Math Quiz App")

menu = st.selectbox("Choose option", ["Register", "Login"])

# =====================
# Register
# =====================
if menu == "Register":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if len(password) < 6:
            st.error("Password must be at least 6 characters")
        else:
            cursor.execute("SELECT COUNT(*) FROM users WHERE username=?", (username,))
            if cursor.fetchone()[0] > 0:
                st.error("Username already exists")
            else:
                cursor.execute("INSERT INTO users (username, pwd) VALUES (?, ?)", (username, password))
                conn.commit()
                st.success("Registered successfully ✅")

# =====================
# Login + Quiz
# =====================
elif menu == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        cursor.execute("SELECT id FROM users WHERE username=? AND pwd=?", (username, password))
        user = cursor.fetchone()

        if user:
            st.success("Login successful 🎉")

            level = st.selectbox("Choose level", ["easy", "medium", "hard"])

            cursor.execute("SELECT question, answer FROM questions WHERE level=?", (level,))
            questions = cursor.fetchall()

            if questions:
                q = random.choice(questions)
                st.write("### " + q[0])

                user_answer = st.text_input("Your answer")

                if st.button("Submit Answer"):
                    if user_answer.lower() == q[1].lower():
                        st.success("Correct ✅")
                    else:
                        st.error(f"Wrong ❌ Correct answer: {q[1]}")

        else:
            st.error("Wrong username or password")
