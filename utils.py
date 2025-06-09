import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your environment or .env file.")

genai.configure(api_key=api_key)


def query_gemini(prompt, model="gemini-2.0-flash", max_tokens=500, temperature=0.7):
    """
    Sends a prompt to Gemini and returns the generated response.

    Args:
        prompt (str): The prompt text to send.
        model (str): The model name.
        max_tokens (int): Max tokens to generate.
        temperature (float): Sampling temperature.

    Returns:
        str: The generated text from Gemini.
    """
    try:
        model_obj = genai.GenerativeModel(model)
        response = model_obj.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error querying Gemini: {e}")
        return "Sorry, I am having trouble processing your request right now."
