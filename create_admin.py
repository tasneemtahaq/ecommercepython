# create_admin.py
from src.database import Session
from src.database import User
from src.auth import AuthSystem
from config import Config

def create_admin_user():
    """Create admin user from configuration"""
    try:
        auth = AuthSystem()  # This auto-creates admin if missing
        session = Session()
        
        # Verify admin exists
        admin = session.query(User).filter_by(username=Config.ADMIN_USERNAME).first()
        
        if admin:
            print(f"✅ Admin user exists:\nUsername: {admin.username}\nEmail: {admin.email}")
        else:
            print("❌ Admin creation failed - check database connection")
            
    except Exception as e:
        print(f"⚠️ Error creating admin: {str(e)}")

if __name__ == "__main__":
    create_admin_user()