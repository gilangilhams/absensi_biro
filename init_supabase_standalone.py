"""
Initialize Supabase database tables - standalone version
"""

import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL tidak ditemukan di .env")
    exit(1)

def init_supabase():
    """Create all tables di Supabase"""
    
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    try:
        print("🔄 Creating tables...")
        
        # Create MAPEL table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS MAPEL (
            ID_MAPEL SERIAL PRIMARY KEY,
            NAMA_MAPEL TEXT NOT NULL
        )
        """)
        print("✅ MAPEL table created")
        
        # Create GURU table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS GURU (
            ID_GURU SERIAL PRIMARY KEY,
            NAMA_GURU TEXT NOT NULL,
            NO_TELP TEXT UNIQUE,
            ID_MAPEL INTEGER REFERENCES MAPEL(ID_MAPEL),
            PASSWORD TEXT UNIQUE
        )
        """)
        print("✅ GURU table created")
        
        # Create ADMIN table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ADMIN (
            ID_ADMIN SERIAL PRIMARY KEY,
            USERNAME TEXT NOT NULL UNIQUE,
            PASSWORD TEXT NOT NULL,
            NAMA_ADMIN TEXT
        )
        """)
        print("✅ ADMIN table created")
        
        # Create SISWA table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS SISWA (
            ID_SISWA SERIAL PRIMARY KEY,
            NAMA_SISWA TEXT NOT NULL,
            KELAS TEXT NOT NULL
        )
        """)
        print("✅ SISWA table created")
        
        # Create ABSENSI table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ABSENSI (
            ID_ABSEN SERIAL PRIMARY KEY,
            TANGGAL DATE DEFAULT CURRENT_DATE,
            ID_SISWA INTEGER REFERENCES SISWA(ID_SISWA),
            ID_GURU INTEGER REFERENCES GURU(ID_GURU),
            ID_MAPEL INTEGER REFERENCES MAPEL(ID_MAPEL),
            TOPIK_MATERI TEXT,
            STATUS TEXT
        )
        """)
        print("✅ ABSENSI table created")
        
        # Create LOG_ABSENSI table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS LOG_ABSENSI (
            ID_LOG SERIAL PRIMARY KEY,
            ID_ABSEN_LAMA INTEGER,
            AKSI TEXT,
            USER_PELAKU TEXT,
            WAKTU_KEJADIAN TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            KETERANGAN TEXT
        )
        """)
        print("✅ LOG_ABSENSI table created")
        
        # Create default admin
        cursor.execute("SELECT * FROM ADMIN WHERE USERNAME = %s", ('admin',))
        if cursor.fetchone() is None:
            admin_user = os.getenv("ADMIN_USERNAME", "admin")
            admin_pass = os.getenv("ADMIN_PASSWORD", "admin123")
            admin_name = os.getenv("ADMIN_NAME", "Administrator")
            
            cursor.execute(
                "INSERT INTO ADMIN (USERNAME, PASSWORD, NAMA_ADMIN) VALUES (%s, %s, %s)",
                (admin_user, admin_pass, admin_name)
            )
            print(f"✅ Default admin '{admin_user}' created")
        
        conn.commit()
        print("\n✅ SUPABASE INITIALIZATION COMPLETE!")
        print("✅ Database ready to use")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    init_supabase()
