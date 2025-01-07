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

    # Layout for Login Section
    st.subheader("Log In")
    with st.form("Login Form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
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
                st.error("Please fill out both fields.")

    # Reset Password Section
    st.subheader("Forgot Password?")
    reset_email = st.text_input("Enter your registered email address", placeholder="Enter your email")
    reset_btn = st.button("Reset Password")

    if reset_btn:
        if reset_email:
            # Mock-up: In reality, you would send an email with a reset link
            c.execute("SELECT username FROM users WHERE email = ?", (reset_email,))
            user = c.fetchone()
            if user:
                st.success(f"Password reset instructions have been sent to {reset_email}.")
            else:
                st.error("No user found with this email.")
        else:
            st.error("Please enter your email address.")

    # Spacer between sections for better UX
    st.markdown("<hr>", unsafe_allow_html=True)

    # Sign-Up Section (Initially hidden)
    if st.button("Sign Up (Expand)"):
        st.session_state.signup_expanded = not st.session_state.get("signup_expanded", False)
    
    if st.session_state.get("signup_expanded", False):
        st.subheader("Sign Up")
        with st.form("Sign Up Form"):
            # User Inputs
            new_username = st.text_input("New Username", placeholder="Choose a username")
            new_full_name = st.text_input("Full Name", placeholder="Enter your full name")
            new_email = st.text_input("Email Address", placeholder="Enter your email address")
            new_password = st.text_input("New Password", type="password", placeholder="Choose a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
            
            # Additional Details
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=0)
            age = st.number_input("Age", min_value=1, max_value=120, step=1, help="Enter your age in years")
    
            # Submit Button
            signup_btn = st.form_submit_button("Sign Up")
    
            if signup_btn:
                # Validate Input
                if not (new_username and new_full_name and new_email and new_password and confirm_password and gender and age):
                    st.error("Please fill out all fields.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match!")
                else:
                    try:
                        # Hash the password and insert into the database
                        hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
                        
                        # Insert the new user into the database
                        c.execute("""
                            INSERT INTO users (username, full_name, email, password, gender, age)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (new_username, new_full_name, new_email, hashed_password.decode("utf-8"), gender, age))
                        
                        conn.commit()
                        st.success("Account created successfully! You can now log in.")
                    except sqlite3.IntegrityError:
                        st.error("Username already exists. Please choose a different username.")
                    except Exception as e:
                        st.error(f"Error during sign-up: {e}")

    # Footer
    st.markdown("---")
    st.caption("Diabetes Prediction App © 2025")

    # Close the database connection
    conn.close()
