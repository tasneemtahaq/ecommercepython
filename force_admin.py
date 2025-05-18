# force_admin.py
from src.database import Session, User
from config import Config
import bcrypt

def force_create_admin():
    session = Session()
    
    # Delete any existing admin
    session.query(User).filter(User.username == Config.ADMIN_USERNAME).delete()
    
    # Create new admin with verified parameters
    hashed = bcrypt.hashpw(
        Config.ADMIN_PASSWORD.encode('utf-8'),
        bcrypt.gensalt()
    )
    admin = User(
        username=Config.ADMIN_USERNAME,
        password=hashed.decode('utf-8'),
        email=Config.ADMIN_EMAIL,
        is_admin=True
    )
    
    session.add(admin)
    session.commit()
    session.close()
    print("Admin forcefully created")

if __name__ == "__main__":
    force_create_admin()