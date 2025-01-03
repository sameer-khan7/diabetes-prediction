import streamlit as st
import sqlite3
import bcrypt
import os

def login_page():
    # App Title and Introduction
    st.title("Diabetes Prediction App")
    st.caption("A user-friendly platform to predict diabetes and track results.")

    # Get the correct file path for the database
    current_dir = os.path.dirname(__file__)  # Path to the directory containing this script
    db_path = os.path.join(current_dir, "users.db")  # Path to the database file

    # Database setup (ensure this runs only once and does not overwrite existing data)
    conn = sqlite3.connect(db_path)  # Use the correct file path
    c = conn.cursor()

    # Layout for Login and Sign-Up Sections
    col1, col2 = st.columns(2)  # Split the page into two columns

    # Login Section
    with col1:
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
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
                else:
                    st.error("Please fill out all fields.")

    # Sign-Up Section
    with col2:
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

    # Footer
    st.markdown("---")
    st.caption("Powered by Streamlit | Diabetes Prediction App © 2025")

    # Close the database connection
    conn.close()
