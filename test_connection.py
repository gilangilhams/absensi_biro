import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
print(f"Attempting to connect to: {db_url[:50]}...")

try:
    conn = psycopg2.connect(db_url)
    print("✅ Connection successful!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    print(f"PostgreSQL version: {cursor.fetchone()}")
    
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
