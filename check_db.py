import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def check():
    conn = pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", ""),
        db=os.getenv("DB_NAME", "ovaira"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute("DESCRIBE users")
            columns = [row['Field'] for row in cursor.fetchall()]
            print(f"Columns in 'users' table: {columns}")
            
            required = ['gender', 'department', 'license_number']
            missing = [c for c in required if c not in columns]
            
            if missing:
                print(f"⚠️ MISSING COLUMNS: {missing}")
                print("Please run: python migrate_db.py")
            else:
                print("✅ Database schema is up to date!")
    except Exception as e:
        print(f"❌ Error checking database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check()
