import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    """Test database connection"""
    try:
        # Get database URL from .env
        db_url = os.getenv('DATABASE_URL')
        
        # Parse connection string
        # Format: postgresql://username:password@host/database
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Database connection successful!")
        print(f"📊 PostgreSQL version: {version[0]}")
        
        # Check tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"\n📋 Tables in database:")
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
