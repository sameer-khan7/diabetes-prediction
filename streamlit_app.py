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

# Display Login page if user is not logged in
if not st.session_state.logged_in:
    login.login_page()
else:
    # Tab-based navigation
    tabs = ["📊 Dashboard", "📄 Health Report", "🔮 Prediction", "👤 Profile Management"]
    
    # Add the Admin Dashboard tab only for admin
    if st.session_state.username == "admin":
        tabs.insert(2, "👩‍💼 Admin Dashboard")
    
    selected_tab = st.selectbox("Select a Page", tabs, key="tab_selection")

    if selected_tab == "📊 Dashboard":
        dashboard.dashboard_page()
    elif selected_tab == "📄 Health Report":
        health_report.health_report_page()
    elif selected_tab == "👩‍💼 Admin Dashboard" and st.session_state.username == "admin":
        admin_dashboard.admin_dashboard_page()
    elif selected_tab == "🔮 Prediction":
        prediction.prediction_page()
    elif selected_tab == "👤 Profile Management":
        user_management.profile_page()
