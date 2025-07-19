from groq import Groq
import os
import streamlit as st
from dotenv import load_dotenv

api_key=st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY is missing! Please add it to Streamlit secrets or your environment variables."
    )

# Initialize Groq client
client=Groq(api_key=api_key)


def analyze_text_with_groq(text: str)->str:
    """
    Analyze text for privacy risk using Groq API.
    """
    prompt=(
        "You are a privacy risk analyzer. Identify sensitive info like email, phone numbers, addresses, "
        "bank details, etc., in the given text and give a risk score (Low, Medium, High) with recommendations.\n\n"
        f"Text: {text}"
    )

    response=client.chat.completions.create(
        model="llama3-8b-8192",  
        messages=[{"role": "user","content":prompt}],
        temperature=0.3
    )

   
    return response.choices[0].message.content

