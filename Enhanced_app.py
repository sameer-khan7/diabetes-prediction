import streamlit as st
import pickle
import numpy as np

# Load the trained model
model = pickle.load(open('model.pkl', 'rb'))

st.title('Diabetes Prediction App')
st.write("This app predicts the likelihood of diabetes based on user inputs.")

# Collect inputs for all 8 features
pregnancies = st.number_input('Pregnancies', min_value=0, help="Number of times pregnant")
glucose = st.number_input('Glucose Level', min_value=0.0, help="Plasma glucose concentration in an oral glucose tolerance test")
blood_pressure = st.number_input('Blood Pressure (mm Hg)', min_value=0.0, help="Diastolic blood pressure")
skin_thickness = st.number_input('Skin Thickness (mm)', min_value=0.0, help="Triceps skin fold thickness")
insulin = st.number_input('Insulin (mu U/ml)', min_value=0.0, help="2-Hour serum insulin")
bmi = st.number_input('BMI', min_value=0.0, help="Body Mass Index (weight in kg/(height in m)^2)")
dpf = st.number_input('Diabetes Pedigree Function', min_value=0.0, help="Likelihood of diabetes based on family history")
age = st.number_input('Age (years)', min_value=0, help="Age in years")

# Arrange inputs for prediction
features = np.array([pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]).reshape(1, -1)

if st.button('Predict'):
    prediction = model.predict(features)
    prediction_prob = model.predict_proba(features)[0][1]

    if prediction == 1:
        st.error(f"The model predicts that you are likely to have diabetes. Probability: {prediction_prob:.2f}")
    else:
        st.success(f"The model predicts that you are unlikely to have diabetes. Probability: {prediction_prob:.2f}")

# Add sidebar with information about the model
st.sidebar.header("About")
st.sidebar.write("This model uses Logistic Regression trained on the Pima Indians Diabetes Dataset.")

# Display Feature Importance (if applicable in model)
if hasattr(model, 'coef_'):
    st.subheader("Feature Importance")
    import matplotlib.pyplot as plt
    feature_names = ['Pregnancies', 'Glucose', 'Blood Pressure', 'Skin Thickness', 'Insulin', 'BMI', 'Diabetes Pedigree Function', 'Age']
    importance = model.coef_[0]
    plt.barh(feature_names, importance)
    plt.xlabel("Importance")
    plt.ylabel("Features")
    st.pyplot(plt)
