#app.py
from flask import Flask, render_template, request, redirect, flash, session, url_for, jsonify
from werkzeug.utils import secure_filename
import os
from analyzer_core import extract_text_from_pdf, analyze_report_with_gemini
from models import MedicalAnalysis

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'  # Secret key for session security (change in production)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Directory where uploaded files will be stored

# Allowed extensions for file uploads 
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure the upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    Returns True if file is a PDF.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Landing Page 
@app.route('/')
def landing():
    """Render the landing page."""
    return render_template('index.html')


# Upload Page
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """
    Handle file upload, extract text from PDF, and analyze using Gemini.
    """
    if request.method == 'POST':
        # Check if file part exists in request
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)

        file = request.files['file']

        # Check if a file was actually selected
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Validate and process PDF
        if file and allowed_file(file.filename):
            report_text = extract_text_from_pdf(file.stream)

            # Validate extracted text
            if not report_text:
                flash("PDF could not be read. It might be scanned or empty.")
                return redirect(request.url)

            # Analyze report text via Gemini
            analysis_result = analyze_report_with_gemini(report_text)

            if isinstance(analysis_result, MedicalAnalysis):
                # Save analysis to session for display
                session['analysis'] = analysis_result.model_dump()
                return redirect(url_for('show_results'))
            else:
                flash(f"Analysis Failed: {analysis_result.get('error', 'Unknown Error')}")
                return redirect(request.url)
        else:
            flash('Only PDF files allowed.')
            return redirect(request.url)

    return render_template('upload.html')


# Results Page
@app.route('/results')
def show_results():
    """Display analysis results stored in session."""
    analysis_data = session.get('analysis')

    if not analysis_data:
        flash("No analysis found. Upload a report first.")
        return redirect(url_for('upload_file'))

    return render_template('results.html', analysis=analysis_data)


# Chat Page
@app.route('/chat')
def chat_ui():
    """Render chat interface and reset chat history."""
    session['chat_history'] = []
    return render_template('chat.html')


# Chat API
@app.route('/chat_api', methods=['POST'])
def chat_api():
    """
    Handle AJAX chat messages and return Gemini analysis.
    """
    user_msg = request.json.get("message", "")

    if not user_msg:
        return jsonify({"error": "Empty message"}), 400

    # Perform analysis
    analysis_result = analyze_report_with_gemini(user_msg)

    if isinstance(analysis_result, MedicalAnalysis):
        return jsonify({"analysis": analysis_result.model_dump()})
    else:
        return jsonify({"error": "Analysis failed"}), 500


# Run Application
if __name__ == '__main__':
    # Enable debug mode for development
    app.run(debug=True)