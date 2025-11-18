# models.py
from pydantic import BaseModel, Field
from typing import List, Literal

# Define the acceptable categories for severity and doctor type
Severity = Literal["Low", "Moderate", "High - Urgent Visit Recommended", "Critical - Immediate Physician Visit Required"]
DoctorType = Literal["General Practitioner", "Cardiologist", "Endocrinologist", "Oncologist", "Pediatrician", "Gastroenterologist", "Other Specialist"]

class MedicalAnalysis(BaseModel):
    """Structured data output for the medical report analysis."""
    severity_analysis: Severity = Field(
        description="Overall severity level based on the report findings."
    )
    key_abnormal_findings: List[str] = Field(
        description="A list of 3-5 most critical or abnormal findings from the report in patient-friendly language."
    )
    precautions_and_next_steps: List[str] = Field(
        description="Clear, actionable steps and precautions the patient should take immediately (e.g., monitor blood pressure, change diet)."
    )
    medication_suggestion: str = Field(
        description="A cautious suggestion regarding potential medication/supplement needs. Must start with a strong disclaimer: 'CONSULT A DOCTOR. This AI cannot prescribe medications.'"
    )
    physician_recommendation: str = Field(
        description="A clear instruction on whether a doctor's visit is required and how urgent it is."
    )
    recommended_doctor_type: DoctorType = Field(
        description="The recommended type of medical professional to visit based on the primary findings."
    )