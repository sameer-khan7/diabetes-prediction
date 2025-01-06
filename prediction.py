import streamlit as st
import pickle
import numpy as np
import os
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
import shap

# Helper Function for SHAP Integration
def st_shap(plot, height=None):
    """Render a SHAP force plot in Streamlit."""
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)

def prediction_page():
    # Paths to the model and scaler
    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, 'model.pkl')
    scaler_path = os.path.join(current_dir, 'scaler.pkl')
    db_path = os.path.join(current_dir, "users.db")

    # Load the trained model and scaler with error handling
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
        if st.button("🔒 Log Out", key="logout_button"):
            st.session_state.page = "login"
            st.session_state.pop("username", None)  # Clear session data
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Page title
    st.title("Diabetes Prediction App")
    st.write("This app predicts the likelihood of diabetes based on user inputs or uploaded data.")

    # Sidebar navigation
    st.sidebar.header("Navigation")
    if st.sidebar.button("Go to Dashboard", key="go_to_dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

    # Input Section
    st.subheader("Input Your Data")
    pregnancies = st.number_input('Pregnancies', min_value=0, value=0, help="Number of times pregnant")
    glucose = st.number_input('Glucose Level', min_value=0.0, value=120.0, help="Plasma glucose concentration")
    blood_pressure = st.number_input('Blood Pressure (mm Hg)', min_value=0.0, value=70.0, help="Diastolic blood pressure")
    skin_thickness = st.number_input('Skin Thickness (mm)', min_value=0.0, value=20.0, help="Triceps skin fold thickness")
    insulin = st.number_input('Insulin (mu U/ml)', min_value=0.0, value=80.0, help="2-Hour serum insulin")
    bmi = st.number_input('BMI', min_value=0.0, value=25.0, help="Body Mass Index (weight in kg/(height in m)^2)")
    dpf = st.number_input('Diabetes Pedigree Function', min_value=0.0, value=0.5, help="Family history influence")
    age = st.number_input('Age (years)', min_value=0, value=30, help="Age in years")

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

                # Explanation of Prediction (SHAP) for Tree-Based Models
                st.subheader("Explainable AI Insights")
                
                try:
                    # Feature names must match the scaled features
                    feature_names = [
                        'Pregnancies', 'Glucose', 'Blood Pressure', 'Skin Thickness',
                        'Insulin', 'BMI', 'Diabetes Pedigree Function', 'Age'
                    ]
                
                    # Convert the scaled_features array to DataFrame with column names
                    scaled_features_df = pd.DataFrame(scaled_features, columns=feature_names)
                
                    # Use TreeExplainer for tree-based models like Random Forest
                    explainer = shap.TreeExplainer(model)
                    shap_values = explainer.shap_values(scaled_features_df)
                
                    # Debugging information
                    st.write(f"Scaled Features Shape: {scaled_features_df.shape}")
                    st.write(f"SHAP values Length: {len(shap_values)}")
                
                    # Handle SHAP values for binary classification
                    if isinstance(shap_values, list):
                        if len(shap_values) > 1:
                            shap_values_positive_class = shap_values[1]  # SHAP values for the positive class (class 1)
                            st.write(f"SHAP values for positive class: {shap_values_positive_class}")
                        else:
                            shap_values_positive_class = shap_values[0]  # Only one class in shap_values, use the first one
                            st.write(f"SHAP values for the single class: {shap_values_positive_class}")
                
                    # Display the force plot for individual prediction
                    st.write("Feature Contributions to the Prediction (Force Plot):")
                    shap.initjs()
                    force_plot = shap.force_plot(
                        explainer.expected_value[1] if len(shap_values) > 1 else explainer.expected_value[0],
                        shap_values_positive_class[0, :],  # SHAP values for the first instance
                        scaled_features_df.iloc[0, :],  # Use the first row of the DataFrame
                        feature_names=feature_names
                    )
                    st_shap(force_plot)
                
                    # Display a summary plot for feature importance
                    st.write("Overall Feature Importance (Summary Plot):")
                    shap.summary_plot(
                        shap_values_positive_class, 
                        scaled_features_df, 
                        feature_names=feature_names, 
                        plot_type="bar", 
                        show=False
                    )
                    st.pyplot()
                
                except Exception as e:
                    st.error(f"Error explaining prediction: {e}")

                


            except Exception as e:
                st.error(f"Error during prediction: {e}")

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
