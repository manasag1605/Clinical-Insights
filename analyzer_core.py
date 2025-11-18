# analyzer_core.py
import os
from dotenv import load_dotenv # Needed for robust key loading
from google import genai
from google.genai import types
from pypdf import PdfReader
from models import MedicalAnalysis 

# IMPORTANT: Call load_dotenv() here as well to guarantee key availability
load_dotenv() 

# The Gemini Client is initialized after the key is loaded
client = genai.Client()

def extract_text_from_pdf(pdf_stream) -> str:
    """Extracts text content from a PDF file stream (from Flask upload)."""
    try:
        reader = PdfReader(pdf_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"ERROR during PDF extraction: {e}")
        return ""

def analyze_report_with_gemini(report_text: str) -> MedicalAnalysis | dict:
    """Analyzes text using Gemini and returns a structured Pydantic object."""
    if not report_text:
        return {"error": "Input text is empty. Cannot analyze."}

    system_instruction = (
        "You are a highly analytical, empathetic, and CAUTIOUS AI medical assistant. "
        "Your analysis must be strictly based on the provided text. "
        "You MUST return the results in the exact JSON schema provided. "
        "ALWAYS include a prominent disclaimer."
    )

    prompt = (
        "Analyze the following raw medical report text from a patient's lab/imaging report. "
        "Extract the key abnormal data points and provide a severity analysis, "
        "precautions, and a clear physician recommendation, "
        "strictly adhering to the requested JSON schema. \n\n"
        "MEDICAL REPORT TEXT:\n"
        f"---{report_text}---"
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=MedicalAnalysis,
                system_instruction=system_instruction
            )
        )
        analysis_data = MedicalAnalysis.model_validate_json(response.text)
        return analysis_data

    except Exception as e:
        return {"error": f"AI Analysis Failed: {e}"}