"""
Setup script untuk migrate data dari SQLite ke Supabase
Gunakan ini setelah Anda setup Supabase connection
"""

import sqlite3
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

SQLITE_DB = 'absensi_biro.db'
POSTGRES_URL = os.getenv('DATABASE_URL')

if not POSTGRES_URL:
    print("❌ DATABASE_URL tidak ditemukan. Setup Supabase dulu!")
    exit(1)

def migrate_data():
    """Migrate data dari SQLite ke PostgreSQL/Supabase"""
    
    # Connect ke SQLite
    sqlite_conn = sqlite3.connect(SQLITE_DB)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cursor = sqlite_conn.cursor()
    
    # Connect ke Supabase
    pg_conn = psycopg2.connect(POSTGRES_URL)
    pg_cursor = pg_conn.cursor()
    
    try:
        print("🔄 Memulai migrasi data...")
        
        # Migrate MAPEL
        sqlite_cursor.execute("SELECT * FROM MAPEL")
        mapel_data = sqlite_cursor.fetchall()
        for row in mapel_data:
            pg_cursor.execute(
                "INSERT INTO MAPEL (ID_MAPEL, NAMA_MAPEL) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (row['ID_MAPEL'], row['NAMA_MAPEL'])
            )
        print(f"✅ Migrated {len(mapel_data)} records dari MAPEL")
        
        # Migrate GURU
        sqlite_cursor.execute("SELECT * FROM GURU")
        guru_data = sqlite_cursor.fetchall()
        for row in guru_data:
            pg_cursor.execute(
                "INSERT INTO GURU (ID_GURU, NAMA_GURU, NO_TELP, ID_MAPEL, PASSWORD) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                (row['ID_GURU'], row['NAMA_GURU'], row['No_Telp'], row['ID_MAPEL'], row['PASSWORD'])
            )
        print(f"✅ Migrated {len(guru_data)} records dari GURU")
        
        # Migrate ADMIN
        sqlite_cursor.execute("SELECT * FROM ADMIN")
        admin_data = sqlite_cursor.fetchall()
        for row in admin_data:
            pg_cursor.execute(
                "INSERT INTO ADMIN (ID_ADMIN, USERNAME, PASSWORD, NAMA_ADMIN) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                (row['ID_ADMIN'], row['USERNAME'], row['PASSWORD'], row['NAMA_ADMIN'])
            )
        print(f"✅ Migrated {len(admin_data)} records dari ADMIN")
        
        # Migrate SISWA
        sqlite_cursor.execute("SELECT * FROM SISWA")
        siswa_data = sqlite_cursor.fetchall()
        for row in siswa_data:
            pg_cursor.execute(
                "INSERT INTO SISWA (ID_SISWA, NAMA_SISWA, KELAS) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                (row['ID_SISWA'], row['NAMA_SISWA'], row['KELAS'])
            )
        print(f"✅ Migrated {len(siswa_data)} records dari SISWA")
        
        # Migrate ABSENSI
        sqlite_cursor.execute("SELECT * FROM ABSENSI")
        absensi_data = sqlite_cursor.fetchall()
        for row in absensi_data:
            pg_cursor.execute(
                "INSERT INTO ABSENSI (ID_ABSEN, TANGGAL, ID_SISWA, ID_GURU, ID_MAPEL, TOPIK_MATERI, STATUS) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                (row['ID_ABSEN'], row['TANGGAL'], row['ID_SISWA'], row['ID_GURU'], row['ID_MAPEL'], row['TOPIK_MATERI'], row['STATUS'])
            )
        print(f"✅ Migrated {len(absensi_data)} records dari ABSENSI")
        
        # Migrate LOG_ABSENSI
        sqlite_cursor.execute("SELECT * FROM LOG_ABSENSI")
        log_data = sqlite_cursor.fetchall()
        for row in log_data:
            pg_cursor.execute(
                "INSERT INTO LOG_ABSENSI (ID_LOG, ID_ABSEN_LAMA, AKSI, USER_PELAKU, WAKTU_KEJADIAN, KETERANGAN) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                (row['ID_LOG'], row['ID_ABSEN_LAMA'], row['AKSI'], row['USER_PELAKU'], row['WAKTU_KEJADIAN'], row['KETERANGAN'])
            )
        print(f"✅ Migrated {len(log_data)} records dari LOG_ABSENSI")
        
        pg_conn.commit()
        print("\n✅ MIGRASI BERHASIL! Data sudah di Supabase")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        pg_conn.rollback()
    finally:
        sqlite_conn.close()
        pg_conn.close()

if __name__ == "__main__":
    migrate_data()
