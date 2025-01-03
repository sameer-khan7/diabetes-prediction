import streamlit as st
import pickle
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def prediction_page():
    # Paths to the model and scaler
    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, 'model.pkl')
    scaler_path = os.path.join(current_dir, 'scaler.pkl')

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

    # Sidebar Navigation
    st.sidebar.header("Navigation")
    if st.sidebar.button("Go to Dashboard", key="go_to_dashboard"):
        st.session_state.page = "dashboard"  # Update session state for navigation
        st.experimental_rerun()  # Trigger rerun to navigate to the dashboard page

    # Sidebar Information
    st.sidebar.header("About")
    st.sidebar.write("""
    This app uses a Logistic Regression model trained on the Pima Indians Diabetes Dataset.
    Enter your health metrics in the input fields to get predictions and probabilities.
    """)
    st.sidebar.subheader("Instructions")
    st.sidebar.write("""
    - Input values for the required features.
    - Click the "Predict" button to see results.
    """)

    st.sidebar.header("Parameter Explanations")
    st.sidebar.write("""
    - **Pregnancies**: Higher pregnancies may increase the likelihood of diabetes due to gestational diabetes risk.
    - **Glucose Level**: Elevated glucose levels are a primary indicator of diabetes.
    - **Blood Pressure**: High blood pressure is often associated with diabetes.
    - **Skin Thickness**: Indicates body fat distribution, which can affect insulin resistance.
    - **Insulin**: Abnormal insulin levels can signify poor glucose regulation.
    - **BMI**: Higher BMI suggests obesity, a major risk factor for diabetes.
    - **Diabetes Pedigree Function**: Reflects the influence of family history on diabetes risk.
    - **Age**: Older age increases the likelihood of developing diabetes.
    """)

    # Page title
    st.title('Diabetes Prediction App')
    st.write("This app predicts the likelihood of diabetes based on user inputs.")

    # Collect inputs for all 8 features with default values
    pregnancies = st.number_input('Pregnancies', min_value=0, value=0, help="Number of times pregnant")
    glucose = st.number_input('Glucose Level', min_value=0.0, value=120.0, help="Plasma glucose concentration in an oral glucose tolerance test")
    blood_pressure = st.number_input('Blood Pressure (mm Hg)', min_value=0.0, value=70.0, help="Diastolic blood pressure")
    skin_thickness = st.number_input('Skin Thickness (mm)', min_value=0.0, value=20.0, help="Triceps skin fold thickness")
    insulin = st.number_input('Insulin (mu U/ml)', min_value=0.0, value=80.0, help="2-Hour serum insulin")
    bmi = st.number_input('BMI', min_value=0.0, value=25.0, help="Body Mass Index (weight in kg/(height in m)^2)")
    dpf = st.number_input('Diabetes Pedigree Function', min_value=0.0, value=0.5, help="Likelihood of diabetes based on family history")
    age = st.number_input('Age (years)', min_value=0, value=30, help="Age in years")

    # Arrange inputs for prediction
    features = np.array([pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]).reshape(1, -1)

    # Prediction logic
    if st.button('Predict'):
        try:
            # Scale the features before prediction
            scaled_features = scaler.transform(features)
            prediction = model.predict(scaled_features)
            prediction_prob = model.predict_proba(scaled_features)[0][1]

            # Display inputs
            st.subheader("Your Inputs:")
            user_inputs = {
                "Pregnancies": pregnancies,
                "Glucose Level": glucose,
                "Blood Pressure": blood_pressure,
                "Skin Thickness": skin_thickness,
                "Insulin": insulin,
                "BMI": bmi,
                "Diabetes Pedigree Function": dpf,
                "Age": age,
            }
            st.write(user_inputs)

            # Display results
            threshold = 0.5  # Default threshold
            st.subheader("Prediction Probability:")
            st.progress(prediction_prob)
            if prediction_prob >= threshold:
                st.error(f"The model predicts that you are likely to have diabetes. Probability: {prediction_prob:.2f}")
            else:
                st.success(f"The model predicts that you are unlikely to have diabetes. Probability: {prediction_prob:.2f}")

        except Exception as e:
            st.error(f"Error during prediction: {e}")

    # Feature importance visualization (if applicable)
    if hasattr(model, 'coef_'):
        st.subheader("Feature Importance")
        feature_names = ['Pregnancies', 'Glucose', 'Blood Pressure', 'Skin Thickness', 'Insulin', 'BMI'
