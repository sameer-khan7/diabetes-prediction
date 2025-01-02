import streamlit as st
import sqlite3
import bcrypt

def login_page():
    st.title("Login Page")

    # Initialize session states for login and sign-up fields
    if "login_username" not in st.session_state:
        st.session_state.login_username = ""
    if "login_password" not in st.session_state:
        st.session_state.login_password = ""
    if "signup_username" not in st.session_state:
        st.session_state.signup_username = ""
    if "signup_password" not in st.session_state:
        st.session_state.signup_password = ""

    # Database Connection
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Login Section
    st.subheader("Log In")
    st.session_state.login_username = st.text_input("Username", key="login_username")
    st.session_state.login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log In"):
        c.execute("SELECT * FROM users WHERE username = ?", (st.session_state.login_username,))
        user = c.fetchone()
        if user and bcrypt.checkpw(st.session_state.login_password.encode('utf-8'), user[1].encode('utf-8')):
            st.session_state.page = "Prediction"
            st.session_state.username = st.session_state.login_username
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

    # Sign-Up Section
    st.subheader("Sign Up")
    with st.form(key="signup_form"):
        st.session_state.signup_username = st.text_input("New Username", key="signup_username", value=st.session_state.signup_username)
        st.session_state.signup_password = st.text_input("New Password", type="password", key="signup_password", value=st.session_state.signup_password)

        # Form Submit Button
        if st.form_submit_button("Sign Up"):
            if st.session_state.signup_username and st.session_state.signup_password:
                hashed_password = bcrypt.hashpw(st.session_state.signup_password.encode('utf-8'), bcrypt.gensalt())
                try:
                    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                              (st.session_state.signup_username, hashed_password.decode('utf-8')))
                    conn.commit()
                    st.success("Account created! Please log in.")
                    st.session_state.signup_username = ""  # Clear after success
                    st.session_state.signup_password = ""
                except sqlite3.IntegrityError:
                    st.error("Username already exists.")
            else:
                st.error("Please fill out all fields.")

    conn.close()

login_page()
