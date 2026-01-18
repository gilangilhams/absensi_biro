import streamlit as st
import sqlite3
import pandas as pd

# 1. CSS untuk menyembunyikan navigasi bawaan dan mempercantik tampilan
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stButton>button {width: 100%;}
    .danger-box {
        padding: 20px;
        border: 2px solid #ff4b4b;
        border-radius: 10px;
        background-color: #fff1f1;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Fungsi Database
def jalankan_query(sql, params=()):
    with sqlite3.connect('absensi_biro.db') as conn:
        return pd.read_sql_query(sql, conn, params=params)

def eksekusi_sql(sql, params=()):
    with sqlite3.connect('absensi_biro.db') as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

st.title("📊 Portal Admin")

# 3. Sidebar Navigasi
with st.sidebar:
    st.subheader("Menu Admin")
    if st.button("🏠 Kembali ke Menu Utama"):
        st.switch_page("app.py")
    st.divider()
    if st.session_state.get('admin_logged_in'):
        if st.button("🔓 Logout"):
            st.session_state['admin_logged_in'] = False
            st.rerun()

# 4. Logika Login
if 'admin_logged_in' not in st.session_state:
    st.session_state['admin_logged_in'] = False

if not st.session_state['admin_logged_in']:
    st.subheader("Login Otoritas Admin")
    user_adm = st.text_input("Username")
    pass_adm = st.text_input("Password", type="password")
    if st.button("Login Admin"):
        res = jalankan_query("SELECT * FROM ADMIN WHERE USERNAME=? AND PASSWORD=?", (user_adm, pass_adm))
        if not res.empty:
            st.session_state['admin_logged_in'] = True
            st.rerun()
        else:
            st.error("Akses Ditolak!")

# 5. Dashboard Admin (Jika Sudah Login)
else:
    # --- SUSUNAN TAB (URUTAN BARU) ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Rekapitulasi Absensi", 
        "🔍 Analisis Siswa",
        "📥 Upload Data Siswa", 
        "⚙️ Pengaturan Data"
    ])

    # --- TAB 1: REKAPITULASI ---
    with tab1:
        st.write("### Rekapitulasi Pembelajaran Bulanan")
        bln_list = {"Januari":"01","Februari":"02","Maret":"03","April":"04","Mei":"05","Juni":"06","Juli":"07","Agustus":"08","September":"09","Oktober":"10","November":"11","Desember":"12"}
        
        col1, col2, col3 = st.columns(3)
        bln = col1.selectbox("Pilih Bulan", bln_list.keys())
        thn = col2.selectbox("Pilih Tahun", ["2026", "2027", "2028"])
        
        df_kelas = jalankan_query("SELECT DISTINCT KELAS FROM SISWA")
        filter_kelas = col3.selectbox("Filter Kelas", ["Semua"] + list(df_kelas['KELAS']))

        where_clause = f"WHERE strftime('%m', A.TANGGAL)='{bln_list[bln]}' AND strftime('%Y', A.TANGGAL)='{thn}'"
        if filter_kelas != "Semua":
            where_clause += f" AND S.KELAS='{filter_kelas}'"

        query_rekap = f"""
            SELECT 
                S.KELAS, 
                S.NAMA_SISWA,
                SUM(CASE WHEN A.STATUS = 'Hadir' THEN 1 ELSE 0 END) as KEHADIRAN,
                IFNULL(
                    GROUP_CONCAT(DISTINCT CASE WHEN A.STATUS = 'Hadir' THEN M.NAMA_MAPEL END), 
                    'Tidak ada mapel'
                ) as MAPEL_DIIKUTI,
                IFNULL(
                    GROUP_CONCAT(DISTINCT CASE WHEN A.STATUS = 'Hadir' THEN A.TOPIK_MATERI END), 
                    '-'
                ) as TOPIK_PELAJARAN
            FROM SISWA S
            LEFT JOIN ABSENSI A ON S.ID_SISWA = A.ID_SISWA
            LEFT JOIN MAPEL M ON A.ID_MAPEL = M.ID_MAPEL
            {where_clause}
            GROUP BY S.ID_SISWA, S.NAMA_SISWA, S.KELAS
            ORDER BY S.KELAS ASC, S.NAMA_SISWA ASC
        """
        df = jalankan_query(query_rekap)
        cari_nama = st.text_input("🔍 Cari Nama Siswa", placeholder="Ketik nama siswa...")
        if cari_nama:
            df = df[df['NAMA_SISWA'].str.contains(cari_nama, case=False)]

        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Laporan CSV", csv, f"Rekap_{bln}_{thn}.csv", "text/csv")
        else:
            st.warning("Data tidak ditemukan untuk periode ini.")

    # --- TAB 2: ANALISIS SISWA (PINDAH KE POSISI 2) ---
    with tab2:
        st.write("### 🔍 Analisis Individu Siswa")
        st.info("Cari nama siswa untuk melihat frekuensi kehadiran di setiap mata pelajaran.")

        df_semua_siswa = jalankan_query("SELECT ID_SISWA, NAMA_SISWA, KELAS FROM SISWA ORDER BY NAMA_SISWA ASC")
        
        if not df_semua_siswa.empty:
            opsi_siswa = {f"{row['NAMA_SISWA']} ({row['KELAS']})": row['ID_SISWA'] for _, row in df_semua_siswa.iterrows()}
            pilih_siswa_label = st.selectbox("Pilih atau Ketik Nama Siswa", ["-- Pilih Siswa --"] + list(opsi_siswa.keys()))

            if pilih_siswa_label != "-- Pilih Siswa --":
                id_siswa_pilihan = opsi_siswa[pilih_siswa_label]
                
                query_analisis = """
                    SELECT 
                        M.NAMA_MAPEL as 'Mata Pelajaran',
                        COUNT(*) as 'Total Kehadiran',
                        GROUP_CONCAT(A.TANGGAL, ', ') as 'Tanggal Kehadiran'
                    FROM ABSENSI A
                    JOIN MAPEL M ON A.ID_MAPEL = M.ID_MAPEL
                    WHERE A.ID_SISWA = ? AND A.STATUS = 'Hadir'
                    GROUP BY M.ID_MAPEL
                    ORDER BY COUNT(*) DESC
                """
                
                df_hasil = jalankan_query(query_analisis, (int(id_siswa_pilihan),))

                if not df_hasil.empty:
                    st.write(f"#### Hasil Analisis untuk: {pilih_siswa_label}")
                    total_semua_hadir = df_hasil['Total Kehadiran'].sum()
                    st.metric("Total Seluruh Kehadiran", f"{total_semua_hadir} Kali")

                    st.dataframe(
                        df_hasil,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Total Kehadiran": st.column_config.NumberColumn(format="%d ✨"),
                            "Tanggal Kehadiran": st.column_config.TextColumn("Detail Tanggal")
                        }
                    )
                    
                    csv_siswa = df_hasil.to_csv(index=False).encode('utf-8')
                    st.download_button(label="📥 Download Data Analisis Siswa", data=csv_siswa, file_name=f"Analisis_{pilih_siswa_label.replace(' ', '_')}.csv", mime="text/csv")
                else:
                    st.warning(f"Siswa {pilih_siswa_label} belum memiliki catatan kehadiran ('Hadir').")
        else:
            st.error("Data siswa tidak ditemukan.")

    # --- TAB 3: UPLOAD DATA SISWA (PINDAH KE POSISI 3) ---
    with tab3:
        st.write("### 📥 Import Data Siswa dari Excel")
        st.info("Pastikan file Excel memiliki header: **ID_SISWA, NAMA_SISWA, KELAS**")
        
        file_excel = st.file_uploader("Pilih file Excel (.xlsx)", type=["xlsx"])
        
        if file_excel:
            try:
                df_upload = pd.read_excel(file_excel)
                st.write("Preview data yang akan diupload:")
                st.dataframe(df_upload.head(), use_container_width=True)
                
                if st.button("🚀 Konfirmasi Simpan ke Database"):
                    with sqlite3.connect('absensi_biro.db') as conn:
                        df_upload.to_sql('SISWA', conn, if_exists='append', index=False)
                    st.success(f"✅ Berhasil mengupload {len(df_upload)} siswa!")
                    st.balloons()
            except Exception as e:
                st.error(f"Gagal memproses file: {e}")
        st.divider()

        st.write("### 📋 Daftar & Manajemen Siswa")
        query_siswa = """
            SELECT FALSE as Pilih, S.ID_SISWA, S.NAMA_SISWA, S.KELAS, 
                   IFNULL(GROUP_CONCAT(DISTINCT M.NAMA_MAPEL), 'Belum ada data') as MATA_PELAJARAN
            FROM SISWA S
            LEFT JOIN ABSENSI A ON S.ID_SISWA = A.ID_SISWA
            LEFT JOIN MAPEL M ON A.ID_MAPEL = M.ID_MAPEL
            GROUP BY S.ID_SISWA
            ORDER BY S.KELAS ASC, S.NAMA_SISWA ASC
        """
        df_siswa = jalankan_query(query_siswa)
        
        cari_siswa = st.text_input("🔍 Cari Nama Siswa dalam Tabel", placeholder="Ketik nama untuk memfilter...")
        df_filtered = df_siswa.copy()
        if cari_siswa:
            df_filtered = df_filtered[df_filtered['NAMA_SISWA'].str.contains(cari_siswa, case=False)]

        edited_df = st.data_editor(
            df_filtered,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Pilih": st.column_config.CheckboxColumn("Pilih", default=False),
                "ID_SISWA": None,
                "NAMA_SISWA": "Nama Siswa",
                "KELAS": "Kelas",
                "MATA_PELAJARAN": "Mata Pelajaran"
            },
            disabled=["ID_SISWA", "NAMA_SISWA", "KELAS", "MATA_PELAJARAN"]
        )

        items_to_delete = edited_df[edited_df['Pilih'] == True]
        if not items_to_delete.empty:
            st.warning(f"⚠️ Anda memilih {len(items_to_delete)} siswa untuk dihapus.")
            pw_verif = st.text_input("Masukkan Password Admin untuk konfirmasi hapus", type="password")
            
            if st.button("🗑️ Hapus Siswa Terpilih", type="primary"):
                res_pw = jalankan_query("SELECT * FROM ADMIN WHERE PASSWORD=?", (pw_verif,))
                if not res_pw.empty:
                    try:
                        list_id = items_to_delete['ID_SISWA'].tolist()
                        with sqlite3.connect('absensi_biro.db') as conn:
                            cursor = conn.cursor()
                            cursor.executemany("DELETE FROM SISWA WHERE ID_SISWA=?", [(i,) for i in list_id])
                            cursor.executemany("DELETE FROM ABSENSI WHERE ID_SISWA=?", [(i,) for i in list_id])
                            conn.commit()
                        st.success(f"✅ {len(list_id)} siswa berhasil dihapus!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal menghapus: {e}")
                else:
                    st.error("❌ Password salah!")

    # --- TAB 4: PENGATURAN (POSISI TERAKHIR) ---
    with tab4:
        st.write("### ⚠️ Zona Bahaya (Danger Zone)")
        st.info("Fitur ini akan menghapus seluruh data absensi. Harap verifikasi identitas Anda.")

        if 'status_hapus' not in st.session_state:
            st.session_state.status_hapus = False

        if not st.session_state.status_hapus:
            if st.button("🗑️ Kosongkan Tabel Absensi", type="primary"):
                st.session_state.status_hapus = True
                st.rerun()
        else:
            st.warning("🚨 **VERIFIKASI DIPERLUKAN**: Masukkan password admin untuk menghapus.")
            verifikasi_pw = st.text_input("Masukkan Password Admin", type="password")
            
            col_ya, col_batal = st.columns(2)
            with col_ya:
                if st.button("✅ KONFIRMASI & HAPUS", use_container_width=True):
                    res = jalankan_query("SELECT * FROM ADMIN WHERE PASSWORD=?", (verifikasi_pw,))
                    if not res.empty:
                        try:
                            eksekusi_sql("DELETE FROM ABSENSI")
                            eksekusi_sql("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'ABSENSI'")
                            st.success("Tabel Absensi Berhasil Dikosongkan!")
                            st.session_state.status_hapus = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"Gagal: {e}")
                    else:
                        st.error("❌ Password Salah!")
            with col_batal:
                if st.button("❌ BATAL", use_container_width=True):
                    st.session_state.status_hapus = False
                    st.rerun()