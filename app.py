import os
from dotenv import load_dotenv

# Load environment variables FIRST before any imports
load_dotenv()

import streamlit as st
import sqlite3
import pandas as pd
import sys
from pathlib import Path

# Try to import Supabase DB, fallback to SQLite
try:
    from supabase_db import db
    USE_SUPABASE = True
except Exception as e:
    print(f"⚠️ Supabase not available: {e}, falling back to SQLite")
    USE_SUPABASE = False

# Fallback: Mencari path folder tempat script ini berjalan
if not USE_SUPABASE:
    from init_db import init_database
    init_database()
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, 'absensi_biro.db')
    
    def jalankan_query(sql, params=()):
        with sqlite3.connect(DB_PATH) as conn:
            return pd.read_sql_query(sql, conn, params=params)
else:
    # Using Supabase
    def jalankan_query(sql, params=()):
        # Convert SQL to PostgreSQL compatible if needed
        result = db.execute_query(sql, params)
        return pd.DataFrame(result) if result else pd.DataFrame()


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