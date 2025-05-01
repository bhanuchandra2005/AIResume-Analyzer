from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
import platform
import subprocess
from PIL import Image 
import pdf2image
import google.generativeai as genai
import datetime
import PyPDF2
import tempfile
import sys

# Page configuration
st.set_page_config(
    page_title="Resume AI Analyzer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced modern CSS with glassmorphism and subtle animations
st.markdown("""
<style>
    /* Main theme colors - Enhanced palette */
    :root {
        --primary-color: #3E64FF;
        --primary-light: #5A7DFF;
        --secondary-color: #5EDFFF;
        --accent-color: #FF9190;
        --text-color: #2D3748;
        --light-bg: #F9FAFE;
        --card-bg: rgba(255, 255, 255, 0.9);
        --border-color: rgba(226, 232, 240, 0.8);
        --glass-bg: rgba(255, 255, 255, 0.7);
        --glass-border: rgba(255, 255, 255, 0.2);
        --glass-shadow: rgba(0, 0, 0, 0.05);
    }
    
    /* Global styles and animations */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Remove custom background gradient to use default Streamlit background */
    /* .stApp {
        background: linear-gradient(135deg, #F5F7FF 0%, #F0FCFF 100%);
    } */
    
    /* Animation keyframes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes glowPulse {
        0% { box-shadow: 0 0 5px rgba(99, 102, 241, 0.2); }
        50% { box-shadow: 0 0 15px rgba(99, 102, 241, 0.4); }
        100% { box-shadow: 0 0 5px rgba(99, 102, 241, 0.2); }
    }
    
    /* Typography */
    .main-header {
        font-size: 3.2rem;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-align: center;
        letter-spacing: -0.02em;
        animation: fadeIn 0.8s ease-out;
    }
    
    .tagline {
        font-size: 1.25rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
        animation: fadeIn 0.8s ease-out 0.2s both;
    }
    
    .sub-header {
        font-size: 1.6rem;
        color: var(--primary-color);
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border-color);
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px var(--glass-shadow);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.4rem;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(62, 100, 255, 0.25);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.2),
            transparent
        );
        transition: 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(79, 70, 229, 0.35);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Improved file uploader */
    .stFileUploader {
        border: 2px dashed var(--primary-light);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 15px;
        background-color: rgba(238, 242, 255, 0.5);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: var(--primary-color);
        background-color: rgba(238, 242, 255, 0.8);
    }
    
    /* Text area and input styling */
    .stTextArea, .stTextInput {
        transition: all 0.2s ease;
    }
    
    .stTextArea:focus, .stTextInput:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
    }
    
    .stTextArea textarea, .stTextInput input {
        border-radius: 10px;
        border: 1px solid var(--border-color);
        padding: 1rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Feature boxes with improved design */
    .feature-box {
        background: linear-gradient(145deg, #EEF2FF, #E0F2FE);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        border-left: 4px solid #4F46E5;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    
    .feature-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    }
    
    .feature-title {
        font-weight: 600;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    
    /* Success message */
    .stSuccess {
        background-color: rgba(209, 250, 229, 0.9) !important;
        color: #065F46 !important;
        border: 1px solid rgba(110, 231, 183, 0.5) !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
    }
    
    /* Info message */
    .stInfo {
        background-color: rgba(49, 70, 101, 0.6) !important;
        color: rgba(255, 255, 255, 0.9) !important;
        border: none !important;
        border-radius: 8px !important;
    }
    
    /* Warning message */
    .stWarning {
        background-color: rgba(254, 240, 138, 0.8);
        color: #854D0E;
        border: 1px solid rgba(252, 211, 77, 0.5);
        border-radius: 12px;
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
    }
    
    /* Error message */
    .stError {
        background-color: rgba(254, 205, 211, 0.8);
        color: #9F1239;
        border: 1px solid rgba(251, 113, 133, 0.5);
        border-radius: 12px;
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
    }
    
    /* Preview box with subtle shadow */
    .preview-box {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--border-color);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.03);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        transition: all 0.3s ease;
    }
    
    .preview-box:hover {
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
    }
    
    /* Results section styling - ensure everything is white */
    .result-content h1, .result-content h2, .result-content h3, 
    .result-content h4, .result-content h5, .result-content h6 {
        color: white !important;
        font-weight: 700 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    .result-content p, .result-content li, .result-content span, 
    .result-content div, .result-content code, .result-content pre,
    .result-content strong, .result-content b, .result-content em, 
    .result-content i, .result-content a, .result-content blockquote,
    .result-content td, .result-content th, .result-content tr,
    .result-content caption, .result-content section, .result-content article {
        color: white !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }
    
    /* Ensure markdown formatting is displayed properly */
    .result-content ul, .result-content ol {
        margin-bottom: 1.5rem !important;
        color: white !important;
    }
    
    .result-content * {
        color: white !important;
    }
    
    /* Footer cards styling */
    .footer-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7));
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--glass-border);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.03);
        transition: all 0.3s ease;
    }
    
    .footer-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.06);
    }
    
    /* Streamlit element customization */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    /* Remove padding from main container edges */
    .main .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Custom progress bar for spinner */
    .stSpinner > div {
        border-top-color: var(--primary-color) !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    /* Team member cards hover effect */
    .team-card {
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        z-index: 1;
    }
    
    .team-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, var(--primary-light) 0%, var(--secondary-color) 100%);
        opacity: 0;
        z-index: -1;
        transition: opacity 0.3s ease;
        border-radius: 8px;
    }
    
    .team-card:hover::before {
        opacity: 0.03;
    }
    
    .team-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Animated border for feature cards */
    @keyframes borderGlow {
        0% { border-color: var(--primary-color); }
        50% { border-color: var(--secondary-color); }
        100% { border-color: var(--primary-color); }
    }
    
    .animated-border {
        animation: borderGlow 4s infinite;
    }
    
    /* File uploader improvements for better visibility */
    .stFileUploader > div > label {
        color: #2D3748 !important;
        font-weight: 500 !important;
    }
    
    .stFileUploader > div > div > span {
        color: #2D3748 !important;
    }
    
    /* Improve visibility of success messages */
    .stSuccess {
        background-color: rgba(209, 250, 229, 0.9) !important;
        color: #065F46 !important;
        border: 1px solid rgba(110, 231, 183, 0.5) !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
    }
    
    /* Make all UI text more visible */
    .uploadedFileName, .stMarkdown p, .stFileUploader p {
        color: #2D3748 !important;
        font-weight: 500 !important;
    }
    
    /* Make labels and text inputs more visible */
    label, .stTextInput, .stTextArea, .stSelectbox, div[data-baseweb="select"] span {
        color: #2D3748 !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)

# Configure the API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    # Fallback to hardcoded key if environment variable is not set
    genai.configure(api_key="AIzaSyDydWxM_3IoML4ZPSe-YAlBQOZvXGCz8PI")

def check_poppler_installation():
    """Check if poppler is installed and return its version and possible paths."""
    paths_to_check = [
        # Standard system paths
        "/usr/bin/pdftoppm",
        "/usr/local/bin/pdftoppm",
        # Potential Streamlit Cloud paths
        "/home/appuser/.conda/bin/pdftoppm",
        "/app/.apt/usr/bin/pdftoppm"
    ]
    
    results = {
        "found": False,
        "version": None,
        "path": None,
        "paths_checked": paths_to_check
    }
    
    # First try which command (should work on Unix systems)
    try:
        path = subprocess.check_output(["which", "pdftoppm"], text=True).strip()
        if path:
            results["found"] = True
            results["path"] = path
            # Try to get version
            try:
                version = subprocess.check_output([path, "-v"], stderr=subprocess.STDOUT, text=True).strip()
                results["version"] = version
            except:
                pass
            return results
    except:
        # which command failed, continue checking specific paths
        pass
        
    # Check each potential path
    for path in paths_to_check:
        if os.path.exists(path):
            results["found"] = True
            results["path"] = path
            try:
                version = subprocess.check_output([path, "-v"], stderr=subprocess.STDOUT, text=True).strip()
                results["version"] = version
            except:
                pass
            break
    
    return results

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # If pdf_content is a dictionary with 'text' key, it's our text fallback
    if isinstance(pdf_content, dict) and 'text' in pdf_content:
        # Include the text directly in the prompt
        text_prompt = f"""Resume content:
{pdf_content['text']}

Job Description:
{prompt}

{input}"""
        response = model.generate_content(text_prompt)
    else:
        # Normal flow with image
        response = model.generate_content([input, pdf_content[0], prompt])
    
    return response.text

def extract_text_with_pypdf2(uploaded_file):
    # Extract text from PDF using PyPDF2
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            ## First try with pdf2image and poppler
            try:
                # Check poppler installation - might be useful for debugging
                poppler_info = check_poppler_installation()
                
                # Save PDF to a temporary file (sometimes helps with cloud environments)
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
                    temp_pdf.write(uploaded_file.read())
                    temp_pdf_path = temp_pdf.name
                
                # Different handling for Windows vs Linux/Cloud environments
                if platform.system() == "Windows":
                    # Windows-specific path
                    poppler_path = r"C:\Program Files (x86)\poppler\Library\bin"
                    images = pdf2image.convert_from_path(temp_pdf_path, poppler_path=poppler_path)
                else:
                    # For Linux/Cloud environments where poppler is installed globally
                    # Try using the path we found if any
                    if poppler_info["found"]:
                        poppler_path = os.path.dirname(poppler_info["path"])
                        images = pdf2image.convert_from_path(
                            temp_pdf_path,
                            poppler_path=poppler_path
                        )
                    else:
                        # Standard approach
                        images = pdf2image.convert_from_path(temp_pdf_path)
                
                # Clean up the temporary file
                os.unlink(temp_pdf_path)
                
                first_page = images[0]
                
                # Convert to bytes
                img_byte_arr = io.BytesIO()
                first_page.save(img_byte_arr, format='JPEG')
                img_byte_arr = img_byte_arr.getvalue()
                
                pdf_parts = [
                    {
                        "mime_type": "image/jpeg",
                        "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
                    }
                ]
                return pdf_parts
            
            except Exception as e:
                st.warning(f"PDF image conversion failed: {str(e)}. Using text extraction instead.")
                
                # Debug information - display in an expander
                with st.expander("Technical Details (for debugging)"):
                    st.write("### System Information")
                    st.write(f"Platform: {platform.platform()}")
                    st.write(f"Python version: {sys.version}")
                    
                    st.write("### Poppler Check Results")
                    poppler_info = check_poppler_installation()
                    st.write(f"Poppler found: {poppler_info['found']}")
                    st.write(f"Poppler path: {poppler_info['path']}")
                    st.write(f"Poppler version: {poppler_info['version']}")
                    st.write("Paths checked:")
                    for path in poppler_info['paths_checked']:
                        st.write(f"- {path} (exists: {os.path.exists(path)})")
                
                # Fallback to text extraction
                uploaded_file.seek(0)  # Reset file pointer
                text = extract_text_with_pypdf2(uploaded_file)
                
                # Return the text directly in a special format for our modified get_gemini_response
                return {'text': text}
                
        except Exception as e:
            st.error(f"PDF processing error: {str(e)}")
            raise
    else:
        raise FileNotFoundError("No file uploaded")

# App header section with enhanced styling
st.markdown('<div class="main-header">Resume AI Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Powered by AI to help you land your dream job</div>', unsafe_allow_html=True)

# Enhanced feature boxes with hover effects and better contrast
st.markdown("""
<div style="display: flex; gap: 1.2rem; margin-bottom: 2.5rem;">
    <div class="feature-box animated-border" style="background: linear-gradient(145deg, #EEF2FF, #E0F7FF); border-left: 4px solid #3E64FF; flex: 1;">
        <div class="feature-title">📊 ATS Compatibility</div>
        <p style="color: #334155; font-size: 0.95rem; line-height: 1.6;">Check how well your resume aligns with job requirements and ATS systems</p>
    </div>
    <div class="feature-box animated-border" style="background: linear-gradient(145deg, #FFF1F2, #FFE4E6); border-left: 4px solid #FF9190; flex: 1;">
        <div class="feature-title" style="color: #FF9190;">🎯 Skills Gap Analysis</div>
        <p style="color: #334155; font-size: 0.95rem; line-height: 1.6;">Identify missing skills and keywords that could improve your chances</p>
    </div>
    <div class="feature-box animated-border" style="background: linear-gradient(145deg, #ECFDF5, #D1FAE5); border-left: 4px solid #4CAF50; flex: 1;">
        <div class="feature-title" style="color: #4CAF50;">✨ Expert Recommendations</div>
        <p style="color: #334155; font-size: 0.95rem; line-height: 1.6;">Get personalized suggestions to enhance your resume for specific roles</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Create two columns for better layout with glass card styling
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="sub-header">Job Description</div>', unsafe_allow_html=True)
    input_text = st.text_area(
        "Paste the job description here",
        height=250,
        key="input",
        help="Copy and paste the entire job description from the posting"
    )

with col2:
    st.markdown('<div class="sub-header">Your Resume</div>', unsafe_allow_html=True)
    
    # More visible file uploader label
    st.markdown('<p style="font-weight: 600; color: #2D3748; margin-bottom: 8px;">Upload your resume (PDF format)</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["pdf"])
    
    if uploaded_file is not None:
        # More visible success message
        st.markdown('<div style="background-color: rgba(209, 250, 229, 0.9); color: #065F46; padding: 10px; border-radius: 8px; font-weight: 500; margin: 10px 0;"><span>✅ Resume uploaded successfully!</span></div>', unsafe_allow_html=True)
        try:
            # Try to display a preview
            try:
                # Save PDF to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
                    temp_pdf.write(uploaded_file.getvalue())
                    temp_pdf_path = temp_pdf.name
                
                # Check poppler and get path
                poppler_info = check_poppler_installation()
                
                if platform.system() == "Windows":
                    poppler_path = r"C:\Program Files (x86)\poppler\Library\bin"
                    images = pdf2image.convert_from_path(temp_pdf_path, poppler_path=poppler_path)
                else:
                    # For Linux/Cloud environments
                    if poppler_info["found"]:
                        poppler_path = os.path.dirname(poppler_info["path"])
                        images = pdf2image.convert_from_path(
                            temp_pdf_path,
                            poppler_path=poppler_path
                        )
                    else:
                        # Standard approach
                        images = pdf2image.convert_from_path(temp_pdf_path)
                
                # Clean up
                os.unlink(temp_pdf_path)
                
                # Modern styling for the preview
                st.markdown("""
                <style>
                .preview-container {
                    margin-top: 20px;
                    position: relative;
                    overflow: hidden;
                    border-radius: 12px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
                    transition: all 0.3s ease;
                }
                .preview-container:hover {
                    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
                    transform: translateY(-5px);
                }
                .preview-title {
                    text-align: center;
                    margin-top: 15px;
                    font-weight: 600;
                    color: #3E64FF;
                    font-size: 1.1rem;
                    letter-spacing: 0.5px;
                }
                </style>
                """, unsafe_allow_html=True)
                
                # Display preview with improved styling
                st.markdown('<div class="preview-container">', unsafe_allow_html=True)
                st.image(images[0], use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('<div class="preview-title">Resume Preview</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.warning("Could not display PDF preview. Using text mode for analysis.")
                # Show a text preview instead
                uploaded_file.seek(0)
                try:
                    text = extract_text_with_pypdf2(uploaded_file)
                    st.markdown("""
                    <style>
                    .text-preview-container {
                        background-color: rgba(30, 41, 59, 0.04);
                        border-radius: 12px;
                        padding: 20px;
                        font-family: 'Courier New', monospace;
                        font-size: 14px;
                        line-height: 1.5;
                        color: #1e293b;
                        max-height: 300px;
                        overflow-y: auto;
                        border-left: 4px solid #3E64FF;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    st.markdown(f'<div class="text-preview-container">{text[:500]}...</div>', unsafe_allow_html=True)
                    st.markdown('<div class="preview-title">Resume Content Preview</div>', unsafe_allow_html=True)
                except Exception as text_e:
                    st.warning(f"Could not generate text preview: {str(text_e)}")
        except Exception as e:
            st.warning(f"Could not preview resume: {str(e)}")

# Enhanced action buttons with gradient and animation
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        submit1 = st.button("✨ Analyze Resume", use_container_width=True)
    with col_btn2:
        submit3 = st.button("📊 Calculate Match", use_container_width=True)

input_prompt1 = """
You are an experienced Technical Human Resource Manager with expertise in resume evaluation. 
Your task is to review the provided resume against the job description.
Please provide a structured analysis including:
1. Overall alignment of the candidate's profile with the role
2. Key strengths that make the candidate a good fit
3. Areas where the candidate's experience or skills may be lacking
4. Specific recommendations to improve the resume for this position
5. Conclude with a final assessment of fit
"""

input_prompt3 = """
You are an advanced ATS (Applicant Tracking System) analyzer with deep understanding of recruiting technology.
Evaluate the resume against the job description and provide:
1. An overall match percentage (0-100%)
2. Key matching keywords and skills found in both the resume and job description
3. Important keywords or skills mentioned in the job description but missing from the resume
4. Recommendations for improving resume match rate
Format your response with clear sections and bullet points for readability.
"""

# Results section with enhanced styling
if submit1 or submit3:
    if not input_text.strip():
        st.error("⚠️ Please enter a job description before analyzing.")
    elif uploaded_file is None:
        st.error("⚠️ Please upload your resume before analyzing.")
    else:
        with st.spinner("Analyzing your resume... This may take a few moments."):
            try:
                # Reset file pointer to beginning
                uploaded_file.seek(0)
                pdf_content = input_pdf_setup(uploaded_file)
                
                # Remove the result-section div wrapper
                st.markdown('<div class="sub-header">Analysis Results</div>', unsafe_allow_html=True)
                
                # Display analysis mode (image or text) with better styling
                if isinstance(pdf_content, dict) and 'text' in pdf_content:
                    st.markdown('<div style="background-color: rgba(49, 70, 101, 0.6); color: rgba(255, 255, 255, 0.9); padding: 10px 15px; border-radius: 8px; font-weight: 500; margin-bottom: 20px;">📄 Using text-based analysis mode</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div style="background-color: rgba(49, 70, 101, 0.6); color: rgba(255, 255, 255, 0.9); padding: 10px 15px; border-radius: 8px; font-weight: 500; margin-bottom: 20px;">🖼️ Using image-based analysis mode</div>', unsafe_allow_html=True)
                
                if submit1:
                    response = get_gemini_response(input_prompt1, pdf_content, input_text)
                    st.markdown("<h2 style='color: white; font-weight: 700;'>Resume Evaluation</h2>", unsafe_allow_html=True)
                    st.markdown(f"<div class='result-content'>{response}</div>", unsafe_allow_html=True)
                elif submit3:
                    response = get_gemini_response(input_prompt3, pdf_content, input_text)
                    st.markdown("<h2 style='color: white; font-weight: 700;'>Match Assessment</h2>", unsafe_allow_html=True)
                    st.markdown(f"<div class='result-content'>{response}</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
                st.error("If this issue persists, please try a different PDF file format or reach out for support.")

# Redesigned footer section with enhanced styling
st.markdown("<hr style='margin-top: 3rem; margin-bottom: 2rem; opacity: 0.3;'>", unsafe_allow_html=True)

# App description with animated fade-in
st.markdown("<h3 style='text-align: center; color: #3E64FF; font-size: 1.8rem; margin-bottom: 1rem; font-weight: 600;'>Resume AI Analyzer</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B; font-size: 1rem; max-width: 700px; margin: 0 auto 2rem auto; line-height: 1.6;'>This tool uses advanced AI to analyze resumes against job descriptions and provide actionable feedback.</p>", unsafe_allow_html=True)

# Project Guide with glassmorphism card
st.markdown("<h4 style='text-align: center; color: #3E64FF; margin-top: 2rem; margin-bottom: 1.5rem; font-size: 1.2rem; letter-spacing: 0.05em; font-weight: 600;'>PROJECT GUIDE</h4>", unsafe_allow_html=True)

guide_col1, guide_col2, guide_col3 = st.columns([1, 1, 1])
with guide_col2:
    st.markdown("""
    <div class="footer-card team-card" style="text-align: center;">
        <h4 style="color: #3E64FF; font-weight: 600; margin-bottom: 0.5rem; font-size: 1.1rem;">P. PRATHIBHA SWARAJ</h4>
        <p style="color: #64748B; font-size: 0.9rem; font-weight: 500;">ASSISTANT PROFESSOR</p>
    </div>
    """, unsafe_allow_html=True)

# Team section with enhanced cards
st.markdown("<h4 style='text-align: center; color: #3E64FF; margin-top: 2.5rem; margin-bottom: 1.5rem; font-size: 1.2rem; letter-spacing: 0.05em; font-weight: 600;'>TEAM MEMBERS</h4>", unsafe_allow_html=True)

team_cols = st.columns(3)
with team_cols[0]:
    st.markdown("""
    <div class="footer-card team-card" style="text-align: center;">
        <h4 style="color: #3E64FF; font-weight: 600; margin-bottom: 0.5rem; font-size: 1.1rem;">BHANU CHANDRA MEGHARAJ</h4>
        <p style="color: #64748B; font-size: 0.9rem; font-weight: 500;">23241A3338</p>
    </div>
    """, unsafe_allow_html=True)

with team_cols[1]:
    st.markdown("""
    <div class="footer-card team-card" style="text-align: center;">
        <h4 style="color: #3E64FF; font-weight: 600; margin-bottom: 0.5rem; font-size: 1.1rem;">SRAKSHIN CHITYALA</h4>
        <p style="color: #64748B; font-size: 0.9rem; font-weight: 500;">23241A3321</p>
    </div>
    """, unsafe_allow_html=True)

with team_cols[2]:
    st.markdown("""
    <div class="footer-card team-card" style="text-align: center;">
        <h4 style="color: #3E64FF; font-weight: 600; margin-bottom: 0.5rem; font-size: 1.1rem;">AKSHAJ REDDY ADDANDI</h4>
        <p style="color: #64748B; font-size: 0.9rem; font-weight: 500;">23241A3303</p>
    </div>
    """, unsafe_allow_html=True)

# Copyright with subtle animation
st.markdown(f"""
<p style='text-align: center; color: #94A3B8; font-size: 0.85rem; margin-top: 2.5rem; font-weight: 400;'>
    © {datetime.datetime.now().year} Resume AI Analyzer. All rights reserved.
</p>
""", unsafe_allow_html=True)




