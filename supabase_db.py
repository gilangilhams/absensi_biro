import os
import psycopg2
import psycopg2.extras
from contextlib import contextmanager
from sql_converter import convert_sql_for_postgres

class SupabaseDB:
    def __init__(self):
        """Initialize Supabase connection"""
        # Try to get DATABASE_URL from environment or streamlit secrets
        self.db_url = os.getenv("DATABASE_URL")
        
        # If not found in env, try streamlit secrets (only if streamlit is available)
        if not self.db_url:
            try:
                import streamlit as st
                self.db_url = st.secrets.get("database_url")
            except:
                pass
        
        if not self.db_url:
            raise ValueError("DATABASE_URL not found in environment variables or Streamlit secrets")
    
    @contextmanager
    def get_connection(self):
        """Get database connection context manager"""
        try:
            conn = psycopg2.connect(self.db_url)
        except (psycopg2.OperationalError, Exception) as e:
            # Connection failed - re-raise so caller can handle it
            raise ConnectionError(f"Failed to connect to Supabase: {e}")
        try:
            yield conn
        finally:
            conn.close()
    
    def execute_query(self, query, params=None):
        """Execute query that returns results"""
        # Convert SQLite syntax to PostgreSQL if needed
        query, params = convert_sql_for_postgres(query, params)
        
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def execute_update(self, query, params=None):
        """Execute query that modifies data"""
        # Convert SQLite syntax to PostgreSQL if needed
        query, params = convert_sql_for_postgres(query, params)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
    
    def init_tables(self):
        """Create all required tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                # Create MAPEL table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS MAPEL (
                    ID_MAPEL SERIAL PRIMARY KEY,
                    NAMA_MAPEL TEXT NOT NULL
                )
                """)
                
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
                
                # Create ADMIN table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS ADMIN (
                    ID_ADMIN SERIAL PRIMARY KEY,
                    USERNAME TEXT NOT NULL UNIQUE,
                    PASSWORD TEXT NOT NULL,
                    NAMA_ADMIN TEXT
                )
                """)
                
                # Create SISWA table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS SISWA (
                    ID_SISWA SERIAL PRIMARY KEY,
                    NAMA_SISWA TEXT NOT NULL,
                    KELAS TEXT NOT NULL
                )
                """)
                
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
                
                conn.commit()
                print("✅ Tables created/verified successfully")
                
            except Exception as e:
                print(f"❌ Error creating tables: {e}")
                conn.rollback()
    
    def check_admin_exists(self):
        """Check if default admin exists"""
        result = self.execute_query("SELECT * FROM ADMIN WHERE USERNAME = %s", ('admin',))
        return len(result) > 0
    
    def create_default_admin(self):
        """Create default admin if not exists"""
        if not self.check_admin_exists():
            # Read from secrets
            try:
                admin_user = st.secrets.get("admin_username", "admin")
                admin_pass = st.secrets.get("admin_password", "admin123")
                admin_name = st.secrets.get("admin_name", "Administrator")
            except:
                admin_user = os.getenv("ADMIN_USERNAME", "admin")
                admin_pass = os.getenv("ADMIN_PASSWORD", "admin123")
                admin_name = os.getenv("ADMIN_NAME", "Administrator")
            
            self.execute_update(
                "INSERT INTO ADMIN (USERNAME, PASSWORD, NAMA_ADMIN) VALUES (%s, %s, %s)",
                (admin_user, admin_pass, admin_name)
            )
            print(f"✅ Default admin '{admin_user}' created")

# Create global instance
db = SupabaseDB()
