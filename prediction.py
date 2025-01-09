import streamlit as st
import pickle
import numpy as np
import os
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
import lime
from lime.lime_tabular import LimeTabularExplainer
import seaborn as sns

# Helper Function for LIME Integration
def explain_prediction_with_lime(model, scaler, features, feature_names):
    explainer = LimeTabularExplainer(
        training_data=np.array(scaler.inverse_transform(features)),
        feature_names=feature_names,
        class_names=["No Diabetes", "Diabetes"],
        mode="classification"
    )
    explanation = explainer.explain_instance(features[0], model.predict_proba, num_features=len(feature_names))
    fig = explanation.as_pyplot_figure()
    st.pyplot(fig)

def prediction_page():
    # Paths to the model, scaler, and database
    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, 'model.pkl')
    scaler_path = os.path.join(current_dir, 'scaler.pkl')
    db_path = os.path.join(current_dir, "users.db")

    # Load the trained model and scaler
    try:
        model = pickle.load(open(model_path, 'rb'))
        scaler = pickle.load(open(scaler_path, 'rb'))
    except FileNotFoundError as e:
        st.error(f"File not found: {e}")
        return
    except Exception as e:
        st.error(f"Error loading model or scaler: {e}")
        return

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
        if st.button("🔒 Log Out", key="logout_button_predict"):
            st.session_state.page = "login"
            st.session_state.pop("username", None)  # Clear session data
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Page title
    st.title("Diabetes Prediction App")
    st.write("This app predicts the likelihood of diabetes based on user inputs or uploaded data.")

    # Sidebar navigation
    #st.sidebar.header("Navigation")
    #if st.sidebar.button("Go to Dashboard", key="go_to_dashboard"):
    #    st.session_state.page = "dashboard"
    #    st.rerun()
    #if st.sidebar.button("Profile Management", key="go_to_profile"):
    #    st.session_state.page = "profile"
    #    st.rerun()

    # Retrieve user data from the database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT gender, age FROM users WHERE username = ?", (st.session_state.get("username"),))
    user_data = c.fetchone()
    conn.close()

    gender = user_data[0] if user_data else "Other"
    user_age = user_data[1] if user_data else 30  # Default age if not found

    # Input Section
    st.subheader("Input Your Data")

    # Show pregnancies input only for female users
    if gender == "Female":
        pregnancies = st.number_input('Pregnancies', min_value=0, value=0, help="Number of times pregnant")
    else:
        pregnancies = 0  # Default value for male users

    glucose = st.number_input('Glucose Level', min_value=0.0, value=120.0, help="Plasma glucose concentration")
    blood_pressure = st.number_input('Blood Pressure (mm Hg)', min_value=0.0, value=70.0, help="Diastolic blood pressure")
    skin_thickness = st.number_input('Skin Thickness (mm)', min_value=0.0, value=20.0, help="Triceps skin fold thickness")
    insulin = st.number_input('Insulin (mu U/ml)', min_value=0.0, value=80.0, help="2-Hour serum insulin")
    bmi = st.number_input('BMI', min_value=0.0, value=25.0, help="Body Mass Index (weight in kg/(height in m)^2)")
    dpf = st.number_input('Diabetes Pedigree Function', min_value=0.0, value=0.5, help="Family history influence")
    age = st.number_input('Age (years)', min_value=0, value=user_age, help="Age in years", disabled=True)

    # Arrange inputs for prediction
    features = np.array([pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]).reshape(1, -1)

    # Prediction Button
    if st.button("Predict"):
        if any(v == 0 for v in [glucose, bmi]):
            st.error("Please provide valid inputs for Glucose and BMI.")
        else:
            try:
                scaled_features = scaler.transform(features)
                prediction = model.predict(scaled_features)
                prediction_prob = model.predict_proba(scaled_features)[0][1]

                # Display results
                st.subheader("Prediction Results")
                if prediction == 1:
                    result = "Positive"
                    st.error(f"Prediction: Likely to have diabetes. Probability: {prediction_prob:.2f}")
                else:
                    result = "Negative"
                    st.success(f"Prediction: Unlikely to have diabetes. Probability: {prediction_prob:.2f}")

                # Save to Database
                if "username" in st.session_state:
                    conn = sqlite3.connect(db_path)
                    c = conn.cursor()
                    c.execute("""
                        INSERT INTO results (username, glucose, bmi, prediction)
                        VALUES (?, ?, ?, ?)
                    """, (st.session_state.username, glucose, bmi, result))
                    conn.commit()
                    conn.close()
                    st.success("Prediction saved to your dashboard.")
                else:
                    st.warning("Log in to save your predictions.")

                # Health Score Calculation
                health_score = 100 - (0.5 * glucose + 0.3 * bmi + 0.2 * age)  # Example formula
                health_score = max(0, min(health_score, 100))

                # Display Health Score
                st.subheader("Your Health Score")
                st.write(f"Your Health Score is: {health_score:.2f}/100")

                # Provide Suggestions Based on Health Score
                if health_score < 50:
                    st.warning("Your health score is low. Consult a doctor and improve your diet and exercise.")
                elif 50 <= health_score < 80:
                    st.info("Your health score is moderate. Maintain a balanced diet and stay active.")
                else:
                    st.success("Your health score looks great! Keep up the good work!")

            except Exception as e:
                st.error(f"Error during prediction: {e}")

    # EDA Section
    if st.sidebar.checkbox("Explore Dataset"):
        st.subheader("Dataset Insights")
        try:
            current_dir = os.path.dirname(__file__)
            dataset_path = os.path.join(current_dir, "diabetes.csv")  # Update with your dataset path
            dataset = pd.read_csv(dataset_path)
    
            # Display Dataset
            st.write("First 5 Rows of the Dataset:")
            st.dataframe(dataset.head())
    
            # Correlation Heatmap
            st.subheader("Correlation Heatmap")
            correlation_matrix = dataset.corr()
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)
    
            # Feature Distribution
            st.subheader("Feature Distributions")
            selected_feature = st.selectbox("Select a Feature to View Distribution", dataset.columns)
            fig, ax = plt.subplots()
            sns.histplot(dataset[selected_feature], kde=True, ax=ax, color="blue")
            ax.set_title(f"Distribution of {selected_feature}")
            st.pyplot(fig)
    
        except FileNotFoundError:
            st.error("Dataset file not found. Please upload or specify the correct path.")

    # Batch Prediction
    st.subheader("Batch Prediction")
    uploaded_file = st.file_uploader("Upload a CSV file for batch prediction", type=["csv"])
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        if st.button("Predict for Uploaded Data"):
            try:
                scaled_data = scaler.transform(data)
                predictions = model.predict(scaled_data)
                data["Prediction"] = ["Positive" if p == 1 else "Negative" for p in predictions]
                st.write(data)

                # Download Results
                st.download_button("Download Predictions", data.to_csv(index=False), file_name="predictions.csv")
            except Exception as e:
                st.error(f"Error processing batch predictions: {e}")
