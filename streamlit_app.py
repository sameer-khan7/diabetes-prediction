import streamlit as st
import login
import prediction
import dashboard
import user_management

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "login"

# Navigation logic
if st.session_state.page == "login":
    login.login_page()
elif st.session_state.page == "prediction":
    prediction.prediction_page()
elif st.session_state.page == "profile":
    user_management.profile_page()
elif st.session_state.page == "dashboard":
    dashboard.dashboard_page()
