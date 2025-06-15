import streamlit as st
import json
import random
from utils.cf_engine import evaluate_answer
import time
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="🎮 Siapa Aku?", layout="centered")

# ========================
# CSS Custom Lucu & Warna Cerah
# ========================
st.markdown("""
    <style>
        body {
            background-color: #FFFBF0;
        }
        .big-title {
            font-size: 40px;
            color: #FF6F61;
            font-weight: bold;
        }
        .soal-box {
            background-color: #FFF7D4;
            padding: 20px;
            border-radius: 15px;
            border: 2px dashed #FFD700;
            margin-bottom: 20px;
        }
        .input-box {
            background-color: #FFF;
            border: 2px solid #ADD8E6;
            border-radius: 10px;
            padding: 10px;
        }
        .btn {
            background-color: #FFDDC1;
            color: black;
            border-radius: 10px;
            padding: 10px;
        }
        .stButton>button {
            margin-top: 0px;
            margin-bottom: 0px;
            padding: 0.6em 1.2em;
        }
    </style>
""", unsafe_allow_html=True)

# ========================
# Session State Init
# ========================
if "page" not in st.session_state:
    st.session_state.page = "home"

if "questions" not in st.session_state:
    st.session_state.questions = []

if "show_rules" not in st.session_state:
    st.session_state.show_rules = False

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "score_list" not in st.session_state:
    st.session_state.score_list = []

if "finished" not in st.session_state:
    st.session_state.finished = False

# ========================
# Navigasi Sederhana
# ========================
def go_to(page):
    st.session_state.page = page
    st.rerun()

# ========================
# Halaman Awal
# ========================
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center;'>Siapa Aku? - Game Edukatif CF</h1>", unsafe_allow_html=True)
    st.image("assets/images/wp-master-1.png", use_container_width=True)
    st.markdown("""
    Selamat datang di game **Siapa Aku?** 👧👦  
    🧩 Tebak siapa atau apa yang sedang dijelaskan dari petunjuk yang diberikan!

    👉 Ayo klik tombol di bawah ini untuk mulai bermain!
    """)

    col1, col2 = st.columns([1, 1.5])

    with col1:
        aturan_clicked = st.button("📜 Aturan Bermain", use_container_width=True)

    with col2:
        mulai_clicked = st.button("🚀 Mulai Bermain", type="primary", use_container_width=True)

    if aturan_clicked:
        st.session_state.show_rules = not st.session_state.get("show_rules", False)

    if mulai_clicked:
        with open("data/soal.json", "r") as f:
            all_questions = json.load(f)
        st.session_state.questions = random.sample(all_questions, 10)
        st.session_state.current_index = 0
        st.session_state.score_list = []
        st.session_state.finished = False
        go_to("game")

    if st.session_state.get("show_rules", False):
        st.info("""
        ### 📜 Aturan Main:
        - Akan ada **10 soal** acak yang muncul satu per satu.
        - Jawaban dinilai berdasarkan **kata kunci & kesesuaian jawaban**.
        - Kamu akan lihat hasilnya di akhir yaa 🎉
        """)

# ========================
# Halaman Game dengan Timer
# ========================
elif st.session_state.page == "game":
    idx = st.session_state.current_index
    soal = st.session_state.questions[idx]

    if st.button("🔙 Kembali"):
        go_to("home")

    st_autorefresh(interval=1000, key="auto_refresh")

    if "start_time" not in st.session_state or idx != st.session_state.get("last_idx", -1):
        st.session_state.start_time = time.time()
        st.session_state.last_idx = idx

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, 60 - elapsed)

    # Jika waktu habis otomatis lanjut
    if remaining <= 0:
        st.session_state.score_list.append(0)
        if idx < 9:
            st.session_state.current_index += 1
            st.session_state.start_time = time.time()
            st.rerun()
        else:
            st.session_state.finished = True
            go_to("hasil")
        st.stop()


    # Tampilkan waktu mundur
    st.markdown(f"""
    <div style="text-align: center; padding: 15px; background-color: #ffeaa7; border-radius: 15px; margin-bottom: 20px;">
        <span style="font-size: 18px;">⏰ <strong>Sisa Waktu:</strong></span><br>
        <span style="font-size: 36px; font-weight: bold; color: #d63031;">{remaining} detik</span>
    </div>
    """, unsafe_allow_html=True)
    

    # Jika waktu habis otomatis lanjut
    if remaining == 0:
        st.session_state.score_list.append(0)
        if idx < 9:
            st.session_state.current_index += 1
            st.rerun()
        else:
            st.session_state.finished = True
            go_to("hasil")
        st.stop()

    st.progress((idx + 1) / 10, text=f"✨ Soal {idx + 1} dari 10")

    st.markdown(f"""
    <div class="soal-box">
        <strong>📢 Petunjuk:</strong><br>
        {soal['deskripsi']}
    </div>
    """, unsafe_allow_html=True)

    key_jawaban = f"jawaban_{idx}"
    jawaban = st.text_input("✍️ Tulis jawabanmu di sini ya:", key=key_jawaban)

    if st.button("✅ Jawab"):
        if jawaban.strip() == "":
            st.warning("⚠️ Wah, kamu belum isi jawaban nih!")
        else:
            score, _ = evaluate_answer(jawaban, soal)
            st.session_state.score_list.append(score)

            if idx < 9:
                st.session_state.current_index += 1
                st.rerun()
            else:
                st.session_state.finished = True
                go_to("hasil")

# ========================
# Halaman Hasil
# ========================
elif st.session_state.page == "hasil":
    st.balloons()
    st.markdown("## 🌟 Permainan Selesai!")
    st.markdown("### Ini hasil kamu ya:")

    total_score = sum(st.session_state.score_list)
    max_score = len(st.session_state.score_list)
    percent = int((total_score / max_score) * 100)

    st.metric(label="🎯 Skor Akhir", value=f"{percent}%", delta=f"{int(total_score)} dari {max_score} benar")

    if percent == 100:
        st.success("🏆 Hebat banget! Semua benar 🎉")
    elif percent >= 70:
        st.info("😊 Bagus! Kamu sudah pintar.")
    elif percent >= 40:
        st.warning("😅 Lumayan, masih bisa belajar lagi ya!")
    else:
        st.error("😭 Ayo semangat belajar lagi ya!")

    if st.button("🔁 Main Lagi"):
        go_to("home")
