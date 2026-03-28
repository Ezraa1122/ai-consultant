import dotenv
import os

import streamlit as st
from pypdf import PdfReader
from openai import OpenAI

#initialize client (OpenAI class)
dotenv.load_dotenv()
client = OpenAI(
    base_url = "https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN")
)

#pdf text extraction
def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

#AI analyzing
def analyze_text(text):
    promt = f"""
    You are a top-tier strategy consultant.

    Analyze the following document and provide:

    1. Key Insights (3-5 bullet points)
    2. Risks (2-3 bullet points)
    3. Recommendations (3-5 bullet points)

    Keep it concise, structured, and business-focused.

    Document:
    {text[:8000]}
    """
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
                {
                    "role" : "system",
                    "content" : "You are a strategy consultant at a top consulting firm."
                },
                {
                    "role" : "user",
                    "content" : promt
                }
        ]
    )

    #print(response.model_dump)

    return response.choices[0].message.content

#UI
st.set_page_config(page_title="AI Consultant")
st.title("AI Consultant")

uploaded_file = st.file_uploader("Upload a buisness report (PDF)")

if uploaded_file:
    st.info("Processsing document...")
    text = extract_text(uploaded_file)

    if text.strip():
        result = analyze_text(text)
        st.success("Analysis complete!")
        st.write(result)
    else:
        st.error("Could not extract text from this PDF.")