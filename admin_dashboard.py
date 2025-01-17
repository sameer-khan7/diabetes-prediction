import streamlit as st
import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.db')

def admin_dashboard_page():

    # Improved Logout Button
    st.markdown(
        """
        <style>
        .logout-button {
            display: flex;
            justify-content: flex-end;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    logout_container = st.container()
    with logout_container:
        st.markdown('<div class="logout-button">', unsafe_allow_html=True)
        if st.button("🔒 Log Out", key="logout_button_admin"):
            st.session_state.page = "login"
            st.session_state.logged_in = False  # Reset logged-in status
            st.session_state.pop("username", None)  # Clear session data
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.title("👩‍💼 Admin Dashboard")
    st.markdown("Welcome to the Admin Dashboard. Here, you can manage users and predictions.")

    conn = sqlite3.connect(DB_PATH)
    users_df = pd.read_sql_query("SELECT * FROM users", conn)
    predictions_df = pd.read_sql_query("SELECT * FROM results", conn)
    conn.close()

    # Display user data
    st.subheader("All Users")
    st.dataframe(users_df, use_container_width=True)

    # User Management
    st.subheader("Manage Users")
    selected_user = st.selectbox("Select a User to Manage", users_df["username"])
    if st.button("Delete User"):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE username = ?", (selected_user,))
        conn.commit()
        conn.close()
        st.success(f"User {selected_user} deleted successfully!")
        st.rerun()

    # Display predictions
    st.subheader("All Predictions")
    st.dataframe(predictions_df, use_container_width=True)
