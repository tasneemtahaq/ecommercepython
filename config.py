import os
from dotenv import load_dotenv

load_dotenv()  # This must be at the top

class Config:
    # Existing configurations
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # Stripe configurations
    STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")  # Add this line
    
    # Admin configurations
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
    ENV = os.getenv("ENV", "production")

    @staticmethod
    def verify_stripe():
        if not Config.STRIPE_SECRET_KEY:
            raise ValueError("STRIPE_SECRET_KEY missing from environment")
        if not Config.STRIPE_PUBLIC_KEY:
            raise ValueError("STRIPE_PUBLIC_KEY missing from environment")