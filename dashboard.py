import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

def dashboard_page():
    # Sidebar Navigation
    st.sidebar.header("Navigation")
    if st.sidebar.button("Go to Prediction", key="go_to_prediction"):
        st.session_state.page = "prediction"
        st.rerun()

    # Improved Logout Button
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
        
    # Dashboard Title
    st.title("📊 User Dashboard")
    st.markdown("Welcome to your personal dashboard. Here you can view your saved predictions and insights.")

    # Fetch results from the database
    if "username" in st.session_state:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT glucose, bmi, prediction, timestamp FROM results WHERE username = ?", (st.session_state.username,))
        results = c.fetchall()
        conn.close()

        if results:
            # Convert results to a DataFrame
            df = pd.DataFrame(results, columns=["Glucose", "BMI", "Prediction", "Timestamp"])

            # Display Metrics
            st.subheader("📈 Key Metrics")
            avg_glucose = df["Glucose"].mean()
            avg_bmi = df["BMI"].mean()
            positive_predictions = (df["Prediction"] == "Positive").sum()
            negative_predictions = (df["Prediction"] == "Negative").sum()

            col1, col2, col3 = st.columns(3)
            col1.metric("Average Glucose", f"{avg_glucose:.2f} mg/dL")
            col2.metric("Average BMI", f"{avg_bmi:.2f}")
            col3.metric("Positive Predictions", positive_predictions)

            # Display Table
            st.subheader("📋 Saved Results")
            st.dataframe(df, use_container_width=True)

            # Add Charts
            st.subheader("📊 Insights")
            
            # Glucose Distribution Chart
            fig1 = px.histogram(df, x="Glucose", title="Glucose Level Distribution", nbins=10, color_discrete_sequence=["#636EFA"])
            st.plotly_chart(fig1, use_container_width=True)

            # BMI Distribution Chart
            fig2 = px.histogram(df, x="BMI", title="BMI Distribution", nbins=10, color_discrete_sequence=["#EF553B"])
            st.plotly_chart(fig2, use_container_width=True)

            # Predictions Pie Chart
            fig3 = px.pie(df, names="Prediction", title="Prediction Breakdown", color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("You don't have any saved results yet. Make a prediction to see data here.")
    else:
        st.error("You must be logged in to access the dashboard.")
