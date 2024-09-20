# app.py

import streamlit as st
from PIL import Image
import numpy as np
import cv2

# Import functions from the backend
from disease_backend import detect_emotion, get_motivational_content

def main():
    st.title("Emotion Detection App")
    st.write("This app uses computer vision to detect whether you're happy. If not, it provides motivational content!")

    # Webcam capture
    img_file_buffer = st.camera_input("Take a picture")

    if img_file_buffer is not None:
        # To read image file buffer as a PIL Image and convert to OpenCV format
        img = Image.open(img_file_buffer)
        img = np.array(img)  # Convert PIL image to numpy array (OpenCV format)

        # Perform emotion detection
        dominant_emotion = detect_emotion(img)

        # Display the emotion detected
        if dominant_emotion:
            st.write(f"Detected Emotion: {dominant_emotion}")
            if dominant_emotion == "happy":
                st.success("You are happy! Keep smiling!")
            else:
                st.warning("You are not happy. Here's something to cheer you up:")
                st.write(f"**Motivational Quote:** {get_motivational_content()}")
        else:
            st.write("No faces detected. Please try again.")

        # Display the image
        st.image(img, caption=f"Detected Emotion: {dominant_emotion}", use_column_width=True)

if __name__ == '__main__':
    main()
