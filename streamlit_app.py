import streamlit as st
import login
import prediction
import dashboard
import user_management
import health_report
import admin_dashboard

st.set_page_config(
    page_title="Diabetes Prediction App",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = "login"
if "username" not in st.session_state:
    st.session_state.username = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "new_prediction" not in st.session_state:
    st.session_state.new_prediction = False  # Flag to track if a new prediction was made

# Display Login page if user is not logged in
if not st.session_state.logged_in:
    login.login_page()

else:
    # Define tabs for navigation
    tabs = ["📊 Dashboard", "📄 Health Report", "🔮 Prediction", "👤 Profile Management"]

    # Add the Admin Dashboard tab only for admin
    if st.session_state.username == "admin":
        tabs.append("👩‍💼 Admin Dashboard")

    # Create tabs using Streamlit's tab functionality
    active_tabs = st.tabs(tabs)

    with active_tabs[0]:  # Dashboard
        #if st.session_state.get("new_prediction", False):
            # Reset the flag and reload the dashboard
        #    st.session_state.new_prediction = False
        #   st.rerun()
        dashboard.dashboard_page()

    with active_tabs[1]:  # Health Report
        health_report.health_report_page()

    with active_tabs[2]:  # Prediction
        prediction.prediction_page()

    with active_tabs[3]:  # Profile Management
        user_management.profile_page()

    if "👩‍💼 Admin Dashboard" in tabs:  # Admin Dashboard (only visible for admin)
        with active_tabs[4]:
            admin_dashboard.admin_dashboard_page()
