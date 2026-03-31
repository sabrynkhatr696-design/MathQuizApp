import streamlit as st
import sqlite3
from datetime import datetime
import random

DB_PATH = "global.db"

st.set_page_config(
    page_title="Math Quiz App",
    page_icon="🎯",
    layout="centered"
)

st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #ff4b8b;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #444;
        font-size: 18px;
        margin-bottom: 25px;
    }
    .question-box {
        background-color: #fff4f8;
        padding: 18px;
        border-radius: 15px;
        border: 2px solid #ffd1e1;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .score-box {
        background-color: #eefaf0;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #b7ebc0;
        font-size: 20px;
        font-weight: bold;
        color: #1f7a36;
        text-align: center;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)


def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    username = username.strip().lower()
    password = password.strip()

    if not username or not password:
        conn.close()
        return False, "Please fill in all fields."

    if len(password) < 6:
        conn.close()
        return False, "Password must be at least 6 characters."

    cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
    exists = cursor.fetchone()[0]

    if exists > 0:
        conn.close()
        return False, "Username already exists."

    cursor.execute(
        "INSERT INTO users (username, pwd) VALUES (?, ?)",
        (username, password)
    )
    conn.commit()
    conn.close()
    return True, "Registered successfully."


def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    username = username.strip().lower()
    password = password.strip()

    cursor.execute(
        "SELECT id, username FROM users WHERE username = ? AND pwd = ?",
        (username, password)
    )
    result = cursor.fetchone()
    conn.close()
    return result


def get_questions_by_level(level):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, question, answer FROM questions WHERE level = ?",
        (level,)
    )
    questions = cursor.fetchall()
    conn.close()
    random.shuffle(questions)
    return questions


def save_score(user_id, score_out_of_10):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO scores (user_id, score, date) VALUES (?, ?, ?)",
        (user_id, score_out_of_10, today)
    )
    conn.commit()
    conn.close()


def reset_quiz_state():
    st.session_state.quiz_started = False
    st.session_state.questions = []
    st.session_state.current_question = 0
    st.session_state.correct_answers = 0
    st.session_state.selected_level = None
    st.session_state.feedback = ""


# session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = ""

if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "correct_answers" not in st.session_state:
    st.session_state.correct_answers = 0

if "selected_level" not in st.session_state:
    st.session_state.selected_level = None

if "feedback" not in st.session_state:
    st.session_state.feedback = ""


st.markdown('<div class="main-title">🎯 Math Quiz App</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Solve all questions, get your final score out of 10, and enjoy the quiz ✨</div>',
    unsafe_allow_html=True
)


if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            user = login_user(login_username, login_password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user_id = user[0]
                st.session_state.username = user[1]
                reset_quiz_state()
                st.success(f"Welcome back, {user[1]} 🎉")
                st.rerun()
            else:
                st.error("Incorrect username or password.")

    with tab2:
        st.subheader("Register")
        reg_username = st.text_input("Choose a username", key="reg_username")
        reg_password = st.text_input("Choose a password", type="password", key="reg_password")

        if st.button("Register"):
            success, message = register_user(reg_username, reg_password)
            if success:
                st.success(message + " You can now log in.")
            else:
                st.error(message)

else:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.success(f"Logged in as: {st.session_state.username}")
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = ""
            reset_quiz_state()
            st.rerun()

    if not st.session_state.quiz_started:
        st.subheader("Start Your Quiz")
        level = st.selectbox("Choose difficulty level", ["easy", "medium", "hard"])

        if st.button("Start Quiz"):
            questions = get_questions_by_level(level)
            if not questions:
                st.warning(f"No questions found for level '{level}'.")
            else:
                st.session_state.questions = questions
                st.session_state.selected_level = level
                st.session_state.quiz_started = True
                st.session_state.current_question = 0
                st.session_state.correct_answers = 0
                st.session_state.feedback = ""
                st.rerun()

    else:
        total_questions = len(st.session_state.questions)
        current_index = st.session_state.current_question

        if current_index < total_questions:
            q_id, question_text, correct_answer = st.session_state.questions[current_index]

            st.write(f"**Level:** {st.session_state.selected_level.title()}")
            st.progress((current_index + 1) / total_questions)
            st.write(f"**Question {current_index + 1} of {total_questions}**")

            st.markdown(
                f'<div class="question-box"><h2 style="margin:0;">{question_text}</h2></div>',
                unsafe_allow_html=True
            )

            user_answer = st.text_input("Your answer", key=f"answer_{current_index}")

            if st.button("Submit Answer"):
                if user_answer.strip().lower() == str(correct_answer).strip().lower():
                    st.session_state.correct_answers += 1
                    st.session_state.feedback = "✅ Correct answer!"
                else:
                    st.session_state.feedback = f"❌ Wrong answer. Correct answer: {correct_answer}"

                st.session_state.current_question += 1
                st.rerun()

            if st.session_state.feedback:
                st.info(st.session_state.feedback)

        else:
            correct = st.session_state.correct_answers
            total = len(st.session_state.questions)
            score_out_of_10 = round((correct / total) * 10, 2)

            save_score(st.session_state.user_id, score_out_of_10)

            st.balloons()
            st.markdown(
                f'<div class="score-box">Your final score: {score_out_of_10} / 10 🎓</div>',
                unsafe_allow_html=True
            )
            st.write(f"Correct answers: **{correct} / {total}**")

            if score_out_of_10 >= 8:
                st.success("Excellent work! 🌟")
            elif score_out_of_10 >= 5:
                st.info("Good job! Keep practicing 💪")
            else:
                st.warning("Nice try. Practice more and come back stronger 📚")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Play Again"):
                    reset_quiz_state()
                    st.rerun()
            with col2:
                if st.button("Change Level"):
                    reset_quiz_state()
                    st.rerun()
