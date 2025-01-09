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

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Display Login page if user is not logged in
if not st.session_state.logged_in:
    st.title("Welcome to the Diabetes Prediction App")
    st.caption("🔒 Please log in or sign up to access the app.")
    login.login_page()

else:
    # Tab-based navigation for logged-in users
    tabs = st.tabs(["📊 Dashboard", "🔮 Prediction", "👤 Profile Management"])

    with tabs[0]:  # Dashboard Tab
        dashboard.dashboard_page()
    with tabs[1]:  # Prediction Tab
        prediction.prediction_page()
    with tabs[2]:  # Profile Management Tab
        user_management.profile_page()
