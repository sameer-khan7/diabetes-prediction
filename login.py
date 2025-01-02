import streamlit as st
import sqlite3
import bcrypt

def login_page():
    # Ensure that the session state is initialized properly
    if "login_username" not in st.session_state:
        st.session_state["login_username"] = ""
    if "login_password" not in st.session_state:
        st.session_state["login_password"] = ""
    if "signup_username" not in st.session_state:
        st.session_state["signup_username"] = ""
    if "signup_password" not in st.session_state:
        st.session_state["signup_password"] = ""

    st.title("Login Page")

    # Database Connection
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Login Section
    st.subheader("Log In")
    username = st.text_input("Username", value=st.session_state.login_username, key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log In"):
        if username and password:
            c.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = c.fetchone()
            if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
                st.session_state.page = "Prediction"
                st.session_state.username = username
                st.success("Login successful! Redirecting...")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password.")
        else:
            st.error("Please fill out all fields.")

    # Sign-Up Section
    st.subheader("Sign Up")
    new_username = st.text_input("New Username", value=st.session_state.signup_username, key="signup_username")
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
