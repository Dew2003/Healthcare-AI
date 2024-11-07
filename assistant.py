# assistant.py

import requests

def get_health_assistance(query, category):
    API_KEY="7eff5afad45744488b4c01d1c0291ae5"
    #API_KEY = "d2206f3d828044788d555ff324064895"
    
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }

    
    prompt = f"Provide health assistance for this query: '{query}' under the category '{category}'."

    
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful health assistant AI."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800
    }

    #ENDPOINT = "https://asst.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"
    ENDPOINT = "https://hreport.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2024-08-01-preview"

    # Send request
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

    # Parse the JSON response and extract the AI's message
    response_json = response.json()
    ai_message = response_json['choices'][0]['message']['content']

    return ai_message
