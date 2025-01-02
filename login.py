import streamlit as st
import sqlite3
import bcrypt

# Initialize session state for form inputs
if "login_username" not in st.session_state:
    st.session_state["login_username"] = ""
if "login_password" not in st.session_state:
    st.session_state["login_password"] = ""
if "signup_username" not in st.session_state:
    st.session_state["signup_username"] = ""
if "signup_password" not in st.session_state:
    st.session_state["signup_password"] = ""
if "signup_success" not in st.session_state:
    st.session_state["signup_success"] = False

def login_page():
    st.title("Login Page")

    # Debugging Section - Check reruns
    st.write("Session State Debug:", st.session_state)

    # Database Connection
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Login Section
    with st.form("Login"):
        st.subheader("Log In")
        username = st.text_input("Username", value=st.session_state["login_username"])
        password = st.text_input("Password", type="password", value=st.session_state["login_password"])
        login_btn = st.form_submit_button("Log In")

        if login_btn:
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
    with st.form("Sign Up"):
        st.subheader("Sign Up")
        new_username = st.text_input("New Username", value=st.session_state["signup_username"], key="signup_username")
        new_password = st.text_input("New Password", type="password", value=st.session_state["signup_password"], key="signup_password")
        signup_btn = st.form_submit_button("Sign Up")

        if signup_btn:
            if new_username and new_password:
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                try:
                    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                              (new_username, hashed_password.decode('utf-8')))
                    conn.commit()
                    st.session_state["signup_success"] = True
                    st.success("Account created successfully! Please log in.")
                    # Reset sign-up fields
                    st.session_state["signup_username"] = ""
                    st.session_state["signup_password"] = ""
                except sqlite3.IntegrityError:
                    st.error("Username already exists. Please choose a different username.")
            else:
                st.error("Please fill out all fields.")

    conn.close()

# Run the login page
login_page()
