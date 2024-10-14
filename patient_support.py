# patient_support.py
from transformers import pipeline


qa_model = pipeline("question-answering")

def get_medicine_info(question):
    """
    Takes a user's question and returns an AI-generated answer about medicines.
    """
    
    context =
    
    response = qa_model(question=question, context=context)
    return response['answer']
