import streamlit as st
import sqlite3
import bcrypt

def login_page():
    st.title("Login Page")

    # Database Connection
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Login Section
    st.subheader("Log In")
    username = st.text_input("Username", key="login_username")  # Use key to track state
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log In"):
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            st.session_state.page = "Prediction"
            st.session_state.username = username  # Store the username in session state
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

    # Sign-Up Section
    st.subheader("Sign Up")
    new_username = st.text_input("New Username", key="signup_username")
    new_password = st.text_input("New Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        if new_username and new_password:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            try:
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                          (new_username, hashed_password.decode('utf-8')))
                conn.commit()
                st.success("Account created! Please log in.")
            except sqlite3.IntegrityError:
                st.error("Username already exists.")
        else:
            st.error("Please fill out all fields.")

    conn.close()

login_page()
