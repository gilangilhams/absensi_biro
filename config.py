import streamlit as st
import os

def get_admin_credentials():
    """Get admin credentials from Streamlit secrets or environment variables"""
    try:
        # Try to get from Streamlit secrets first
        admin_user = st.secrets.get("admin_username", os.getenv("ADMIN_USERNAME", "admin"))
        admin_pass = st.secrets.get("admin_password", os.getenv("ADMIN_PASSWORD", "admin123"))
        admin_name = st.secrets.get("admin_name", os.getenv("ADMIN_NAME", "Administrator"))
    except Exception:
        # Fallback to environment variables
        admin_user = os.getenv("ADMIN_USERNAME", "admin")
        admin_pass = os.getenv("ADMIN_PASSWORD", "admin123")
        admin_name = os.getenv("ADMIN_NAME", "Administrator")
    
    return admin_user, admin_pass, admin_name
