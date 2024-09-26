def get_health_assistance(query, category):
    """
    Uses a generative AI model (e.g., GPT) to provide assistance on health-related questions based on categories.
    """
    # Defining prompt templates for each category
    prompts = {
        "Symptoms & Diagnosis": f"Provide a health diagnosis or medical information based on these symptoms or condition: {query}.",
        "Nutrition & Diet": f"Provide diet and nutritional advice based on this query: {query}.",
        "Mental Health": f"Provide mental health support and advice for the following issue: {query}.",
        "Fitness & Exercise": f"Provide fitness or workout advice for the following query: {query}.",
    }

    # Choose the prompt based on the category selected by the user
    chosen_prompt = prompts.get(category, f"Assist with the following health-related query: {query}")

    try:
        # Call OpenAI's API
        response = openai.Completion.create(
            engine="text-davinci-003",  # Using GPT-3.5 for example
            prompt=chosen_prompt,
            max_tokens=150,
            temperature=0.7
        )
        # Extract response text
        answer = response.choices[0].text.strip()
        return answer
    except Exception as e:
        return f"Error: {str(e)}"
