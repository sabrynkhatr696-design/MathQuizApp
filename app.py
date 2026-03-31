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

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
.main-title {
    text-align: center;
    color: #ff4b8b;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 8px;
}
.subtitle {
    text-align: center;
    color: #555;
    font-size: 18px;
    margin-bottom: 24px;
}
.info-chip {
    background: #f6f7fb;
    padding: 10px 14px;
    border-radius: 12px;
    border: 1px solid #e3e6f0;
    margin-bottom: 14px;
    font-size: 16px;
}
.score-box {
    background: linear-gradient(135deg, #eefaf0, #f8fff8);
    padding: 20px;
    border-radius: 16px;
    border: 2px solid #b7ebc0;
    font-size: 24px;
    font-weight: bold;
    color: #1f7a36;
    text-align: center;
    margin-top: 20px;
    margin-bottom: 12px;
}
.question-card {
    padding: 24px;
    border-radius: 18px;
    color: #222;
    font-size: 26px;
    font-weight: 700;
    margin-top: 18px;
    margin-bottom: 18px;
    border: 2px solid rgba(0,0,0,0.05);
}
.small-note {
    color: #777;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

QUESTION_COLORS = [
    "#FFE5EC",  # pink
    "#E3F2FD",  # light blue
    "#E8F5E9",  # light green
    "#FFF8E1",  # light yellow
    "#F3E5F5",  # lavender
    "#E0F7FA",  # cyan
    "#FFF3E0",  # peach
    "#FCE4EC",  # rose
]

# -----------------------------
# Database helpers
# -----------------------------
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
    return True, "Registered successfully. You can log in now."

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

# -----------------------------
# Session reset
# -----------------------------
def reset_quiz_state():
    st.session_state.quiz_started = False
    st.session_state.questions = []
    st.session_state.current_question = 0
    st.session_state.correct_answers = 0
    st.session_state.selected_level = None
    st.session_state.current_feedback = None
    st.session_state.answer_locked = False
    st.session_state.quiz_finished = False

# -----------------------------
# Session state init
# -----------------------------
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

if "current_feedback" not in st.session_state:
    st.session_state.current_feedback = None

if "answer_locked" not in st.session_state:
    st.session_state.answer_locked = False

if "quiz_finished" not in st.session_state:
    st.session_state.quiz_finished = False

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="main-title">🎯 Math Quiz App</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Solve the quiz step by step and get your final score out of 10 ✨</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Login / Register
# -----------------------------
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("🔐 Login"):
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

        if st.button("📝 Register"):
            success, message = register_user(reg_username, reg_password)
            if success:
                st.success(message)
            else:
                st.error(message)

# -----------------------------
# Main app
# -----------------------------
else:
    top1, top2 = st.columns([4, 1])

    with top1:
        st.markdown(f"## 👋 Hello, {st.session_state.username}")
    with top2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = ""
            reset_quiz_state()
            st.rerun()

    # Start screen
    if not st.session_state.quiz_started and not st.session_state.quiz_finished:
        st.subheader("Start Your Quiz")
        level = st.selectbox("Choose difficulty level", ["easy", "medium", "hard"])

        if st.button("🚀 Start Quiz"):
            questions = get_questions_by_level(level)
            if not questions:
                st.warning(f"No questions found for level '{level}'.")
            else:
                st.session_state.questions = questions
                st.session_state.selected_level = level
                st.session_state.quiz_started = True
                st.session_state.current_question = 0
                st.session_state.correct_answers = 0
                st.session_state.current_feedback = None
                st.session_state.answer_locked = False
                st.session_state.quiz_finished = False
                st.rerun()

    # Quiz screen
    elif st.session_state.quiz_started and not st.session_state.quiz_finished:
        total_questions = len(st.session_state.questions)
        idx = st.session_state.current_question

        if idx < total_questions:
            q_id, question_text, correct_answer = st.session_state.questions[idx]
            card_color = QUESTION_COLORS[idx % len(QUESTION_COLORS)]

            st.markdown(
                f"""
                <div class="info-chip">
                    <b>Level:</b> {st.session_state.selected_level.title()} &nbsp;&nbsp;|&nbsp;&nbsp;
                    <b>Question:</b> {idx + 1} / {total_questions} &nbsp;&nbsp;|&nbsp;&nbsp;
                    <b>Score:</b> {st.session_state.correct_answers}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress((idx + 1) / total_questions)

            st.markdown(
                f"""
                <div class="question-card" style="background-color:{card_color};">
                    {question_text}
                </div>
                """,
                unsafe_allow_html=True
            )

            answer_key = f"user_answer_{idx}"
            user_answer = st.text_input(
                "Your answer",
                key=answer_key,
                disabled=st.session_state.answer_locked
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("✅ Check Answer", disabled=st.session_state.answer_locked):
                    if user_answer.strip().lower() == str(correct_answer).strip().lower():
                        st.session_state.correct_answers += 1
                        st.session_state.current_feedback = ("success", "✅ Correct! Great job!")
                    else:
                        st.session_state.current_feedback = (
                            "error",
                            f"❌ Wrong. Correct answer: {correct_answer}"
                        )
                    st.session_state.answer_locked = True
                    st.rerun()

            with col2:
                if st.button("➡️ Next Question", disabled=not st.session_state.answer_locked):
                    st.session_state.current_question += 1
                    st.session_state.current_feedback = None
                    st.session_state.answer_locked = False

                    if st.session_state.current_question >= total_questions:
                        st.session_state.quiz_started = False
                        st.session_state.quiz_finished = True

                    st.rerun()

            if st.session_state.current_feedback:
                kind, msg = st.session_state.current_feedback
                if kind == "success":
                    st.success(msg)
                else:
                    st.error(msg)

            st.markdown('<div class="small-note">Tip: Check your answer first, then go to the next question.</div>', unsafe_allow_html=True)

    # Final result
    elif st.session_state.quiz_finished:
        correct = st.session_state.correct_answers
        total = len(st.session_state.questions)
        score_out_of_10 = round((correct / total) * 10, 2) if total > 0 else 0

        save_score(st.session_state.user_id, score_out_of_10)

        st.balloons()

        st.markdown(
            f'<div class="score-box">🏆 Your Final Score: {score_out_of_10} / 10</div>',
            unsafe_allow_html=True
        )

        st.write(f"Correct answers: **{correct} / {total}**")

        if score_out_of_10 >= 8:
            st.success("Excellent work! 🌟")
        elif score_out_of_10 >= 5:
            st.info("Good job! Keep practicing 💪")
        else:
            st.warning("Nice try. Practice more and come back stronger 📚")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 Restart Quiz"):
                reset_quiz_state()
                st.rerun()
        with c2:
            if st.button("🎯 Change Level"):
                reset_quiz_state()
                st.rerun()
