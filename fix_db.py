import sqlite3

def bersihkan():
    conn = sqlite3.connect('absensi_biro.db')
    cursor = conn.cursor()
    
    # 1. Mencari semua Trigger (perintah otomatis) yang ada di database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='trigger'")
    semua_trigger = cursor.fetchall()
    
    # 2. Hapus semua trigger tersebut agar database kembali normal
    for t in semua_trigger:
        cursor.execute(f"DROP TRIGGER IF EXISTS {t[0]}")
        print(f"✅ Berhasil menghapus trigger: {t[0]}")
    
    conn.commit()
    conn.close()
    print("--- Database sekarang sudah bersih dari error CURRENT_SESSION ---")

if __name__ == "__main__":
    bersihkan()