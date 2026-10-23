import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key nahi mili. .env file check karo.")
else:
    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model="gemma-4-31b-it",
            contents="Classify this support ticket: I was charged twice and need a refund immediately. Return topic and urgency."
        )

        print(response.text)

    except Exception as e:
        print("Model test failed:", e)