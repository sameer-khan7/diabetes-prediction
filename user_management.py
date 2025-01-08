import streamlit as st
import sqlite3
import os

# Get the full path to the database file
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.db')

def profile_page():
    # Sidebar with clickable buttons for navigation
    st.sidebar.title("Navigation")
    
    # Creating clickable buttons for Dashboard and Prediction pages
    if st.sidebar.button("Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()  # To reload the app with the selected page

    if st.sidebar.button("Prediction"):
        st.session_state.page = "prediction"
        st.rerun()  # To reload the app with the selected page

    # Logout Button
    st.markdown(
        """
        <style>
        .logout-button {
            display: flex;
            justify-content: flex-end;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    logout_container = st.container()
    with logout_container:
        st.markdown('<div class="logout-button">', unsafe_allow_html=True)
        if st.button("🔒 Log Out", key="logout_button"):
            st.session_state.page = "login"
            st.session_state.pop("username", None)  # Clear session data
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Profile Page Content
    st.title("👤 User Profile Management")
    
    if "username" not in st.session_state:
        st.error("You must be logged in to access the profile management page.")
        return
    
    username = st.session_state["username"]

    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Fetch user details
    c.execute("SELECT username, full_name, email, gender, age FROM users WHERE username = ?", (username,))
    user_data = c.fetchone()

    if user_data:
        username, full_name, email, gender, age = user_data
        
        # Display Profile Information
        st.subheader("📋 Profile Information")
        st.text_input("Username", value=username, disabled=True)
        full_name = st.text_input("Full Name", value=full_name)
        email = st.text_input("Email", value=email)
        gender = st.selectbox("Gender", options=["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(gender))
        age = st.number_input("Age", value=age, min_value=0)

        # Update Profile Information
        if st.button("Update Profile"):
            c.execute(
                "UPDATE users SET full_name = ?, email = ?, gender = ?, age = ? WHERE username = ?",
                (full_name, email, gender, age, username)
            )
            conn.commit()
            st.success("Profile updated successfully!")
    
        # Password Reset
        st.subheader("🔑 Reset Password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Reset Password"):
            if new_password and confirm_password:
                if new_password == confirm_password:
                    hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
                    c.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password.decode("utf-8"), username))
                    conn.commit()
                    st.success("Password reset successfully!")
                else:
                    st.error("Passwords do not match!")
            else:
                st.error("Please fill in both password fields.")
    else:
        st.error("User not found!")
    
    conn.close()

    # Add a section for downloading the database
    st.subheader("📥 Download Database")
    st.markdown("You can download the current database file for backup or analysis purposes.")
    with open(DB_PATH, "rb") as db_file:
        st.download_button(
            label="Download Database",
            data=db_file,
            file_name="users.db",
            mime="application/octet-stream",
        )
