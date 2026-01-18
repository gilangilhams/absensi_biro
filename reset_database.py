import sqlite3

def hapus_data_absen():
    # Menghubungkan ke database
    conn = sqlite3.connect('absensi_biro.db')
    cursor = conn.cursor()
    
    print("Mencoba menghapus data...")
    
    try:
        # 1. Hapus isi tabel ABSENSI secara paksa
        cursor.execute("DELETE FROM ABSENSI")
        
        # 2. Reset urutan ID ke angka 1
        cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'ABSENSI'")
        
        conn.commit()
        print("✅ BERHASIL: Semua data di tabel ABSENSI telah dihapus dan ID kembali ke 1.")
        
    except sqlite3.OperationalError as e:
        print(f"❌ ERROR: {e}")
        print("Tip: Pastikan tabel 'ABSENSI' memang ada di database Anda.")
        
    except Exception as e:
        print(f"❌ Terjadi kesalahan lain: {e}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    hapus_data_absen()