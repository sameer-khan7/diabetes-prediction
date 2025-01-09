import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os
from fpdf import FPDF

# Define the database path
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.db')

def generate_pdf(df, username):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Health Report for {username}", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt="Summary:", ln=True)
    pdf.ln(5)

    # Add data
    for i, row in df.iterrows():
        pdf.cell(200, 10, txt=f"{row['Timestamp']}: Glucose={row['Glucose']}, BMI={row['BMI']}, Prediction={row['Prediction']}", ln=True)
    
    pdf_file = f"{username}_health_report.pdf"
    pdf.output(pdf_file)
    return pdf_file

def dashboard_page():
    # Sidebar Navigation
    #st.sidebar.header("Navigation")
    #if st.sidebar.button("Prediction", key="go_to_prediction"):
    #    st.session_state.page = "prediction"
    #    st.rerun()
    #if st.sidebar.button("Profile Management", key="go_to_profile"):
    #    st.session_state.page = "profile"
    #    st.rerun()

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
        if st.button("🔒 Log Out", key="logout_button_dashboard"):
            st.session_state.page = "login"
            st.session_state.logged_in = False  # Reset logged-in status
            st.session_state.pop("username", None)  # Clear session data
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Dashboard Title
    st.title("📊 User Dashboard")
    st.markdown("Welcome to your personal dashboard. Here you can view your saved predictions and insights.")

    # Fetch user details and results from the database
    if "username" in st.session_state:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Fetch user details
        c.execute("SELECT full_name, gender, age FROM users WHERE username = ?", (st.session_state.username,))
        user_details = c.fetchone()

        # Fetch user predictions
        c.execute("SELECT glucose, bmi, prediction, timestamp FROM results WHERE username = ?", (st.session_state.username,))
        results = c.fetchall()
        conn.close()

        # Display user details
        if user_details:
            full_name, gender, age = user_details
            st.subheader("👤 User Information")
            st.markdown(f"**Full Name:** {full_name}")
            st.markdown(f"**Gender:** {gender}")
            st.markdown(f"**Age:** {age} years")

        # Check if there are any saved results
        if results:
            
            # Convert results to a DataFrame
            df = pd.DataFrame(results, columns=["Glucose", "BMI", "Prediction", "Timestamp"])
            
            if st.button("Generate Health Report"):
                pdf_file = generate_pdf(df, st.session_state.username)
                with open(pdf_file, "rb") as f:
                    st.download_button("Download Report", data=f, file_name=pdf_file, mime="application/pdf")

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

            # Display Original Data by Default
            st.subheader("📋 Saved Results")
            st.dataframe(df, use_container_width=True)

            # Filter Options
            st.subheader("🔍 Filter Your Results")
            with st.expander("Apply Filters"):
                start_date = st.date_input("Start Date", key="filter_start_date")
                end_date = st.date_input("End Date", key="filter_end_date")
                glucose_min = st.number_input("Minimum Glucose Level", value=0.0, step=0.1, key="filter_glucose_min")
                glucose_max = st.number_input("Maximum Glucose Level", value=200.0, step=0.1, key="filter_glucose_max")

                # Apply Filters Button
                if st.button("Apply Filters"):
                    filtered_df = df[
                        (pd.to_datetime(df["Timestamp"]) >= pd.to_datetime(start_date)) &
                        (pd.to_datetime(df["Timestamp"]) <= pd.to_datetime(end_date)) &
                        (df["Glucose"] >= glucose_min) & 
                        (df["Glucose"] <= glucose_max)
                    ]

                    # Display Filtered Data
                    st.subheader("📋 Filtered Results")
                    if not filtered_df.empty:
                        st.dataframe(filtered_df, use_container_width=True)

                        # Download Filtered Results
                        csv = filtered_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Filtered Results as CSV",
                            data=csv,
                            file_name="filtered_results.csv",
                            mime="text/csv",
                        )
                    else:
                        st.warning("No data matches the applied filters. Please adjust your filter criteria.")

            # Trend Analysis
            st.subheader("📊 Trend Analysis")
            fig_trends = px.line(
                df,
                x="Timestamp",
                y=["Glucose", "BMI"],
                title="Health Metrics Trends Over Time",
                markers=True,
            )
            st.plotly_chart(fig_trends, use_container_width=True)

            # Health Alerts and Recommendations
            st.subheader("🚨 Health Alerts and 💡 Recommendations")
            if avg_glucose > 140:
                st.warning("Your average glucose level is above normal. Consider consulting a doctor.")
                st.info("**Glucose Recommendation**: Reduce sugar intake and monitor carbohydrate consumption.")
            if avg_bmi > 25:
                st.warning("Your average BMI is in the overweight range. Consider improving your diet and exercise.")
                st.info("**BMI Recommendation**: Incorporate regular physical activity and balanced meals.")
            if positive_predictions > 0:
                st.warning("You have positive diabetes predictions. Schedule a medical checkup for further evaluation.")

            # Insights Charts
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

    # Admin Controls
    if st.session_state.username == "admin":
        st.subheader("👩‍💼 Admin Dashboard")
        conn = sqlite3.connect(DB_PATH)
        users_df = pd.read_sql_query("SELECT * FROM users", conn)
        predictions_df = pd.read_sql_query("SELECT * FROM results", conn)
        conn.close()
    
        # Display user data
        st.write("All Users:")
        st.dataframe(users_df, use_container_width=True)
    
        # Display predictions
        st.write("All Predictions:")
        st.dataframe(predictions_df, use_container_width=True)
    
        # Add user management
        selected_user = st.selectbox("Select a User to Manage", users_df["username"])
        if st.button("Delete User"):
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE username = ?", (selected_user,))
            conn.commit()
            conn.close()
            st.success(f"User {selected_user} deleted successfully!")
            st.rerun()

