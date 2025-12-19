import streamlit as st
import numpy as np
from PIL import Image
import time
import utils
from utils import load_model, predict_gesture, determine_winner, get_emoji_for_choice, manual_gesture_selection

# Page configuration
st.set_page_config(
    page_title="Batu Gunting Kertas - 2 Pemain",
    page_icon="✊✌️✋",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .game-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .player-section {
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .player1-section {
        background-color: #e3f2fd;
        border: 2px solid #1976d2;
    }
    .player2-section {
        background-color: #f3e5f5;
        border: 2px solid #7b1fa2;
    }
    .result-section {
        text-align: center;
        padding: 2rem;
        border-radius: 10px;
        margin: 2rem 0;
    }
    .winner-section {
        background-color: #e8f5e8;
        border: 2px solid #4caf50;
    }
    .tie-section {
        background-color: #fff3e0;
        border: 2px solid #ff9800;
    }
    .choice-emoji {
        font-size: 4rem;
        text-align: center;
    }
    .confidence-score {
        font-size: 0.9rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'welcome'
if 'player1_choice' not in st.session_state:
    st.session_state.player1_choice = None
if 'player1_image' not in st.session_state:
    st.session_state.player1_image = None
if 'player1_confidence' not in st.session_state:
    st.session_state.player1_confidence = 0
if 'player2_choice' not in st.session_state:
    st.session_state.player2_choice = None
if 'player2_image' not in st.session_state:
    st.session_state.player2_image = None
if 'player2_confidence' not in st.session_state:
    st.session_state.player2_confidence = 0
if 'player1_score' not in st.session_state:
    st.session_state.player1_score = 0
if 'player2_score' not in st.session_state:
    st.session_state.player2_score = 0

# Load model
load_model()

def reset_game():
    """Reset the game state"""
    st.session_state.game_state = 'welcome'
    st.session_state.player1_choice = None
    st.session_state.player1_image = None
    st.session_state.player1_confidence = 0
    st.session_state.player2_choice = None
    st.session_state.player2_image = None
    st.session_state.player2_confidence = 0

def start_new_round():
    """Start a new round keeping scores"""
    st.session_state.game_state = 'player1_turn'
    st.session_state.player1_choice = None
    st.session_state.player1_image = None
    st.session_state.player1_confidence = 0
    st.session_state.player2_choice = None
    st.session_state.player2_image = None
    st.session_state.player2_confidence = 0

def welcome_screen():
    """Display welcome screen"""
    st.markdown('<div class="game-title">✊✌️✋ Batu Gunting Kertas ✊✌️✋</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
        ### Selamat Datang di Permainan 2 Pemain!

        **Cara Bermain:**
        1. Pemain 1 memilih batu, gunting, atau kertas
        2. Pemain 2 memilih batu, gunting, atau kertas
        3. Pemenang akan diumumkan!

        **Aturan:**
        - 🗿 Batu menghancurkan Gunting ✌️
        - ✌️ Gunting memotong Kertas ✋
        - ✋ Kertas membungkus Batu 🗿

        Gunakan kamera atau unggah foto untuk membuat pilihan Anda!
        """)

        if st.button("🎮 Mulai Bermain", type="primary", use_container_width=True):
            st.session_state.game_state = 'player1_turn'
            st.rerun()

def player_turn(player_num):
    """Handle player turn"""
    player_name = f"Pemain {player_num}"
    player_class = f"player{player_num}-section"

    st.markdown(f'<div class="player-section {player_class}">', unsafe_allow_html=True)
    st.markdown(f"### 🎯 Giliran {player_name}")
    st.markdown(f"Silakan pilih Batu ✊, Gunting ✌️, atau Kertas ✋")

    # Check if model is available
    load_model()  # This will set the warning if model fails to load

    # Always use camera/upload - with fallback to simple classifier
    st.info("🤖 **AI Detection**: Menggunakan AI untuk mendeteksi gesture Anda. Model akan bekerja secara otomatis.")

    # Input method selection
    input_method = st.radio(
        f"Metode Input {player_name}:",
        ["📸 Kamera", "📁 Upload Foto"],
        key=f"input_method_{player_num}"
    )

    captured_image = None

    if input_method == "📸 Kamera":
        camera_image = st.camera_input(
            f"📸 Ambil Foto {player_name}",
            key=f"camera_{player_num}"
        )
        if camera_image:
            captured_image = Image.open(camera_image)
    else:
        uploaded_file = st.file_uploader(
            f"📁 Upload Foto {player_name}",
            type=['jpg', 'jpeg', 'png'],
            key=f"upload_{player_num}"
        )
        if uploaded_file:
            captured_image = Image.open(uploaded_file)

    if captured_image is not None:
        # Display the captured image
        st.image(captured_image, caption=f"Pilihan {player_name}", width=300)

        # Process the image
        with st.spinner(f"🤖 AI sedang menganalisis pilihan {player_name}..."):
            prediction, confidence = predict_gesture(captured_image)

            if prediction and confidence > 0.3:  # Lower confidence threshold for simple classifier
                # Store player choice
                if player_num == 1:
                    st.session_state.player1_choice = prediction
                    st.session_state.player1_image = captured_image
                    st.session_state.player1_confidence = confidence
                else:
                    st.session_state.player2_choice = prediction
                    st.session_state.player2_image = captured_image
                    st.session_state.player2_confidence = confidence

                # Display prediction
                emoji = get_emoji_for_choice(prediction)
                st.markdown(f"### {emoji} {prediction.capitalize()}")
                st.markdown(f'<div class="confidence-score">AI Confidence: {confidence:.2%}</div>', unsafe_allow_html=True)

                # Continue button
                if st.button(f"✅ Lanjutkan", key=f"continue_{player_num}", type="primary"):
                    if player_num == 1:
                        st.session_state.game_state = 'player2_turn'
                    else:
                        st.session_state.game_state = 'results'
                    st.rerun()
            else:
                st.error("❌ Tidak dapat mendeteksi pilihan dengan pasti. Silakan coba lagi.")
                st.info("💡 Tips: Pastikan gesture Anda jelas (Batu = kepal tangan, Gunting = 2 jari, Kertas = tangan terbuka)")

                # Show manual selection as fallback
                st.markdown("---")
                manual_prediction, manual_confidence = manual_gesture_selection(player_name)

                if st.button(f"🔄 Gunakan Pilihan Manual {player_name}", key=f"manual_{player_num}"):
                    # Store manual choice
                    if player_num == 1:
                        st.session_state.player1_choice = manual_prediction
                        st.session_state.player1_image = captured_image
                        st.session_state.player1_confidence = manual_confidence
                    else:
                        st.session_state.player2_choice = manual_prediction
                        st.session_state.player2_image = captured_image
                        st.session_state.player2_confidence = manual_confidence

                    # Move to next state
                    if player_num == 1:
                        st.session_state.game_state = 'player2_turn'
                    else:
                        st.session_state.game_state = 'results'
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

def results_screen():
    """Display results and winner"""
    st.markdown('<div class="game-title">🏆 Hasil Pertandingan 🏆</div>', unsafe_allow_html=True)

    # Display both players' choices
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="player-section player1-section">', unsafe_allow_html=True)
        st.markdown("### 👤 Pemain 1")
        if st.session_state.player1_image:
            st.image(st.session_state.player1_image, width=250)
        else:
            # Demo mode - show placeholder
            st.markdown("### 🎮 Mode Demo")
        emoji1 = get_emoji_for_choice(st.session_state.player1_choice)
        st.markdown(f'<div class="choice-emoji">{emoji1}</div>', unsafe_allow_html=True)
        st.markdown(f"### {st.session_state.player1_choice.capitalize()}")
        st.markdown(f'<div class="confidence-score">Confidence: {st.session_state.player1_confidence:.2%}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="player-section player2-section">', unsafe_allow_html=True)
        st.markdown("### 👥 Pemain 2")
        if st.session_state.player2_image:
            st.image(st.session_state.player2_image, width=250)
        else:
            # Demo mode - show placeholder
            st.markdown("### 🎮 Mode Demo")
        emoji2 = get_emoji_for_choice(st.session_state.player2_choice)
        st.markdown(f'<div class="choice-emoji">{emoji2}</div>', unsafe_allow_html=True)
        st.markdown(f"### {st.session_state.player2_choice.capitalize()}")
        st.markdown(f'<div class="confidence-score">Confidence: {st.session_state.player2_confidence:.2%}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Determine winner
    try:
        winner, winner_text, result_text = determine_winner(
            st.session_state.player1_choice,
            st.session_state.player2_choice
        )
    except Exception as e:
        st.error(f"Error determining winner: {e}")
        # Fallback to tie if there's an error
        winner = 'tie'
        winner_text = None
        result_text = "Terjadi kesalahan dalam menentukan pemenang."

    # Display winner
    if winner == 'player1':
        st.session_state.player1_score += 1
        result_class = "winner-section"
        result_title = "🎉 Pemain 1 Menang!"
    elif winner == 'player2':
        st.session_state.player2_score += 1
        result_class = "winner-section"
        result_title = "🎉 Pemain 2 Menang!"
    else:
        result_class = "tie-section"
        result_title = "🤝 Seri!"

    st.markdown(f'<div class="result-section {result_class}">', unsafe_allow_html=True)
    st.markdown(f"## {result_title}")
    if winner_text:
        st.markdown(f"### {winner_text}")
    else:
        st.markdown(f"### {result_text}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Display score
    st.markdown("### 📊 Skor Saat Ini")
    score_col1, score_col2, score_col3 = st.columns([1, 1, 1])
    with score_col1:
        st.metric("Pemain 1", st.session_state.player1_score)
    with score_col2:
        st.metric("Pemain 2", st.session_state.player2_score)
    with score_col3:
        st.metric("Total Rondes", st.session_state.player1_score + st.session_state.player2_score)

    # Action buttons
    button_col1, button_col2 = st.columns(2)
    with button_col1:
        if st.button("🔄 Main Lagi", type="primary", use_container_width=True):
            start_new_round()
            st.rerun()
    with button_col2:
        if st.button("🏠 Kembali ke Menu", use_container_width=True):
            reset_game()
            st.rerun()

def show_sidebar():
    """Display sidebar with game info"""
    with st.sidebar:
        st.markdown("## 📋 Informasi Game")

        st.markdown("### 🎮 Cara Bermain")
        st.markdown("""
        1. Pemain 1 membuat pilihan
        2. Pemain 2 membuat pilihan
        3. Sistem akan menentukan pemenang
        """)

        st.markdown("### 📜 Aturan")
        st.markdown("""
        - 🗿 **Batu** menghancurkan Gunting ✌️
        - ✌️ **Gunting** memotong Kertas ✋
        - ✋ **Kertas** membungkus Batu 🗿
        """)

        st.markdown("### 💡 Tips")
        st.markdown("""
        - Pastikan pencahayaan cukup
        - Tangan terlihat jelas
        - Latar belakang sederhana
        """)

        if st.session_state.player1_score > 0 or st.session_state.player2_score > 0:
            st.markdown("### 🏆 Skor")
            st.metric("Pemain 1", st.session_state.player1_score)
            st.metric("Pemain 2", st.session_state.player2_score)

# Main game logic
show_sidebar()

# Display different screens based on game state
if st.session_state.game_state == 'welcome':
    welcome_screen()
elif st.session_state.game_state == 'player1_turn':
    player_turn(1)
elif st.session_state.game_state == 'player2_turn':
    player_turn(2)
elif st.session_state.game_state == 'results':
    results_screen()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; margin-top: 2rem;'>"
    "Dibuat dengan ❤️ menggunakan Streamlit dan Teachable Machine"
    "</div>",
    unsafe_allow_html=True
)