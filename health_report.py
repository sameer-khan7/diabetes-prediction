import streamlit as st
import sqlite3
import pandas as pd
from fpdf import FPDF
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.db')

def generate_pdf(df, username, full_name, gender, age):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add DejaVuSans regular and bold fonts (supports Unicode)
    pdf.add_page()
    pdf.add_font("DejaVuSans", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVuSans", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", uni=True)

    # Set the regular font for most content
    pdf.set_font("DejaVuSans", size=12)

    # Cover Page
    pdf.set_font("DejaVuSans", size=16, style="B")  # Use bold variant here
    pdf.cell(200, 10, txt="Health Report", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("DejaVuSans", size=12)
    pdf.cell(200, 10, txt=f"Generated for: {full_name} ({username})", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Gender: {gender}, Age: {age} years", ln=True, align="C")
    pdf.cell(200, 10, txt="Generated by Diabetes Prediction App", ln=True, align="C")
    pdf.ln(20)

    # Summary Section
    pdf.set_font("DejaVuSans", size=14, style="B")  # Use bold variant here
    pdf.cell(200, 10, txt="Summary of Health Metrics", ln=True, align="L")
    pdf.ln(5)
    avg_glucose = df["Glucose"].mean()
    avg_bmi = df["BMI"].mean()
    positive_predictions = (df["Prediction"] == "Positive").sum()
    pdf.set_font("DejaVuSans", size=12)
    pdf.cell(200, 10, txt=f"- Average Glucose Level: {avg_glucose:.2f} mg/dL", ln=True)
    pdf.cell(200, 10, txt=f"- Average BMI: {avg_bmi:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"- Positive Diabetes Predictions: {positive_predictions}", ln=True)
    pdf.ln(10)

    # Detailed Results Table
    pdf.set_font("DejaVuSans", size=14, style="B")  # Use bold variant here
    pdf.cell(200, 10, txt="Detailed Results", ln=True, align="L")
    pdf.ln(5)
    pdf.set_font("DejaVuSans", size=10)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(60, 10, "Timestamp", border=1, fill=True)
    pdf.cell(40, 10, "Glucose", border=1, fill=True, align="C")
    pdf.cell(40, 10, "BMI", border=1, fill=True, align="C")
    pdf.cell(50, 10, "Prediction", border=1, fill=True, align="C")
    pdf.ln()

    for _, row in df.iterrows():
        pdf.cell(60, 10, row["Timestamp"], border=1)
        pdf.cell(40, 10, f"{row['Glucose']:.2f}", border=1, align="C")
        pdf.cell(40, 10, f"{row['BMI']:.2f}", border=1, align="C")
        pdf.cell(50, 10, row["Prediction"], border=1, align="C")
        pdf.ln()

    # Recommendations Section
    pdf.ln(10)
    pdf.set_font("DejaVuSans", size=14, style="B")  # Use bold variant here
    pdf.cell(200, 10, txt="Recommendations", ln=True, align="L")
    pdf.ln(5)
    pdf.set_font("DejaVuSans", size=12)
    if avg_glucose > 140:
        pdf.set_text_color(255, 0, 0)
        pdf.cell(200, 10, txt="⚠️ High glucose levels detected. Reduce sugar intake and consult a doctor.", ln=True)
    if avg_bmi > 25:
        pdf.cell(200, 10, txt="⚠️ High BMI detected. Maintain a balanced diet and exercise regularly.", ln=True)
    if positive_predictions > 0:
        pdf.cell(200, 10, txt="⚠️ Positive diabetes predictions detected. Schedule a medical checkup.", ln=True)

    # Reset text color
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Stay healthy and monitor your metrics regularly!", ln=True)

    # Save the PDF
    pdf_file = f"{username}_health_report.pdf"
    pdf.output(pdf_file)
    return pdf_file


def health_report_page():

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
        if st.button("🔒 Log Out", key="logout_button_report"):
            st.session_state.page = "login"
            st.session_state.logged_in = False  # Reset logged-in status
            st.session_state.pop("username", None)  # Clear session data
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.title("📄 Health Report")
    st.markdown("Generate and download your personalized health report summarizing your predictions and metrics.")

    if "username" in st.session_state:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT full_name, gender, age FROM users WHERE username = ?", (st.session_state.username,))
        user_details = c.fetchone()
        c.execute("SELECT glucose, bmi, prediction, timestamp FROM results WHERE username = ?", (st.session_state.username,))
        results = c.fetchall()
        conn.close()

        if user_details and results:
            # Display user information
            full_name, gender, age = user_details
            st.subheader("👤 User Details")
            st.markdown(f"- **Full Name**: {full_name}")
            st.markdown(f"- **Gender**: {gender}")
            st.markdown(f"- **Age**: {age} years")

            # Prepare results data
            df = pd.DataFrame(results, columns=["Glucose", "BMI", "Prediction", "Timestamp"])

            # Display results summary
            st.subheader("📋 Summary of Metrics")
            avg_glucose = df["Glucose"].mean()
            avg_bmi = df["BMI"].mean()
            positive_predictions = (df["Prediction"] == "Positive").sum()
            st.markdown(f"- **Average Glucose Level**: {avg_glucose:.2f} mg/dL")
            st.markdown(f"- **Average BMI**: {avg_bmi:.2f}")
            st.markdown(f"- **Positive Diabetes Predictions**: {positive_predictions}")

            # Generate and download PDF
            pdf_file = generate_pdf(df, st.session_state.username, full_name, gender, age)
            with open(pdf_file, "rb") as f:
                st.download_button("📥 Download Health Report", data=f, file_name=pdf_file, mime="application/pdf")
        else:
            st.error("No data available to generate the report.")
    else:
        st.error("You must be logged in to access this page.")
