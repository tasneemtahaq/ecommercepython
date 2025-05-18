import os
from dotenv import load_dotenv
import streamlit as st

class Config:
    try:
        # Try Streamlit secrets first (production)
        DATABASE_URL = st.secrets["database"]["DATABASE_URL"]
        STRIPE_SECRET_KEY = st.secrets["stripe"]["SECRET_KEY"]
        STRIPE_PUBLIC_KEY = st.secrets["stripe"]["PUBLIC_KEY"]
        ADMIN_USERNAME = st.secrets["admin"]["USERNAME"]
        ADMIN_PASSWORD = st.secrets["admin"]["PASSWORD"]
        ADMIN_EMAIL = st.secrets["admin"]["EMAIL"]
        ENV = st.secrets["environment"]["ENV"]
    except Exception:
        # Fall back to .env file (local development)
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL")
        STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
        STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
        ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
        ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
        ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
        ENV = os.getenv("ENV")