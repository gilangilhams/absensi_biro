import streamlit as st

st.set_page_config(page_title="Sistem Absensi", layout="centered")

# CSS ini untuk menyembunyikan tulisan 'pages' di samping secara paksa
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

st.title("🏫 Sistem Absensi Biro")
st.write("Silakan pilih pintu masuk Anda:")

col1, col2 = st.columns(2)

with col1:
    if st.button("🚪 MASUK SEBAGAI GURU", use_container_width=True):
        st.switch_page("pages/Guru.py") # Pastikan filenya bernama Guru.py

with col2:
    if st.button("🔐 MASUK SEBAGAI ADMIN", use_container_width=True):
        st.switch_page("pages/Admin.py") # Pastikan filenya bernama Admin.py