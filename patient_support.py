# patient_support.py
from transformers import pipeline

# Load a generative model (Hugging Face pipeline)
qa_model = pipeline("question-answering")

def get_medicine_info(question):
    """
    Takes a user's question and returns an AI-generated answer about medicines.
    """
    # You can provide a more complex context from a medicine database or API
    context = """
    Paracetamol is used to treat mild pain and fever. Ibuprofen is another common anti-inflammatory medicine. Consult your doctor for more details.
    """
    
    response = qa_model(question=question, context=context)
    return response['answer']
