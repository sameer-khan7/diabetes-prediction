import streamlit as st
import login
import prediction
import dashboard

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "login"

# Top navigation bar
def show_top_bar():
    st.sidebar.markdown("---")
    st.sidebar.button("Log Out", on_click=logout)

# Logout functionality
def logout():
    st.session_state.page = "login"
    st.session_state.pop("username", None)  # Clear logged-in user data
    st.experimental_rerun()

# Navigation logic
if st.session_state.page == "login":
    login.login_page()
elif st.session_state.page == "prediction":
    show_top_bar()  # Show logout button in the sidebar
    prediction.prediction_page()
elif st.session_state.page == "dashboard":
    show_top_bar()  # Show logout button in the sidebar
    dashboard.dashboard_page()
