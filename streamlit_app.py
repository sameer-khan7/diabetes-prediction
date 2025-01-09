import streamlit as st
import login
import prediction
import dashboard
import user_management

# Page configuration for better UI/UX
st.set_page_config(
    page_title="Diabetes Prediction App",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "login"

# Tab-based navigation for a better user experience
tabs = st.tabs(["🔑 Login", "📊 Dashboard", "🔮 Prediction", "👤 Profile Management"])

with tabs[0]:  # Login Tab
    login.login_page()

if "logged_in" in st.session_state and st.session_state.logged_in:  # Check login status
    with tabs[1]:  # Dashboard Tab
        dashboard.dashboard_page()
    with tabs[2]:  # Prediction Tab
        prediction.prediction_page()
    with tabs[3]:  # Profile Management Tab
        user_management.profile_page()

