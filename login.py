import streamlit as st
import sqlite3
import bcrypt

def login_page():
    st.title("Login Page")

    # Initialize session state for form inputs
    if "new_username" not in st.session_state:
        st.session_state.new_username = ""
    if "new_password" not in st.session_state:
        st.session_state.new_password = ""

    # Database Connection
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Login Form
    st.subheader("Log In")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log In"):
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            st.session_state.page = "Prediction"
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

    # Sign-Up Form
    st.subheader("Sign Up")
    new_username = st.text_input("New Username", key="signup_username", value=st.session_state.new_username)
    new_password = st.text_input("New Password", type="password", key="signup_password", value=st.session_state.new_password)

    # Save the input values to session state
    st.session_state.new_username = new_username
    st.session_state.new_password = new_password

    if st.button("Sign Up"):
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, hashed_password.decode('utf-8')))
            conn.commit()
            st.success("Account created! Please log in.")
            # Clear session state for sign-up fields
            st.session_state.new_username = ""
            st.session_state.new_password = ""
        except sqlite3.IntegrityError:
            st.error("Username already exists.")
    
    conn.close()

login_page()
