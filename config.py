import streamlit as st

class Config:
    # Database
    DATABASE_URL = st.secrets["database"]["DATABASE_URL"]
    
    # Stripe
    STRIPE_SECRET_KEY = st.secrets["stripe"]["SECRET_KEY"]
    STRIPE_PUBLIC_KEY = st.secrets["stripe"]["PUBLIC_KEY"]
    
    # Admin
    ADMIN_USERNAME = st.secrets["admin"]["USERNAME"]
    ADMIN_PASSWORD = st.secrets["admin"]["PASSWORD"]
    ADMIN_EMAIL = st.secrets["admin"]["EMAIL"]
    
    # Environment
    ENV = st.secrets["environment"]["ENV"]