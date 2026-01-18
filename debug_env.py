import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
print("DATABASE_URL from .env:")
print(db_url)
print()

if db_url:
    print("✅ DATABASE_URL found!")
    print(f"Length: {len(db_url)}")
    print(f"Starts with: {db_url[:50]}...")
else:
    print("❌ DATABASE_URL NOT found!")
    print("Checking .env file...")
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            content = f.read()
            print(content)
    else:
        print(".env file not found!")
