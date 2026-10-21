import streamlit as st
from google import genai

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Asep AI",
    page_icon="🤖",
    layout="centered"
)

# Judul ala Asep AI
st.title("🤖 Asep AI - Asisten Santai")
st.write("Sini cerita bro, aman-aman semua. Ada apa hari lu?")

# Inisialisasi Client Gemini dengan Streamlit Secrets yang aman
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"Waduh Bro, API Key-nya belum diset dengan benar di Secrets: {e}")
    st.stop()

# Sistem instruksi karakter Asep AI
system_instruction = """
Lu adalah Asep AI, asisten virtual yang ramah, santai, menggunakan gaya bahasa gaul 
seperti 'bro', 'woles', 'gaskeun', dan akrab banget sama pengguna.
Tapi tetap bantu jawab pertanyaan atau keluh kesah mereka dengan solutif.
"""

# Simpan riwayat chat di memori sesi Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan pesan chat sebelumnya
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kolom ngetik pesan chat
if user_input := st.chat_input("Tulis keluh kesah atau obrolan lu di sini, Bro..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Kirim ke model Gemini menggunakan SDK google-genai terbaru
    try:
        chat_full_prompt = f"{system_instruction}\n\nUser: {user_input}"
        
        # Menggunakan model standar gemini-2.5-flash yang kompatibel
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=chat_full_prompt,
        )
        ai_reply = response.text
    except Exception as e:
        ai_reply = f"Waduh Bro, lagi ada kendala jaringan nih: {e}"

    with st.chat_message("assistant"):
        st.markdown(ai_reply)
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
