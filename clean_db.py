import sqlite3
import os

# Kosongkan semua data tapi keep schema
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'absensi_biro.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    # Disable foreign key checks temporarily
    cursor.execute("PRAGMA foreign_keys = OFF")
    
    # Delete all data dari setiap tabel
    cursor.execute("DELETE FROM LOG_ABSENSI")
    cursor.execute("DELETE FROM ABSENSI")
    cursor.execute("DELETE FROM SISWA")
    cursor.execute("DELETE FROM GURU")
    cursor.execute("DELETE FROM MAPEL")
    cursor.execute("DELETE FROM ADMIN")
    
    # Reset auto-increment
    cursor.execute("DELETE FROM sqlite_sequence")
    
    # Re-enable foreign key checks
    cursor.execute("PRAGMA foreign_keys = ON")
    
    conn.commit()
    print("✅ Database cleaned! All data removed, schema kept.")
    
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    conn.close()
