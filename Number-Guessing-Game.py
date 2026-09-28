import random
import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Number Guessing Game",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# GAME SETTINGS
# =========================================================
RANGES = {
    "Easy": (1, 50),
    "Medium": (15, 100),
    "Hard": (1, 100),
}

# =========================================================
# CUSTOM CSS
# =========================================================
st.html("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800;900&family=Rajdhani:wght@500;600;700&display=swap');

/* ========================================================
   GLOBAL
   ======================================================== */

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
}

.stApp {
    min-height: 100vh;

    background:
        radial-gradient(
            circle at 15% 10%,
            rgba(124, 58, 237, 0.20),
            transparent 30%
        ),
        radial-gradient(
            circle at 85% 15%,
            rgba(236, 72, 153, 0.16),
            transparent 28%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(59, 130, 246, 0.12),
            transparent 35%
        ),
        #06060f;

    color: #f5f3ff;
}

.block-container {
    max-width: 1250px;
    padding-top: 1.8rem;
    padding-bottom: 2rem;
}

/* ========================================================
   MAIN TITLE
   ======================================================== */

.game-title {
    text-align: center;
    margin-bottom: 5px;
}

.game-title h1 {
    margin: 0;
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(2rem, 5vw, 4rem);
    font-weight: 900;
    letter-spacing: 4px;
}

.title-emoji {
    display: inline-block;
    margin-right: 12px;
    -webkit-text-fill-color: initial;
    color: white;

    filter:
        drop-shadow(0 0 6px rgba(255,255,255,0.9))
        drop-shadow(0 0 15px rgba(192,132,252,0.9));

    animation: emojiPulse 1.8s ease-in-out infinite;
}

.title-text {
    background: linear-gradient(
        90deg,
        #c084fc,
        #f472b6,
        #60a5fa,
        #c084fc
    );

    background-size: 250% auto;

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    animation: titleGlow 5s linear infinite;
}

@keyframes titleGlow {
    to {
        background-position: 250% center;
    }
}

@keyframes emojiPulse {
    0%, 100% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.12);
    }
}

.subtitle {
    text-align: center;
    color: #9f9ab3;
    font-size: 1.05rem;
    letter-spacing: 2px;
    margin-bottom: 32px;
}

/* ========================================================
   SCREEN TITLE
   ======================================================== */

.screen-title {
    text-align: center;
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(1.4rem, 3vw, 2rem);
    font-weight: 800;
    letter-spacing: 2px;
    color: #e9d5ff;
    margin: 15px 0 6px;
}

.screen-subtitle {
    text-align: center;
    color: #817b94;
    font-size: 1rem;
    margin-bottom: 25px;
}

/* ========================================================
   DIFFICULTY SELECTION
   ======================================================== */

.selection-panel {
    margin-top: 20px;
    padding: 28px;
    border-radius: 28px;

    background:
        linear-gradient(
            145deg,
            rgba(24, 20, 44, 0.96),
            rgba(10, 9, 22, 0.96)
        );

    border: 1px solid rgba(168, 85, 247, 0.20);

    box-shadow:
        0 0 50px rgba(124, 58, 237, 0.08),
        inset 0 0 40px rgba(124, 58, 237, 0.025);
}

.difficulty-card {
    border-radius: 22px;
    padding: 28px 18px 20px;
    min-height: 210px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.065),
            rgba(255,255,255,0.018)
        );

    backdrop-filter: blur(14px);

    border: 1px solid rgba(255,255,255,0.09);

    text-align: center;

    box-shadow:
        0 14px 40px rgba(0,0,0,0.25);

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease;
}

.difficulty-card:hover {
    transform: translateY(-6px);
}

.difficulty-card.easy {
    border-color: rgba(34,197,94,0.35);
    box-shadow:
        0 0 30px rgba(34,197,94,0.10);
}

.difficulty-card.medium {
    border-color: rgba(234,179,8,0.35);
    box-shadow:
        0 0 30px rgba(234,179,8,0.10);
}

.difficulty-card.hard {
    border-color: rgba(239,68,68,0.35);
    box-shadow:
        0 0 30px rgba(239,68,68,0.10);
}

.difficulty-icon {
    font-size: 2.7rem;
    margin-bottom: 8px;
}

.difficulty-name {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: 2px;
}

.difficulty-range {
    color: #9993aa;
    margin-top: 8px;
    font-size: 1rem;
}

.difficulty-description {
    color: #716c80;
    margin-top: 3px;
    margin-bottom: 15px;
    font-size: 0.88rem;
}

/* ========================================================
   MAIN GAME ARENA
   ======================================================== */

.game-arena {
    margin-top: 15px;
    padding: 32px;

    border-radius: 30px;

    background:
        radial-gradient(
            circle at 50% 0%,
            rgba(168,85,247,0.10),
            transparent 40%
        ),
        linear-gradient(
            145deg,
            rgba(22,18,40,0.98),
            rgba(7,7,16,0.98)
        );

    border: 1px solid rgba(168,85,247,0.25);

    box-shadow:
        0 0 70px rgba(124,58,237,0.10),
        inset 0 0 60px rgba(124,58,237,0.025);
}

/* ========================================================
   LEVEL BADGE
   ======================================================== */

.level-badge {
    width: fit-content;
    margin: 0 auto 15px;

    padding: 7px 16px;

    border-radius: 999px;

    background: rgba(168,85,247,0.10);
    border: 1px solid rgba(168,85,247,0.30);

    color: #d8b4fe;

    font-family: 'Orbitron', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;

    letter-spacing: 1.2px;
}

/* ========================================================
   BIG GAME HEADING
   ======================================================== */

.game-heading-big {
    text-align: center;

    font-family: 'Orbitron', sans-serif;

    font-size: clamp(1.8rem, 4vw, 3rem);

    font-weight: 900;

    letter-spacing: 2px;

    background: linear-gradient(
        90deg,
        #ffffff,
        #d8b4fe,
        #f9a8d4,
        #ffffff
    );

    background-size: 220% auto;

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    animation: titleGlow 5s linear infinite;

    margin-bottom: 6px;
}

.game-heading-small {
    text-align: center;

    color: #777187;

    font-size: 1rem;

    letter-spacing: 1px;

    margin-bottom: 28px;
}

/* ========================================================
   RANGE DISPLAY
   ======================================================== */

.range-display {
    text-align: center;
    margin-bottom: 20px;
}

.range-label {
    color: #716c80;
    font-size: 0.8rem;
    letter-spacing: 1.5px;
}

.range-number {
    font-family: 'Orbitron', sans-serif;
    color: #c084fc;
    font-size: 1.25rem;
    font-weight: 800;
}

/* ========================================================
   STATS
   ======================================================== */

.stat-card {
    padding: 16px 10px;

    border-radius: 16px;

    text-align: center;

    background: rgba(255,255,255,0.035);

    border: 1px solid rgba(255,255,255,0.07);

    margin-bottom: 20px;
}

.stat-value {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: #c084fc;
}

.stat-label {
    color: #777187;
    font-size: 0.75rem;
    letter-spacing: 1.2px;
}

/* ========================================================
   NUMBER INPUT
   ======================================================== */

div[data-testid="stNumberInput"] {
    max-width: 620px;
    margin: 0 auto;
}

div[data-testid="stNumberInput"] label {
    color: #d5cee2 !important;

    font-family: 'Orbitron', sans-serif !important;

    font-size: 0.9rem !important;

    letter-spacing: 1.2px !important;

    text-align: center !important;

    display: block !important;
}

div[data-testid="stNumberInput"] input {
    height: 65px !important;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.06),
            rgba(255,255,255,0.025)
        ) !important;

    color: #ffffff !important;

    border:
        1px solid rgba(192,132,252,0.40) !important;

    border-radius: 16px !important;

    font-size: 1.5rem !important;

    font-family: 'Orbitron', sans-serif !important;

    text-align: center !important;

    box-shadow:
        0 0 20px rgba(168,85,247,0.06) !important;
}

div[data-testid="stNumberInput"] input:focus {
    border-color: #c084fc !important;

    box-shadow:
        0 0 25px rgba(192,132,252,0.22) !important;
}

/* ========================================================
   SUBMIT BUTTON
   ======================================================== */

.stFormSubmitButton {
    max-width: 620px;
    margin: 15px auto 0;
}

.stFormSubmitButton > button {
    height: 58px !important;

    border-radius: 16px !important;

    border:
        1px solid rgba(192,132,252,0.45) !important;

    background:
        linear-gradient(
            135deg,
            rgba(124,58,237,0.55),
            rgba(236,72,153,0.32)
        ) !important;

    color: white !important;

    font-family: 'Orbitron', sans-serif !important;

    font-size: 1rem !important;

    font-weight: 800 !important;

    letter-spacing: 1.5px !important;

    transition: all 0.2s ease !important;

    box-shadow:
        0 0 25px rgba(168,85,247,0.10) !important;
}

.stFormSubmitButton > button:hover {
    transform: translateY(-3px);

    border-color: #d8b4fe !important;

    box-shadow:
        0 0 30px rgba(192,132,252,0.25) !important;
}

/* ========================================================
   NORMAL BUTTONS
   ======================================================== */

.stButton > button {
    min-height: 48px;

    border-radius: 13px !important;

    border:
        1px solid rgba(192,132,252,0.30) !important;

    background:
        linear-gradient(
            135deg,
            rgba(124,58,237,0.30),
            rgba(236,72,153,0.16)
        ) !important;

    color: #ffffff !important;

    font-family: 'Orbitron', sans-serif !important;

    font-weight: 700 !important;

    letter-spacing: 0.8px !important;

    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px);

    border-color: #c084fc !important;

    box-shadow:
        0 0 20px rgba(192,132,252,0.18) !important;
}

/* ========================================================
   FEEDBACK
   ======================================================== */

.feedback-box {
    max-width: 620px;

    margin: 20px auto 0;

    padding: 18px;

    border-radius: 15px;

    text-align: center;

    font-family: 'Orbitron', sans-serif;

    font-size: 1rem;

    font-weight: 700;

    letter-spacing: 0.5px;
}

.success-box {
    background: rgba(34,197,94,0.10);

    border:
        1px solid rgba(34,197,94,0.32);

    color: #86efac;

    box-shadow:
        0 0 25px rgba(34,197,94,0.08);
}

.higher-box {
    background: rgba(59,130,246,0.10);

    border:
        1px solid rgba(59,130,246,0.30);

    color: #93c5fd;
}

.lower-box {
    background: rgba(244,63,94,0.10);

    border:
        1px solid rgba(244,63,94,0.30);

    color: #fda4af;
}

/* ========================================================
   BEST SCORE PANEL
   ======================================================== */

.best-panel {
    margin-top: 15px;

    padding: 24px;

    border-radius: 22px;

    background:
        linear-gradient(
            145deg,
            rgba(20,17,38,0.96),
            rgba(10,9,22,0.96)
        );

    border:
        1px solid rgba(96,165,250,0.18);
}

.best-title {
    text-align: center;

    font-family: 'Orbitron', sans-serif;

    font-size: 1rem;

    font-weight: 800;

    letter-spacing: 1.5px;

    color: #bfdbfe;

    margin-bottom: 16px;
}

.best-current {
    text-align: center;

    padding: 20px 10px;

    border-radius: 16px;

    background: rgba(255,255,255,0.035);

    border:
        1px solid rgba(255,255,255,0.06);
}

.best-current-number {
    font-family: 'Orbitron', sans-serif;

    font-size: 2rem;

    font-weight: 900;

    color: #c084fc;
}

.best-current-label {
    color: #777187;

    font-size: 0.75rem;

    letter-spacing: 1px;
}

/* ========================================================
   OTHER BEST SCORES
   ======================================================== */

.score-row {
    display: flex;

    justify-content: space-between;

    align-items: center;

    padding: 11px 13px;

    margin-top: 9px;

    border-radius: 11px;

    background: rgba(255,255,255,0.03);

    border:
        1px solid rgba(255,255,255,0.05);
}

.score-level {
    color: #aaa4b7;

    font-weight: 700;

    letter-spacing: 0.5px;
}

.score-number {
    font-family: 'Orbitron', sans-serif;

    color: #c084fc;

    font-weight: 800;
}

/* ========================================================
   CELEBRATION
   ======================================================== */

.celebration {
    position: fixed;

    inset: 0;

    z-index: 999999;

    pointer-events: none;

    overflow: hidden;

    animation:
        celebrationFade
        4s
        ease
        forwards;
}

.celebration-title {
    position: absolute;

    left: 50%;
    top: 42%;

    transform:
        translate(-50%, -50%)
        scale(0.4);

    text-align: center;

    white-space: nowrap;

    font-family: 'Orbitron', sans-serif;

    font-size: clamp(
        1.8rem,
        7vw,
        4.5rem
    );

    font-weight: 900;

    letter-spacing: 3px;

    color: white;

    text-shadow:
        0 0 10px rgba(255,255,255,0.9),
        0 0 25px rgba(192,132,252,0.9),
        0 0 50px rgba(236,72,153,0.7);

    animation:
        celebrationTitle
        1s
        cubic-bezier(.17,.89,.32,1.35)
        forwards;
}

.paper {
    position: absolute;

    width: 10px;
    height: 20px;

    top: 45%;
    left: 50%;

    opacity: 0;

    animation:
        paperBurst
        2.8s
        cubic-bezier(.12,.8,.25,1)
        forwards;
}

.paper:nth-child(2n) {
    width: 8px;
    height: 15px;
}

.paper:nth-child(3n) {
    width: 13px;
    height: 8px;
    border-radius: 50%;
}

.paper:nth-child(4n) {
    width: 7px;
    height: 25px;
}

@keyframes celebrationTitle {

    0% {
        opacity: 0;

        transform:
            translate(-50%, -50%)
            scale(0.35)
            rotate(-8deg);
    }

    45% {
        opacity: 1;

        transform:
            translate(-50%, -50%)
            scale(1.15)
            rotate(2deg);
    }

    70% {
        transform:
            translate(-50%, -50%)
            scale(1)
            rotate(0deg);
    }

    100% {
        opacity: 1;

        transform:
            translate(-50%, -50%)
            scale(1)
            rotate(0deg);
    }
}

@keyframes paperBurst {

    0% {
        opacity: 1;

        transform:
            translate(-50%, -50%)
            rotate(0deg)
            scale(0.4);
    }

    25% {
        opacity: 1;
    }

    100% {
        opacity: 0;

        transform:
            translate(
                calc(-50% + var(--x)),
                calc(-50% + var(--y))
            )
            rotate(var(--rotate))
            scale(1);
    }
}

@keyframes celebrationFade {

    0% {
        opacity: 1;
    }

    80% {
        opacity: 1;
    }

    100% {
        opacity: 0;
        visibility: hidden;
    }
}

/* ========================================================
   FOOTER
   ======================================================== */

.footer {
    text-align: center;

    color: #575264;

    margin-top: 35px;

    font-size: 0.82rem;

    letter-spacing: 1px;
}

/* ========================================================
   MOBILE
   ======================================================== */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 1.2rem;
    }

    .game-title h1 {
        font-size: 1.9rem;
        letter-spacing: 2px;
    }

    .title-emoji {
        margin-right: 5px;
    }

    .subtitle {
        font-size: 0.78rem;
        letter-spacing: 1px;
    }

    .selection-panel {
        padding: 18px 12px;
    }

    .difficulty-card {
        min-height: 155px;
        padding: 18px 10px;
    }

    .difficulty-icon {
        font-size: 2.1rem;
    }

    .difficulty-name {
        font-size: 1rem;
    }

    .difficulty-range {
        font-size: 0.85rem;
    }

    .difficulty-description {
        font-size: 0.78rem;
    }

    .game-arena {
        padding: 22px 14px;
        border-radius: 23px;
    }

    .game-heading-big {
        font-size: 1.7rem;
    }

    div[data-testid="stNumberInput"] input {
        height: 60px !important;
        font-size: 1.25rem !important;
    }

    .celebration-title {
        font-size: 2rem;
        letter-spacing: 1px;
    }
}

</style>
""")

# =========================================================
# SESSION STATE
# =========================================================

if "screen" not in st.session_state:
    st.session_state.screen = "selection"

if "difficulty" not in st.session_state:
    st.session_state.difficulty = None

if "secret_number" not in st.session_state:
    st.session_state.secret_number = None

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "message" not in st.session_state:
    st.session_state.message = ""

if "message_type" not in st.session_state:
    st.session_state.message_type = ""

if "celebrate" not in st.session_state:
    st.session_state.celebrate = False

if "best_scores" not in st.session_state:
    st.session_state.best_scores = {
        "Easy": None,
        "Medium": None,
        "Hard": None,
    }

# =========================================================
# GAME FUNCTIONS
# =========================================================

def start_game(level):
    minimum, maximum = RANGES[level]

    st.session_state.difficulty = level

    st.session_state.secret_number = random.randint(
        minimum,
        maximum
    )

    st.session_state.attempts = 0

    st.session_state.game_over = False

    st.session_state.message = ""

    st.session_state.message_type = ""

    st.session_state.celebrate = False

    st.session_state.screen = "game"


def restart_game():
    level = st.session_state.difficulty

    minimum, maximum = RANGES[level]

    st.session_state.secret_number = random.randint(
        minimum,
        maximum
    )

    st.session_state.attempts = 0

    st.session_state.game_over = False

    st.session_state.message = ""

    st.session_state.message_type = ""

    st.session_state.celebrate = False


def change_difficulty():
    st.session_state.screen = "selection"

    st.session_state.difficulty = None

    st.session_state.secret_number = None

    st.session_state.attempts = 0

    st.session_state.game_over = False

    st.session_state.message = ""

    st.session_state.message_type = ""

    st.session_state.celebrate = False


def check_guess(guess):

    secret = st.session_state.secret_number

    st.session_state.attempts += 1

    # =====================================================
    # CORRECT
    # =====================================================

    if guess == secret:

        st.session_state.game_over = True

        st.session_state.message = "🎉 Correct!"

        st.session_state.message_type = "success"

        st.session_state.celebrate = True

        level = st.session_state.difficulty

        current_score = st.session_state.attempts

        best = st.session_state.best_scores[level]

        if best is None or current_score < best:

            st.session_state.best_scores[level] = current_score

    # =====================================================
    # SECRET IS HIGHER
    # =====================================================

    elif guess < secret:

        st.session_state.message = (
            f"It is more than {guess}."
        )

        st.session_state.message_type = "higher"

        st.session_state.celebrate = False

    # =====================================================
    # SECRET IS LOWER
    # =====================================================

    else:

        st.session_state.message = (
            f"It is less than {guess}."
        )

        st.session_state.message_type = "lower"

        st.session_state.celebrate = False


def reset_best_scores():

    st.session_state.best_scores = {
        "Easy": None,
        "Medium": None,
        "Hard": None,
    }


# =========================================================
# CELEBRATION
# =========================================================

if st.session_state.celebrate:

    papers = ""

    pieces = [
        (-45, -380, -220),
        (-35, -300, -300),
        (-25, -210, -370),
        (-15, -120, -330),
        (-5, -40, -390),
        (5, 60, -350),
        (15, 140, -390),
        (25, 220, -320),
        (35, 310, -350),
        (45, 390, -250),

        (-40, -420, -120),
        (-30, -350, 40),
        (-20, -280, 140),
        (-10, -170, 200),
        (10, 170, 190),
        (20, 280, 140),
        (30, 360, 20),
        (40, 430, -100),

        (-30, -250, -220),
        (-20, -180, -280),
        (-10, -80, -250),
        (10, 90, -260),
        (20, 190, -230),
        (30, 280, -180),

        (-45, -450, 220),
        (-30, -350, 300),
        (-15, -220, 350),
        (15, 230, 350),
        (30, 350, 300),
        (45, 450, 200),
    ]

    for index, (rotation, x, y) in enumerate(pieces):

        delay = (index % 7) * 0.035

        papers += f"""
        <div
            class="paper"
            style="
                --x:{x}px;
                --y:{y}px;
                --rotate:{rotation + (index * 17)}deg;
                animation-delay:{delay}s;
                background:hsl({(index * 47) % 360}, 90%, 65%);
            "
        ></div>
        """

    st.html(f"""
    <div class="celebration">

        {papers}

        <div class="celebration-title">
            🎉 CORRECT! 🎉
        </div>

    </div>
    """)

    st.session_state.celebrate = False


# =========================================================
# MAIN TITLE
# =========================================================

st.html("""
<div class="game-title">

    <h1>
        <span class="title-emoji">🎯</span>
        <span class="title-text">
            NUMBER GUESSING GAME
        </span>
    </h1>

</div>

<div class="subtitle">
    GUESS THE NUMBER • BEAT YOUR BEST • HAVE FUN
</div>
""")


# =========================================================
# SCREEN 1 — DIFFICULTY SELECTION
# =========================================================

if st.session_state.screen == "selection":

    st.html("""
    <div class="selection-panel">

        <div class="screen-title">
            🎮 CHOOSE YOUR LEVEL
        </div>

        <div class="screen-subtitle">
            Pick your challenge and enter the game
        </div>

    </div>
    """)

    col1, col2, col3 = st.columns(
        3,
        gap="medium"
    )

    # =====================================================
    # EASY
    # =====================================================

    with col1:

        st.html("""
        <div class="difficulty-card easy">

            <div class="difficulty-icon">
                🟢
            </div>

            <div class="difficulty-name">
                EASY
            </div>

            <div class="difficulty-range">
                Numbers 1 — 50
            </div>

            <div class="difficulty-description">
                A relaxed challenge
            </div>

        </div>
        """)

        if st.button(
            "🎮 PLAY EASY",
            key="play_easy",
            use_container_width=True
        ):

            start_game("Easy")

            st.rerun()

    # =====================================================
    # MEDIUM
    # =====================================================

    with col2:

        st.html("""
        <div class="difficulty-card medium">

            <div class="difficulty-icon">
                🟡
            </div>

            <div class="difficulty-name">
                MEDIUM
            </div>

            <div class="difficulty-range">
                Numbers 15 — 100
            </div>

            <div class="difficulty-description">
                Time to think harder
            </div>

        </div>
        """)

        if st.button(
            "🎮 PLAY MEDIUM",
            key="play_medium",
            use_container_width=True
        ):

            start_game("Medium")

            st.rerun()

    # =====================================================
    # HARD
    # =====================================================

    with col3:

        st.html("""
        <div class="difficulty-card hard">

            <div class="difficulty-icon">
                🔴
            </div>

            <div class="difficulty-name">
                HARD
            </div>

            <div class="difficulty-range">
                Numbers 1 — 100
            </div>

            <div class="difficulty-description">
                The ultimate challenge
            </div>

        </div>
        """)

        if st.button(
            "🎮 PLAY HARD",
            key="play_hard",
            use_container_width=True
        ):

            start_game("Hard")

            st.rerun()

    # =====================================================
    # SCORE PREVIEW
    # =====================================================

    st.write("")

    st.html("""
    <div class="best-panel">

        <div class="best-title">
            🏆 YOUR BEST SCORES
        </div>

    </div>
    """)

    score_col1, score_col2, score_col3 = st.columns(3)

    for column, level_name, icon in [
        (score_col1, "Easy", "🟢"),
        (score_col2, "Medium", "🟡"),
        (score_col3, "Hard", "🔴"),
    ]:

        with column:

            score = st.session_state.best_scores[level_name]

            score_text = (
                "—"
                if score is None
                else str(score)
            )

            st.html(f"""
            <div class="score-row">

                <span class="score-level">
                    {icon} {level_name}
                </span>

                <span class="score-number">
                    {score_text}
                </span>

            </div>
            """)

    st.write("")

    if st.button(
        "🗑️ RESET BEST SCORES",
        key="selection_reset_scores",
        use_container_width=True
    ):

        reset_best_scores()

        st.rerun()


# =========================================================
# SCREEN 2 — MAIN GAME
# =========================================================

else:

    level = st.session_state.difficulty

    minimum, maximum = RANGES[level]

    # =====================================================
    # TOP NAVIGATION
    # =====================================================

    nav_left, nav_center, nav_right = st.columns(
        [1, 2, 1]
    )

    with nav_left:

        if st.button(
            "← CHANGE LEVEL",
            key="change_level",
            use_container_width=True
        ):

            change_difficulty()

            st.rerun()

    with nav_center:

        st.html(f"""
        <div class="level-badge">
            {level.upper()} MODE
        </div>
        """)

    with nav_right:

        if st.button(
            "🔄 RESTART",
            key="top_restart",
            use_container_width=True
        ):

            restart_game()

            st.rerun()

    # =====================================================
    # MAIN ARENA
    # =====================================================

    st.html(f"""
    <div class="game-arena">

        <div class="game-heading-big">
            🎯 GUESS NOW
        </div>

        <div class="game-heading-small">
            Find the secret number
            and beat your best score
        </div>

        <div class="range-display">

            <div class="range-label">
                SECRET NUMBER RANGE
            </div>

            <div class="range-number">
                {minimum} — {maximum}
            </div>

        </div>

    </div>
    """)

    # =====================================================
    # GAME STATS
    # =====================================================

    stat1, stat2, stat3 = st.columns(3)

    with stat1:

        st.html(f"""
        <div class="stat-card">

            <div class="stat-value">
                {st.session_state.attempts}
            </div>

            <div class="stat-label">
                ATTEMPTS
            </div>

        </div>
        """)

    with stat2:

        best = st.session_state.best_scores[level]

        best_text = (
            "—"
            if best is None
            else str(best)
        )

        st.html(f"""
        <div class="stat-card">

            <div class="stat-value">
                {best_text}
            </div>

            <div class="stat-label">
                BEST SCORE
            </div>

        </div>
        """)

    with stat3:

        st.html(f"""
        <div class="stat-card">

            <div class="stat-value">
                {minimum}-{maximum}
            </div>

            <div class="stat-label">
                RANGE
            </div>

        </div>
        """)

    # =====================================================
    # NUMBER INPUT
    # =====================================================

    if not st.session_state.game_over:

        with st.form(
            "main_game_form",
            clear_on_submit=False
        ):

            guess = st.number_input(
                "ENTER YOUR NUMBER",
                min_value=minimum,
                max_value=maximum,
                value=None,
                step=1,
                placeholder=(
                    f"Type a number from "
                    f"{minimum} to {maximum}"
                ),
            )

            submitted = st.form_submit_button(
                "🎯 GUESS",
                use_container_width=True
            )

        if submitted:

            if guess is None:

                st.warning(
                    "🎯 Please enter a number first."
                )

            else:

                check_guess(int(guess))

                st.rerun()

    # =====================================================
    # FEEDBACK
    # =====================================================

    if st.session_state.message:

        message = st.session_state.message

        message_type = (
            st.session_state.message_type
        )

        if message_type == "success":

            st.html(f"""
            <div class="feedback-box success-box">
                {message}
            </div>
            """)

        elif message_type == "higher":

            st.html(f"""
            <div class="feedback-box higher-box">
                {message}
            </div>
            """)

        elif message_type == "lower":

            st.html(f"""
            <div class="feedback-box lower-box">
                {message}
            </div>
            """)

    # =====================================================
    # GAME OVER
    # =====================================================

    if st.session_state.game_over:

        st.write("")

        play_again, change_level = st.columns(2)

        with play_again:

            if st.button(
                "🎮 PLAY AGAIN",
                key="game_play_again",
                use_container_width=True
            ):

                restart_game()

                st.rerun()

        with change_level:

            if st.button(
                "🎚️ CHANGE LEVEL",
                key="game_change_level",
                use_container_width=True
            ):

                change_difficulty()

                st.rerun()

    # =====================================================
    # CURRENT BEST SCORE
    # =====================================================

    st.write("")

    current_best = st.session_state.best_scores[level]

    current_best_text = (
        "No score yet"
        if current_best is None
        else f"{current_best} attempts"
    )

    st.html(f"""
    <div class="best-panel">

        <div class="best-title">
            🏆 {level.upper()} BEST
        </div>

        <div class="best-current">

            <div class="best-current-number">
                {current_best_text}
            </div>

            <div class="best-current-label">
                FEWEST ATTEMPTS
            </div>

        </div>

    </div>
    """)


# =========================================================
# FOOTER
# =========================================================

st.html("""
<div class="footer">
    🎯 KEEP GUESSING • KEEP IMPROVING • HAVE FUN
</div>
""")