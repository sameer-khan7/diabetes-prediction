import streamlit as st
import login
import prediction

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "login"  # Default page

# Navigation logic
if st.session_state.page == "login":
    login.login_page()
elif st.session_state.page == "prediction":
    prediction.prediction_page()

# Navigation buttons
if st.session_state.page == "prediction":
    if st.button("Log Out"):
        st.session_state.page = "login"
        st.rerun()
