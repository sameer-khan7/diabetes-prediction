import streamlit as st
import sqlite3
import bcrypt

def login_page():
    # Initialize session state variables
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None

    # Database setup (ensure this runs only once and does not overwrite existing data)
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()

    # If the user is already logged in, redirect to the dashboard
    if st.session_state.logged_in:
        st.success(f"Welcome back, {st.session_state.username}!")
        st.write("You are already logged in.")
        if st.button("Go to Dashboard"):
            st.session_state.page = "dashboard"
        conn.close()
        return

    # Login Section
    st.title("Login Page")
    st.subheader("Log In")
    with st.form("Login Form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Log In")

        if login_btn:
            if username and password:
                # Check if the username exists in the database
                c.execute("SELECT password FROM users WHERE username = ?", (username,))
                user = c.fetchone()
                if user and bcrypt.checkpw(password.encode("utf-8"), user[0].encode("utf-8")):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.page = "dashboard"
                    st.success(f"Welcome, {username}!")
                else:
                    st.error("Invalid username or password.")
            else:
                st.error("Please fill out all fields.")

    # Sign-Up Section
    st.subheader("Sign Up")
    with st.form("Sign Up Form"):
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        signup_btn = st.form_submit_button("Sign Up")

        if signup_btn:
            if new_username and new_password:
                try:
                    # Hash the password and insert into the database
                    hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
                    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                              (new_username, hashed_password.decode("utf-8")))
                    conn.commit()
                    st.success("Account created successfully! You can now log in.")
                except sqlite3.IntegrityError:
                    st.error("Username already exists. Please choose a different username.")
                except Exception as e:
                    st.error(f"Error during sign-up: {e}")
            else:
                st.error("Please fill out all fields.")

    conn.close()
