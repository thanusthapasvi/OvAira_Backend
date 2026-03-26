import pymysql
import sys

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "ovaira"
}

def check_db():
    print("Checking database connection...")
    try:
        conn = pymysql.connect(**db_config)
        print("✅ Database connection successful.")
        
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES LIKE 'users'")
        table = cursor.fetchone()
        
        if not table:
            print("❌ 'users' table NOT FOUND!")
            return
            
        print("✅ 'users' table found. Checking columns...")
        cursor.execute("DESCRIBE users")
        columns = [row[0] for row in cursor.fetchall()]
        print("Columns found:", columns)
        
        required_columns = ["full_name", "email", "mobile", "password_hash", "otp", "otp_expiry", "is_verified"]
        missing = [col for col in required_columns if col not in columns]
        
        if missing:
             print(f"❌ Missing columns: {missing}")
        else:
             print("✅ All required columns present.")
             
        conn.close()
        
    except pymysql.err.OperationalError as e:
        print(f"❌ Connection failed: {e}")
        print("Make sure XAMPP/MySQL is running.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    check_db()
