from src.database import Session, User
from config import Config
import bcrypt

def verify_admin():
    session = Session()
    
    # Check admin existence
    admin = session.query(User).filter_by(username=Config.ADMIN_USERNAME).first()
    
    if not admin:
        print("❌ Admin user not found in database")
        return False
    
    # Verify password hash
    password_valid = bcrypt.checkpw(
        Config.ADMIN_PASSWORD.encode(),
        admin.password.encode()
    )
    
    print(f"🔑 Password match: {password_valid}")
    print(f"👑 Admin status: {admin.is_admin}")
    print(f"🔒 Hashed password: {admin.password}")
    
    return password_valid and admin.is_admin

if __name__ == "__main__":
    if verify_admin():
        print("✅ Admin credentials are valid")
    else:
        print("❌ Admin configuration issue detected")