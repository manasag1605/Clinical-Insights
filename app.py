# app.py
from dotenv import load_dotenv
load_dotenv() # IMPORTANT: This loads the key from .env

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
# Import core logic and Pydantic model
from analyzer_core import extract_text_from_pdf, analyze_report_with_gemini
from models import MedicalAnalysis 

app = Flask(__name__)
# Security configuration
app.config['SECRET_KEY'] = 'your_super_secret_key_here' # <-- Change this!
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part selected')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            # 1. Extraction: Read the file stream directly from Flask's request object
            report_text = extract_text_from_pdf(file.stream)
            
            if not report_text:
                flash("Failed to extract readable text from the PDF. It might be a scanned image or empty.")
                return redirect(request.url)

            # 2. Analysis
            analysis_result = analyze_report_with_gemini(report_text)
            
            if isinstance(analysis_result, MedicalAnalysis):
                # SUCCESS: Render the results page
                return render_template('results.html', analysis=analysis_result)
            else:
                # FAILURE: Show error message
                flash(f"Analysis Failed: {analysis_result.get('error', 'Unknown Error')}")
                return redirect(request.url)
                
        else:
            flash('File type not allowed. Please upload a PDF.')
            return redirect(request.url)
            
    return render_template('index.html')

if __name__ == '__main__':
    if not os.getenv("GEMINI_API_KEY"):
        print("!!! WARNING: GEMINI_API_KEY environment variable not set. Analysis will fail. !!!")
    app.run(debug=True)