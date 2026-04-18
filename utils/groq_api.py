from groq import Groq
import os
import streamlit as st

# Load API key safely
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

# Initialize client only if key exists
client = Groq(api_key=api_key) if api_key else None


def analyze_text_with_groq(text: str) -> str:
    """
    Analyze text for privacy risk using Groq API.
    """

    # 🔴 Handle missing API key gracefully
    if not client:
        return "⚠️ Groq API key is missing. Running in limited mode. Please configure API key."

    prompt = (
        "You are a privacy risk analyzer. Identify sensitive info like email, phone numbers, addresses, "
        "bank details, etc., in the given text and give a risk score (Low, Medium, High) with recommendations.\n\n"
        f"Text: {text}"
    )

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Error calling Groq API: {str(e)}"
