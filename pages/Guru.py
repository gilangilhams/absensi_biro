import os
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Try to import Supabase DB, fallback to SQLite
try:
    from supabase_db import db
    USE_SUPABASE = True
except Exception as e:
    print(f"⚠️ Supabase not available: {e}, falling back to SQLite")
    USE_SUPABASE = False

if not USE_SUPABASE:
    from init_db import init_database
    init_database()
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    if "pages" in BASE_DIR:
        DB_PATH = os.path.join(os.path.dirname(BASE_DIR), 'absensi_biro.db')
    else:
        DB_PATH = os.path.join(BASE_DIR, 'absensi_biro.db')
    
    def jalankan_query(sql, params=()):
        with sqlite3.connect(DB_PATH) as conn:
            return pd.read_sql_query(sql, conn, params=params)
    
    def eksekusi_sql(sql, params=()):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
else:
    def jalankan_query(sql, params=()):
        result = db.execute_query(sql, params)
        return pd.DataFrame(result) if result else pd.DataFrame()
    
    def eksekusi_sql(sql, params=()):
        db.execute_update(sql, params)

# --- TAMPILAN ---
st.set_page_config(page_title="Portal Guru", layout="centered")

# Sembunyikan sidebar navigasi asli
st.markdown("""<style>[data-testid="stSidebarNav"] {display: none;}</style>""", unsafe_allow_html=True)

st.title("👨‍🏫 Portal Guru - ABSENSI")

with st.sidebar:
    st.subheader("Menu Guru")
    if st.button("🏠 Kembali ke Menu Utama"):
        st.switch_page("app.py")
    st.divider()

# --- LOGIKA LOGIN ---
if 'guru_logged_in' not in st.session_state:
    st.session_state['guru_logged_in'] = False

if not st.session_state['guru_logged_in']:
    st.subheader("Login Guru")
    df_mapel = jalankan_query("SELECT ID_MAPEL, NAMA_MAPEL FROM MAPEL")
    opsi_mapel = {row['NAMA_MAPEL']: row['ID_MAPEL'] for index, row in df_mapel.iterrows()}
    
    sel_mapel = st.selectbox("Pilih Mata Pelajaran", opsi_mapel.keys())
    pw = st.text_input("Password", type="password")
    
    if st.button("Masuk"):
        res = jalankan_query("""
            SELECT G.*, M.NAMA_MAPEL 
            FROM GURU G 
            JOIN MAPEL M ON G.ID_MAPEL = M.ID_MAPEL 
            WHERE G.ID_MAPEL=? AND G.PASSWORD=?""", 
            (opsi_mapel[sel_mapel], pw))
            
        if not res.empty:
            st.session_state['guru_logged_in'] = True
            st.session_state['guru_data'] = res.iloc[0]
            st.rerun()
        else:
            st.error("Kombinasi Mapel dan Password salah!")

else:
    user = st.session_state['guru_data']
    st.success(f"Login Aktif: **{user['NAMA_GURU']}** | Mapel: **{user['NAMA_MAPEL']}**")
    
    if st.sidebar.button("🔓 Logout"):
        st.session_state['guru_logged_in'] = False
        st.rerun()

    st.divider()

    # --- BAGIAN 1: PILIH KELAS & TOPIK ---
    col_a, col_b = st.columns(2)
    
    df_kelas = jalankan_query("SELECT DISTINCT KELAS FROM SISWA")
    pilih_kelas = col_a.selectbox("1. Pilih Kelas", df_kelas['KELAS'])
    
    # Ambil tanggal hari ini secara otomatis
    tgl_hari_ini = datetime.now().strftime("%Y-%m-%d")
    col_b.info(f"📅 Tanggal: {tgl_hari_ini}")

    topik = st.text_input("2. Topik Materi", placeholder="Misal: Aljabar, Tenses, atau Praktikum")

    # --- BAGIAN 2: TABEL ABSENSI MASSAL ---
    st.write("### Presensi Siswa")
    st.info("💡 Siswa yang **Hadir** wajib dicentang. Siswa tidak dicentang otomatis dianggap **Tidak Memilih Mapel**.")
    
    # Ambil data siswa berdasarkan kelas yang dipilih
    df_siswa_kelas = jalankan_query(
        "SELECT ID_SISWA, NAMA_SISWA FROM SISWA WHERE KELAS = ? ORDER BY NAMA_SISWA ASC", 
        (pilih_kelas,)
    )
    
    # Tambahkan kolom 'Presensi' dengan default False (kosong)
    df_siswa_kelas['Presensi'] = False

    # --- TAMBAHAN: FITUR SEARCH BAR ---
    cari_nama = st.text_input("🔍 Cari Nama Siswa di Kelas Ini", placeholder="Ketik nama siswa untuk mempermudah pencarian...")
    
    # Logika Filter berdasarkan input pencarian
    df_tampil = df_siswa_kelas.copy()
    if cari_nama:
        df_tampil = df_tampil[df_tampil['NAMA_SISWA'].str.contains(cari_nama, case=False)]

    # Editor Tabel menggunakan dataframe yang sudah difilter
    edited_df = st.data_editor(
        df_tampil,
        column_config={
            "Presensi": st.column_config.CheckboxColumn(
                "Hadir?", 
                help="Centang jika siswa hadir",
                default=False
            ),
            "ID_SISWA": None, 
            "NAMA_SISWA": "Nama Lengkap Siswa"
        },
        disabled=["NAMA_SISWA"],
        use_container_width=True,
        hide_index=True,
        key="editor_guru_search"
    )

    # Indikator Visual (Mengacu pada editor yang sedang dikerjakan)
    total_siswa_tampil = len(edited_df)
    total_hadir = edited_df['Presensi'].sum()
    
    st.write(f"📊 **Terpantau:** `{total_hadir}` siswa hadir dari daftar yang muncul.")

    # Indikator Visual (Warna Metrik)
    total_siswa = len(edited_df)
    total_hadir = edited_df['Presensi'].sum()
    total_luar_mapel = total_siswa - total_hadir
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Total Siswa", total_siswa)
    col_m2.metric("Hadir ✅", total_hadir)
    # Warna delta inverse untuk menandai jumlah yang 'tidak memilih mapel'
    col_m3.metric("Luar Mapel ⚪", total_luar_mapel, delta="-", delta_color="off")

    # --- BAGIAN 3: PROSES SIMPAN ---
    st.divider()
    if st.button("💾 Simpan Data Absensi", use_container_width=True, type="primary"):
        if not topik:
            st.error("⚠️ Topik Materi belum diisi!")
        else:
            with st.spinner('Menyimpan ke sistem...'):
                try:
                    for index, row in edited_df.iterrows():
                        # LOGIKA STATUS BARU: Jika tidak dicentang, status menjadi "Tidak Memilih Mapel"
                        status_final = "Hadir" if row['Presensi'] else "Tidak Memilih Mapel"
                        
                        eksekusi_sql(
                            """INSERT INTO ABSENSI 
                               (ID_SISWA, ID_GURU, ID_MAPEL, TOPIK_MATERI, STATUS, TANGGAL) 
                               VALUES (?,?,?,?,?,?)""",
                            (int(row['ID_SISWA']), int(user['ID_GURU']), 
                             int(user['ID_MAPEL']), topik, status_final, tgl_hari_ini)
                        )
                    st.success(f"✅ Absensi kelas {pilih_kelas} berhasil disimpan dengan status yang sesuai!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Gagal simpan: {e}")