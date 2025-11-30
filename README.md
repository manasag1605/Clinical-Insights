# Clinical-Insights
Clinical Insights Assistant

A Flask application that analyzes medical PDF reports using Google Gemini 2.5 Pro and presents the results in a clean, patient-friendly dashboard.
Includes two modes of interaction:
PDF Upload → AI Dashboard Summary
Interactive Medical Chatbot


Features:

->PDF Report Interpretation: Extracts text from uploaded PDFs and generates structured insights: severity, abnormal findings, precautions, medication caution, and physician recommendation.

->Medical Chatbot: Interactive chat interface producing the same structured MedicalAnalysis output.

->Schema-Guaranteed Safety: Uses Pydantic models to enforce safe, consistent AI responses.

->Modern UI: Template-driven frontend with responsive design and severity visuals.

Tech Stack:

Backend: Python, Flask, Pydantic
AI: Google Gemini (via google-genai)
Frontend: HTML, CSS (custom modern theme)
PDF Extraction: pypdf
Config: .env for API keys

Project Structure: 

clinical-insights/
│── app.py                     # Flask routes & core logic
│── analyzer_core.py           # PDF text extraction + Gemini request
│── models.py                  # Pydantic MedicalAnalysis schema
│── requirements.txt
│── .env                       # API key (not committed)
│── static/
│     ├── style.css
│     ├── doctor.svg
│     └── user.svg
│── templates/
│     ├── index.html           # Landing page
│     ├── upload.html          # PDF upload page
│     ├── results.html         # Analysis dashboard
│     └── chat.html            # Medical chatbot UI
└── uploads/                   # Temporary uploads (auto-created)

Installation: 

pip install -r requirements.txt

Create a .env file:

GOOGLE_API_KEY=your_api_key_here

Run the app:

python app.py

Disclaimer:
This application provides AI-generated insights for informational use only.
It is not a substitute for professional medical diagnosis or treatment.

