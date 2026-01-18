import sqlite3
import os

def init_database():
    """Initialize database with required tables if they don't exist"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, 'absensi_biro.db')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Create ADMIN table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ADMIN (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            USERNAME TEXT UNIQUE NOT NULL,
            PASSWORD TEXT NOT NULL,
            NAMA_ADMIN TEXT NOT NULL
        )
        """)
        
        # Create GURU table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS GURU (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            USERNAME TEXT UNIQUE NOT NULL,
            PASSWORD TEXT NOT NULL,
            NAMA_GURU TEXT NOT NULL,
            NIP TEXT UNIQUE,
            BIDANG_STUDI TEXT
        )
        """)
        
        # Create ABSENSI table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ABSENSI (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_GURU INTEGER NOT NULL,
            TANGGAL DATE NOT NULL,
            STATUS TEXT NOT NULL,
            KETERANGAN TEXT,
            FOREIGN KEY (ID_GURU) REFERENCES GURU(ID)
        )
        """)
        
        # Check if default admin exists, if not create it
        cursor.execute("SELECT * FROM ADMIN WHERE USERNAME = ?", ('admin',))
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO ADMIN (USERNAME, PASSWORD, NAMA_ADMIN) VALUES (?, ?, ?)",
                ('admin', 'admin123', 'Administrator')
            )
        
        conn.commit()
        print("✅ Database initialized successfully!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_database()
