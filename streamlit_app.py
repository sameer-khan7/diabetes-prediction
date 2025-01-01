import streamlit as st

# Set default page to Login
if "page" not in st.session_state:
    st.session_state.page = "Login"

# Navigation Logic
if st.session_state.page == "Login":
    import login
elif st.session_state.page == "Prediction":
    import prediction
elif st.session_state.page == "Dashboard":
    import dashboard
