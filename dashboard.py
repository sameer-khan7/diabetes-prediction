import streamlit as st
import sqlite3
import pandas as pd

def dashboard_page():
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
