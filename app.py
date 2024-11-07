import streamlit as st
from streamlit_lottie import st_lottie
import json
import numpy as np
from PIL import Image
#import disease_backend  
import emotion_backend 
from report import analyze_report
from assistant import get_health_assistance
import requests



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
#st.snow()

section = st.sidebar.radio(
    "Select an option",
    ("🤖 Health Assistant AI", "😊 Emotion Detection","🩺Report Analysis")
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


elif section == "🩺Report Analysis":
    st.title("Medical Report Analysis")

    # File uploader to allow user to upload the report
    uploaded_file = st.file_uploader("Upload a medical report", type=["jpg", "jpeg", "png"])

    # If a file is uploaded, process it
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Report", use_column_width=True)

        # Analyze the report using the backend function
        with st.spinner("Analyzing the report..."):
            diagnosis, error = analyze_report(uploaded_file)

        if error:
            st.error(error)
        elif diagnosis:
            st.write("Diagnosis:")
            st.write(diagnosis)
