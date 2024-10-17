import streamlit as st
from streamlit_lottie import st_lottie
import json
import numpy as np
from PIL import Image
import disease_backend  
import emotion_backend 
from assistant import get_health_assistance


path = "a1.json"
with open(path,"r") as file: 
    url = json.load(file) 



 


st.title("Health Care AI")
st_lottie(url, 
    reverse=True, 
    height=100, 
    width=100, 
    speed=0.1, 
    loop=True, 
    quality='high', 
    key='a1'
)    
st.snow()

section = st.sidebar.radio(
    "Select an option",
    ("🤖 Health Assistant AI", "😊 Emotion Detection", "🩺 Disease Detection")
)

if section == "🤖 Health Assistant AI":
    st.markdown("<h2>💬 Health Assistance via AI</h2>", unsafe_allow_html=True)

    user_query = st.text_input("Ask any health-related question (e.g., symptoms, treatments, fitness advice,About Medicine):")

    category = st.radio(
        "What kind of advice are you looking for?",
        ("Symptoms & Diagnosis", "Nutrition & Diet", "Mental Health", "Fitness & Exercise","About Medicine")
    )

    
    if user_query or category:
        st.session_state.ai_response = None

    
    if "ai_response" not in st.session_state:
        st.session_state.ai_response = None

    
    if st.button("💡 Get AI Assistance"):
        if user_query and category:
            with st.spinner("Thinking..."):
                st.session_state.ai_response = get_health_assistance(user_query, category)
        else:
            st.error("Please enter a question and select a category.")

    if st.session_state.ai_response:
        st.markdown(f"**AI Response:**\n\n{st.session_state.ai_response}")


elif section == "😊 Emotion Detection":
    st.markdown("<h2>Emotion Detection and Motivation</h2>", unsafe_allow_html=True)
    
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    camera_option = st.radio("Select Input Method", ("Upload Image", "Use Camera"))

    if camera_option == "Upload Image":
        uploaded_file = st.file_uploader("Choose an image for emotion detection...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            image_array = np.array(image)
    elif camera_option == "Use Camera":
        captured_image = st.camera_input("Capture an image for emotion detection")
        if captured_image is not None:
            image = Image.open(captured_image)
            image_array = np.array(image)

    if 'image_array' in locals() and image_array is not None:
        st.image(image_array, caption='Captured Image', use_column_width=True)

        
        with st.spinner('Analyzing Emotion...'):  
            dominant_emotion = emotion_backend.detect_emotion(image_array)

        if dominant_emotion:
            st.markdown(f"<h3>Detected Emotion: {dominant_emotion.capitalize()}</h3>", unsafe_allow_html=True)
            

            recommendations = emotion_backend.enhanced_emotion_recommendations(dominant_emotion, giphy_api_key="your_giphy_api_key")

            
            st.success(f"**Motivational Quote:** {recommendations['quote']}")

            
            if recommendations['video_title'] and recommendations['video_url']:
                st.write(f"**Recommended Video:** [{recommendations['video_title']}]({recommendations['video_url']})")
                st.video(recommendations['video_url'])

            
            if recommendations['gif_url']:
                st.image(recommendations['gif_url'], caption="Here's a GIF for you!", use_column_width=True)

        else:
            st.error("Could not detect any emotion. Please try again.")

    st.markdown("</div>", unsafe_allow_html=True)

elif section == "🩺 Disease Detection":
    st.markdown("<h2>Disease Detection</h2>", unsafe_allow_html=True)
    
    symptoms_input = st.text_input("Enter symptoms separated by commas (e.g., itching, skin rash, fatigue):")

    if st.button("🔍 Predict Disease"):
        if symptoms_input:
            with st.spinner('Analyzing Symptoms...'):
                user_symptoms = [s.strip() for s in symptoms_input.split(',')]
                try:
                    predicted_disease = disease_backend.get_predicted_value(user_symptoms)
                    dis_des, precautions, medications, rec_diet, workout = disease_backend.helper(predicted_disease)

                    st.markdown(f"<h3>Predicted Disease: {predicted_disease}</h3>", unsafe_allow_html=True)
                    st.write(f"**Description**: {dis_des}")

                    st.write("### Precautions")
                    st.write("\n".join([f"- {pre}" for pre in precautions[0]]))

                    st.write("### Medications")
                    st.write("\n".join([f"- {med}" for med in medications]))

                    st.write("### Recommended Diet")
                    st.write("\n".join([f"- {diet}" for diet in rec_diet]))

                    st.write("### Suggested Workout")
                    st.write(workout)
                except KeyError:
                    st.error("Some symptoms might be misspelled or not recognized. Please try again.")
        else:
            st.error("Please enter symptoms to predict the disease.")
