# backend.py

import numpy as np
from fer import FER

# Load emotion detection model
emotion_detector = FER()

# Motivational quotes
motivational_quotes = [
    "Keep smiling, because life is a beautiful thing!",
    "Happiness is the best makeup.",
    "Every day may not be good, but there is something good in every day.",
    "Stay positive, work hard, make it happen!"
]

def detect_emotion(image):
    """Detect the dominant emotion from the image."""
    emotions = emotion_detector.detect_emotions(image)
    if emotions:
        top_emotion = emotions[0]['emotions']
        dominant_emotion = max(top_emotion, key=top_emotion.get)
        return dominant_emotion
    return None

def get_motivational_content():
    """Return a random motivational quote."""
    return np.random.choice(motivational_quotes)
