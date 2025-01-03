import streamlit as st
import sqlite3
import pandas as pd

def dashboard_page():
    # Add a navigation button in the sidebar
    st.sidebar.header("Navigation")
    if st.sidebar.button("Go to Prediction"):
        st.session_state.page = "prediction"
        st.rerun()
        
    # Top bar with logout button
    col1, col2 = st.columns([9, 1])
    with col2:
        if st.button("Log Out"):
            st.session_state.page = "login"
            st.session_state.pop("username", None)  # Clear user data
            st.rerun()
            
    st.title("User Dashboard")
    
    # Fetch results from database
    if "username" in st.session_state:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT glucose, bmi, prediction, timestamp FROM results WHERE username = ?", (st.session_state.username,))
        results = c.fetchall()
        conn.close()
        
        if results:
            # Display results in a DataFrame
            df = pd.DataFrame(results, columns=["Glucose", "BMI", "Prediction", "Timestamp"])
            st.write("Your Saved Results:")
            st.dataframe(df, use_container_width=True)
        else:
            st.write("No results saved yet.")
    else:
        st.error("You must be logged in to access the dashboard.")
