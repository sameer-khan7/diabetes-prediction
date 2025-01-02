import streamlit as st
import sqlite3
import bcrypt

# Function to set up the database
def setup_database():
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        # Ensure the `users` table exists
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT UNIQUE,
                password TEXT
            )
            """
        )
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Error setting up the database: {e}")

# Function to handle sign-up
def handle_signup(username, password):
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Insert user into the database
        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password.decode("utf-8")),
        )
        conn.commit()
        conn.close()

        return True, "Account created successfully! Please log in."
    except sqlite3.IntegrityError:
        return False, "Username already exists. Please choose a different username."
    except Exception as e:
        return False, f"An error occurred: {e}"

# Main login page
def login_page():
    st.title("Login Page")

    # Debug: Show session state
    st.write("Debug Session State:", st.session_state)

    # Sign-Up Section
    st.subheader("Sign Up")
    with st.form("signup_form"):
        # Use local variables for inputs
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        signup_btn = st.form_submit_button("Sign Up")

        # Handle form submission
        if signup_btn:
            st.success("Button clicked successfully! No database interaction.")

# Initialize the app
setup_database()
login_page()
