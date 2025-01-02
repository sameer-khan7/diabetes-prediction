import streamlit as st

def minimal_test():
    st.title("Minimal Test App")
    with st.form("Test Form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_btn = st.form_submit_button("Submit")
        if submit_btn:
            st.write(f"Username: {username}")
            st.success("Form submitted successfully!")

minimal_test()
