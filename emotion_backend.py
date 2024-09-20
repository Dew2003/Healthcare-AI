# emotion_backend.py

from fer import FER
import numpy as np

# Load emotion detection model
emotion_detector = FER()

# List of motivational quotes
motivational_quotes = [
    "Keep smiling, because life is beautiful!",
    "Happiness is the best makeup.",
    "Every day may not be good, but there is something good in every day.",
    "Stay positive, work hard, make it happen!"
]

def detect_emotion(image_array):
    """
    Detect the dominant emotion in the image using the FER model.
    """
    emotions = emotion_detector.detect_emotions(image_array)
    if emotions:
        top_emotion = emotions[0]['emotions']
        dominant_emotion = max(top_emotion, key=top_emotion.get)
        return dominant_emotion
    return None

def get_motivational_content():
    """
    Returns a random motivational quote.
    """
    return np.random.choice(motivational_quotes)
