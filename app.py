import streamlit as st
import pickle

# Load the trained model
model = pickle.load(open('model.pkl', 'rb'))

st.title('Diabetes Prediction App')

# Collect inputs for all 8 features
pregnancies = st.number_input('Pregnancies', min_value=0)
glucose = st.number_input('Glucose Level', min_value=0.0)
blood_pressure = st.number_input('Blood Pressure', min_value=0.0)
skin_thickness = st.number_input('Skin Thickness', min_value=0.0)
insulin = st.number_input('Insulin', min_value=0.0)
bmi = st.number_input('BMI', min_value=0.0)
diabetes_pedigree = st.number_input('Diabetes Pedigree Function', min_value=0.0)
age = st.number_input('Age', min_value=0)

# Predict when the user clicks the button
if st.button('Predict'):
    # Prepare the input as a 2D list for prediction
    features = [[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree, age]]
    prediction = model.predict(features)

    # Display the result
    result = 'Positive' if prediction[0] == 1 else 'Negative'
    st.write(f'Diabetes Prediction: {result}')
