from sqlalchemy.exc import SQLAlchemyError
from src.database import Session, User
import bcrypt
from config import Config

class AuthSystem:
    def __init__(self):
        self.session = Session()
        self.ensure_admin_exists()

    def ensure_admin_exists(self):
        """Create admin user if missing"""
        admin = self.session.query(User).filter_by(username=Config.ADMIN_USERNAME).first()
        if not admin:
            hashed = bcrypt.hashpw(Config.ADMIN_PASSWORD.encode(), bcrypt.gensalt())
            new_admin = User(
                username=Config.ADMIN_USERNAME,
                password=hashed.decode(),
                email=Config.ADMIN_EMAIL,
                is_admin=True
            )
            self.session.add(new_admin)
            self.session.commit()

    def login_user(self, username: str, password: str):
        try:
            user = self.session.query(User).filter_by(username=username).first()
            
            if user and bcrypt.checkpw(password.encode(), user.password.encode()):
                return user
            
            # Handle admin special case
            if username == Config.ADMIN_USERNAME:
                self.ensure_admin_exists()
                user = self.session.query(User).filter_by(username=username).first()
                if user and bcrypt.checkpw(password.encode(), user.password.encode()):
                    return user
            
            return None
        except SQLAlchemyError as e:
            print(f"Database error: {str(e)}")
            return None

    def register_user(self, username: str, password: str, email: str):
        try:
            if self.session.query(User).filter_by(username=username).first():
                return False
                
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            new_user = User(
                username=username,
                password=hashed.decode(),
                email=email,
                is_admin=False
            )
            self.session.add(new_user)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Registration error: {str(e)}")
            return False