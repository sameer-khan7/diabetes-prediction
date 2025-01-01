import streamlit as st
import sqlite3
import pandas as pd

def dashboard_page():
    st.title("User Dashboard")
    
    # Fetch results from database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT glucose, bmi, prediction, timestamp FROM results WHERE username = ?", (st.session_state.username,))
    results = c.fetchall()
    conn.close()
    
    if results:
        df = pd.DataFrame(results, columns=["Glucose", "BMI", "Prediction", "Timestamp"])
        st.write("Your Saved Results:")
        st.dataframe(df)
    else:
        st.write("No results saved yet.")
    
dashboard_page()
