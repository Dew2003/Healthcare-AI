import streamlit as st
from streamlit_lottie import st_lottie
import json
import numpy as np
from PIL import Image
import emotion_backend 
from report import analyze_report
from assistant import get_health_assistance


path = "a1.json"
with open(path, "r") as file:
    url = json.load(file)



st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Select a section",
    ("🏠 Home", "🤖 Health Assistant AI", "😊 Emotion Detection", "🩺 Report Analysis"),
    index=0  
)




if section == "🏠 Home":
    st.title("Welcome to Healthcare AI")
    st_lottie(url, height=150, width=150, speed=0.5, loop=True)

    st.markdown("""
        ### Choose an option to get started:
        
        **🤖 Health Assistant AI**  
        Ask any health-related questions, including information about symptoms, treatments, fitness advice, and medicines.
        
        **😊 Emotion Detection**  
        Capture or upload an image to detect your emotion and receive motivational content based on your mood.
        
        **🩺 Report Analysis**  
        Upload a medical report image to get AI-assisted analysis of the report's findings.
    """, unsafe_allow_html=True)


if section == "🤖 Health Assistant AI":
    st.markdown("<h2>💬 Health Assistance via AI</h2>", unsafe_allow_html=True)

    user_query = st.text_input("Ask any health-related question (e.g., symptoms, treatments, fitness advice, About Medicine):")
    category = st.radio(
        "What kind of advice are you looking for?",
        ("Symptoms & Diagnosis", "Nutrition & Diet", "Mental Health", "Fitness & Exercise", "About Medicine")
    )

    if st.button("💡 Get AI Assistance"):
        if user_query and category:
            with st.spinner("Thinking..."):
                ai_response = get_health_assistance(user_query, category)
                st.markdown(f"**AI Response:**\n\n{ai_response}")
        else:
            st.error("Please enter a question and select a category.")


elif section == "😊 Emotion Detection":
    st.markdown("<h2>Emotion Detection and Motivation</h2>", unsafe_allow_html=True)
    
    camera_option = st.radio("Select Input Method", ("Upload Image", "Use Camera"))

    if camera_option == "Upload Image":
        uploaded_file = st.file_uploader("Choose an image for emotion detection...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            image_array = np.array(image)
            st.image(image_array, caption='Uploaded Image', use_column_width=True)
    elif camera_option == "Use Camera":
        captured_image = st.camera_input("Capture an image for emotion detection")
        if captured_image is not None:
            image = Image.open(captured_image)
            image_array = np.array(image)
            st.image(image_array, caption='Captured Image', use_column_width=True)

    if 'image_array' in locals() and image_array is not None:
        with st.spinner('Analyzing Emotion...'):  
            dominant_emotion = emotion_backend.detect_emotion(image_array)

        if dominant_emotion:
            st.markdown(f"<h3>Detected Emotion: {dominant_emotion.capitalize()}</h3>", unsafe_allow_html=True)
            recommendations = emotion_backend.enhanced_emotion_recommendations(dominant_emotion, giphy_api_key="your_giphy_api_key")
            st.success(f"**Motivational Quote:** {recommendations['quote']}")
            if recommendations['video_url']:
                st.video(recommendations['video_url'])


elif section == "🩺 Report Analysis":
    st.markdown("<h2>Medical Report Analysis</h2>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload a medical report", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Report", use_column_width=True)
        with st.spinner("Analyzing the report..."):
            diagnosis, error = analyze_report(uploaded_file)
        if error:
            st.error(error)
        elif diagnosis:
            st.write("Diagnosis:")
            st.write(diagnosis)

st.markdown("---")
st.markdown("Powered by Healthcare AI  2024. For support, contact [Dewashish Dwivedi](mailto:ddwivedi2003@gmail.com).")

