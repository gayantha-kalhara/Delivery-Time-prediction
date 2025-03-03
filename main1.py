import numpy as np

import streamlit as st

import pickle


# Load model
model = pickle.load(open("model.pickel", "rb"))
st.set_page_config(page_title="Delivery Time Prediction", layout="wide")

# Custom CSS to add background image and style elements
st.markdown(
    """
    <style>
        .reportview-container {
            background-image: url('https://www.odtap.com/wp-content/uploads/2018/10/food-delivery.jpg');  /* Add your image URL here */
            background-size: cover;
            background-position: center;
        }

        .stTextInput, .stSelectbox, .stButton, .stText {
            background-color: rgba(255, 255, 255, 0.7);  /* Light background for input fields */
            border-radius: 5px;
        }

        .stButton button {
            background-color: #FF6347;  /* Tomato color for button */
            color: white;
            font-weight: bold;
        }

        .stButton button:hover {
            background-color: #FF4500;  /* Darker tomato on hover */
        }

        .stTitle {
            color: #FF6347;  /* Tomato color for title */
        }
    </style>
    """, unsafe_allow_html=True
)


st.title("Delivery Time Prediction")

# Inputs (excluding Order_ID)
Distance_km = st.text_input("Distance (km)", key='2')
Weather = st.selectbox("Weather", ['windy', 'clear', 'Rainy', 'Foggy', 'snowy'])
Traffic_level = st.selectbox("Traffic Level", ['Low', 'Medium', 'High'])
Time_of_Day = st.selectbox("Time of Day", ['Morning', 'Afternoon', 'Evening', 'Night'])
Vehicle_Type = st.selectbox("Vehicle Type", ['Bike', 'Car', 'Scooter'])
Preparation_Time = st.text_input("Preparation Time (minutes)", key='3')
Courier_Experience_yrs = st.text_input("Courier Experience (years)", key='4')

# Mapping categorical values to numerical values
Weather_mapping = {'clear': 0, 'Rainy': 1, 'Foggy': 2, 'snowy': 3, 'windy': 4}
Traffic_level_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
Time_of_Day_mapping = {'Morning': 0, 'Afternoon': 1, 'Evening': 2, 'Night': 3}
Vehicle_Type_mapping = {'Bike': 0, 'Car': 1, 'Scooter': 2}

# Convert categorical inputs
Weather_value = Weather_mapping[Weather]
Traffic_level_value = Traffic_level_mapping[Traffic_level]
Time_of_Day_value = Time_of_Day_mapping[Time_of_Day]
Vehicle_Type_value = Vehicle_Type_mapping[Vehicle_Type]

# Convert numerical inputs safely
try:
    Distance_km = float(Distance_km) if Distance_km.replace('.', '', 1).isdigit() else 0.0
except ValueError:
    Distance_km = 0.0

try:
    Preparation_Time = int(Preparation_Time) if Preparation_Time.isdigit() else 0
except ValueError:
    Preparation_Time = 0

# Ensure Courier_Experience_yrs is numeric
try:
    Courier_Experience_yrs = float(Courier_Experience_yrs) if Courier_Experience_yrs.replace('.', '', 1).isdigit() else 0.0
except ValueError:
    Courier_Experience_yrs = 0.0

# Prediction Button
if st.button("Predict"):
    # Prepare the input array (Ensure all features are numeric)
    inp = np.array([[Distance_km, Weather_value, Traffic_level_value, Time_of_Day_value, Vehicle_Type_value, Preparation_Time, Courier_Experience_yrs]])
    
    # Ensure input is of type float (model expects numerical values)
    inp = np.array(inp, dtype=float)
    
    # Make prediction
    try:
        prediction = model.predict(inp)
        st.success(f"Predicted Delivery Time: {prediction[0]:.2f} minutes")
    except Exception as e:
        st.error(f"Error during prediction: {str(e)}")

