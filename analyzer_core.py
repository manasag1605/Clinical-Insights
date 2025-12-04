#analyzer_core.py
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pypdf import PdfReader
from models import MedicalAnalysis

# Load environment variables from .env file
load_dotenv()

# Initialize Gemini client
client = genai.Client()


def extract_text_from_pdf(pdf_stream) -> str:
    """
    Extract text content from a PDF file stream.
    Returns the extracted text or an empty string if extraction fails.
    """
    try:
        reader = PdfReader(pdf_stream)
        text = ""

        # Loop through each page and extract text
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""

def analyze_report_with_gemini(report_text: str) -> MedicalAnalysis | dict:
    """
    Analyze the extracted medical report text using Gemini AI.
    Returns a MedicalAnalysis object on success or dict with error details on failure.
    """
    if not report_text:
        return {"error": "Empty input."}

    system_instruction = (
        "You are a cautious AI medical assistant. Respond strictly in JSON schema format."
    )

    # User prompt for model
    prompt = f"Analyze this medical report text:\n---{report_text}---"

    try:
        # Send request to Gemini model
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=[{"role": "user", "parts": [{"text": prompt}]}],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=MedicalAnalysis,
                system_instruction=system_instruction
            )
        )

        # Validate and convert returned JSON into Pydantic model
        return MedicalAnalysis.model_validate_json(response.text)

    except Exception as e:
        return {"error": f"AI Analysis Failed: {e}"}