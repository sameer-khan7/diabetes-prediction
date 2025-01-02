import streamlit as st
import sqlite3
import bcrypt

# Initialize session state variables
if "signup_username" not in st.session_state:
    st.session_state.signup_username = ""
if "signup_password" not in st.session_state:
    st.session_state.signup_password = ""
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
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return

    # Sign-Up Section
    st.subheader("Sign Up")
    with st.form("Sign Up Form"):  # Define form with a unique key
        st.session_state.signup_username = st.text_input(
            "New Username", value=st.session_state.signup_username
        )
        st.session_state.signup_password = st.text_input(
            "New Password", type="password", value=st.session_state.signup_password
        )
        signup_btn = st.form_submit_button("Sign Up")  # Add submit button

        if signup_btn:
            # Debugging step: Check button press
            st.write("Sign Up button pressed")

            if st.session_state.signup_username and st.session_state.signup_password:
                try:
                    # Hash the password
                    hashed_password = bcrypt.hashpw(
                        st.session_state.signup_password.encode("utf-8"), bcrypt.gensalt()
                    )
                    # Insert user into database
                    c.execute(
                        "INSERT INTO users (username, password) VALUES (?, ?)",
                        (st.session_state.signup_username, hashed_password.decode("utf-8")),
                    )
                    conn.commit()

                    # Reset form fields and show success message
                    st.session_state.signup_username = ""
                    st.session_state.signup_password = ""
                    st.success("Account created successfully! Please log in.")
                    st.session_state.signup_success = True

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
