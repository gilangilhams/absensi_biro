import streamlit as st
import os
import sqlite3
import pandas as pd
from init_db import init_database

# Initialize database on startup
init_database()

# Mencari path folder tempat script ini berjalan
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Jika file ini ada di dalam folder 'pages', kita harus naik satu tingkat
if "pages" in BASE_DIR:
    DB_PATH = os.path.join(os.path.dirname(BASE_DIR), 'absensi_biro.db')
else:
    DB_PATH = os.path.join(BASE_DIR, 'absensi_biro.db')

def jalankan_query(sql, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(sql, conn, params=params)


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