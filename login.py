import streamlit as st
import sqlite3
import bcrypt

# Initialize session state variables
if "signup_success" not in st.session_state:
    st.session_state.signup_success = False

def login_page():
    st.title("Login Page")

    # Debug: Session state output
    st.write("Debug Session State:", st.session_state)

    # Connect to SQLite database
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        # Ensure table exists
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT UNIQUE,
                password TEXT
            )
            """
        )
        conn.commit()
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return

    # Sign-Up Section
    st.subheader("Sign Up")
    with st.form("Sign Up Form"):  # Define form with a unique key
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        signup_btn = st.form_submit_button("Sign Up")  # Add submit button

        if signup_btn:
            st.write("Sign Up button pressed")  # Debugging step

            if new_username and new_password:
                try:
                    # Hash the password
                    hashed_password = bcrypt.hashpw(
                        new_password.encode("utf-8"), bcrypt.gensalt()
                    )
                    # Insert user into database
                    c.execute(
                        "INSERT INTO users (username, password) VALUES (?, ?)",
                        (new_username, hashed_password.decode("utf-8")),
                    )
                    conn.commit()

                    # Reset form fields and show success message
                    st.session_state.signup_success = True
                    st.success("Account created successfully! Please log in.")

                except sqlite3.IntegrityError:
                    st.error("Username already exists. Please choose a different username.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.error("Please fill out all fields.")

    # Close database connection
    try:
        conn.close()
    except Exception as e:
        st.error(f"Error closing the database connection: {e}")

# Run the login page
login_page()
