import streamlit as st
from streamlit_lottie import st_lottie
import json
import numpy as np
from PIL import Image
import requests
from datetime import datetime
import emotion_backend 
from report import analyze_report
from assistant import get_health_assistance

# Load Lottie animation for homepage
path = "a1.json"
with open(path, "r") as file:
    url = json.load(file)

# Function to fetch user's location using IP address
def get_location():
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()
        return data.get("city", "London")  # Default to London if location not found
    except Exception:
        return "London"  # Fallback location

# Function to fetch weather data
def get_weather(city):
    api_key = "265e26310e7e16d6972f798c9be865a1s"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(weather_url)
    data = response.json()
    
    if data.get("main"):
        temperature = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        advice = generate_weather_advice(temperature, weather)
        return temperature, weather, advice
    else:
        return None, None, "Could not fetch weather data."

# Function to provide advice based on temperature and weather
def generate_weather_advice(temperature, weather):
    if temperature < 10:
        return "It's quite cold. Stay warm and consider indoor activities!"
    elif temperature < 20:
        return "The weather is cool. A light jacket might be needed!"
    elif temperature < 30:
        return "The weather is pleasant. Perfect for a walk outside!"
    else:
        return "It's quite warm. Stay hydrated and avoid direct sunlight during peak hours!"

# Sidebar navigation
st.sidebar.title("Navigation")
selected_sidebar_section = st.sidebar.radio(
    "Select a section",
    ("🏠 Home", "🤖 Health Assistant AI", "😊 Emotion Detection", "🩺 Report Analysis")
)

# Home Page
if selected_sidebar_section == "🏠 Home":
    st.title("Welcome to Healthcare AI")
    st_lottie(url, height=150, width=150, speed=0.5, loop=True)

    # Automatically fetch the user's location and display weather
    st.markdown("### 🌤 Current Weather")
    city = get_location()
    st.write(f"Detected Location: **{city}**")

    if city:
        temperature, weather, advice = get_weather(city)
        if temperature is not None:
            st.write(f"**Temperature:** {temperature}°C")
            st.write(f"**Weather:** {weather.capitalize()}")
            st.write(f"**Advice:** {advice}")
        else:
            st.error("Could not retrieve weather information. Please try again later.")
    
    st.markdown("""
        ### Choose an option to get started:
        
        **🤖 Health Assistant AI**  
        Ask any health-related questions, including information about symptoms, treatments, fitness advice, and medicines.
        
        **😊 Emotion Detection**  
        Capture or upload an image to detect your emotion and receive motivational content based on your mood.
        
        **🩺 Report Analysis**  
        Upload a medical report image to get AI-assisted analysis of the report's findings.
    """, unsafe_allow_html=True)

# (Remaining sections: Health Assistant AI, Emotion Detection, and Report Analysis)

st.markdown("---")
st.markdown("Powered by Healthcare AI © 2024. For support, contact [ddwivedi2003@gmail.com](mailto:ddwivedi2003@gmail.com).")
