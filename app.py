# app.py
import streamlit as st
from src.auth import AuthSystem
from src.utils import load_css

class EcommerceApp:
    def __init__(self):
        self.configure_page()
    
    def configure_page(self):
        # SINGLE CONFIGURATION POINT
        st.set_page_config(
            page_title="E-Commerce Admin Portal",
            page_icon="🛒",
            layout="wide",
            initial_sidebar_state="auto",
            menu_items={
                'Get Help': 'https://example.com/help',
                'Report a bug': 'https://example.com/bug',
                'About': "### E-Commerce Admin Dashboard"
            }
        )
        load_css()
    
    def run(self):
        # Your existing navigation logic
        if 'user' not in st.session_state:
            st.switch_page("pages/6_Auth.py")
        else:
            if st.session_state.user.get('is_admin'):
                st.switch_page("pages/7_Admin.py")
            else:
                st.switch_page("pages/1_Home.py")

if __name__ == "__main__":
    app = EcommerceApp()
    app.run()