import sqlite3

def tambah_admin(user, pw, nama):
    conn = sqlite3.connect('absensi_biro.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO ADMIN (USERNAME, PASSWORD, NAMA_ADMIN) VALUES (?, ?, ?)", (user, pw, nama))
        conn.commit()
        print(f"Admin {nama} berhasil ditambahkan!")
    except Exception as e:
        print(f"Gagal: {e}")
    finally:
        conn.close()

# Masukkan data admin baru di sini
tambah_admin('admin', 'admin123', 'admin testing')