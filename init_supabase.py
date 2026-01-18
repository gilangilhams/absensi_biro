"""
Initialize Supabase database tables
Run this ONCE to create all tables
"""

from supabase_db import db

print("🔄 Initializing Supabase tables...")
db.init_tables()
db.create_default_admin()
print("✅ Supabase initialization complete!")
