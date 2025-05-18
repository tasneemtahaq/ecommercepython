import streamlit as st
from src.auth import AuthSystem
from src.utils import load_css
import re
from config import Config

def validate_email(email):
    """Basic email validation using regex"""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

def show():
    load_css()
    st.title("🔐 Account Authentication")
    
    auth = AuthSystem()
    tab_login, tab_register = st.tabs(["Sign In", "Create Account"])

    with tab_login:
        with st.form("login_form", clear_on_submit=True):
            st.subheader("Existing Users")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Sign In →", use_container_width=True):
                with st.spinner("Authenticating..."):
                    user = auth.login_user(username, password)
                    if user:
                        st.session_state.user = {
                            "id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "is_admin": user.is_admin
                        }
                        st.switch_page("pages/7_Admin.py" if user.is_admin else "pages/1_Home.py")
                    else:
                        st.error("Invalid username or password")

    with tab_register:
        with st.form("register_form", clear_on_submit=True):
            st.subheader("New Users")
            new_user = st.text_input("New Username")
            new_pass = st.text_input("New Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")
            email = st.text_input("Email")
            
            if st.form_submit_button("Create Account →", use_container_width=True):
                if not all([new_user, new_pass, confirm_pass, email]):
                    st.error("All fields are required")
                elif new_pass != confirm_pass:
                    st.error("Passwords don't match")
                elif len(new_pass) < 8:
                    st.error("Password must be 8+ characters")
                elif not validate_email(email):
                    st.error("Invalid email format")
                else:
                    if auth.register_user(new_user, new_pass, email):
                        st.success("Account created! Please login")
                    else:
                        st.error("Username already exists")

    if Config.ENV == "development":
        st.markdown("---")
        with st.expander("Admin Credentials (Dev Only)"):
            st.code(f"Username: {Config.ADMIN_USERNAME}\nPassword: {Config.ADMIN_PASSWORD}")

if __name__ == "__main__":
    show()