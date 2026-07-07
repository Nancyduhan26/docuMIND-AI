import google.generativeai as genai
from config import GOOGLE_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)
def ask_gemini(context, question):
        prompt = f"""
    Context:
    {context}

    Question:
    {question}
    """
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text