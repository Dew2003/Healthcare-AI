# disease_detection.py

import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

# Load the pre-trained model
model = load_model('model.h5')

def predict_disease(image):
    """
    Takes an uploaded image, processes it, and returns the predicted disease label.
    """
    img = Image.open(image)
    img = img.resize((224, 224))  # Adjust to the input size of your model
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=1)  # Get predicted class

    # Map to disease names (replace with actual labels from your model)
    disease_labels = {0: 'Disease A', 1: 'Disease B', 2: 'Disease C'}
    return disease_labels.get(predicted_class[0], "Unknown Disease")
