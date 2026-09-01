import streamlit as st
from questions import QUESTIONS

# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------
st.set_page_config(
    page_title="밸런스 게임",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# CSS
# --------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #fff7ed 0%, #fdf2f8 50%, #eef2ff 100%);
    }

    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 900;
        margin-top: 20px;
        margin-bottom: 5px;
        background: linear-gradient(90deg, #ff4d6d, #845ef7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .category-box {
        background: rgba(255,255,255,0.75);
        padding: 10px 18px;
        border-radius: 30px;
        text-align: center;
        display: inline-block;
        font-weight: 700;
        color: #7c3aed;
        border: 1px solid #e9d5ff;
        margin-bottom: 20px;
    }

    .question-card {
        background: rgba(255,255,255,0.95);
        border-radius: 28px;
        padding: 35px 25px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.08);
        margin: 10px 0 25px 0;
        text-align: center;
    }

    .vs {
        font-size: 22px;
        font-weight: 900;
        color: #9ca3af;
        margin: 15px 0;
    }

    .option-card {
        min-height: 180px;
        border-radius: 24px;
        padding: 30px 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        font-weight: 800;
        font-size: 24px;
    }

    .option-a {
        background: linear-gradient(135deg, #ffe4e6, #fecdd3);
        color: #9f1239;
    }

    .option-b {
        background: linear-gradient(135deg, #e0e7ff, #c7d2fe);
        color: #3730a3;
    }

    .option-emoji {
        font-size: 55px;
        margin-bottom: 15px;
    }

    .result-card {
        background: white;
        border-radius: 30px;
        padding: 40px 25px;
        text-align: center;
        box-shadow: 0 15px 40px rgba(0,0,0,0.1);
    }

    .result-title {
        font-size: 32px;
        font-weight: 900;
        margin-bottom: 15px;
    }

    .big-result {
        font-size: 70px;
        font-weight: 900;
        color: #7c3aed;
        margin: 20px 0;
    }

    div.stButton > button {
        border-radius: 15px;
        min-height: 55px;
        font-size: 18px;
        font-weight: 800;
        border: none;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
    }

    .footer {
        text-align: center;
        color: #9ca3af;
        margin-top: 40px;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 세션 상태 초기화
# --------------------------------------------------
def initialize():
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if "category" not in st.session_state:
        st.session_state.category = None

    if "questions" not in st.session_state:
        st.session_state.questions = []

    if "current" not in st.session_state:
        st.session_state.current = 0

    if "answers" not in st.session_state:
        st.session_state.answers = []

    if "score_a" not in st.session_state:
        st.session_state.score_a = 0

    if "score_b" not in st.session_state:
        st.session_state.score_b = 0


initialize()


# --------------------------------------------------
# 게임 시작
# --------------------------------------------------
def start_game(category):
    st.session_state.category = category

    if category == "random":
        import random
        all_questions = []

        for category_name, questions in QUESTIONS.items():
            for question in questions:
                item = question.copy()
                item["category"] = category_name
                all_questions.append(item)

        random.shuffle(all_questions)
        st.session_state.questions = all_questions[:10]

    else:
        st.session_state.questions = QUESTIONS[category].copy()

    st.session_state.current = 0
    st.session_state.answers = []
    st.session_state.score_a = 0
    st.session_state.score_b = 0
    st.session_state.page = "game"


# --------------------------------------------------
# 게임 초기화
# --------------------------------------------------
def restart():
    st.session_state.page = "home"
    st.session_state.category = None
    st.session_state.questions = []
    st.session_state.current = 0
    st.session_state.answers = []
    st.session_state.score_a = 0
    st.session_state.score_b = 0


# --------------------------------------------------
# 선택
# --------------------------------------------------
def choose(answer):
    st.session_state.answers.append(answer)

    if answer == "A":
        st.session_state.score_a += 1
    else:
        st.session_state.score_b += 1

    st.session_state.current += 1

    if st.session_state.current >= len(st.session_state.questions):
        st.session_state.page = "result"


# --------------------------------------------------
# 홈 화면
# --------------------------------------------------
def home_page():

    st.markdown(
        '<div class="main-title">⚖️ 밸런스 게임</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">당신이라면 어느 쪽을 선택하시겠어요?</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 🎮 게임 종류")

    categories = [
        ("🍔", "음식", "food"),
        ("🏖️", "주말", "weekend"),
        ("✈️", "여행", "travel"),
        ("💰", "소비", "money"),
        ("💑", "연애", "love"),
        ("🎲", "랜덤", "random"),
    ]

    cols = st.columns(2)

    for i, (emoji, title, key) in enumerate(categories):
        with cols[i % 2]:

            st.markdown(
                f"""
                <div class="question-card">
                    <div style="font-size:50px">{emoji}</div>
                    <h3>{title}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                f"{emoji} {title} 시작하기",
                key=f"category_{key}",
                use_container_width=True
            ):
                start_game(key)


# --------------------------------------------------
# 게임 화면
# --------------------------------------------------
def game_page():

    questions = st.session_state.questions
    current = st.session_state.current
    question = questions[current]

    total = len(questions)
    progress = current / total

    st.progress(progress)

    st.markdown(
        f"""
        <div style="text-align:center; color:#6b7280;">
            {current + 1} / {total}
        </div>
        """,
        unsafe_allow_html=True
    )

    category_name = question.get("category", st.session_state.category)

    category_labels = {
        "food": "🍔 음식",
        "weekend": "🏖️ 주말",
        "travel": "✈️ 여행",
        "money": "💰 소비",
        "love": "💑 연애",
        "random": "🎲 랜덤"
    }

    st.markdown(
        f"""
        <div style="text-align:center;">
            <div class="category-box">
                {category_labels.get(category_name, "⚖️ 밸런스 게임")}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="question-card">
            <h2>{question["question"]}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="option-card option-a">
                <div class="option-emoji">
                    {question["a_emoji"]}
                </div>
                <div>
                    {question["a"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        if st.button(
            "🔴 A 선택",
            key=f"a_{current}",
            use_container_width=True
        ):
            choose("A")
            st.rerun()

    with col2:

        st.markdown(
            f"""
            <div class="option-card option-b">
                <div class="option-emoji">
                    {question["b_emoji"]}
                </div>
                <div>
                    {question["b"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        if st.button(
            "🔵 B 선택",
            key=f"b_{current}",
            use_container_width=True
        ):
            choose("B")
            st.rerun()

    st.markdown(
        '<div class="footer">당신의 선택은?</div>',
        unsafe_allow_html=True
    )


# --------------------------------------------------
# 결과 화면
# --------------------------------------------------
def result_page():

    total = len(st.session_state.answers)
    score_a = st.session_state.score_a
    score_b = st.session_state.score_b

    if score_a > score_b:
        result = "A"
        message = "당신은 A 선택을 더 선호하는 사람이에요!"
        emoji = "🔴"
    elif score_b > score_a:
        result = "B"
        message = "당신은 B 선택을 더 선호하는 사람이에요!"
        emoji = "🔵"
    else:
        result = "50 : 50"
        message = "와! 선택이 완벽하게 반반이에요!"
        emoji = "⚖️"

    st.markdown(
        """
        <div class="result-card">
            <div style="font-size:70px;">🏆</div>
            <div class="result-title">게임 완료!</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown(
        f"""
        <div class="result-card">
            <div style="font-size:60px;">{emoji}</div>
            <div class="big-result">{result}</div>
            <h3>{message}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🔴 A 선택",
            f"{score_a}회",
            f"{round(score_a / total * 100)}%"
        )

    with col2:
        st.metric(
            "🔵 B 선택",
            f"{score_b}회",
            f"{round(score_b / total * 100)}%"
        )

    st.write("")

    if st.button(
        "🔄 다시 하기",
        use_container_width=True
    ):
        restart()
        st.rerun()

    if st.button(
        "🏠 홈으로 돌아가기",
        use_container_width=True
    ):
        restart()
        st.rerun()


# --------------------------------------------------
# 페이지 실행
# --------------------------------------------------
if st.session_state.page == "home":
    home_page()

elif st.session_state.page == "game":
    game_page()

elif st.session_state.page == "result":
    result_page()
