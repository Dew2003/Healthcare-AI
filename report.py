
from PIL import Image
import pytesseract
import requests

# Configuration
API_KEY = "7eff5afad45744488b4c01d1c0291ae5"
ENDPOINT = "https://hreport.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2024-02-15-preview"

# Function to process the image and analyze the report
def analyze_report(uploaded_file):
    try:
        # Open the image from the uploaded file
        image = Image.open(uploaded_file)
        
        # Extract text using pytesseract (OCR)
        extracted_text = pytesseract.image_to_string(image)
        if not extracted_text.strip():
            return None, "No text could be extracted from the image."

        # Prepare payload for GPT-4
        headers = {
            "Content-Type": "application/json",
            "api-key": API_KEY,
        }

        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AI assistant that helps people analyze medical reports."
                },
                {
                    "role": "user",
                    "content": f"Diagnose the report:\n\n{extracted_text}"
                }
            ],
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 800
        }

        # Send request to Azure OpenAI GPT-4 API
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()

        if "choices" in response_data:
            diagnosis = response_data['choices'][0]['message']['content']
            return diagnosis, None
        else:
            return None, "No valid response from GPT-4."

    except Exception as e:
        return None, f"Failed to process the image or request. Error: {str(e)}"

