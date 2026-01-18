import sqlite3
import os

def init_database():
    """Initialize database with required tables if they don't exist"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, 'absensi_biro.db')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Create MAPEL table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS MAPEL (
            ID_MAPEL INTEGER NOT NULL,
            NAMA_MAPEL TEXT NOT NULL,
            PRIMARY KEY(ID_MAPEL AUTOINCREMENT)
        )
        """)
        
        # Create GURU table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS GURU (
            ID_GURU INTEGER NOT NULL,
            NAMA_GURU TEXT NOT NULL,
            No_Telp INTEGER UNIQUE,
            ID_MAPEL INTEGER,
            PASSWORD INTEGER UNIQUE,
            PRIMARY KEY(ID_GURU AUTOINCREMENT),
            FOREIGN KEY(ID_MAPEL) REFERENCES MAPEL(ID_MAPEL)
        )
        """)
        
        # Create ADMIN table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ADMIN (
            ID_ADMIN INTEGER,
            USERNAME TEXT NOT NULL UNIQUE,
            PASSWORD TEXT NOT NULL,
            NAMA_ADMIN TEXT,
            PRIMARY KEY(ID_ADMIN AUTOINCREMENT)
        )
        """)
        
        # Create SISWA table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS SISWA (
            ID_SISWA INTEGER PRIMARY KEY AUTOINCREMENT,
            NAMA_SISWA TEXT NOT NULL,
            KELAS TEXT NOT NULL
        )
        """)
        
        # Create ABSENSI table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ABSENSI (
            ID_ABSEN INTEGER,
            TANGGAL TEXT DEFAULT (DATE('now')),
            ID_SISWA INTEGER,
            ID_GURU INTEGER,
            ID_MAPEL INTEGER,
            TOPIK_MATERI TEXT,
            STATUS TEXT,
            PRIMARY KEY(ID_ABSEN AUTOINCREMENT),
            FOREIGN KEY(ID_GURU) REFERENCES GURU(ID_GURU),
            FOREIGN KEY(ID_MAPEL) REFERENCES MAPEL(ID_MAPEL),
            FOREIGN KEY(ID_SISWA) REFERENCES SISWA(ID_SISWA)
        )
        """)
        
        # Create LOG_ABSENSI table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS LOG_ABSENSI (
            ID_LOG INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_ABSEN_LAMA INTEGER,
            AKSI TEXT,
            USER_PELAKU TEXT,
            WAKTU_KEJADIAN DATETIME DEFAULT CURRENT_TIMESTAMP,
            KETERANGAN TEXT
        )
        """)
        
        # Check if default admin exists, if not create it with environment variables
        cursor.execute("SELECT * FROM ADMIN WHERE USERNAME = ?", ('admin',))
        if cursor.fetchone() is None:
            # Read from environment variables with fallback values
            admin_user = os.getenv('ADMIN_USERNAME', 'admin')
            admin_pass = os.getenv('ADMIN_PASSWORD', 'admin123')
            admin_name = os.getenv('ADMIN_NAME', 'Administrator')
            
            cursor.execute(
                "INSERT INTO ADMIN (USERNAME, PASSWORD, NAMA_ADMIN) VALUES (?, ?, ?)",
                (admin_user, admin_pass, admin_name)
            )
        
        conn.commit()
        
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_database()

