import streamlit as st
import sqlite3
import bcrypt

def login_page():
    st.title("Login Page")

    # Database setup
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT UNIQUE,
                password TEXT
            )
        """)
        conn.commit()
    except Exception as e:
        st.error(f"Database error: {e}")
        return

    # Debug: Show session state
    st.write("Session State:", st.session_state)

    # Login Section
    st.subheader("Log In")
    with st.form("Login Form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Log In")

        if login_btn:
            if username and password:
                c.execute("SELECT password FROM users WHERE username = ?", (username,))
                user = c.fetchone()
                if user and bcrypt.checkpw(password.encode("utf-8"), user[0].encode("utf-8")):
                    st.session_state.page = "prediction"
                    st.experimental_rerun()
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
                    hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
                    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                              (new_username, hashed_password.decode("utf-8")))
                    conn.commit()
                    st.success("Account created successfully!")
                except sqlite3.IntegrityError:
                    st.error("Username already exists.")
                except Exception as e:
                    st.error(f"Error during sign-up: {e}")
            else:
                st.error("Please fill out all fields.")

    conn.close()
