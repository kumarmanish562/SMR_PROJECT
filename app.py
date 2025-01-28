from flask import Flask, render_template, request
import google.generativeai as genai
import PyPDF2
import pytesseract
from PIL import Image
import docx
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)


# Configure Gemini API (replace with your actual API key)
genai.configure(api_key='')
model = genai.GenerativeModel('gemini-pro')

# Language mapping
LANGUAGES = {
    'hindi': 'Hindi',
    'bengali': 'Bengali',
    'punjabi': 'Punjabi',
    'marathi': 'Marathi'
}

# Set upload folder
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'bmp', 'tiff'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to extract text from PDF
def extract_text_from_pdf(filepath):
    text = ""
    with open(filepath, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(filepath):
    doc = docx.Document(filepath)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Function to extract text from TXT
def extract_text_from_txt(filepath):
    with open(filepath, 'r') as file:
        return file.read()

# Function to extract text from images (using OCR)
def extract_text_from_image(filepath):
    # Open the image using Pillow
    img = Image.open(filepath)
    
    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(img)
    return text

# Main function to handle file extraction based on file type
def extract_text_from_file(filepath):
    ext = filepath.rsplit('.', 1)[1].lower()
    
    if ext == 'pdf':
        return extract_text_from_pdf(filepath)
    elif ext == 'docx':
        return extract_text_from_docx(filepath)
    elif ext == 'txt':
        return extract_text_from_txt(filepath)
    elif ext in ['jpg', 'jpeg', 'png', 'bmp', 'tiff']:
        return extract_text_from_image(filepath)
    else:
        return "Unsupported file format"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    translation = ''
    if request.method == 'POST':
        # Check if file is uploaded
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            
            if allowed_file(file.filename):
                # Save the file temporarily
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Extract text from the uploaded file
                text = extract_text_from_file(filepath)
        
        # Check if text is pasted
        elif request.form.get('text'):
            text = request.form.get('text')
        
        else:
            return render_template('translate.html', 
                                   translation='Please provide text or upload a file.', 
                                   languages=LANGUAGES)
        
        # Get selected language
        target_language = request.form.get('language', 'hindi')
        
        # Translate using Gemini
        try:
            response = model.generate_content(
                f"Translate this text to {LANGUAGES[target_language]}: {text}"
            )
            translation = response.text
        except Exception:
            translation = "Translation error occurred."
    
    return render_template('translate.html', 
                           translation=translation, 
                           languages=LANGUAGES)

# Define other routes for your app (e.g., service, language, etc.)
@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/certificate')
def certificate():
    return render_template('certificate.html')

@app.route('/financial')
def financial():
    return render_template('financial.html')

@app.route('/marketing')
def marketing():
    return render_template('marketing.html')

@app.route('/medical')
def medical():
    return render_template('medical.html')

@app.route('/legal ')
def legal():
    return render_template('legal.html')

@app.route('/quote')
def quote():
    return render_template('quote.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/language')
def language():
    return render_template('language.html')
@app.route('/hindi')
def hindi():
    return render_template('hindi.html')
@app.route('/english')
def english():
    return render_template('english.html')

@app.route('/tamil')
def tamil():
    return render_template('tamil.html')

@app.route('/punjabi')
def punjabi():
    return render_template('punjabi.html')

@app.route('/kannada')
def kannada():
    return render_template('kannada.html')

@app.route('/telugu')
def telugu():
    return render_template('telugu.html')

@app.route('/malayalam')
def malayalam():
    return render_template('malayalam.html')

@app.route('/bengali')    
def bengali():
    return render_template('bengali.html')

@app.route('/marathi')
def marathi():
    return render_template('marathi.html')

@app.route('/gujarati')
def gujarati():
    return render_template('gujarati.html')

@app.route('/odia')
def odia():
    return render_template('odia.html')

@app.route('/assamese')
def assamese():
    return render_template('assamese.html')

@app.route('/sanskrit')
def sanskrit():
    return render_template('sanskrit.html')




# Custom error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
