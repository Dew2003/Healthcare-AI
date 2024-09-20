import streamlit as st
import numpy as np
from PIL import Image
import disease_backend  # Import disease backend
import emotion_backend  # Import emotion backend

# Streamlit frontend
st.title("Health and Happiness Assistance System")

# Disease Detection Section
st.header("Disease Detection")
symptoms_input = st.text_input("Enter symptoms separated by commas (e.g., itching, skin_rash, fatigue):")

if st.button("Predict Disease"):
    if symptoms_input:
        user_symptoms = [s.strip() for s in symptoms_input.split(',')]
        try:
            predicted_disease = disease_backend.get_predicted_value(user_symptoms)
            dis_des, precautions, medications, rec_diet, workout = disease_backend.helper(predicted_disease)

            # Display disease prediction results
            st.subheader(f"Predicted Disease: {predicted_disease}")
            st.write(f"**Description**: {dis_des}")
            
            st.write("### Precautions")
            for pre in precautions[0]:
                st.write(f"- {pre}")

            st.write("### Medications")
            for med in medications:
                st.write(f"- {med}")

            st.write("### Recommended Diet")
            for diet in rec_diet:
                st.write(f"- {diet}")

            st.write("### Suggested Workout")
            st.write(workout)
        except KeyError:
            st.error("Some symptoms might be misspelled or not recognized. Please try again.")
    else:
        st.error("Please enter symptoms to predict the disease.")

# Emotion Detection Section
st.header("Emotion Detection and Motivation")

# Option to capture photo using the camera
camera_option = st.radio("Select Input Method", ("Upload Image", "Use Camera"))

if camera_option == "Upload Image":
    uploaded_file = st.file_uploader("Choose an image for emotion detection...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image_array = np.array(image)  # Convert to NumPy array
elif camera_option == "Use Camera":
    captured_image = st.camera_input("Capture an image for emotion detection")
    if captured_image is not None:
        image = Image.open(captured_image)
        image_array = np.array(image)  # Convert to NumPy array

if 'image_array' in locals() and image_array is not None:
    st.image(image_array, caption='Captured Image', use_column_width=True)

    # Detect the emotion
    dominant_emotion = emotion_backend.detect_emotion(image_array)

    if dominant_emotion:
        st.subheader(f"Detected Emotion: {dominant_emotion.capitalize()}")
        # Get a motivational quote
        quote = emotion_backend.get_motivational_content()
        st.write(f"**Motivational Quote:** {quote}")
    else:
        st.error("Could not detect any emotion. Please try again.")
